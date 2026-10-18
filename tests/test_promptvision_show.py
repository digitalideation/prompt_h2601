"""Offline checks for the tiny PromptVision presentation builder."""
import base64
import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'promptvision_show.py'
spec = importlib.util.spec_from_file_location('promptvision_show', SCRIPT)
show = importlib.util.module_from_spec(spec)
spec.loader.exec_module(show)

PNG = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jRZkAAAAASUVORK5CYII=')


def add_entry(root, folder='01_Echo Land', country='Echo Land', cover=True, audio=True, info=True):
    team = root / folder
    team.mkdir()
    if audio:
        (team / 'track.mp3').write_bytes(b'fake test mp3')
    (team / 'source.png').write_bytes(PNG)
    if cover:
        (team / 'cover.png').write_bytes(PNG)
    if info:
        (team / 'entry.txt').write_text('Country: '+country+'\nTitle: Sunset\nModel: Model X\nPrompt: Cold synths\n  with warm chords\nTranslation: Blue means calm.\nIteration: Replaced percussion.', encoding='utf-8')
    return team


class PromptVisionShowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_generates_static_page_and_ordered_scorewiz_roster(self):
        add_entry(self.root, '02_Neon', 'Neon Republic')
        add_entry(self.root, '01_Echo Land', 'Echo Land')
        entries, warnings = show.build(self.root)
        self.assertEqual([e['country'] for e in entries], ['Echo Land', 'Neon Republic'])
        self.assertEqual(warnings, [])
        html = (self.root / 'promptvision_show.html').read_text()
        self.assertIn('<audio id="audio"', html)
        self.assertIn('01_Echo%20Land/track.mp3', html)
        self.assertIn('Cold synths\\nwith warm chords', html)
        self.assertIn("$('details').hidden=true", html)
        self.assertEqual((self.root / 'scorewiz_countries.txt').read_text(), 'Echo Land\nNeon Republic\n')
        self.assertTrue((self.root / '01_Echo Land/track.mp3').exists())
        show.build(self.root)  # Safe to rebuild as new submissions arrive.

    def test_missing_cover_uses_source_but_warns(self):
        add_entry(self.root, cover=False)
        entries, warnings = show.build(self.root)
        self.assertEqual(entries[0]['source'], entries[0]['cover'])
        self.assertIn('missing cover', warnings[0])

    def test_missing_audio_skips_entry_and_does_not_overwrite_on_empty(self):
        add_entry(self.root, '01_Missing', audio=False)
        add_entry(self.root, '02_Ready')
        entries, warnings = show.build(self.root)
        self.assertEqual(len(entries), 1)
        self.assertIn('missing track', warnings[0])
        (self.root / '02_Ready/track.mp3').unlink()
        with self.assertRaisesRegex(ValueError, 'No complete entries'):
            show.build(self.root)
        self.assertEqual((self.root / 'scorewiz_countries.txt').read_text(), 'Echo Land\n')

    def test_prompt_and_names_remain_inert_text(self):
        t = add_entry(self.root, country='</script><script>bad()</script>')
        p = t / 'entry.txt'
        p.write_text(p.read_text().replace('Cold synths','<img src=x onerror=bad()>'), encoding='utf-8')
        show.build(self.root)
        html = (self.root / 'promptvision_show.html').read_text()
        self.assertNotIn('</script><script>bad()', html)
        self.assertIn('\\u003c/script>', html)
        self.assertNotIn('.innerHTML', html)

    def test_reject_unrelated_html_and_duplicate_number(self):
        add_entry(self.root)
        (self.root / 'promptvision_show.html').write_text('My own page')
        with self.assertRaises(FileExistsError):
            show.build(self.root)
        (self.root / 'promptvision_show.html').unlink()
        add_entry(self.root, '01_Another Country')
        with self.assertRaisesRegex(ValueError, 'Duplicate entry number'):
            show.build(self.root)


if __name__ == '__main__':
    unittest.main()
