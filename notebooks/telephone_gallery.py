"""Build an offline reveal gallery from embedded or ordinary Telephone PNGs."""
import base64
import io
import re
from html import escape
from pathlib import Path

from PIL import Image

from telephone_helpers import route
from telephone_steg import decode


PLAIN_SESSION = "unrecorded"
PLAIN_MODE = "unrecorded"


def _filename_route(path, root):
    """Infer only the group and sequence encoded by a valid handoff filename."""
    relative = path.relative_to(root)
    groups = [part for part in relative.parts[:-1] if re.fullmatch(r"Group_[A-F]", part)]
    if len(groups) != 1:
        raise ValueError("A plain PNG must be inside one Group_A to Group_F folder.")
    name = path.name
    if not re.fullmatch(r"0[1-5](?:_0[1-5]){0,4}\.png", name):
        raise ValueError("Filename is not a Telephone chain name (example: 05_01.png).")
    sequence = [int(part) for part in name[:-4].split("_")]
    expected = route(groups[0][-1], sequence[-1], len(sequence))
    if expected["outgoing"] != name:
        raise ValueError("Filename does not follow the assigned clockwise seat order.")
    return expected


def scan(folder, fallback_session="", fallback_mode="", prompt_overrides=None):
    """Keep valid PNGs visible; only embedded records can reveal original prompts.

    Session and mode are inferred from embedded records if unambiguous. Optional
    fallback values can place ordinary PNGs into a known session/mode.
    prompt_overrides optionally maps paths such as 'Group_A/01.png' to known prompts.
    """
    folder = Path(folder)
    if not folder.is_dir():
        raise ValueError("Choose the downloaded folder containing Group_A, Group_B, etc.")
    if not isinstance(fallback_session, str) or not isinstance(fallback_mode, str):
        raise ValueError("Fallback session and mode must be text.")
    if fallback_mode and fallback_mode not in ("live", "practice"):
        raise ValueError("Fallback mode must be 'live', 'practice', or blank.")
    if prompt_overrides is None:
        prompt_overrides = {}
    if not isinstance(prompt_overrides, dict) or any(
        not isinstance(key, str) or not isinstance(value, str)
        for key, value in prompt_overrides.items()
    ):
        raise ValueError("Manual prompts must map filenames to prompt text.")
    records, warnings, candidates = {}, [], []
    paths = sorted(path for path in folder.rglob("*") if path.is_file() and path.suffix.lower() == ".png")
    if not paths:
        warnings.append("No PNG files found in this folder.")
    for path in paths:
        relative = path.relative_to(folder)
        try:
            if path.stat().st_size > 20 * 1024 * 1024:
                raise ValueError("Image exceeds 20 MB.")
            data = path.read_bytes()
            # A PNG that cannot be decoded should not be shown, even as a fallback.
            with Image.open(io.BytesIO(data)) as img:
                if img.format != "PNG" or img.width * img.height > 16_000_000:
                    raise ValueError("Use a valid PNG smaller than 16 megapixels.")
                img.load()
            try:
                record = decode(data)
            except ValueError as error:
                # Missing/damaged hidden data does not make the image unusable.
                if str(error).startswith("No Telephone record found."):
                    missing_reason = "No embedded prompt record"
                elif str(error).startswith(("Hidden record damaged", "Invalid hidden record length", "Truncated hidden record", "Use the original RGB PNG")):
                    missing_reason = "Hidden prompt record unreadable"
                    warnings.append(f"{relative}: {missing_reason}; image included without prompt.")
                else:
                    raise  # Validation errors in an embedded record need attention.
                record = _filename_route(path, folder)
                record.update({"prompt": None, "mode": None, "session": None,
                               "record_source": "missing", "missing_reason": missing_reason})
            else:
                if path.name != record["outgoing"]:
                    raise ValueError("Filename does not match its hidden route.")
                groups = [part for part in relative.parts[:-1] if part.startswith("Group_")]
                if groups and any(group != record["folder"] for group in groups):
                    raise ValueError("Group folder does not match its hidden route.")
                record["record_source"] = "embedded"
            candidates.append((relative, data, record))
        except Exception as error:
            warnings.append(f"{relative}: {type(error).__name__}: {error}")

    embedded = [r for _, _, r in candidates if r["record_source"] == "embedded"]
    sessions = {r["session"] for r in embedded}
    modes = {r["mode"] for r in embedded}
    session = fallback_session or (next(iter(sessions)) if len(sessions) == 1 else PLAIN_SESSION)
    mode = fallback_mode or (next(iter(modes)) if len(modes) == 1 else PLAIN_MODE)

    for relative, data, record in candidates:
        if record["record_source"] == "missing":
            record["session"], record["mode"] = session, mode
            prompt = prompt_overrides.get(relative.as_posix())
            if prompt and prompt.strip():
                record["prompt"] = prompt
                record["record_source"] = "manual"
        start = int(record["outgoing"].split("_")[0].split(".")[0])
        key = (record["session"], record["mode"], record["group"], start, record["round"])
        entry = {"record": record, "data": data, "path": str(relative)}
        if key in records:
            warnings.append(f"Duplicate chain position: {relative}. Resolve duplicates and rescan.")
            records[key] = None
        else:
            records[key] = entry
    return records, warnings


