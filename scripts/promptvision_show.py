#!/usr/bin/env python3
"""Build an offline listening show from numbered PromptVision team folders.

Usage: python scripts/promptvision_show.py /path/to/PromptVision
No packages to install; re-run as teams submit or fix their files.
"""
import json
import math
import struct
import wave
import zlib
from pathlib import Path
import re
import sys
from urllib.parse import quote

AUDIO = ("mp3", "wav", "m4a", "ogg")
IMAGES = ("png", "jpg", "jpeg", "webp")
FIELDS = {"country", "title", "story", "model", "prompt", "lyrics", "translation", "iteration"}
REQUIRED_FIELDS = FIELDS - {"lyrics"}
PAGE = r'''<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>PromptVision | Listening Show</title>
<style>
:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#11151c;color:#f4f4f1;font:16px/1.45 system-ui,sans-serif}
main{max-width:1250px;margin:auto;padding:20px}header,nav{display:flex;align-items:center;gap:12px;flex-wrap:wrap;justify-content:space-between}
h1{margin:0;font-size:clamp(24px,3vw,36px)}.muted,small{color:#abb3c2}header{margin-bottom:18px}button,select{background:#293344;color:inherit;border:1px solid #5a6576;border-radius:6px;padding:10px;font:inherit;cursor:pointer}button:disabled{opacity:.4;cursor:default}
.stage{display:grid;grid-template-columns:minmax(0,3fr) minmax(210px,1fr);gap:18px;margin-top:18px}
.cover{width:100%;height:min(58vh,590px);object-fit:contain;background:#06090f;border-radius:8px}
.side{background:#202936;border-radius:8px;padding:16px;align-self:start}.side img{width:100%;height:180px;object-fit:contain;background:#090c13;border-radius:5px}
#country{font-size:clamp(22px,3vw,36px);margin:8px 0 0}#title{font-size:18px;color:#ccd9ed;margin:0 0 16px}
audio{width:100%;margin:16px 0 8px}#details{padding:14px;background:#202936;border-radius:6px;white-space:pre-wrap;overflow-wrap:anywhere}#story{white-space:pre-line;overflow-wrap:anywhere;font-size:17px;color:#dbe2ee;max-width:760px}#full-track{font-size:13px;color:#c0cce0}
@media(max-width:720px){.stage{grid-template-columns:1fr}.side img{height:140px}.cover{height:42vh}}
</style>
<main><header><div><h1>PromptVision 2026</h1><small>A country you can hear</small></div>
<label>Entry <select id="choose" aria-label="Choose entry"></select></label></header>
<nav><div><button id="prev">Previous</button> <button id="next">Next country</button> <button id="reveal">Reveal prompt</button></div><span class="muted" id="count"></span></nav>
<section class="stage"><div><img class="cover" id="cover" alt="Generated cover image">
<h2 id="country"></h2><p id="title"></p><h3>Our country</h3><p id="story"></p><audio id="audio" controls preload="metadata"></audio>
<label id="full-track"><input type="checkbox" id="full"> Play entire track (otherwise stop at 75 seconds for the live show)</label>
<p><small id="duration-note">Submitted tracks should be between 1 and 2 minutes. Moving to another entry stops playback.</small></p>
<div id="details" hidden></div></div><aside class="side"><strong>Visual inspiration</strong><p class="muted">Source image from the creative brief</p><img id="source" alt="Source inspiration image"></aside></section>
<p class="muted">Arrow keys: previous / next country. Reveal the prompt after listening. ScoreWiz voting is separate.</p>
</main><script type="application/json" id="entries">__DATA__</script>
<script>
const entries=JSON.parse(document.getElementById('entries').textContent),$=id=>document.getElementById(id);
let index=0;const audio=$('audio');
entries.forEach((e,i)=>$('choose').add(new Option(e.country,i)));
function display(){const e=entries[index];audio.pause();audio.removeAttribute('src');audio.load();audio.src=e.audio;
 $('cover').src=e.cover;$('source').src=e.source;$('country').textContent=e.country;
 $('title').textContent=e.title;$('story').textContent=e.story || 'Country story not supplied yet.';$('count').textContent='Entry '+(index+1)+' of '+entries.length;
 $('choose').value=index;$('prev').disabled=index===0;$('next').disabled=index===entries.length-1;
 $('details').hidden=true;$('reveal').textContent='Reveal prompt';
 $('details').textContent='Model: '+e.model+'\n\nFinal prompt:\n'+e.prompt+(e.lyrics?'\n\nLyrics:\n'+e.lyrics:'')+'\n\nVisual-to-audio translation:\n'+e.translation+'\n\nIteration:\n'+e.iteration;}
$('prev').onclick=()=>{if(index>0){index--;display()}};
$('next').onclick=()=>{if(index<entries.length-1){index++;display()}};
$('choose').onchange=()=>{index=Number($('choose').value);display()};
$('reveal').onclick=()=>{$('details').hidden=!$('details').hidden;$('reveal').textContent=$('details').hidden?'Reveal prompt':'Hide prompt'};
audio.addEventListener('timeupdate',()=>{if(!$('full').checked && audio.currentTime>=75)audio.pause()});
audio.addEventListener('loadedmetadata',()=>{const d=audio.duration;$('duration-note').textContent=Number.isFinite(d)&& (d<60||d>120)?'CHECK: Submitted track lasts '+Math.round(d)+' seconds; the allowed duration is 60–120 seconds.':'Submitted tracks should be between 1 and 2 minutes. Moving to another entry stops playback.'});
document.addEventListener('keydown',event=>{if(['INPUT','SELECT','BUTTON','AUDIO'].includes(document.activeElement.tagName))return;
 if(event.key==='ArrowRight')$('next').click();if(event.key==='ArrowLeft')$('prev').click()});
display();
</script></html>'''


