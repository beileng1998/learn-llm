"""Diagrams for lesson pages, drawn as SVG with no plotting library."""

from html import escape

from learn_llm.plot import AXIS, DOT, LINE, TEXT

# Mia's one-day recipe: p = w * t, g = p + b, e = g - s, L = e * e.
_BOXES = {"w": (40, 40), "t": (40, 120), "p": (200, 80), "b": (200, 175),
          "g": (360, 125), "s": (360, 215), "e": (520, 170), "L": (660, 170)}
_EDGES = [("w", "p", "×"), ("t", "p", "×"), ("p", "g", "+"), ("b", "g", "+"),
          ("g", "e", "−"), ("s", "e", "−"), ("e", "L", "²")]
_BW, _BH = 76, 44


def one_day(values: dict | None = None, blames: dict | None = None, highlight: str = ""):
    """The recipe for one day's squared error as boxes and arrows.

    `values` fills each box's value (forward); `blames` writes each box's blame under it
    (backward). `highlight` names one box to outline.
    """
    import marimo as mo

    values, blames = values or {}, blames or {}
    parts = ['<svg viewBox="0 0 760 270" width="100%" style="max-width:760px" role="img" '
             'aria-label="w times t gives p; p plus b gives g; g minus s gives e; e squared gives L" '
             'xmlns="http://www.w3.org/2000/svg" font-family="ui-monospace, monospace" text-anchor="middle">',
             f'<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
             f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{AXIS}"/></marker></defs>']
    for a, b, op in _EDGES:
        (xa, ya), (xb, yb) = _BOXES[a], _BOXES[b]
        x1, y1, x2, y2 = xa + _BW / 2, ya, xb - _BW / 2 - 4, yb
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{AXIS}" marker-end="url(#arrow)"/>')
        parts.append(f'<text x="{(x1 + x2) / 2}" y="{(y1 + y2) / 2 - 6}" font-size="15" fill="{TEXT}">{op}</text>')
    for name, (x, y) in _BOXES.items():
        stroke = DOT if name == highlight else AXIS
        width = 3 if name == highlight else 1.2
        parts.append(f'<rect x="{x - _BW / 2}" y="{y - _BH / 2}" width="{_BW}" height="{_BH}" rx="6" '
                     f'fill="none" stroke="{stroke}" stroke-width="{width}"/>')
        value = values.get(name)
        label = f"{name} = {value:g}" if isinstance(value, (int, float)) else name
        parts.append(f'<text x="{x}" y="{y + 5}" font-size="14" fill="{TEXT}">{escape(label)}</text>')
        if name in blames:
            parts.append(f'<text x="{x}" y="{y + _BH / 2 + 17}" font-size="13" fill="{LINE}">'
                         f'{escape(str(blames[name]))}</text>')
    parts.append("</svg>")
    return mo.Html("".join(parts))
