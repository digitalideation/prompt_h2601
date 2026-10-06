"""Offline teaching-flow tests. No API credentials or paid requests."""
import builtins
import contextlib
import io
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch
from zipfile import ZipFile

import nbformat
from nbclient import NotebookClient
from PIL import Image, PngImagePlugin

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "notebooks"
sys.path.insert(0, str(NOTEBOOKS))
import telephone_helpers as helper


def sources(name):
    return [cell.source for cell in nbformat.read(NOTEBOOKS / name, as_version=4).cells
            if cell.cell_type == "code"]


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
                    compile(cell.source, str(path), "exec")

    def test_all_offline_cells_execute_in_order(self):
        import replicate
        for path in NOTEBOOKS.glob("*.ipynb"):
            with self.subTest(notebook=path.name), tempfile.TemporaryDirectory() as folder:
                with working_directory(folder), contextlib.redirect_stdout(io.StringIO()):
                    with patch.object(replicate.Client, "run", side_effect=AssertionError("Offline API call")):
                        namespace = {}
                        for source in sources(path.name):
                            exec(source, namespace)
                        self.assertTrue(list(Path(folder).rglob("image.png")))
                        self.assertTrue(list(Path(folder).rglob("*.json")))

    @unittest.skipUnless(os.environ.get("RUN_JUPYTER_KERNEL_TESTS") == "1", "Optional full kernel test; enable in an environment permitting local kernel sockets")
    def test_notebooks_execute_offline_in_kernel(self):
        for path in NOTEBOOKS.glob("*.ipynb"):
            with self.subTest(notebook=path.name), tempfile.TemporaryDirectory() as folder:
                shutil.copy(NOTEBOOKS / "telephone_helpers.py", folder)
                nb = nbformat.read(path, as_version=4)
                # Assert even an accidental SDK call cannot contact Replicate.
                nb.cells.insert(0, nbformat.v4.new_code_cell(
                    "import replicate\n"
                    "def forbidden(*args, **kwargs):\n    raise AssertionError('Offline API call')\n"
                    "replicate.Client.run = forbidden\n"))
                NotebookClient(nb, timeout=90, kernel_name="python3").execute(cwd=folder)
                self.assertTrue(list(Path(folder).rglob("image.png")))
                self.assertTrue(list(Path(folder).rglob("*.json")))

    def test_basic_live_call_and_save_are_separate(self):
        cells = sources("01_replicate_basics.ipynb")
        with tempfile.TemporaryDirectory() as folder, working_directory(folder), contextlib.redirect_stdout(io.StringIO()):
            ns = {}
            exec(cells[0], ns)
            exec(cells[2], ns)
            calls = []

            class FileOutput:
                def read(self):
                    return helper.practice_image()

            class FakeClient:
                def run(self, model, **kwargs):
                    calls.append((model, kwargs))
                    return [FileOutput()]

            ns.update(LIVE=True, client=FakeClient())
            with patch.object(builtins, "input", return_value="GENERATE"):
                exec(cells[3], ns)
            ns["inputs"]["prompt"] = "Changed after generation"
            exec(cells[4], ns)
            exec(cells[4], ns)
            self.assertEqual(len(calls), 1)
            record = json.loads((ns["run_folder"] / "prompt.json").read_text())
            self.assertNotEqual(record["inputs"]["prompt"], "Changed after generation")
            self.assertEqual(calls[0][1]["use_file_output"], True)
            with patch.object(builtins, "input", return_value="CANCEL"):
                exec(cells[3], ns)
            self.assertEqual(len(calls), 1)
            self.assertIsNone(ns["run_context"])

    def test_telephone_live_flow_requires_incoming_and_does_not_send_it(self):
        cells = sources("02_artistic_telephone.ipynb")
        with tempfile.TemporaryDirectory() as folder, working_directory(folder), contextlib.redirect_stdout(io.StringIO()):
            ns = {}
            exec(cells[0], ns)
            exec(cells[1], ns)
            ns["mode_choice"].value = True
            ns["round_choice"].value = 2
            exec(cells[2], ns)
            exec(cells[5], ns)
            calls = []

            class FileOutput:
                def read(self):
                    return helper.practice_image()

            class FakeClient:
                def run(self, model, **kwargs):
                    calls.append(kwargs)
                    return [FileOutput()]

            ns["client"] = FakeClient()
            with patch.object(builtins, "input", return_value="GENERATE"):
                exec(cells[7], ns)
                self.assertEqual(len(calls), 0)
                ns["incoming_bytes"] = helper.practice_image()
                ns["source_filename"] = "05.png"
                exec(cells[7], ns)
            exec(cells[8], ns)
            exec(cells[8], ns)
            exec(cells[9], ns)
            self.assertEqual(len(calls), 1)
            self.assertNotIn("image", calls[0]["input"])
            self.assertEqual(ns["handoff"].name, "05_01.png")
            self.assertIn("handoff", ns["handoff"].parts)
            self.assertEqual(len(helper.history(ns["root"])), 1)

    def test_error_message_does_not_echo_token(self):
        class APIError(Exception):
            status = 401
        result = helper.error_message(APIError("private-credential-sentinel"))
        self.assertNotIn("private-credential-sentinel", result)
        self.assertIn("token", result)


if __name__ == "__main__":
    unittest.main()