def metadata(path):
    """Read 'Field: value' text, including optional indented or multiline prompts."""
    values, current = {}, None
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        key, colon, value = line.partition(":")
        if colon and key.strip().lower() in FIELDS:
            current = key.strip().lower()
            values[current] = value.strip()
        elif current and line.strip():
            values[current] += "\n" + line.strip()
    return values


def media(folder, name, formats):
    choices = [folder / f"{name}.{ext}" for ext in formats]
    available = [p for p in choices if p.is_file() and not p.is_symlink() and p.stat().st_size > 0]
    if len(available) > 1:
        raise ValueError(f"Keep only one {name} file in {folder.name}")
    return available[0] if available else None


def build(folder):
    folder = Path(folder).expanduser().resolve()
    if not folder.is_dir():
        raise ValueError(f"Not a directory: {folder}")
    entries, warnings, numbers = [], [], set()
    for team in sorted(folder.iterdir()):
        if not re.fullmatch(r"\d{2}_.+", team.name) or not team.is_dir() or team.is_symlink():
            continue
        number = team.name[:2]
        if number in numbers:
            raise ValueError(f"Duplicate entry number: {number}")
        numbers.add(number)
        track = media(team, "track", AUDIO)
        source = media(team, "source", IMAGES)
        cover = media(team, "cover", IMAGES)
        info = team / "entry.txt"
        if not track or not source or not info.is_file() or info.is_symlink():
            warnings.append(f"{team.name}: missing track, source image or entry.txt; skipped")
            continue
        if not cover:
            warnings.append(f"{team.name}: missing cover; showing source as a temporary fallback")
            cover = source
        values = metadata(info)
        for field in sorted(REQUIRED_FIELDS - values.keys()):
            warnings.append(f"{team.name}: missing {field} in entry.txt")
        def link(path):
            return quote(f"{team.name}/{path.name}", safe="/")
        entries.append({"country": values.get("country") or team.name[3:].replace("_", " "),
                        "title": values.get("title") or "Untitled", "audio": link(track),
                        "source": link(source), "cover": link(cover),
                        **{k: values.get(k, "") for k in ("story", "model", "prompt", "lyrics", "translation", "iteration")}})
    if len({e["country"].casefold() for e in entries}) != len(entries):
        raise ValueError("Country names must be unique for ScoreWiz")
    if not entries:
        raise ValueError("No complete entries. Expected 01_CountryName/ with track, source and entry.txt.")
    page_path = folder / "promptvision_show.html"
    roster_path = folder / "scorewiz_countries.txt"
    if page_path.exists() and '<script type="application/json" id="entries">' not in page_path.read_text(encoding="utf-8"):
        raise FileExistsError("Refusing to overwrite an unrelated promptvision_show.html")
    content = json.dumps(entries, ensure_ascii=True).replace("<", "\\u003c")
    page_path.write_text(PAGE.replace("__DATA__", content), encoding="utf-8")
    roster_path.write_text("\n".join(e["country"] for e in entries) + "\n", encoding="utf-8")
    print(f"Ready: {len(entries)} countries. Open {page_path}")
    print(f"ScoreWiz country names: {roster_path}")
    for note in warnings:
        print("CHECK:", note)
    return entries, warnings


