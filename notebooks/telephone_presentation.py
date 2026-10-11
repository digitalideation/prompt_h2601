"""Instructor-facing, one-image-at-a-time Telephone reveal for JupyterLab.

Keep the live reveal inside the notebook. No server, API or HTML export is needed.
"""
import base64
from html import escape

from telephone_helpers import route


def ordered_chains(records):
    """Stable order: session, mode, group, originating seat (chain start)."""
    chains = sorted({key[:4] for key in records})
    # Ignore groups with only duplicate entries: there is nothing to present.
    return [chain for chain in chains if any(
        key[:4] == chain and entry is not None
        for key, entry in records.items()
    )]


def chain_positions(records, chain):
    """A stable five-round index, including missing and duplicate slots."""
    session, mode, group, start = chain
    result = []
    for round_number in range(1, 6):
        seat = ((start + round_number - 2) % 5) + 1
        filename = route(group, seat, round_number)["outgoing"]
        key = (session, mode, group, start, round_number)
        result.append({
            "round": round_number,
            "filename": filename,
            "entry": records.get(key),
            "status": "duplicate" if key in records and records[key] is None
                      else "missing" if key not in records else "ready",
        })
    return result


def _image(entry):
    src = base64.b64encode(entry["data"]).decode("ascii")
    return (f'<img alt="Selected handoff image" src="data:image/png;base64,{src}" '
            'style="display:block;max-width:100%;max-height:100%;width:auto;'
            'height:auto;object-fit:contain;margin:0 auto;">')


def _prompt(entry):
    if entry is None:
        return "<span style='color:#777'>Image not available.</span>"
    record = entry["record"]
    source = record.get("record_source", "embedded")
    prompt = record.get("prompt")
    if not prompt:
        return "<span style='color:#777'>Prompt unavailable (not embedded in this PNG).</span>"
    note = ("Original embedded prompt" if source == "embedded"
            else "Prompt supplied separately — not recovered from PNG")
    return ('<div style="font-size:12px;color:#666;margin-bottom:7px">'
            + escape(note) + '</div><div style="white-space:pre-wrap;'
            'overflow-wrap:anywhere">' + escape(prompt) + '</div>')


def _title(chain):
    session, mode, group, start = chain
    return f"Group {group} · Chain {start:02d} · {session} / {mode}"


def image_slide(chain, position, position_number, total, image_height=420):
    """Compact, viewport-aware stage; prompt is not part of this HTML.

    image_height is a maximum size in CSS pixels, also capped at 55% of
    the browser viewport height for laptops and JupyterLab.
    """
    if not isinstance(image_height, int) or not 200 <= image_height <= 1000:
        raise ValueError("IMAGE_HEIGHT must be an integer between 200 and 1000.")
    if position["entry"] is None:
        status = "Duplicate chain position" if position["status"] == "duplicate" else "Image missing"
        content = ('<p style="font-size:25px;text-align:center;color:#bcbcbc">'
                   + escape(status) + '</p>')
    else:
        content = _image(position["entry"])
    return (
        '<div style="background:#111;color:white;border-radius:10px;'
        'padding:12px 16px 16px;">'
        '<div style="display:flex;justify-content:space-between;gap:12px;'
        'font:13px system-ui;color:#c4c4c4;margin-bottom:14px">'
        '<span>' + escape(_title(chain)) + '</span>'
        '<span>Image ' + str(position_number) + ' of ' + str(total)
        + ' · Round ' + str(position["round"])
        + ' · ' + escape(position["filename"]) + '</span></div>'
        f'<div style="height:min({image_height}px,55vh);display:flex;align-items:center;'
        'justify-content:center;overflow:hidden">' + content + '</div></div>'
    )


def summary_slide(records, chain):
    """The five handoffs and ALL their available prompts, without truncation."""
    positions = chain_positions(records, chain)
    cards = []
    for position in positions:
        entry = position["entry"]
        if entry is None:
            reason = ("Duplicate; resolve files" if position["status"] == "duplicate"
                      else "Missing image")
            photo = ('<div style="height:165px;background:#eee;display:flex;'
                     'align-items:center;justify-content:center;color:#777">'
                     + reason + '</div>')
        else:
            src = base64.b64encode(entry["data"]).decode("ascii")
            photo = (f'<img src="data:image/png;base64,{src}" '
                     f'alt="Round {position["round"]}" '
                     'style="display:block;width:100%;height:165px;'
                     'object-fit:contain;background:#efefef;">')
        cards.append(
            '<div style="border:1px solid #dedede;border-radius:8px;'
            'background:white;overflow:hidden;min-width:0;">'
            + photo
            + '<div style="padding:12px;font:14px/1.5 system-ui;color:#222">'
            + '<div style="font-weight:700;margin-bottom:10px">Round '
            + str(position["round"]) + ' · ' + escape(position["filename"]) + '</div>'
            + _prompt(entry)
            + '</div></div>'
        )
    return (
        '<div style="font-family:system-ui;color:#1e1e1e;background:#f6f6f4;'
        'padding:22px;border-radius:10px;">'
        '<div style="font-size:24px;font-weight:700;margin-bottom:6px">'
        + escape(_title(chain)) + '</div>'
        '<p style="color:#555;margin:0 0 20px">Complete chain overview · '
        'all five positions, images and available prompts</p>'
        '<div style="display:grid;grid-template-columns:repeat(5,minmax(0,1fr));'
        'gap:12px;align-items:start;overflow-x:auto;min-width:760px">'
        + ''.join(cards) + '</div></div>'
    )


