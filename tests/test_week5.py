"""Focused offline tests for current standalone course notebooks."""
import contextlib
import io
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
from types import SimpleNamespace

import nbformat
from PIL import Image
from IPython.core.inputtransformer2 import TransformerManager

NOTEBOOKS = Path(__file__).resolve().parents[1] / "notebooks"


def practice_image():
    output = io.BytesIO()
    Image.new("RGB", (128, 128), "steelblue").save(output, format="PNG")
    return output.getvalue()


def basic_cells(name="01_replicate_basics.ipynb"):
    return {cell.id: cell.source for cell in nbformat.read(NOTEBOOKS / name, as_version=4).cells
            if cell.cell_type == "code"}


def prediction_client(status="succeeded", output=("https://example.invalid/image.png",)):
    prediction = SimpleNamespace(id="test-prediction", status=status,
        output=list(output) if output is not None else None, wait=Mock())
    return SimpleNamespace(models=SimpleNamespace(get=Mock(return_value=SimpleNamespace(
        latest_version=SimpleNamespace(id="test-version")))),
        predictions=SimpleNamespace(create=Mock(return_value=prediction)))


@contextlib.contextmanager
def working_directory(folder):
    old = Path.cwd()
    os.chdir(folder)
    try:
        yield
    finally:
        os.chdir(old)