def render(records, warnings):
    parts = ['<!doctype html><html lang="en"><meta charset="utf-8">',
             '<meta name="viewport" content="width=device-width,initial-scale=1">',
             '<title>Artistic Telephone reveal</title><style>',
             'body{font:16px system-ui;margin:24px;background:#f5f5f5;color:#17202a}',
             '.chain{display:grid;grid-template-columns:repeat(5,minmax(150px,1fr));gap:12px;overflow:auto}',
             'article{background:white;padding:12px;border:1px solid #ddd;border-radius:8px}',
             'img{width:100%;height:200px;object-fit:contain}pre{white-space:pre-wrap;overflow-wrap:anywhere}',
             '.unrecorded{color:#666;font-size:.9em}',
             '</style><body><h1>Artistic Telephone reveal</h1>',
             '<p>Images are arranged by the chain filenames. Embedded prompts can be revealed;'
             ' ordinary PNGs are displayed without an invented prompt.</p>']
    if warnings:
        parts.append('<h2>Check these files</h2><ul>' + ''.join('<li>' + escape(w) + '</li>' for w in warnings) + '</ul>')
    sections = sorted({key[:3] for key in records})
    if not sections:
        parts.append('<p>No usable Telephone images yet.</p>')
    for session, mode, group in sections:
        parts.append(f'<h2>Session {escape(session)} | {escape(mode)} | Group {escape(group)}</h2>')
        for start in range(1, 6):
            parts.append(f'<h3>Chain {start:02d}</h3><div class="chain">')
            for round_number in range(1, 6):
                key = (session, mode, group, start, round_number)
                entry = records.get(key)
                seat = (start + round_number - 2) % 5 + 1
                filename = route(group, seat, round_number)["outgoing"]
                parts.append(f'<article><strong>{escape(filename)}</strong>')
                if entry is None:
                    parts.append('<p>' + ('Duplicate: resolve files' if key in records else 'Missing image') + '</p>')
                else:
                    record = entry["record"]
                    encoded = base64.b64encode(entry["data"]).decode("ascii")
                    parts.append(f'<img alt="Round {round_number}, seat {seat:02d}" src="data:image/png;base64,{encoded}">')
                    if record["record_source"] == "missing":
                        parts.append('<p class="unrecorded">Prompt unavailable (not embedded in this PNG).'
                                     ' The image is included in its filename position.</p>')
                    else:
                        label = "Reveal prompt and settings" if record["record_source"] == "embedded" else "Reveal separately supplied prompt"
                        parts.append('<details><summary>' + label + '</summary><pre>'
                                     + escape(record["prompt"]) + '</pre>')
                        if record["record_source"] == "embedded":
                            for item in ("model", "model_version", "settings", "observation"):
                                parts.append('<p><b>' + item + ':</b> ' + escape(str(record.get(item, ""))) + '</p>')
                        else:
                            parts.append('<p>Prompt added manually; not recovered from the PNG.</p>')
                        parts.append('</details>')
                parts.append('</article>')
            parts.append('</div>')
    return ''.join(parts) + '</body></html>'
