"""Offline teaching-flow tests. No API credentials or paid requests."""
import contextlib
import io
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch
from types import SimpleNamespace
from zipfile import ZipFile

import nbformat
from nbclient import NotebookClient
from PIL import Image, PngImagePlugin
from IPython.core.inputtransformer2 import TransformerManager

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "notebooks"
sys.path.insert(0, str(NOTEBOOKS))
import telephone_helpers as helper


def sources(name):
    return [cell.source for cell in nbformat.read(NOTEBOOKS / name, as_version=4).cells
            if cell.cell_type == "code"]


def basic_cells():
    return {cell.id: cell.source for cell in nbformat.read(
        NOTEBOOKS / "01_replicate_basics.ipynb", as_version=4).cells if cell.cell_type == "code"}


def prediction_client(status="succeeded", output=("https://example.invalid/image.png",)):
    prediction = SimpleNamespace(
        id="test-prediction", status=status,
        output=list(output) if output is not None else None, wait=Mock())
    return SimpleNamespace(
        models=SimpleNamespace(get=Mock(return_value=SimpleNamespace(
            latest_version=SimpleNamespace(id="test-version")))),
        predictions=SimpleNamespace(create=Mock(return_value=prediction)))


def context(group="A", seat=1, round_number=1, mode="practice"):
    return {**helper.route(group, seat, round_number), "prompt": "A test scene", "mode": mode,
            "settings": {"num_outputs": 1}, "model": "test/model"}


@contextlib.contextmanager
def working_directory(folder):
    previous = Path.cwd()
    os.chdir(folder)
    try:
        yield
    finally:
        os.chdir(previous)