class TestNotebooks(unittest.TestCase):
    def test_clean_notebook_sources(self):
        for path in NOTEBOOKS.glob("*.ipynb"):
            nb = nbformat.read(path, as_version=4)
            nbformat.validate(nb)
            self.assertNotIn("widgets", nb.metadata)
            for cell in nb.cells:
                if cell.cell_type == "code":
                    self.assertIsNone(cell.execution_count)
                    self.assertEqual(cell.outputs, [])
                    compile(TransformerManager().transform_cell(cell.source), str(path), "exec")

    def test_student_telephone_is_standalone(self):
        cells = basic_cells("03_artistic_telephone.ipynb")
        code = "\n".join(cells.values())
        for snippet in ("def generate_image(inputs, client, MODEL):",
                        "encoded = encode_text(original, prompt_used, steg)",
                        "round_box = widgets.Dropdown(", "prompt_box = widgets.Textarea(",
                        "attempt_box = widgets.Dropdown(", "decode_text(encoded, steg)"):
            self.assertIn(snippet, code)
        for obsolete in ("FileUpload(", "from telephone_", "%pip install -r requirements.txt"):
            self.assertNotIn(obsolete, code)

    def test_telephone_filename_calculator(self):
        code = basic_cells("03_artistic_telephone.ipynb")["play-ui"]
        start = code.index("def filenames(round_number):")
        end = code.index("\n\n", start)
        namespace = {"SEAT": 1}
        exec(code[start:end], namespace)
        self.assertEqual(namespace["filenames"](2), ("05.png", "05_01.png"))
        self.assertEqual(namespace["filenames"](5)[1], "02_03_04_05_01.png")

    def test_basic_connect_generate_view_and_save_without_extra_requests(self):
        import replicate
        cells = basic_cells()
        image_bytes = practice_image()  # Test fixture only, never in the notebook.
        client = prediction_client()
        with tempfile.TemporaryDirectory() as folder, working_directory(folder), contextlib.redirect_stdout(io.StringIO()) as printed:
            ns = {}
            with patch("getpass.getpass", return_value="test-token"), patch.object(replicate, "Client", return_value=client):
                exec(cells["connect"], ns)
            exec(cells["prompt"], ns)
            exec(cells["generate-function"], ns)
            exec(cells["generate"], ns)
            client.models.get.assert_called_once_with("black-forest-labs/flux-schnell")
            request = client.predictions.create.call_args.kwargs
            self.assertEqual(request["version"], "test-version")
            self.assertEqual(request["input"]["prompt"], ns["prompt"])
            self.assertEqual(request["input"]["output_format"], "png")
            client.predictions.create.return_value.wait.assert_called_once()
            with patch("urllib.request.urlopen", side_effect=lambda *a, **k: io.BytesIO(image_bytes)) as download:
                exec(cells["view"], ns)
                self.assertEqual(download.call_args.args, ("https://example.invalid/image.png",))
                exec(cells["save"], ns)
                self.assertEqual(Path("my-image-01.png").read_bytes(), image_bytes)
                exec(cells["view"], ns)
            with self.assertRaises(FileExistsError):
                exec(cells["save"], ns)
            self.assertEqual(Path("my-image-01.png").read_bytes(), image_bytes)
            self.assertEqual(client.predictions.create.call_count, 1)
            self.assertIn("test-prediction", printed.getvalue())
            self.assertNotIn("test-token", printed.getvalue())

    def test_basic_failed_generation_cannot_save_a_previous_image(self):
        cells = basic_cells()
        for status, output in [("failed", None), ("canceled", None), ("succeeded", ()), ("succeeded", None)]:
            with self.subTest(status=status, output=output), tempfile.TemporaryDirectory() as folder:
                with working_directory(folder), contextlib.redirect_stdout(io.StringIO()):
                    client = prediction_client(status, output)
                    ns = {"client": client, "image_bytes": practice_image(), "output": ["old"]}
                    exec(cells["prompt"], ns)
                    exec(cells["generate-function"], ns)
                    with self.assertRaises(ns["GenerationError"]):
                        exec(cells["generate"], ns)
                    self.assertIsNone(ns["output"])
                    self.assertIsNone(ns["image_bytes"])
                    exec(cells["save"], ns)
                    self.assertFalse(Path("my-image-01.png").exists())
                    self.assertEqual(client.predictions.create.call_count, 1)

    def test_basic_download_retry_does_not_generate_again(self):
        cells = basic_cells()
        client = prediction_client()
        with tempfile.TemporaryDirectory() as folder, working_directory(folder), contextlib.redirect_stdout(io.StringIO()):
            ns = {"client": client}
            exec(cells["prompt"], ns)
            exec(cells["generate-function"], ns)
            exec(cells["generate"], ns)
            with patch("urllib.request.urlopen", side_effect=OSError("Interrupted download")):
                with self.assertRaises(OSError):
                    exec(cells["view"], ns)
            self.assertIsNone(ns["image_bytes"])
            with patch("urllib.request.urlopen", return_value=io.BytesIO(practice_image())):
                exec(cells["view"], ns)
            exec(cells["save"], ns)
            self.assertTrue(Path("my-image-01.png").exists())
            self.assertEqual(client.predictions.create.call_count, 1)

    def test_scene_sentence_prompt_reaches_prediction_and_revises(self):
        import replicate
        cells = basic_cells("02_replicate_scene_prompts.ipynb")
        # The working API path, connection and image loading remain identical.
        for cell_id in ("connect", "generate-function", "generate", "view"):
            self.assertEqual(cells[cell_id], basic_cells()[cell_id])
        client = prediction_client()
        data = practice_image()  # A fixture for the downloader only.
        with tempfile.TemporaryDirectory() as folder, working_directory(folder), contextlib.redirect_stdout(io.StringIO()):
            ns = {}
            with patch("getpass.getpass", return_value="test-token"), patch.object(replicate, "Client", return_value=client):
                exec(cells["connect"], ns)
            exec(cells["prompt"], ns)
            exec(cells["build"], ns)
            first_prompt = ns["prompt"]
            self.assertIn("Show a cyclist wearing a mustard-yellow raincoat riding slowly across a stone bridge.", first_prompt)
            self.assertIn("The scene takes place in a quiet riverside town at dawn, with warm orange light filtering through mist.", first_prompt)
            self.assertEqual(client.predictions.create.call_count, 0)
            exec(cells["generate-function"], ns)
            exec(cells["generate"], ns)
            self.assertEqual(client.predictions.create.call_args.kwargs["input"]["prompt"], first_prompt)
            with patch("urllib.request.urlopen", return_value=io.BytesIO(data)):
                exec(cells["view"], ns)
            exec(cells["save"], ns)
            self.assertEqual(Path("my-scene-01.png").read_bytes(), data)
            ns["scene"]["composition"] = "a wide shot from above"
            exec(cells["build"], ns)
            self.assertIn("frame the scene as a wide shot from above.", ns["prompt"])
            self.assertNotIn("street level", ns["prompt"])
            self.assertEqual(client.predictions.create.call_count, 1)
            exec(cells["generate"], ns)
            self.assertEqual(client.predictions.create.call_args.kwargs["input"]["prompt"], ns["prompt"])
            self.assertEqual(client.predictions.create.call_count, 2)
            self.assertEqual(Path("my-scene-01.png").read_bytes(), data)
            self.assertIsNone(ns["image_bytes"])


if __name__ == "__main__":
    unittest.main()
