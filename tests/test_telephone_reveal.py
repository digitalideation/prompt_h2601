"""Exercise the selected-image path without API credentials or network."""
import contextlib
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from PIL import Image
import nbformat

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "notebooks"))
from telephone_helpers import route, practice_image, history, save_record, export_handoff, rebuild_handoff
from telephone_attempts import Attempts
from telephone_steg import encode, decode, HEADER
from telephone_gallery import scan, render
from telephone_presentation import ordered_chains, chain_positions, image_slide, summary_slide, RevealPlayer


def context(seat=1, round_number=1, prompt="A calm lake"):
    return {**route("A", seat, round_number), "session": "class1", "mode": "practice",
            "prompt": prompt, "model": "test/model", "settings": {"num_outputs": 1}}


class TelephoneRevealTests(unittest.TestCase):
    def test_unicode_pixels_and_no_metadata(self):
        source = practice_image()
        record = context(prompt="Un lac bleu, été, 日本語")
        record["api_token"] = "secret-sentinel"
        encoded = encode(source, record)
        decoded = decode(encoded)
        self.assertEqual(decoded["prompt"], record["prompt"])
        self.assertNotIn("api_token", decoded)
        with Image.open(io.BytesIO(source)) as a, Image.open(io.BytesIO(encoded)) as b:
            self.assertEqual(b.info, {})
            self.assertTrue(all(abs(x-y) <= 1 for x, y in zip(a.tobytes(), b.tobytes())))
        with self.assertRaises(ValueError):
            encode(self.small_png(), record)
        with self.assertRaises(ValueError):
            decode(source)
        with Image.open(io.BytesIO(encoded)) as image:
            pixels = bytearray(image.tobytes())
            pixels[HEADER * 8 + 1] ^= 1
            damaged = Image.frombytes("RGB", image.size, bytes(pixels))
            output = io.BytesIO()
            damaged.save(output, format="PNG")
        with self.assertRaisesRegex(ValueError, "damaged"):
            decode(output.getvalue())

    @staticmethod
    def small_png():
        output = io.BytesIO()
        Image.new("RGB", (4, 4)).save(output, format="PNG")
        return output.getvalue()

    def test_iterate_select_earlier_and_prevent_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            attempts = Attempts(folder)
            first_context = context()
            attempts.generate(first_context)
            first_context["prompt"] = "edited afterwards"
            first = attempts.save()
            self.assertEqual(attempts.save(), first)
            attempts.generate(context(prompt="A different lake"))
            second = attempts.save()
            self.assertEqual(len(history(folder)), 2)
            handoff = export_handoff(folder, first)
            self.assertEqual(decode(handoff.read_bytes())["prompt"], "A calm lake")
            self.assertEqual(export_handoff(folder, first), handoff)
            with self.assertRaises(FileExistsError):
                export_handoff(folder, second)
            self.assertNotIn("schema", json.loads((first / "record.json").read_text()))

    def test_verified_export_and_rebuild_of_old_damaged_handoff(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            attempts = Attempts(root)
            attempts.generate(context())
            run = attempts.save()
            target = export_handoff(root, run)
            self.assertEqual(decode(target.read_bytes())["prompt"], "A calm lake")
            target.write_bytes(practice_image())  # Simulate an old invalid PNG.
            with self.assertRaises(FileExistsError):
                export_handoff(root, run)
            replacement = rebuild_handoff(root, run)
            self.assertNotEqual(replacement, target)
            self.assertEqual(decode(replacement.read_bytes())["prompt"], "A calm lake")
            with self.assertRaises(ValueError):
                decode(target.read_bytes())

    def test_live_retry_snapshot_and_recovery_do_not_generate(self):
        with tempfile.TemporaryDirectory() as folder:
            prediction = SimpleNamespace(id="p123", wait=Mock(), reload=Mock(),
                                         status="succeeded", output=["https://example.invalid/image.png"])
            create = Mock(return_value=prediction)
            client = SimpleNamespace(
                models=SimpleNamespace(get=Mock(return_value=SimpleNamespace(latest_version=SimpleNamespace(id="v123")))),
                predictions=SimpleNamespace(create=create, get=Mock(return_value=prediction)))
            attempts = Attempts(folder)
            record = context(seat=1, round_number=2)
            record.update(mode="live", source_filename="05.png")
            with self.assertRaises(ValueError):
                attempts.generate(record, client)
            self.assertEqual(create.call_count, 0)
            attempts.generate(record, client, practice_image())
            record["prompt"] = "later edit"
            record["settings"]["num_outputs"] = 99
            self.assertNotIn("image", create.call_args.kwargs["input"])
            self.assertEqual(create.call_args.kwargs["version"], "v123")
            with self.assertRaises(ValueError):
                attempts.generate(record, client, practice_image())
            with self.assertRaises(OSError):
                attempts.save(downloader=Mock(side_effect=OSError("offline")))
            resumed = Attempts(folder)
            resumed.resume(client)
            saved = resumed.save(downloader=lambda _: practice_image())
            record = json.loads((saved / "record.json").read_text())
            self.assertEqual(record["prompt"], "A calm lake")
            self.assertEqual(record["settings"]["num_outputs"], 1)
            self.assertEqual(record["prediction_id"], "p123")
            self.assertEqual(record["model_version"], "v123")
            self.assertEqual(create.call_count, 1)
            self.assertFalse((Path(folder) / "pending.json").exists())

    def test_failed_prediction_cannot_save_or_export_previous_attempt(self):
        with tempfile.TemporaryDirectory() as folder:
            prediction = SimpleNamespace(id="bad", wait=Mock(), reload=Mock(), status="failed", output=None)
            client = SimpleNamespace(
                models=SimpleNamespace(get=lambda _: SimpleNamespace(latest_version=SimpleNamespace(id="v"))),
                predictions=SimpleNamespace(create=lambda **_: prediction))
            attempts = Attempts(folder)
            attempts.generate(context())
            attempts.save()
            record = context()
            record["mode"] = "live"
            attempts.generate(record, client)
            with self.assertRaises(ValueError):
                attempts.save()
            self.assertIsNone(attempts.saved_run)
            prediction.status = "processing"
            with self.assertRaises(ValueError):
                attempts.discard_failed()
            prediction.status = "failed"
            attempts.discard_failed()
            self.assertIsNone(attempts.pending)
            self.assertEqual(len(history(folder)), 1)

    def test_full_chain_missing_duplicates_and_escaped_prompts(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            group = root / "Group_A"
            group.mkdir()
            for round_number in range(1, 6):
                record = context(seat=round_number, round_number=round_number, prompt="<script>alert(1)</script>")
                (group / record["outgoing"]).write_bytes(encode(practice_image(round_number), record))
            records, warnings = scan(root)
            self.assertEqual(len(records), 5)
            self.assertEqual(warnings, [])
            html = render(records, warnings)
            self.assertNotIn("<script>", html)
            self.assertIn("&lt;script&gt;", html)
            self.assertIn("data:image/png;base64,", html)
            positions = [html.index(">" + "_".join(f"{s:02}" for s in range(1, r+1)) + ".png<") for r in range(1, 6)]
            self.assertEqual(positions, sorted(positions))
            self.assertEqual(html.count("Missing image"), 20)
            duplicate = root / "copy" / "Group_A"
            duplicate.mkdir(parents=True)
            shutil.copy(group / "01.png", duplicate)
            (group / "01_02.png").unlink()
            (group / "broken.png").write_bytes(b"bad")
            records, warnings = scan(root)
            self.assertEqual(len(warnings), 2)
            self.assertIn("Duplicate: resolve files", render(records, warnings))
            self.assertEqual(render(records, warnings).count("Missing image"), 21)

    def test_plain_pngs_show_in_correct_positions_without_records(self):
        with tempfile.TemporaryDirectory() as folder:
            group = Path(folder) / "Group_A"
            group.mkdir()
            # Like an ordinary downloaded image: a valid PNG but no Telephone bits.
            (group / "01.png").write_bytes(practice_image())
            (group / "05_01.png").write_bytes(practice_image())
            records, warnings = scan(folder)
            self.assertEqual(warnings, [])
            self.assertEqual(len(records), 2)
            self.assertIn(("unrecorded", "unrecorded", "A", 1, 1), records)
            self.assertIn(("unrecorded", "unrecorded", "A", 5, 2), records)
            html = render(records, warnings)
            self.assertEqual(html.count("data:image/png;base64,"), 2)
            self.assertEqual(html.count("Prompt unavailable"), 2)
            self.assertNotIn("Reveal prompt and settings", html)

            records, warnings = scan(
                folder, fallback_session="class1", fallback_mode="live",
                prompt_overrides={"Group_A/01.png": "<script>alert('bad')</script>"},
            )
            self.assertEqual(warnings, [])
            html = render(records, warnings)
            self.assertIn("Reveal separately supplied prompt", html)
            self.assertIn("&lt;script&gt;", html)
            self.assertNotIn("<script>", html)
            self.assertEqual(html.count("Prompt unavailable"), 1)

    def test_plain_and_embedded_images_share_known_session(self):
        with tempfile.TemporaryDirectory() as folder:
            group = Path(folder) / "Group_A"
            group.mkdir()
            (group / "01.png").write_bytes(encode(practice_image(), context()))
            (group / "05_01.png").write_bytes(practice_image())
            records, warnings = scan(folder)
            self.assertEqual(warnings, [])
            self.assertEqual(len(records), 2)
            self.assertIn(("class1", "practice", "A", 1, 1), records)
            self.assertIn(("class1", "practice", "A", 5, 2), records)
            html = render(records, warnings)
            self.assertIn("A calm lake", html)
            self.assertEqual(html.count("Prompt unavailable"), 1)

            (group / "02_01.png").write_bytes(practice_image())  # Invalid seat order.
            records, warnings = scan(folder)
            self.assertEqual(len(records), 2)
            self.assertTrue(any("clockwise seat order" in msg for msg in warnings))

    def test_damaged_prompt_record_keeps_image_visible(self):
        with tempfile.TemporaryDirectory() as folder:
            group = Path(folder) / "Group_A"
            group.mkdir()
            encoded = encode(practice_image(), context())
            with Image.open(io.BytesIO(encoded)) as image:
                pixels = bytearray(image.tobytes())
                pixels[HEADER * 8 + 1] ^= 1
                damaged = Image.frombytes("RGB", image.size, bytes(pixels))
                out = io.BytesIO()
                damaged.save(out, format="PNG")
            (group / "01.png").write_bytes(out.getvalue())
            records, warnings = scan(folder)
            self.assertEqual(len(records), 1)
            self.assertTrue(any("unreadable" in msg for msg in warnings))
            self.assertIn("Prompt unavailable", render(records, warnings))

    def test_cinematic_reveal_hides_prompts_until_requested(self):
        with tempfile.TemporaryDirectory() as folder:
            group = Path(folder) / "Group_A"
            group.mkdir()
            first = context(prompt="Secret for the final reveal")
            (group / "01.png").write_bytes(encode(practice_image(), first))
            (group / "05_01.png").write_bytes(practice_image())
            records, warnings = scan(folder)
            self.assertEqual(warnings, [])
            chains = ordered_chains(records)
            self.assertEqual(chains, [
                ("class1", "practice", "A", 1),
                ("class1", "practice", "A", 5),
            ])
            positions = chain_positions(records, chains[0])
            self.assertEqual(len(positions), 5)
            self.assertEqual(positions[1]["status"], "missing")
            self.assertNotIn(first["prompt"], image_slide(chains[0], positions[0], 1, 5))
            self.assertIn("height:min(420px,55vh)", image_slide(chains[0], positions[0], 1, 5))
            self.assertNotIn("min-height:70vh", image_slide(chains[0], positions[0], 1, 5))
            self.assertIn("height:min(320px,55vh)", image_slide(chains[0], positions[0], 1, 5, image_height=320))
            self.assertIn(first["prompt"], summary_slide(records, chains[0]))
            self.assertIn("Prompt unavailable", summary_slide(records, chains[1]))
            presenter = RevealPlayer(records)
            self.assertNotIn(first["prompt"], presenter.stage.value + presenter.prompt.value)
            presenter._reveal(None)
            self.assertIn(first["prompt"], presenter.prompt.value)
            presenter._next(None)
            self.assertEqual(presenter.prompt.value, "")
            for _ in range(4):
                presenter._next(None)
            self.assertEqual(presenter.slide_index, 5)
            self.assertIn(first["prompt"], presenter.stage.value)
            presenter._next(None)
            self.assertEqual(presenter.chain_index, 1)
            self.assertEqual(presenter.slide_index, 0)

    def test_notebook_round_steps_and_prompts_follow_inspection(self):
        notebook = Path(__file__).resolve().parents[1] / "notebooks" / "02_artistic_telephone.ipynb"
        cells = nbformat.read(notebook, as_version=4).cells
        ids = [c.id for c in cells]
        self.assertEqual(len(ids), len(set(ids)))
        steps = ["telephone-6", "telephone-upload-widget", "telephone-8",
                 "telephone-prompt-widget", "telephone-10", "telephone-12"]
        self.assertEqual([ids.index(i) for i in steps], sorted(ids.index(i) for i in steps))
        round_code = next(c.source for c in cells if c.id == "telephone-6")
        inspect_code = next(c.source for c in cells if c.id == "telephone-8")
        prompt_code = next(c.source for c in cells if c.id == "telephone-prompt-widget")
        generate_code = next(c.source for c in cells if c.id == "telephone-10")
        self.assertNotIn('input("Type GENERATE', generate_code)
        self.assertIn("attempts.generate(context, client, incoming_bytes)", generate_code)
        self.assertNotIn("prompt_box", round_code)
        self.assertIn("display(Image", inspect_code)
        self.assertIn("prompt_box = widgets.Textarea", prompt_code)

    def test_notebook_iteration_and_earlier_selection(self):
        notebook = Path(__file__).resolve().parents[1] / "notebooks" / "02_artistic_telephone.ipynb"
        cells = {cell.id: cell.source for cell in nbformat.read(notebook, as_version=4).cells if cell.cell_type == "code"}
        with tempfile.TemporaryDirectory() as folder, contextlib.redirect_stdout(io.StringIO()):
            ns = {}
            exec(cells["telephone-2"], ns)
            ns["root"] = Path(folder)
            ns["attempts"] = Attempts(folder)
            exec(cells["telephone-6"], ns)
            exec(cells["telephone-upload-widget"], ns)
            exec(cells["telephone-8"], ns)
            exec(cells["telephone-prompt-widget"], ns)
            ns["prompt_box"].value = "First prompt"
            exec(cells["telephone-10"], ns)
            exec(cells["telephone-12"], ns)
            ns["prompt_box"].value = "Second prompt"
            exec(cells["telephone-10"], ns)
            exec(cells["telephone-12"], ns)
            exec(cells["telephone-14"], ns)
            first = next(r for r in history(folder) if r["prompt"] == "First prompt")
            ns["selection"].value = first["run_path"]
            ns["prompt_box"].value = "Unsaved third edit"
            exec(cells["telephone-16"], ns)
            self.assertEqual(decode(ns["handoff"].read_bytes())["prompt"], "First prompt")
            self.assertEqual(len(history(folder)), 2)


if __name__ == "__main__":
    unittest.main()
