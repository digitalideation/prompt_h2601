"""Decode original handoffs and build an offline, self-contained reveal gallery."""
import base64
from html import escape
from pathlib import Path

from telephone_helpers import route
from telephone_steg import decode


def scan(folder):
    folder = Path(folder)
    if not folder.is_dir():
        raise ValueError("Choose the downloaded folder containing Group_A, Group_B, etc.")
    records, warnings = {}, []
    paths = sorted(path for path in folder.rglob("*") if path.suffix.lower() == ".png")
    if not paths:
        warnings.append("No PNG files found in this folder.")
    for path in paths:
        try:
            if path.stat().st_size > 20 * 1024 * 1024:
                raise ValueError("Image exceeds 20 MB.")
            data = path.read_bytes()
            record = decode(data)
            if path.name != record["outgoing"]:
                raise ValueError("Filename does not match its hidden route.")
            groups = [part for part in path.relative_to(folder).parts[:-1] if part.startswith("Group_")]
            if groups and any(group != record["folder"] for group in groups):
                raise ValueError("Group folder does not match its hidden route.")
            start = int(record["outgoing"].split("_")[0].split(".")[0])
            key = (record["session"], record["mode"], record["group"], start, record["round"])
            entry = {"record": record, "data": data, "path": str(path.relative_to(folder))}
            if key in records:
                warnings.append(f"Duplicate chain position: {path.relative_to(folder)}. Resolve duplicates and rescan.")
                records[key] = None  # Do not choose one silently, even if copies match.
            else:
                records[key] = entry
        except Exception as error:
            warnings.append(f"{path.relative_to(folder)}: {type(error).__name__}: {error}")
    return records, warnings


def render(records, warnings):
    parts = ['<!doctype html><html lang="en"><meta charset="utf-8">',
             '<meta name="viewport" content="width=device-width,initial-scale=1">',
             '<title>Artistic Telephone reveal</title><style>',
             'body{font:16px system-ui;margin:24px;background:#f5f5f5;color:#17202a}',
             '.chain{display:grid;grid-template-columns:repeat(5,minmax(150px,1fr));gap:12px;overflow:auto}',
             'article{background:white;padding:12px;border:1px solid #ddd;border-radius:8px}',
             'img{width:100%;height:200px;object-fit:contain}pre{white-space:pre-wrap;overflow-wrap:anywhere}',
             '</style><body><h1>Artistic Telephone reveal</h1>',
             '<p>Only selected handoffs appear here. Prompts open below each image. Practice diagrams are labelled separately.</p>']
    if warnings:
        parts.append('<h2>Check these files</h2><ul>' + ''.join('<li>' + escape(w) + '</li>' for w in warnings) + '</ul>')
    sections = sorted({key[:3] for key in records})
    if not sections:
        parts.append('<p>No decodable Telephone images yet.</p>')
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
                    parts.append('<details><summary>Reveal prompt and settings</summary><pre>' + escape(record["prompt"]) + '</pre>')
                    for label in ("model", "model_version", "settings", "observation"):
                        parts.append('<p><b>' + label + ':</b> ' + escape(str(record.get(label, ""))) + '</p>')
                    parts.append('</details>')
                parts.append('</article>')
            parts.append('</div>')
    return ''.join(parts) + '</body></html>'
