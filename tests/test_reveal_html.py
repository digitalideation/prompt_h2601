"""Standalone exporter tests. No Replicate calls or student files are used.

Run: python -m pip install 'stegg==3.0.0' nbformat
     python -m unittest discover -s tests -p test_reveal_html.py -v
Optional browser check: install Playwright/Chromium; RUN_REVEAL_BROWSER_TESTS=1.
"""
import contextlib
import functools
import io
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
import threading
import unittest
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

import nbformat
from PIL import Image
try:
    from steg_core import create_config, encode_text
except ImportError:
    create_config = encode_text = None

NOTEBOOK = Path(__file__).resolve().parents[1] / 'notebooks/04_telephone_reveal_html.ipynb'
CONFIG = create_config(channels='RGB', bits=1, compress=True, strategy='interleaved') if create_config else None


def png(path, prompt=None):
    """Synthetic fixture only, never an AI-generated or student image."""
    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new('RGB', (160, 100), (80, 110, 140))
    if prompt is not None:
        image = encode_text(image, prompt, CONFIG)
    image.save(path, format='PNG')
    return path.read_bytes()


def export(source, output):
    notebook = nbformat.read(NOTEBOOK, as_version=4)
    cell = next(c for c in notebook.cells if c.id == 'export')
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(cell.source, str(NOTEBOOK), 'exec'), {'FOLDER': str(source), 'OUTPUT': str(output)})
    html = (output / 'index.html').read_text(encoding='utf-8')
    data = json.loads(re.search(r'<script id="reveal-data" type="application/json">(.*?)</script>', html, re.S).group(1))
    return html, data