class TestTelephone(unittest.TestCase):
    def test_all_group_round_routes(self):
        for group in "ABCDEF":
            for round_number in range(1, 6):
                outputs = set()
                for seat in range(1, 6):
                    item = helper.route(group, seat, round_number)
                    self.assertEqual(item["folder"], f"Group_{group}")
                    self.assertEqual(len(item["outgoing"].removesuffix(".png").split("_")), round_number)
                    outputs.add(item["outgoing"])
                    if round_number > 1:
                        previous = helper.route(group, (seat - 2) % 5 + 1, round_number - 1)
                        self.assertEqual(item["incoming"], previous["outgoing"])
                        self.assertEqual(previous["send_to"], seat)
                self.assertEqual(len(outputs), 5)
        self.assertEqual(helper.route("A", 1, 2)["outgoing"], "05_01.png")
        self.assertEqual(helper.route("A", 1, 5)["outgoing"], "02_03_04_05_01.png")

    def test_invalid_identity(self):
        for args in [("../A", 1, 1), ("A", 0, 1), ("A", 1, 6), ("A", True, 1)]:
            with self.assertRaises(ValueError):
                helper.route(*args)
        with self.assertRaises(ValueError):
            helper.session_root("../../elsewhere", "A", 1)

    def test_upload_and_metadata_stripping(self):
        image = Image.new("RGB", (20, 20), "red")
        metadata = PngImagePlugin.PngInfo()
        metadata.add_text("prompt", "PRIVATE PROMPT")
        buffer = io.BytesIO()
        image.save(buffer, format="PNG", pnginfo=metadata)
        data = helper.uploaded_image([{"name": "05.png", "content": memoryview(buffer.getvalue())}], "05.png")
        with Image.open(io.BytesIO(data)) as cleaned:
            self.assertEqual(cleaned.info, {})
        self.assertNotIn(b"PRIVATE PROMPT", data)
        with self.assertRaises(ValueError):
            helper.uploaded_image([{"name": "04.png", "content": data}], "05.png")
        with self.assertRaises(ValueError):
            helper.uploaded_image([], "05.png")
        with self.assertRaises(Exception):
            helper.uploaded_image([{"name": "05.png", "content": b"not an image"}], "05.png")

    def test_history_export_and_collision(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            info = context()
            info["api_token"] = "private-credential-sentinel"
            run = helper.save_record(root, info, helper.practice_image())
            info["prompt"] = "Changed later"
            record = helper.history(root)[0]
            self.assertEqual(record["prompt"], "A test scene")
            self.assertNotIn("api_token", record)
            self.assertNotIn("private-credential-sentinel", (run / "record.json").read_text())
            handoff = helper.export_handoff(root, run)
            self.assertEqual(handoff.name, "01.png")
            self.assertIn("practice_handoff", handoff.parts)
            self.assertEqual(helper.export_handoff(root, run), handoff)
            replacement = helper.save_record(root, context(), helper.practice_image(2))
            with self.assertRaises(FileExistsError):
                helper.export_handoff(root, replacement)
            archive = helper.export_after_reveal(root)
            with ZipFile(archive) as bundle:
                self.assertEqual(len(bundle.namelist()), 4)
                self.assertTrue(all(name.endswith(("image.png", "record.json")) for name in bundle.namelist()))


class TestNotebooks(unittest.TestCase):
    def test_clean_notebook_sources(self):
        for path in NOTEBOOKS.glob("*.ipynb"):
            nb = nbformat.read(path, as_version=4)
            nbformat.validate(nb)
            self.assertNotIn(chr(0x2014), path.read_text())
            self.assertNotIn("widgets", nb.metadata)
            for cell in nb.cells:
                if cell.cell_type == "code":
                    self.assertIsNone(cell.execution_count)
                    self.assertEqual(cell.outputs, [])
                    compile(TransformerManager().transform_cell(cell.source), str(path), "exec")

    def test_all_offline_cells_execute_in_order(self):
        import replicate
        for path in NOTEBOOKS.glob("*.ipynb"):
            if path.name == "01_replicate_basics.ipynb":
                continue  # Real generation only; tested below with mocked Replicate.
            with self.subTest(notebook=path.name), tempfile.TemporaryDirectory() as folder:
                with working_directory(folder), contextlib.redirect_stdout(io.StringIO()):
                    with patch.object(replicate.Client, "run", side_effect=AssertionError("Offline API call")):
                        namespace = {}
                        notebook = nbformat.read(path, as_version=4)
                        for cell in notebook.cells:
                            if cell.cell_type == "code" and "setup" not in cell.metadata.get("tags", []):
                                exec(cell.source, namespace)

    @unittest.skipUnless(os.environ.get("RUN_JUPYTER_KERNEL_TESTS") == "1", "Optional full kernel test; enable in an environment permitting local kernel sockets")
    def test_notebooks_execute_offline_in_kernel(self):
        for path in NOTEBOOKS.glob("*.ipynb"):
            if path.name == "01_replicate_basics.ipynb":
                continue  # Real generation only; tested below with mocked Replicate.
            with self.subTest(notebook=path.name), tempfile.TemporaryDirectory() as folder:
                for helper_path in NOTEBOOKS.glob("telephone_*.py"):
                    shutil.copy(helper_path, folder)
                nb = nbformat.read(path, as_version=4)
                nb.cells = [cell for cell in nb.cells if "setup" not in cell.metadata.get("tags", [])]
                # Assert even an accidental SDK call cannot contact Replicate.
                nb.cells.insert(0, nbformat.v4.new_code_cell(
                    "import replicate\n"
                    "def forbidden(*args, **kwargs):\n    raise AssertionError('Offline API call')\n"
                    "replicate.Client.run = forbidden\n"))
                NotebookClient(nb, timeout=90, kernel_name="python3").execute(cwd=folder)

    def test_basic_connect_generate_view_and_save_without_extra_requests(self):
        import replicate
        cells = basic_cells()
        image_bytes = helper.practice_image()  # Test fixture only, never in the notebook.
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
                    ns = {"client": client, "image_bytes": helper.practice_image(), "output": ["old"]}
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
            with patch("urllib.request.urlopen", return_value=io.BytesIO(helper.practice_image())):
                exec(cells["view"], ns)
            exec(cells["save"], ns)
            self.assertTrue(Path("my-image-01.png").exists())
            self.assertEqual(client.predictions.create.call_count, 1)

    def test_error_message_does_not_echo_token(self):
        class APIError(Exception):
            status = 401
        result = helper.error_message(APIError("private-credential-sentinel"))
        self.assertNotIn("private-credential-sentinel", result)
        self.assertIn("token", result)


if __name__ == "__main__":
    unittest.main()
