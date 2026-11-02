#!/usr/bin/env python3
"""Sync public, author-verified merged PRs using gh. Python 3.10+, stdlib only.

No publishing, credential extraction, shell execution, or private-data export.
Search is paginated and recursively partitioned above GitHub's 1,000-result cap.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = {
    'newton-physics/newton': 'Newton',
    'google-deepmind/mujoco_warp': 'MuJoCo Warp',
    'pypose/pypose': 'PyPose',
    'colmap/colmap': 'COLMAP',
}


class SyncError(RuntimeError):
    pass


def gh_json(*args):
    try:
        result = subprocess.run(['gh', *args], capture_output=True, text=True, encoding='utf-8', timeout=60)
    except subprocess.TimeoutExpired as error:
        raise SyncError('GitHub CLI request timed out; previous complete outputs preserved.') from error
    if result.returncode:
        # gh stderr is deliberately not persisted or echoed (credential/privacy boundary).
        status = re.search(r'HTTP (\d+)', result.stderr)
        raise SyncError('GitHub CLI request failed' + (f' (HTTP {status[1]})' if status else '') +
                        '; check gh authentication, network, and API rate limits.')
    return json.loads(result.stdout)


def api(endpoint, **params):
    args = ['api', '--method', 'GET', endpoint]
    for key, value in params.items():
        args.extend(['-f', f'{key}={value}'])
    return gh_json(*args)


def pages(endpoint):
    result = []
    page = 1
    while True:
        batch = api(endpoint, per_page=100, page=page)
        result.extend(batch)
        if len(batch) < 100:
            return result
        page += 1


def stamp(seconds):
    return dt.datetime.fromtimestamp(seconds, dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def search_all(username):
    base = f'is:pr is:merged author:{username}'
    found = {}
    matched = 0

    def window(low=None, high=None):
        nonlocal matched
        q = base if low is None else f'{base} created:{stamp(low)}..{stamp(high)}'
        first = api('search/issues', q=q, per_page=100, page=1, sort='created', order='asc')
        if first.get('incomplete_results'):
            raise SyncError('GitHub returned incomplete search results; no complete ledger was written.')
        count = first['total_count']
        if count > 1000:
            if low is None:
                low = int(dt.datetime(2008, 1, 1, tzinfo=dt.timezone.utc).timestamp())
                high = int(dt.datetime.now(dt.timezone.utc).timestamp())
            if low >= high:
                raise SyncError('More than 1,000 PRs in one second: search cannot prove completeness.')
            mid = (low + high) // 2
            window(low, mid)
            window(mid + 1, high)
            return
        items = first['items']
        for page in range(2, (count + 99) // 100 + 1):
            more = api('search/issues', q=q, per_page=100, page=page, sort='created', order='asc')
            if more.get('incomplete_results') or more['total_count'] != count:
                raise SyncError('Search changed during pagination; retry to obtain a consistent snapshot.')
            items.extend(more['items'])
        if len(items) != count:
            raise SyncError('Search pagination count mismatch.')
        matched += count
        for item in items:
            found[item['html_url']] = item

    window()
    if matched != len(found):
        raise SyncError('Duplicate search matches across partitions.')
    return sorted(found.values(), key=lambda i: i['html_url'])


def classify_repo(repo, username):
    if repo['fork']:
        return 'fork'
    if repo['owner']['login'].lower() == username.lower():
        return 'personal'
    if repo['full_name'] in UPSTREAM:
        return 'verified_upstream'
    return 'other_public_collaboration'


def verify(item, username, repo, editorial):
    name, number = repo['full_name'], item['number']
    if repo['private'] or repo.get('visibility', 'public') != 'public':
        # Do not disclose names, titles, URLs, or diffs of non-public repositories.
        return None, {'reason': 'non_public_repository'}
    pr = api(f'repos/{name}/pulls/{number}')
    rejection = None
    if pr['user']['login'].lower() != username.lower():
        rejection = 'author_mismatch'
    elif not pr['merged_at'] or not pr['merged']:
        rejection = 'not_merged'
    elif pr['base']['repo']['full_name'] != name or pr['base']['repo']['private']:
        rejection = 'base_repository_mismatch'
    if rejection:
        return None, {'url': pr['html_url'], 'reason': rejection,
                      'actual_author': pr['user']['login']}
    files = pages(f'repos/{name}/pulls/{number}/files')
    if len(files) != pr['changed_files']:
        raise SyncError(f'Incomplete file list for {name}#{number}.')
    comments = pages(f'repos/{name}/issues/{number}/comments')
    reviews = pages(f'repos/{name}/pulls/{number}/reviews')
    inline = pages(f'repos/{name}/pulls/{number}/comments')
    key = f'{name}#{number}'
    note = editorial.get('summaries', {}).get(key)
    reviewed = bool(note and note['reviewed_head_sha'] == pr['head']['sha'])
    summary = note['technical_summary'] if reviewed else (
        f'Merged change across {len(files)} files (+{pr["additions"]}/−{pr["deletions"]}); technical summary pending diff review.')
    return {
        'repository': name, 'repository_url': repo['html_url'],
        'repository_fork': repo['fork'], 'repository_parent': repo.get('parent', {}).get('full_name'),
        'repository_category': classify_repo(repo, username),
        'title': pr['title'], 'number': number, 'url': pr['html_url'],
        'author': pr['user']['login'], 'created_at': pr['created_at'], 'merged_at': pr['merged_at'],
        'head_sha': pr['head']['sha'], 'merge_commit_sha': pr['merge_commit_sha'],
        'contribution_type': note['contribution_type'] if reviewed else ['unclassified'],
        'technical_summary': summary,
        'files': [{k: f[k] for k in ('filename', 'status', 'additions', 'deletions', 'sha')} |
                  {'patch_sha256': hashlib.sha256(f['patch'].encode()).hexdigest() if 'patch' in f else None}
                  for f in files],
        'additions': pr['additions'], 'deletions': pr['deletions'],
        'evidence': {
            'verification_status': 'verified', 'author_matches': True, 'merged': True,
            'public_base_repository': True, 'files_complete': True,
            'summary_review_status': 'diff_and_discussion_reviewed' if reviewed else 'pending_editorial_review',
            'details_api': f'https://api.github.com/repos/{name}/pulls/{number}',
            'diff_url': pr['html_url'] + '/files',
            'discussion_urls': sorted({x['html_url'] for x in comments + reviews + inline if x.get('html_url')}),
            'reviewed_files': note.get('evidence_files', []) if reviewed else [],
        },
    }, None


def replace_region(text, name, content):
    begin, end = f'<!-- BEGIN AUTO:{name} -->', f'<!-- END AUTO:{name} -->'
    if text.count(begin) != 1 or text.count(end) != 1 or text.index(begin) >= text.index(end):
        raise SyncError(f'Missing, duplicate, or reversed {name} markers; files left untouched.')
    start = text.index(begin) + len(begin)
    stop = text.index(end)
    return text[:start] + '\n' + content.rstrip() + '\n' + text[stop:]


def md(text):
    # Treat remote titles as plain text, never as Markdown/HTML instructions.
    return re.sub(r'([\\`*_{}\[\]()<>|#!])', r'\\\1', ' '.join(text.split()))


def selected_markdown(data, editorial):
    records = {f'{p["repository"]}#{p["number"]}': p for p in data['pull_requests']}
    lines = []
    count = sum(p['repository_category'] == 'verified_upstream' for p in records.values())
    lines.append(f'**{count} merged upstream PRs** across Newton, MuJoCo Warp, PyPose, and COLMAP. Selected work:')
    lines.append('')
    for group in editorial['selected']:
        eligible = [records[k] for k in group['prs'] if k in records and
                    records[k]['repository_category'] == 'verified_upstream' and
                    records[k]['evidence']['summary_review_status'] == 'diff_and_discussion_reviewed']
        # Do not reuse curated prose if a referenced PR no longer passes verification.
        if len(eligible) != len(group['prs']):
            continue
        links = ' · '.join(f'[#{p["number"]}]({p["url"]})' for p in eligible)
        lines.append(f'- **[{group["label"]}]({eligible[0]["repository_url"]})** — {group["summary"]} {links}')
    lines.extend(['', f'[View All Merged PRs](https://github.com/pulls?q=is%3Apr+is%3Amerged+author%3A{data["username"]}) · '
                  '[Verified contribution ledger](CONTRIBUTIONS.md)', '',
                  '*Upstream merges only above; personal repositories and fork merges are listed separately in the ledger.*'])
    return '\n'.join(lines)


def ledger_markdown(data):
    lines = [f'Author: **{data["username"]}** · **{len(data["pull_requests"])} verified public merged PRs**.', '',
             f'Search scope: all visible merged-PR matches ({data["collection"]["search_matches"]}); '
             f'{len(data["excluded"])} public matches excluded after verification. '
             'Non-public repository content is never exported. Dates below are UTC.', '']
    groups = [('verified_upstream', 'Verified Upstream — Robotics & 3D'),
              ('fork', 'Fork Merges — Not Upstream Acceptance'),
              ('personal', 'Personal Repositories'),
              ('other_public_collaboration', 'Other Public Collaboration')]
    for category, heading in groups:
        subset = [p for p in data['pull_requests'] if p['repository_category'] == category]
        if not subset:
            continue
        lines.extend([f'## {heading}', ''])
        for p in subset:
            lines.extend([f'### {md(p["repository"])} [#{p["number"]}]({p["url"]}) — {md(p["title"])}', '',
                          f'- **Repository:** [{p["repository"]}]({p["repository_url"]})' +
                          (f' (fork of {p["repository_parent"]})' if p['repository_fork'] else ''),
                          f'- **Merged date:** {p["merged_at"]}',
                          f'- **Contribution type:** {", ".join(p["contribution_type"])}',
                          f'- **Technical summary:** {p["technical_summary"]}',
                          f'- **Evidence / verification:** author `{p["author"]}`; non-null `merged_at`; public base; '
                          f'{len(p["files"])} changed files verified. Summary: {p["evidence"]["summary_review_status"]}. '
                          f'[Merged diff]({p["evidence"]["diff_url"]}) · [API]({p["evidence"]["details_api"]}).', ''])
            if p['evidence']['reviewed_files']:
                lines.extend(['Key files: ' + ', '.join(f'`{x}`' for x in p['evidence']['reviewed_files']) + '.', ''])
    if data['excluded']:
        lines.extend(['## Excluded Search Matches', '', 'Search can include bot-authored matches. These are not counted above.', ''])
        for p in data['excluded']:
            lines.append(f'- [PR]({p["url"]}): {p["reason"]}; detail-endpoint author `{p.get("actual_author", "unknown")}`.')
    return '\n'.join(lines)


def dumps(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'


def write_changed(path, content):
    raw = content.encode('utf-8')
    if path.exists() and path.read_bytes() == raw:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as tmp:
        tmp.write(raw)
        temporary = tmp.name
    os.replace(temporary, path)
    return True


def generate(root, data, editorial):
    # Validate both documents before writing anything. Preserve all bytes outside markers.
    readme = (root / 'README.md').read_bytes().decode('utf-8')
    ledger = (root / 'CONTRIBUTIONS.md').read_bytes().decode('utf-8')
    return {
        'README.md': replace_region(readme, 'SELECTED_CONTRIBUTIONS', selected_markdown(data, editorial)),
        'CONTRIBUTIONS.md': replace_region(ledger, 'MERGED_PRS', ledger_markdown(data)),
        'data/merged_prs.json': dumps(data),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--username', help='Explicit public GitHub author; still uses existing gh authentication')
    parser.add_argument('--offline', action='store_true', help='Render the saved verified snapshot without network calls')
    parser.add_argument('--check', action='store_true', help='Exit 1 if generated files would change; do not write')
    args = parser.parse_args()
    verified, excluded, private_count = [], [], 0
    unverified_public = []
    try:
        editorial = json.loads((ROOT / 'data/editorial.json').read_text(encoding='utf-8'))
        if args.offline:
            data = json.loads((ROOT / 'data/merged_prs.json').read_text(encoding='utf-8'))
            if args.username and args.username.lower() != data['username'].lower():
                raise SyncError('Offline snapshot belongs to a different username.')
        else:
            # Stop immediately if authentication fails. Never extract the stored credential.
            identity = api('user')
            username = args.username or identity['login']
            if not re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?', username):
                raise SyncError('Invalid GitHub username.')
            username = api(f'users/{username}')['login']
            if username != editorial['username']:
                raise SyncError('Editorial configuration belongs to another username; create a matching configuration first.')
            candidates = search_all(username)
            repositories = {}
            for item in candidates:
                name = item['repository_url'].removeprefix('https://api.github.com/repos/')
                if name not in repositories:
                    repositories[name] = api(f'repos/{name}')
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
                futures = {pool.submit(verify, item, username, repositories[
                    item['repository_url'].removeprefix('https://api.github.com/repos/')], editorial)
                    : item for item in candidates}
                errors = []
                for future in concurrent.futures.as_completed(futures):
                    try:
                        record, rejection = future.result()
                        if record:
                            verified.append(record)
                        elif rejection['reason'] == 'non_public_repository':
                            private_count += 1
                        else:
                            excluded.append(rejection)
                    except Exception as error:
                        errors.append(error)
                        item = futures[future]
                        repo = repositories[item['repository_url'].removeprefix('https://api.github.com/repos/')]
                        if not repo['private'] and repo.get('visibility', 'public') == 'public':
                            unverified_public.append({'url': item['html_url'], 'status': 'unverified_request_failed'})
                if errors:
                    raise SyncError(f'{len(errors)} PR verification request(s) failed; complete outputs preserved.')
            verified.sort(key=lambda p: (p['merged_at'], p['url']), reverse=True)
            excluded.sort(key=lambda p: p['url'])
            data = {'schema_version': 1, 'username': username,
                    'collection': {'complete': True, 'search_matches': len(candidates),
                                   'verified_public_prs': len(verified), 'non_public_matches_omitted': private_count,
                                   'method': 'REST search, paginated/partitioned; PR author, merge, public base, and files checked'},
                    'pull_requests': verified, 'excluded': excluded}
        output = generate(ROOT, data, editorial)
        changed = [name for name, value in output.items()
                   if not (ROOT / name).exists() or (ROOT / name).read_bytes() != value.encode('utf-8')]
        if args.check:
            print('Generated files current.' if not changed else 'Would change: ' + ', '.join(changed))
            return int(bool(changed))
        for name, value in output.items():
            write_changed(ROOT / name, value)
        print(f'Verified {len(data["pull_requests"])} public PRs; changed {len(changed)} file(s).')
        return 0
    except (SyncError, OSError, ValueError, KeyError) as error:
        if not args.check:
            # Partial file is local-only; never promote it to a complete ledger or selected README.
            write_changed(ROOT / '.local/sync_partial.json', dumps({
                'complete': False, 'verified_public_prs': sorted(verified, key=lambda p: p['url']),
                'excluded': sorted(excluded, key=lambda p: p['url']),
                'unverified_public_prs': sorted(unverified_public, key=lambda p: p['url']),
                'unverified': 'Collection incomplete; previous published snapshot preserved.'}))
        print(f'Sync failed: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
