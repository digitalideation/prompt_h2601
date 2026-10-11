"""Keep generation, local saving and final selection separate."""
from copy import deepcopy
import json
from pathlib import Path
from urllib.request import urlopen

from telephone_helpers import clean_png, practice_image, route, save_record


def download(url):
    with urlopen(url, timeout=120) as response:
        data = response.read(20 * 1024 * 1024 + 1)
    return clean_png(data)


class Attempts:
    def __init__(self, root):
        self.root = Path(root)
        self.pending = None
        self.prediction = None
        self.saved_run = None

    def generate(self, context, client=None, incoming_bytes=None):
        if self.pending is not None:
            raise ValueError("Save the pending attempt first. Do not generate again.")
        expected = route(context["group"], context["seat"], context["round"])
        if not context.get("prompt", "").strip():
            raise ValueError("Write a prompt first.")
        if expected["incoming"]:
            if context.get("source_filename") != expected["incoming"] or incoming_bytes is None:
                raise ValueError("Load your assigned incoming image first.")
            clean_png(incoming_bytes)  # Validate locally; never sent to the model.
        if context["mode"] not in ("practice", "live"):
            raise ValueError("Choose practice or live mode.")
        snapshot = deepcopy({**context, **expected})
        if snapshot["mode"] == "practice":
            self.pending = snapshot
            self.prediction = None
        else:
            model = client.models.get(snapshot["model"])
            if model.latest_version is None:
                raise ValueError("Model has no available version. Ask the instructor.")
            snapshot["model_version"] = model.latest_version.id
            inputs = {**snapshot["settings"], "prompt": snapshot["prompt"]}
            prediction = client.predictions.create(version=snapshot["model_version"], input=inputs)
            # Retain the returned prediction before waiting. Saving can resume polling
            # without creating another paid prediction after a wait/download failure.
            self.prediction = prediction
            snapshot["prediction_id"] = prediction.id
            self.pending = snapshot
            print("Prediction ID:", prediction.id)
            self.root.mkdir(parents=True, exist_ok=True)
            (self.root / "pending.json").write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
        self.saved_run = None

    def save(self, downloader=download):
        if self.pending is None:
            if self.saved_run is not None:
                return self.saved_run
            raise ValueError("No pending attempt. Generate first.")
        if self.pending["mode"] == "practice":
            data = practice_image(self.pending["round"])
        else:
            self.prediction.wait()
            if self.prediction.status != "succeeded":
                raise ValueError("Prediction " + self.prediction.id + " has status " + self.prediction.status
                                 + ". Check Replicate before starting another attempt.")
            urls = self.prediction.output
            if not isinstance(urls, list) or not urls or not isinstance(urls[0], str) or not urls[0].startswith("https://"):
                raise ValueError("No usable image URL. Check the selected model's output format.")
            data = downloader(urls[0])
        self.saved_run = save_record(self.root, self.pending, data)
        self.pending = None
        (self.root / "pending.json").unlink(missing_ok=True)
        return self.saved_run

    def resume(self, client):
        """Recover a recorded live prediction after restarting the kernel."""
        record = json.loads((self.root / "pending.json").read_text(encoding="utf-8"))
        prediction = client.predictions.get(record["prediction_id"])
        self.pending, self.prediction = record, prediction

    def discard_failed(self):
        """Only a confirmed failed/canceled prediction may be cleared for a new try."""
        if self.prediction is None:
            raise ValueError("No live prediction to check.")
        self.prediction.reload()
        if self.prediction.status not in ("failed", "canceled"):
            raise ValueError("Prediction is not confirmed failed or canceled. Retry saving.")
        self.pending = None
        self.prediction = None
        (self.root / "pending.json").unlink(missing_ok=True)
