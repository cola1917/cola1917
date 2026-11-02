#!/usr/bin/env python3
"""Validate content, evidence, links, and generated regions. Stdlib only."""
import argparse
import concurrent.futures
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('sync', ROOT / 'scripts/update_contributions.py')
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def remote_pr(pr):
    result = sync.api(f'repos/{pr["repository"]}/pulls/{pr["number"]}')
    require(result['user']['login'] == pr['author'], f'Author changed: {pr["url"]}')
    require(result['merged'] and result['merged_at'] == pr['merged_at'], f'Merge mismatch: {pr["url"]}')
    require(result['html_url'] == pr['url'], f'Canonical URL mismatch: {pr["url"]}')
    require(result['base']['repo']['full_name'] == pr['repository'], 'Base repository mismatch')
    require(not result['base']['repo']['private'], 'Non-public PR')
    request = urllib.request.Request(pr['url'], method='HEAD', headers={'User-Agent': 'ProfileEvidenceValidator/1.0'})
    with urllib.request.urlopen(request, timeout=35) as response:
        require(response.status == 200, f'PR URL HTTP {response.status}')
    return pr['url']


def remote_url(url):
    if url.startswith('https://api.github.com/'):
        sync.api(url.removeprefix('https://api.github.com/'))
        return url
    request = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'ProfileEvidenceValidator/1.0'})
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            require(response.status == 200, f'Broken external link: {url}')
    except Exception as error:
        raise AssertionError(f'External link check inconclusive: {url}: {error}') from error
    return url


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--online', action='store_true')
    args = parser.parse_args()
    data = json.loads((ROOT / 'data/merged_prs.json').read_text(encoding='utf-8'))
    editorial = json.loads((ROOT / 'data/editorial.json').read_text(encoding='utf-8'))
    require(data['collection']['complete'], 'Incomplete collection')
    require(ROOT.name == data['username'] == editorial['username'], 'Profile repository/author naming mismatch')
    records = data['pull_requests']
    require(len({p['url'] for p in records}) == len(records), 'Duplicate PR')
    require(len(records) == data['collection']['verified_public_prs'], 'Count mismatch')
    require(len(records) + len(data['excluded']) + data['collection']['non_public_matches_omitted'] ==
            data['collection']['search_matches'], 'Unaccounted search match')
    for p in records:
        require(p['author'] == data['username'] and bool(p['merged_at']), 'Unverified author or merge')
        require(p['url'] == f'https://github.com/{p["repository"]}/pull/{p["number"]}', 'PR URL mismatch')
        require(p['evidence']['verification_status'] == 'verified', 'Unverified record')
        require(all(p['evidence'][k] for k in ('author_matches', 'merged', 'public_base_repository', 'files_complete')),
                'Evidence invariant failed')
        if p['repository_category'] == 'verified_upstream':
            require(p['repository'] in sync.UPSTREAM and not p['repository_fork'], 'Fork counted as upstream')
        require(bool(p['technical_summary']), 'Missing summary')
    output = sync.generate(ROOT, data, editorial)
    for name, value in output.items():
        require((ROOT / name).read_bytes() == value.encode(), f'Stale generated file: {name}')
    readme = (ROOT / 'README.md').read_text(encoding='utf-8')
    require(readme.count('\n# ') == 0 and readme.startswith('# Jiangtao Wang\n'), 'Invalid main heading')
    sections = re.findall(r'^## (.+)$', readme, re.M)
    require(sections == ['Open Source Contributions', 'Selected Projects', 'Technical Stack', 'Links'], 'Section order')
    require('self-reported' in readme and 'not been independently verified' in readme, 'Missing project qualification')
    require('![' not in readme and '<img' not in readme.lower() and '<script' not in readme.lower(), 'External resource embed')
    for value in ('4.41×', '34.4% → 73.4%', '86.7%', '60%', '1,000', 'Lambert + GGX'):
        require(value in readme, f'Owner-provided project detail missing: {value}')
    # Scan repository sources only. Do not read .git, ignored local evidence, or external private files.
    sources = [p for p in ROOT.rglob('*') if p.is_file() and
               not any(part in {'.git', '.local', '__pycache__'} for part in p.relative_to(ROOT).parts)]
    secret_patterns = [r'gh[pousr]_[A-Za-z0-9]{30,}', r'github_pat_[A-Za-z0-9_]{30,}',
                       r'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----',
                       r'https?://(?:localhost|127\.0\.0\.1|10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+)(?:[:/]|$)',
                       r'https?://172\.(?:1[6-9]|2\d|3[01])\.\d+\.\d+(?:[:/]|$)']
    for source in sources:
        text = source.read_text(encoding='utf-8')
        for pattern in secret_patterns:
            require(not re.search(pattern, text), f'Possible credential/internal address in {source.relative_to(ROOT)}')
    links = set()
    for name in ('README.md', 'CONTRIBUTIONS.md', 'MAINTENANCE.md'):
        text = (ROOT / name).read_text(encoding='utf-8')
        for link in re.findall(r'\]\(([^)]+)\)', text):
            if link.startswith('https://'):
                links.add(link)
            else:
                require(not link.startswith(('http:', 'file:', '/')), f'Unsupported link: {link}')
                require((ROOT / link.split('#')[0]).is_file(), f'Broken local link: {link}')
    checked = []
    if args.online:
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            checked = list(pool.map(remote_pr, records))
        print(f'PR author/merge/HTTP checks passed: {len(checked)}.', flush=True)
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            futures = [pool.submit(remote_url, url) for url in sorted(links - set(checked))]
            for future in concurrent.futures.as_completed(futures):
                checked.append(future.result())
                if len(checked) % 10 == 0:
                    print(f'URL checks passed: {len(checked)}.', flush=True)
    result = {'offline_checks': 'passed', 'verified_public_prs': len(records),
              'verified_upstream_prs': sum(p['repository_category'] == 'verified_upstream' for p in records),
              'excluded_bot_authored_matches': len(data['excluded']), 'remote_mode': args.online,
              'checked_urls': sorted(checked), 'external_document_urls': len(links),
              'source_files_scanned': len(sources), 'secrets_or_internal_addresses_detected': False}
    sync.write_changed(ROOT / '.local/validation.json', sync.dumps(result))
    print(json.dumps({k: v for k, v in result.items() if k != 'checked_urls'}, indent=2))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(f'Validation failed: {error}', file=sys.stderr)
        sys.exit(1)
