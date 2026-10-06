"""Small local helpers for W5. Generation remains visible in the notebook."""

import io
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
from zipfile import ZipFile, ZIP_DEFLATED

from PIL import Image, ImageDraw, ImageOps

# Initial example from the existing class guide. Instructor can replace this list.
# Each model has its own input dictionary. Never assume schemas are interchangeable.
MODELS = {
    "FLUX.1 schnell (initial class example)": {
        "identifier": "black-forest-labs/flux-schnell",
        "input": {"num_outputs": 1, "aspect_ratio": "1:1", "output_format": "png"},
    }
}


def route(group, seat, round_number):
    """Five simultaneous chains, clockwise, entirely within a group."""
    if group not in "ABCDEF" or len(group) != 1:
        raise ValueError("Choose group A to F.")
    if type(seat) is not int or not 1 <= seat <= 5:
        raise ValueError("Choose seat 1 to 5.")
    if type(round_number) is not int or not 1 <= round_number <= 5:
        raise ValueError("Choose round 1 to 5.")
    lineage = [((seat - round_number + i) % 5) + 1 for i in range(round_number)]
    names = [f"{number:02d}" for number in lineage]
    return {
        "group": group, "seat": seat, "round": round_number,
        "folder": f"Group_{group}",
        "incoming": "_".join(names[:-1]) + ".png" if round_number > 1 else None,
        "outgoing": "_".join(names) + ".png",
        "send_to": seat % 5 + 1,
    }


def clean_png(data):
    """Rebuild pixels as a PNG so metadata never accompanies a game handoff."""
    if not isinstance(data, bytes) or not data or len(data) > 20 * 1024 * 1024:
        raise ValueError("Choose an image smaller than 20 MB.")
    with Image.open(io.BytesIO(data)) as source:
        if source.width * source.height > 16_000_000:
            raise ValueError("Choose an image no larger than 16 megapixels.")
        oriented = ImageOps.exif_transpose(source).convert("RGB")
        result = Image.new("RGB", oriented.size)
        result.paste(oriented)
        buffer = io.BytesIO()
        result.save(buffer, format="PNG")
        return buffer.getvalue()


def practice_image(round_number=1):
    """A labelled test diagram, not an AI-generated scene or model result."""
    canvas = Image.new("RGB", (640, 400), "#edf2f4")
    draw = ImageDraw.Draw(canvas)
    draw.text((24, 20), "OFFLINE PRACTICE / NOT AI GENERATED", fill="#14213d")
    draw.text((24, 44), f"Round {round_number}: test saving, passing and recording", fill="#14213d")
    draw.rectangle((60, 140, 220, 300), fill="#e76f51")
    draw.ellipse((280, 140, 440, 300), fill="#2a9d8f")
    draw.text((60, 330), "One red square beside one green circle", fill="#14213d")
    buffer = io.BytesIO()
    canvas.save(buffer, format="PNG")
    return buffer.getvalue()


def uploaded_image(value, expected_name):
    """Accept ipywidgets 8 tuple/list values; no filename/path is trusted."""
    if len(value) != 1:
        raise ValueError("Upload exactly the assigned image, then rerun this cell.")
    item = value[0]
    if item["name"] != expected_name:
        raise ValueError(f"Expected {expected_name}. Check the round and group folder.")
    return clean_png(bytes(item["content"]))


def error_message(error):
    """Do not print raw request bodies, headers, tokens, or provider traces."""
    status = getattr(error, "status", getattr(error, "status_code", None))
    if status in (401, 403):
        return "Check your API token and account access, then rerun the token cell."
    if status == 402:
        return "Check your Replicate account credit."
    if status in (404, 422):
        return "Ask the instructor to check the model identifier and supported inputs."
    if status == 429:
        return "Rate limit reached. Wait and check your account before trying again."
    return ("Generation did not finish here. Check Replicate for an existing prediction "
            "before retrying; it may still be running or already charged. "
            "Use offline practice if needed. No automatic retry was made.")


def save_record(root, context, image_bytes):
    """Save a private immutable run with a clean image and prompt snapshot."""
    if not context.get("prompt", "").strip():
        raise ValueError("Write a prompt before saving.")
    png = clean_png(image_bytes)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    run = Path(root) / "private" / f"{stamp}_{uuid4().hex[:8]}"
    run.mkdir(parents=True, exist_ok=False)
    (run / "image.png").write_bytes(png)
    # Explicit allowlist: never serialize clients, tokens, widget state or globals.
    keys = ("group", "seat", "round", "folder", "incoming", "outgoing", "send_to",
            "prompt", "model", "settings", "mode", "observation", "source_filename")
    record = {key: context.get(key) for key in keys}
    record["recorded_at_utc"] = datetime.now(timezone.utc).isoformat()
    record["model_version"] = "Unpinned model identifier; resolved version not captured"
    (run / "record.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    return run


def history(root):
    records = []
    for path in sorted((Path(root) / "private").glob("*/record.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        record["run_path"] = str(path.parent)
        records.append(record)
    return records


def export_handoff(root, run):
    """Copy only clean pixels to a group/round filename, not the private log."""
    root, run = Path(root), Path(run)
    if not run.resolve().is_relative_to((root / "private").resolve()):
        raise ValueError("Choose a saved run from this student's private history.")
    record = json.loads((run / "record.json").read_text(encoding="utf-8"))
    expected = route(record["group"], record["seat"], record["round"])
    if record["outgoing"] != expected["outgoing"]:
        raise ValueError("Saved routing information is inconsistent.")
    if record["mode"] not in ("live", "practice"):
        raise ValueError("Unknown generation mode.")
    # Practice exports are kept separate to prevent confusion with live play.
    folder = root / ("handoff" if record["mode"] == "live" else "practice_handoff") / expected["folder"]
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / expected["outgoing"]
    data = clean_png((run / "image.png").read_bytes())
    if target.exists():
        if target.read_bytes() == data:
            return target
        raise FileExistsError("An image is already selected for this round. Ask the instructor before replacing it.")
    with target.open("xb") as stream:
        stream.write(data)
    return target


def export_after_reveal(root):
    """An explicit final submission archive; never includes notebooks or tokens."""
    root = Path(root)
    archive = root / f"after_reveal_{uuid4().hex[:8]}.zip"
    with ZipFile(archive, "w", ZIP_DEFLATED) as bundle:
        for record in history(root):
            run = Path(record["run_path"])
            for name in ("image.png", "record.json"):
                bundle.write(run / name, (run / name).relative_to(root))
        reflection = root / "reflection.json"
        if reflection.exists():
            bundle.write(reflection, "reflection.json")
    return archive


def session_root(session_name, group, seat):
    route(group, seat, 1)
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,40}", session_name):
        raise ValueError("Use 1 to 40 letters, numbers, underscores or hyphens for the session name.")
    return Path("outputs") / "telephone" / session_name / f"Group_{group}_S{seat:02d}"