def demo_image(path, palette):
    """A synthetic colored PNG for testing the layout; no external libraries."""
    width, height = 640, 420
    rows = []
    for y in range(height):
        line = bytearray([0])
        for x in range(width):
            glow = max(0, 100 - ((x - 420) ** 2 + (y - 170) ** 2) // 1100)
            line.extend(min(255, int(a + (b - a) * y / height + glow))
                        for a, b in palette)
        rows.append(bytes(line))

    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff))

    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(b"".join(rows), 6))
           + chunk(b"IEND", b""))
    path.write_bytes(png)


def demo_audio(path, note):
    """A 70-second tone demonstration, NOT real AI music."""
    with wave.open(str(path), "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(8000)
        for offset in range(0, 70 * 8000, 4000):
            samples = []
            for i in range(offset, min(offset + 4000, 70 * 8000)):
                t = i / 8000
                frequency = note * (1 if int(t / 6) % 2 == 0 else 1.25)
                envelope = min(1, t / 1.5) * min(1, (70 - t) / 2)
                sample = int(7500 * envelope * (math.sin(2 * math.pi * frequency * t)
                              + 0.15 * math.sin(2 * math.pi * frequency * 2 * t)))
                samples.append(sample)
            output.writeframes(struct.pack("<" + "h" * len(samples), *samples))


def make_demo():
    """Make two fictional entries beside the repository without touching real entries."""
    root = Path.cwd() / "PromptVision-demo"
    if root.exists():
        raise FileExistsError(f"{root} already exists. Rename or delete it before generating a fresh demo.")
    examples = [
        ("01_RepublicOfEcho", "Republic of Echo", "Signals from Tomorrow",
         "In the Republic of Echo, the sun has not risen for centuries. "
         "Citizens navigate through musical signals transmitted between distant cities. "
         "Once a year, they perform together, hoping their music will bring back the dawn.",
         "Cold electronic pulse, hazy synth layers and a hopeful melody emerging at the end.",
         "[Chorus]\nWe light the dark with our own songs\nUntil the morning comes", 175,
         ((19, 38), (26, 83), (79, 138))),
        ("02_MossArchipelago", "Moss Archipelago", "Songs of the Tides",
         "Across this scattered island country, homes float on giant leaves that rise "
         "with the tides. Every community has its own rhythm, and boats answer one "
         "another with bells. Their festival celebrates the sound of being connected "
         "without sharing a language.",
         "Warm marimba patterns, hand drums and distant bells moving in gentle waves.",
         "", 220, ((12, 33), (69, 135), (38, 91)))
    ]
    for folder, country, title, story, prompt, lyrics, note, palette in examples:
        team = root / folder
        team.mkdir(parents=True, exist_ok=False)
        demo_image(team / "source.png", ((29, 68), (51, 75), (84, 130)))
        demo_image(team / "cover.png", palette)
        demo_audio(team / "track.wav", note)
        (team / "entry.txt").write_text(
            "Country: " + country + "\nTitle: " + title
            + "\nStory: " + story
            + "\nModel: Synthetic demonstration; not MiniMax"
            + "\nPrompt: " + prompt
            + ("\nLyrics: " + lyrics if lyrics else "")
            + "\nTranslation: We translated the original image's color and movement into sound."
            + "\nIteration: We revised the rhythm to better suit the imaginary country.\n",
            encoding="utf-8")
    return root


if __name__ == "__main__":
    if sys.argv[1:] == ["--demo"]:
        folder = make_demo()
    elif len(sys.argv) == 2:
        folder = sys.argv[1]
    else:
        raise SystemExit("Usage: python scripts/promptvision_show.py /path/to/PromptVision | --demo")
    build(folder)