class RevealPlayer:
    """Notebook controls: one image, click to reveal prompt, then advance."""

    def __init__(self, records, image_height=420):
        import ipywidgets as widgets

        if not isinstance(image_height, int) or not 200 <= image_height <= 1000:
            raise ValueError("IMAGE_HEIGHT must be an integer between 200 and 1000.")
        self.image_height = image_height
        self.records = records
        self.chains = ordered_chains(records)
        self.chain_index = 0
        self.slide_index = 0  # 0-4 are image rounds; 5 is chain summary.
        self.prompt_visible = False
        self._updating_select = False

        self.chain_selector = widgets.Dropdown(
            options=[(_title(chain), index) for index, chain in enumerate(self.chains)],
            description="Chain:", layout=widgets.Layout(width="510px"),
            disabled=not bool(self.chains),
        )
        self.previous = widgets.Button(description="← Previous", layout=widgets.Layout(width="120px"))
        self.reveal = widgets.Button(description="Reveal prompt", button_style="info",
                                     layout=widgets.Layout(width="150px"))
        self.next = widgets.Button(description="Next image →", button_style="primary",
                                   layout=widgets.Layout(width="160px"))
        self.status = widgets.HTML()
        self.stage = widgets.HTML()
        self.prompt = widgets.HTML()
        self.previous.on_click(self._previous)
        self.reveal.on_click(self._reveal)
        self.next.on_click(self._next)
        self.chain_selector.observe(self._choose_chain, names="value")

        self.widget = widgets.VBox([
            widgets.HBox([self.chain_selector]),
            widgets.HBox([self.previous, self.reveal, self.next]),
            self.status,
            self.stage,
            self.prompt,
        ], layout=widgets.Layout(width="100%"))
        self._refresh()

    def _positions(self):
        return chain_positions(self.records, self.chains[self.chain_index])

    def _choose_chain(self, change):
        if self._updating_select or change["new"] is None:
            return
        self.chain_index = change["new"]
        self.slide_index = 0
        self.prompt_visible = False
        self._refresh()

    def _previous(self, button):
        if not self.chains:
            return
        if self.slide_index > 0:
            self.slide_index -= 1
        elif self.chain_index > 0:
            self.chain_index -= 1
            self.slide_index = 5  # Previous chain summary.
        self.prompt_visible = False
        self._refresh()

    def _next(self, button):
        if not self.chains:
            return
        if self.slide_index < 5:
            self.slide_index += 1
        elif self.chain_index < len(self.chains) - 1:
            self.chain_index += 1
            self.slide_index = 0
        self.prompt_visible = False
        self._refresh()

    def _reveal(self, button):
        if self.chains and self.slide_index < 5:
            self.prompt_visible = not self.prompt_visible
            self._refresh()

    def _refresh(self):
        if not self.chains:
            self.status.value = "<b>No usable Telephone images. Scan the class folder first.</b>"
            self.stage.value = ""
            self.prompt.value = ""
            for control in (self.previous, self.reveal, self.next):
                control.disabled = True
            return
        chain = self.chains[self.chain_index]
        positions = self._positions()
        pos = positions[min(self.slide_index, 4)]
        self._updating_select = True
        try:
            self.chain_selector.value = self.chain_index
        finally:
            self._updating_select = False
        self.previous.disabled = self.chain_index == 0 and self.slide_index == 0
        self.next.disabled = self.chain_index == len(self.chains) - 1 and self.slide_index == 5
        summary = self.slide_index == 5
        self.reveal.disabled = summary or pos["entry"] is None
        self.reveal.description = "Hide prompt" if self.prompt_visible and not summary else "Reveal prompt"
        self.next.description = ("Next chain →" if summary else
                                 "Chain summary →" if self.slide_index == 4 else "Next image →")
        self.status.value = (
            f'<div style="font:14px system-ui;margin:10px 0;color:#555">'
            f'Chain {self.chain_index+1} / {len(self.chains)}'
            + (' · Summary' if summary else
               f' · Round {pos["round"]} / 5 · Prompt hidden until you reveal it')
            + '</div>'
        )
        self.stage.value = (summary_slide(self.records, chain) if summary
                            else image_slide(chain, pos, self.slide_index+1, 5,
                                             image_height=self.image_height))
        self.prompt.value = (
            '<div style="border:1px solid #dadada;border-radius:8px;padding:18px;'
            'font:18px/1.55 system-ui;white-space:normal;margin-top:10px;">'
            + _prompt(pos["entry"]) + '</div>'
            if self.prompt_visible and not summary else ''
        )


def presentation(records, image_height=420):
    """Show one image at a time, capped to image_height CSS pixels."""
    from IPython.display import display
    player = RevealPlayer(records, image_height=image_height)
    display(player.widget)
    return player
