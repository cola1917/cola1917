import copy
from pathlib import Path
import sys
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import profile_art
import update_contributions as sync


class VisualEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.record = {
            'repository': 'newton-physics/newton', 'repository_category': 'verified_upstream',
            'number': 1, 'url': 'https://github.com/newton-physics/newton/pull/1',
            'evidence': {'summary_review_status': 'diff_and_discussion_reviewed'},
        }
        self.data = {'username': 'cola1917', 'pull_requests': [self.record]}
        self.editorial = {'selected': [{'label': 'Newton', 'prs': ['newton-physics/newton#1'],
                                       'summary': 'Reviewed correctness fix.'}]}

    def test_forks_and_personal_records_cannot_inflate_card_count(self):
        for category in ('fork', 'personal', 'other_public_collaboration'):
            record = copy.deepcopy(self.record)
            record['number'] = len(self.data['pull_requests']) + 1
            record['repository_category'] = category
            self.data['pull_requests'].append(record)
        self.assertEqual(profile_art.eligible_groups(self.data, self.editorial)[0][2], 1)
        asset = profile_art.build_assets(self.data, self.editorial)['assets/contribution-newton-light.svg']
        self.assertIn('1 merged PR', asset)
        self.assertNotIn('4 merged PR', asset)

    def test_unreviewed_pr_is_not_featured_in_graphics_or_links(self):
        self.record['evidence']['summary_review_status'] = 'pending_editorial_review'
        assets = profile_art.build_assets(self.data, self.editorial)
        self.assertFalse(any('contribution-newton' in name for name in assets))
        self.assertNotIn(self.record['url'], sync.selected_markdown(self.data, self.editorial))

    def test_assets_are_static_self_contained_and_have_mobile_theme_variants(self):
        assets = profile_art.build_assets(self.data, self.editorial)
        self.assertEqual(assets, profile_art.build_assets(self.data, self.editorial))
        self.assertIn('assets/banner-mobile-dark.svg', assets)
        self.assertIn('assets/project-retargeting-mobile-light.svg', assets)
        for name, value in assets.items():
            with self.subTest(name=name):
                root = ET.fromstring(value)
                self.assertEqual(root.tag, '{http://www.w3.org/2000/svg}svg')
                self.assertIsNotNone(root.find('{http://www.w3.org/2000/svg}title'))
                self.assertIsNotNone(root.find('{http://www.w3.org/2000/svg}desc'))
                self.assertNotIn('<script', value)
                self.assertNotIn('<image', value)
                self.assertNotIn('https://', value)
                if 'project-' in name:
                    self.assertIn('not an experiment screenshot', value)

    def test_svg_text_is_escaped(self):
        value = profile_art.text(0, 0, '<script>&', 16, '#ffffff')
        self.assertNotIn('<script>', value)
        self.assertIn('&lt;script&gt;&amp;', value)

    def test_all_design_directions_preserve_count_provenance_and_method_qualification(self):
        for design in profile_art.DESIGNS:
            with self.subTest(design=design):
                assets = profile_art.build_assets(self.data, self.editorial, design)
                card = assets['assets/contribution-newton-light.svg']
                self.assertIn('1 merged PR', card)
                for name, value in assets.items():
                    ET.fromstring(value)
                    if 'project-' in name:
                        self.assertIn('not an experiment screenshot', value)


if __name__ == '__main__':
    unittest.main()
