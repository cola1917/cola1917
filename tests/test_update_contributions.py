import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('sync', ROOT / 'scripts/update_contributions.py')
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.repo = {'full_name': 'newton-physics/newton', 'private': False, 'fork': False,
                     'html_url': 'https://github.com/newton-physics/newton',
                     'owner': {'login': 'newton-physics'}}
        self.pr = {'user': {'login': 'cola1917'}, 'merged_at': '2026-10-22T10:36:06Z',
                   'merged': True, 'base': {'repo': self.repo}, 'html_url': 'https://github.com/newton-physics/newton/pull/1',
                   'head': {'sha': 'head'}, 'changed_files': 0, 'title': 'Fix', 'number': 1,
                   'created_at': '2026-10-21T10:00:00Z', 'merge_commit_sha': 'merge', 'additions': 0, 'deletions': 0}

    def test_manual_bytes_preserved_with_crlf(self):
        text = 'Manual\r\n<!-- BEGIN AUTO:X -->\r\nold\r\n<!-- END AUTO:X -->\r\nTAIL\r\n'
        out = sync.replace_region(text, 'X', 'new')
        self.assertTrue(out.startswith('Manual\r\n<!-- BEGIN AUTO:X -->'))
        self.assertTrue(out.endswith('<!-- END AUTO:X -->\r\nTAIL\r\n'))
        self.assertEqual(sync.replace_region(out, 'X', 'new'), out)

    def test_missing_duplicate_reversed_markers_rejected(self):
        for text in ['manual', '<!-- END AUTO:X --><!-- BEGIN AUTO:X -->',
                     '<!-- BEGIN AUTO:X --><!-- BEGIN AUTO:X --><!-- END AUTO:X -->']:
            with self.subTest(text=text), self.assertRaises(sync.SyncError):
                sync.replace_region(text, 'X', 'new')

    def test_copilot_not_author(self):
        self.pr['user']['login'] = 'Copilot'
        with patch.object(sync, 'api', return_value=self.pr):
            record, rejected = sync.verify({'number': 1}, 'cola1917', self.repo, {})
        self.assertIsNone(record)
        self.assertEqual(rejected['reason'], 'author_mismatch')

    def test_closed_is_not_merged(self):
        self.pr['merged_at'] = None
        self.pr['merged'] = False
        with patch.object(sync, 'api', return_value=self.pr):
            record, rejected = sync.verify({'number': 1}, 'cola1917', self.repo, {})
        self.assertIsNone(record)
        self.assertEqual(rejected['reason'], 'not_merged')

    def test_wrong_base_rejected(self):
        self.pr['base'] = {'repo': self.repo | {'full_name': 'someone/fork'}}
        with patch.object(sync, 'api', return_value=self.pr):
            self.assertEqual(sync.verify({'number': 1}, 'cola1917', self.repo, {})[1]['reason'],
                             'base_repository_mismatch')

    def test_nonpublic_content_never_fetched_or_exported(self):
        for properties in [{'private': True}, {'visibility': 'internal'}]:
            with patch.object(sync, 'api') as api:
                record, rejected = sync.verify({'number': 1}, 'cola1917', self.repo | properties, {})
                api.assert_not_called()
            self.assertIsNone(record)
            self.assertEqual(rejected, {'reason': 'non_public_repository'})

    def test_forks_and_own_repo_not_upstream(self):
        self.assertEqual(sync.classify_repo(self.repo | {'fork': True}, 'cola1917'), 'fork')
        self.assertEqual(sync.classify_repo(self.repo | {'owner': {'login': 'cola1917'}}, 'cola1917'), 'personal')
        self.assertEqual(sync.classify_repo(self.repo, 'cola1917'), 'verified_upstream')

    def test_stale_editorial_is_not_reused(self):
        note = {'summaries': {'newton-physics/newton#1': {'reviewed_head_sha': 'old'}}}
        with patch.object(sync, 'api', return_value=self.pr), patch.object(sync, 'pages', return_value=[]):
            record, _ = sync.verify({'number': 1}, 'cola1917', self.repo, note)
        self.assertEqual(record['evidence']['summary_review_status'], 'pending_editorial_review')
        self.assertEqual(record['contribution_type'], ['unclassified'])

    def test_incomplete_files_rejected(self):
        self.pr['changed_files'] = 1
        with patch.object(sync, 'api', return_value=self.pr), patch.object(sync, 'pages', return_value=[]):
            with self.assertRaises(sync.SyncError):
                sync.verify({'number': 1}, 'cola1917', self.repo, {})

    def test_search_pagination(self):
        batches = [{'total_count': 101, 'items': [{'html_url': str(i)} for i in range(100)]},
                   {'total_count': 101, 'items': [{'html_url': '100'}]}]
        with patch.object(sync, 'api', side_effect=batches):
            self.assertEqual(len(sync.search_all('cola1917')), 101)

    def test_search_partition_above_1000(self):
        batches = [{'total_count': 1001, 'items': []},
                   {'total_count': 1, 'items': [{'html_url': 'a'}]},
                   {'total_count': 1, 'items': [{'html_url': 'b'}]}]
        with patch.object(sync, 'api', side_effect=batches) as api:
            self.assertEqual(len(sync.search_all('cola1917')), 2)
            left = api.call_args_list[1].kwargs['q'].split('created:')[1]
            right = api.call_args_list[2].kwargs['q'].split('created:')[1]
            self.assertLess(left.split('..')[1], right.split('..')[0])

    def test_search_incomplete_or_changed_rejected(self):
        for batches in [[{'incomplete_results': True}],
                        [{'total_count': 101, 'items': []}, {'total_count': 102}]]:
            with patch.object(sync, 'api', side_effect=batches), self.assertRaises(sync.SyncError):
                sync.search_all('cola1917')

    def test_repeat_write_keeps_bytes_and_mtime(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'x.txt'
            self.assertTrue(sync.write_changed(path, 'hello\n'))
            before = path.stat().st_mtime_ns
            self.assertFalse(sync.write_changed(path, 'hello\n'))
            self.assertEqual(path.stat().st_mtime_ns, before)

    def test_auth_failure_preserves_outputs_and_stops_requests(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'data').mkdir()
            (root / 'data/editorial.json').write_text('{}', encoding='utf-8')
            (root / 'README.md').write_bytes(b'manual')
            with patch.object(sync, 'ROOT', root), patch.object(sync, 'api', side_effect=sync.SyncError('auth failure')) as api,\
                 patch('sys.argv', ['sync']):
                self.assertEqual(sync.main(), 1)
                self.assertEqual(api.call_count, 1)
            self.assertEqual((root / 'README.md').read_bytes(), b'manual')
            self.assertFalse(json.loads((root / '.local/sync_partial.json').read_text())['complete'])

    def test_generate_checks_both_markers_before_writing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'README.md').write_text('manual', encoding='utf-8')
            (root / 'CONTRIBUTIONS.md').write_text('manual ledger', encoding='utf-8')
            with self.assertRaises(sync.SyncError):
                sync.generate(root, {'pull_requests': [], 'username': 'cola1917'}, {'selected': []})
            self.assertEqual((root / 'README.md').read_text(), 'manual')

    def test_rate_failure_saves_partial_without_replacing_complete_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'data').mkdir()
            (root / 'data/editorial.json').write_text('{"username":"cola1917"}', encoding='utf-8')
            old = b'{"previous_complete_snapshot":true}\n'
            (root / 'data/merged_prs.json').write_bytes(old)
            (root / 'README.md').write_bytes(b'Keep manual README')
            items = [{'repository_url': 'https://api.github.com/repos/newton-physics/newton',
                      'number': n, 'html_url': f'https://github.com/newton-physics/newton/pull/{n}'} for n in (1, 2)]
            def verify(item, *args):
                if item['number'] == 2:
                    raise sync.SyncError('HTTP 403 quota')
                return {'url': item['html_url']}, None
            def api(endpoint):
                return self.repo if endpoint.startswith('repos/') else {'login': 'cola1917'}
            with patch.object(sync, 'ROOT', root), patch.object(sync, 'search_all', return_value=items), \
                 patch.object(sync, 'api', side_effect=api), patch.object(sync, 'verify', side_effect=verify), \
                 patch('sys.argv', ['sync']):
                self.assertEqual(sync.main(), 1)
            self.assertEqual((root / 'data/merged_prs.json').read_bytes(), old)
            self.assertEqual((root / 'README.md').read_bytes(), b'Keep manual README')
            partial = json.loads((root / '.local/sync_partial.json').read_text())
            self.assertFalse(partial['complete'])
            self.assertEqual(len(partial['verified_public_prs']), 1)
            self.assertEqual(partial['unverified_public_prs'][0]['url'], items[1]['html_url'])


if __name__ == '__main__':
    unittest.main()