@unittest.skipIf(create_config is None, 'Install stegg==3.0.0 for HTML exporter tests')
class RevealExportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'input'
        self.source.mkdir()
        self.output = self.root / 'export'

    def test_schema_standalone_and_empty_start(self):
        nb = nbformat.read(NOTEBOOK, as_version=4)
        nbformat.validate(nb)
        code = [c for c in nb.cells if c.cell_type == 'code']
        self.assertEqual(len(code), 3)
        for cell in code:
            self.assertEqual(cell.outputs, [])
            self.assertIsNone(cell.execution_count)
            if cell.id != 'install':
                compile(cell.source, str(NOTEBOOK), 'exec')
        text = '\n'.join(c.source for c in code)
        for unwanted in ['from telephone_', 'import ipywidgets', 'import replicate', 'fetch(']:
            self.assertNotIn(unwanted, text)
        with contextlib.redirect_stdout(io.StringIO()) as log:
            exec(code[-1].source, {'FOLDER': '', 'OUTPUT': str(self.output)})
        self.assertIn('Set FOLDER', log.getvalue())
        self.assertFalse(self.output.exists())

    def test_stegg_unicode_order_and_unchanged_originals(self):
        prompts, originals = [], {}
        for step in range(1, 6):
            name = '_'.join(f'{((4 + i) % 5) + 1:02d}' for i in range(step)) + '.png'
            prompt = f'Round {step}: caf\u00e9 / \u65e5\u672c\u8a9e\nSecond line.'
            prompts.append(prompt)
            path = self.source / 'Group_F' / name
            originals[path] = png(path, prompt)
        html, data = export(self.source, self.output)
        chain = data['chains'][4]
        self.assertEqual(chain['label'], 'Group F / Chain 05')
        self.assertEqual([s['prompt'] for s in chain['slides']], prompts)
        self.assertEqual([s['filename'] for s in chain['slides']], [p.name for p in originals])
        self.assertFalse(data['warnings'])
        for path, before in originals.items():
            self.assertEqual(path.read_bytes(), before)
            self.assertEqual((self.output / 'images' / 'Group_F' / path.name).read_bytes(), before)
        self.assertEqual(len(data['chains']), 5)
        self.assertEqual(sum(s['src'] is None for c in data['chains'] for s in c['slides']), 20)
        self.assertTrue(html.lstrip().startswith('<!doctype html>'))
        self.assertNotIn(str(self.source), html)

    def test_missing_unreadable_duplicate_and_private_attempts(self):
        png(self.source / 'Group_A/01.png')
        png(self.source / 'Group_A/01_02_03.png', 'Later image')
        png(self.source / 'copy/Group_A/01_02_03.png', 'Duplicate')
        (self.source / 'Group_A/01_02_03_04.png').write_bytes(b'not a PNG')
        png(self.source / 'Group_A/02_01.png', 'Invalid order')
        png(self.source / 'Group_A/01_try01.png', 'Private attempt')
        html, data = export(self.source, self.output)
        slides = data['chains'][0]['slides']
        self.assertIsNotNone(slides[0]['src'])
        self.assertIsNone(slides[0]['prompt'])
        self.assertEqual(slides[1]['note'], 'Image missing.')
        self.assertIn('Duplicate', slides[2]['note'])
        self.assertEqual(slides[3]['note'], 'Image could not be opened.')
        self.assertEqual(len(list((self.output / 'images').rglob('*.png'))), 1)
        self.assertEqual(len(data['warnings']), 5)
        self.assertNotIn('Private attempt', html)

    def test_corrupt_stegg_prompt_still_shows_image(self):
        path = self.source / 'Group_A/01.png'
        png(path, 'A secret')
        with Image.open(path) as image:
            image = image.convert('RGB')
        x, y = 88 % image.width, 88 // image.width
        red, green, blue = image.getpixel((x, y))
        image.putpixel((x, y), (red ^ 1, green, blue))
        image.save(path)
        _, data = export(self.source, self.output)
        self.assertIsNotNone(data['chains'][0]['slides'][0]['src'])
        self.assertIsNone(data['chains'][0]['slides'][0]['prompt'])
        self.assertEqual(len(data['warnings']), 1)

    def test_prompt_is_text_not_html_or_liquid(self):
        prompt = '</script><script>window.pwned=1</script>\n{{ site.title }} & "quotes"'
        png(self.source / 'Group_A/01.png', prompt)
        html, data = export(self.source, self.output)
        self.assertEqual(data['chains'][0]['slides'][0]['prompt'], prompt)
        self.assertNotIn(prompt, html)
        self.assertIn('\\u003c/script>', html)
        self.assertNotIn('.innerHTML', html)

    def test_existing_and_nested_outputs_are_never_touched(self):
        original = png(self.source / 'Group_A/01.png', 'A scene')
        self.output.mkdir()
        sentinel = self.output / 'keep.txt'
        sentinel.write_text('do not change')
        for output, error in [(self.output, FileExistsError), (self.source, ValueError),
                              (self.source / 'nested', ValueError), (self.root, ValueError)]:
            with self.subTest(output=output), self.assertRaises(error):
                export(self.source, output)
        self.assertEqual(sentinel.read_text(), 'do not change')
        self.assertEqual((self.source / 'Group_A/01.png').read_bytes(), original)

    def test_linked_files_are_not_published(self):
        png(self.source / 'Group_A/01.png', 'Local')
        outside = self.root / 'outside.png'
        png(outside, 'Not part of the class')
        try:
            (self.source / 'Group_A/02.png').symlink_to(outside)
        except OSError:
            self.skipTest('Creating symlinks is unavailable in this environment')
        _, data = export(self.source, self.output)
        self.assertIsNone(data['chains'][1]['slides'][0]['src'])
        self.assertTrue(any('linked file' in w for w in data['warnings']))

    @unittest.skipUnless(os.environ.get('RUN_REVEAL_BROWSER_TESTS') == '1', 'Optional real browser check')
    def test_browser_file_and_nested_website(self):
        from playwright.sync_api import sync_playwright
        prompt = '</script><img src=x onerror="window.pwned=1">\nA lake.'
        for step in range(1, 6):
            name = '_'.join(f'{i:02d}' for i in range(1, step + 1)) + '.png'
            png(self.source / 'Group_A' / name, prompt if step == 1 else f'Prompt {step}')
        export(self.source, self.output)
        website = self.root / 'web' / 'course/galleries/telephone'
        shutil.copytree(self.output, website)
        handler = functools.partial(SimpleHTTPRequestHandler, directory=str(self.root / 'web'))
        server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        urls = [self.output.joinpath('index.html').as_uri(),
                f'http://127.0.0.1:{server.server_port}/course/galleries/telephone/index.html']
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH'), args=['--no-sandbox'])
            for url in urls:
                with self.subTest(url=url):
                    page = browser.new_page(viewport={'width': 1366, 'height': 768})
                    errors, requests = [], []
                    page.on('pageerror', lambda e: errors.append(str(e)))
                    page.on('request', lambda r: requests.append(r.url))
                    page.goto(url)
                    page.wait_for_function("document.querySelector('#hero').naturalWidth > 0")
                    self.assertFalse(page.locator('#prompt').is_visible())
                    page.locator('#reveal').click()
                    self.assertEqual(page.locator('#prompt').inner_text(), prompt)
                    self.assertIsNone(page.evaluate('window.pwned'))
                    page.locator('#next').click()
                    self.assertFalse(page.locator('#prompt').is_visible())
                    for _ in range(4):
                        page.locator('#next').click()
                    self.assertTrue(page.locator('#summary').is_visible())
                    self.assertEqual(page.locator('.card').count(), 5)
                    self.assertEqual(page.locator('.card p').first.inner_text(), prompt)
                    page.locator('#next').click()
                    self.assertIn('Chain 02', page.locator('#progress').inner_text())
                    self.assertTrue(page.locator('#empty').is_visible())
                    page.locator('#chain').select_option('0')
                    page.locator('#next').click()
                    page.keyboard.press('p')
                    self.assertTrue(page.locator('#prompt').is_visible())
                    page.keyboard.press('ArrowRight')
                    self.assertIn('Round 3', page.locator('#progress').inner_text())
                    self.assertFalse(page.locator('#prompt').is_visible())
                    self.assertEqual(errors, [])
                    self.assertTrue(all(r.startswith(('file:', 'http://127.0.0.1:')) for r in requests))
                    page.set_viewport_size({'width': 390, 'height': 844})
                    self.assertTrue(page.evaluate('document.documentElement.scrollWidth <= innerWidth'))
                    page.close()
            browser.close()


if __name__ == '__main__':
    unittest.main()
