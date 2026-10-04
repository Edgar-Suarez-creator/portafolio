"""Generate the "System diagram" SVG of each project page from a declarative spec.

Why a generator: the nine diagrams were hand-drawn before the code existed and
drifted from it (floating boxes, arrows to the wrong node, tables that do not
exist). A spec per project (see ``specs.py``) is contrasted against the code and
rendered here with one layout engine, so every box is connected and the visual
language is the same on all pages.

Usage::

    python scripts/diagrams/gen_diagrams.py            # rewrite the nine pages
    python scripts/diagrams/gen_diagrams.py 03         # only project 03
    python scripts/diagrams/gen_diagrams.py --preview  # also write preview HTML

The SVG replaces the ``<svg>`` element inside ``.arch-figure`` of
``projects/NN-*.html``; below it the generator writes a plain-language
explanation and a legend (``.dg-explain`` / ``.dg-legend``). Every label is
bilingual: ``("es", "en")`` tuples become two ``<text>`` elements with the
``l-es`` / ``l-en`` classes that the pages already toggle.
"""

from __future__ import annotations

import html
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECTS = ROOT / "projects"

# Palette: the hex values already used by the pages (light theme).
INK = "#111b21"
DIM = "#54655d"
TEAL = "#00a884"
TEAL_DEEP = "#0f766e"
AMBER = "#b45309"
NEUTRAL_STROKE = "rgba(17,27,33,0.16)"

TONES: dict[str, dict[str, str]] = {
    # fill, stroke, subtitle color, title weight
    "input": {"fill": "rgba(0,168,132,0.08)", "stroke": TEAL, "sub": DIM, "w": "600"},
    "llm": {"fill": "rgba(0,168,132,0.10)", "stroke": TEAL_DEEP, "sub": TEAL_DEEP, "w": "700"},
    "tool": {"fill": "rgba(17,27,33,0.02)", "stroke": NEUTRAL_STROKE, "sub": DIM, "w": "600"},
    "rule": {"fill": "rgba(240,180,41,0.08)", "stroke": AMBER, "sub": AMBER, "w": "700"},
    "store": {"fill": "rgba(17,27,33,0.02)", "stroke": NEUTRAL_STROKE, "sub": DIM, "w": "600"},
    "output": {"fill": "rgba(0,168,132,0.06)", "stroke": TEAL, "sub": TEAL_DEEP, "w": "600"},
}

VIEW_W = 1180
MARGIN_X = 30
MARGIN_TOP = 24
ROW_GAP = 64  # vertical channel between rows (holds the buses)
H_GAP = 44
TITLE_PX = 7.4  # avg glyph width, Manrope 13px semibold
MONO_PX = 6.1  # avg glyph width, IBM Plex Mono 10px
MIN_W = 150
PAD_X = 22


Bi = str | tuple[str, str]


def _bi(x: Bi | None) -> tuple[str, str]:
    if x is None:
        return ("", "")
    return (x, x) if isinstance(x, str) else x


@dataclass
class Node:
    id: str
    title: Bi
    sub: list[Bi] = field(default_factory=list)
    tone: str = "tool"
    align: str | None = None  # id of a node in another row to sit directly under/over
    # layout, filled by the engine
    x: float = 0
    y: float = 0
    w: float = 0
    h: float = 0

    @property
    def cx(self) -> float:
        return self.x + self.w / 2

    @property
    def cy(self) -> float:
        return self.y + self.h / 2


@dataclass
class Edge:
    src: str
    dst: str
    label: Bi | None = None
    kind: str = "flow"  # flow | loop | alt


@dataclass
class Group:
    label: Bi
    nodes: list[str]
    color: str = TEAL_DEEP


@dataclass
class Spec:
    explain: tuple[str, str]  # plain-language explanation (es, en) written under the figure
    rows: list[list[Node]]
    edges: list[Edge]
    groups: list[Group] = field(default_factory=list)

    @property
    def caption(self) -> str:
        return self.explain[0]


# --------------------------------------------------------------------------- layout


def _node_size(n: Node) -> tuple[float, float]:
    w_title = max(len(t) for t in _bi(n.title)) * TITLE_PX
    w_sub = max((len(t) * MONO_PX for s in n.sub for t in _bi(s)), default=0)
    w = max(MIN_W, w_title + 2 * PAD_X, w_sub + 2 * PAD_X)
    h = 34 + 16 * len(n.sub) + (8 if n.sub else 0)
    return w, h


def layout(spec: Spec) -> dict[str, Node]:
    nodes: dict[str, Node] = {}
    row0 = {n.id for n in spec.rows[0]}
    grouped = {nid for g in spec.groups for nid in g.nodes}
    y = MARGIN_TOP
    if any(e.kind == "loop" and e.src in row0 and e.dst in row0 for e in spec.edges):
        y += 36
    for row in spec.rows:
        if any(n.id in grouped for n in row):
            y += 36
            ids = {n.id for n in row}
            if any(e.kind == "loop" and e.src in ids and e.dst in ids and e.dst in grouped for e in spec.edges):
                y += 24  # the loop arc runs above the group label
        for n in row:
            n.w, n.h = _node_size(n)
        row_h = max(n.h for n in row)
        total = sum(n.w for n in row)
        gap = H_GAP
        avail = VIEW_W - 2 * MARGIN_X
        if total + gap * (len(row) - 1) > avail:
            gap = max(18, (avail - total) / max(1, len(row) - 1))
            if total + gap * (len(row) - 1) > avail:
                scale = (avail - gap * (len(row) - 1)) / total
                for n in row:
                    n.w *= scale
        width = sum(n.w for n in row) + gap * (len(row) - 1)
        x = (VIEW_W - width) / 2
        for n in row:
            n.x, n.y = x, y + (row_h - n.h) / 2
            x += n.w + gap
            nodes[n.id] = n
        y += row_h + ROW_GAP
    for row in spec.rows:
        for n in row:
            if n.align and n.align in nodes:
                n.x = nodes[n.align].cx - n.w / 2
    last = {n.id for n in spec.rows[-1]}
    under = any(e.src in last and e.dst in last and e.kind != "loop"
                and abs([i for i, n in enumerate(spec.rows[-1]) if n.id == e.src][0]
                        - [i for i, n in enumerate(spec.rows[-1]) if n.id == e.dst][0]) > 1
                for e in spec.edges)
    spec_h = y - ROW_GAP + MARGIN_TOP + (30 if under else 0)
    setattr(spec, "height", spec_h)
    return nodes


def _group_of(spec: Spec, nid: str) -> Group | None:
    for g in spec.groups:
        if nid in g.nodes:
            return g
    return None


def _row_of(spec: Spec, nid: str) -> int:
    for i, row in enumerate(spec.rows):
        if any(n.id == nid for n in row):
            return i
    raise KeyError(nid)


# Animation: nodes rise in sequence, edges draw themselves, then a packet keeps
# travelling along every edge. Everything keys off `.arch-figure.in`, the class the
# page's IntersectionObserver adds when the figure scrolls into view, and is
# switched off under prefers-reduced-motion.
STYLE = """<style>
.dg .dg-node { opacity: 0; transform: translateY(10px); transform-box: fill-box;
  transition: opacity .55s cubic-bezier(.2,.7,.2,1) var(--d), transform .55s cubic-bezier(.2,.7,.2,1) var(--d); }
.arch-figure.in .dg .dg-node { opacity: 1; transform: none; }
.dg .dg-node rect { transition: stroke-width .2s, filter .2s; }
.dg .dg-node:hover rect { stroke-width: 2; filter: drop-shadow(0 6px 14px rgba(0,168,132,.18)); }
.dg .dg-base { stroke-dasharray: 1; stroke-dashoffset: 1; transition: stroke-dashoffset .8s ease-out var(--d); }
.dg .dg-loop .dg-base, .dg .dg-alt .dg-base { stroke-dasharray: .035 .025; stroke-dashoffset: 0; opacity: 0; transition: opacity .6s var(--d); }
.arch-figure.in .dg .dg-base { stroke-dashoffset: 0; opacity: 1; }
.dg .dg-packet { stroke-dasharray: .09 .91; stroke-dashoffset: 1; opacity: 0; }
.arch-figure.in .dg .dg-packet { opacity: .9; animation: dg-flow 2.6s linear infinite; animation-delay: calc(var(--d) + .8s); }
.dg .dg-loop .dg-packet { animation-duration: 3.4s; }
@keyframes dg-flow { from { stroke-dashoffset: 1; } to { stroke-dashoffset: 0; } }
.dg text { pointer-events: none; }
@media (prefers-reduced-motion: reduce) {
  .dg .dg-node, .dg .dg-base, .dg .dg-loop .dg-base, .dg .dg-alt .dg-base { opacity: 1; transform: none; transition: none; stroke-dashoffset: 0; }
  .dg .dg-packet, .arch-figure.in .dg .dg-packet { animation: none; opacity: 0; }
}
</style>"""

# --------------------------------------------------------------------------- render


def _t(x: float, y: float, text: str, *, size: int, fill: str, family: str, weight: str = "400",
       anchor: str = "middle", extra: str = "") -> str:
    return (
        f'<text x="{x:.0f}" y="{y:.0f}" font-family="{family}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" stroke="none"{extra}>'
        f"{html.escape(text)}</text>"
    )


def _bt(x: float, y: float, text: Bi, **kw) -> str:
    """One <text> per language; the page CSS shows the active one."""
    es, en = _bi(text)
    return _t(x, y, es, extra=' class="l-es"' + kw.pop("extra", ""), **kw) + _t(x, y, en, extra=' class="l-en"', **kw)


def _label(x: float, y_base: float, text: Bi, color: str, anchor: str = "middle") -> list[str]:
    """Stack the lines of a label upwards so the last line sits at y_base (per language)."""
    out: list[str] = []
    for lang, txt in zip(("l-es", "l-en"), _bi(text)):
        lines = txt.split("\n")
        out += [_t(x, y_base - 13 * (len(lines) - 1 - i), ln, size=10, fill=color, family="IBM Plex Mono",
                   anchor=anchor, extra=f' class="{lang}"') for i, ln in enumerate(lines)]
    return out


def _node_svg(n: Node, order: int) -> str:
    tone = TONES[n.tone]
    out = [f'<g transform="translate({n.x:.0f}, {n.y:.0f})">',
           f'<g class="dg-node" style="--d:{order * 90}ms">',
           f'<rect width="{n.w:.0f}" height="{n.h:.0f}" rx="9" fill="{tone["fill"]}" '
           f'stroke="{tone["stroke"]}" stroke-width="1.3"/>']
    ty = 22 if n.sub else n.h / 2 + 5
    out.append(_bt(n.w / 2, ty, n.title, size=13, fill=INK, family="Manrope", weight=tone["w"]))
    for i, s in enumerate(n.sub):
        col = tone["sub"] if i == 0 else DIM
        out.append(_bt(n.w / 2, 40 + 16 * i, s, size=10, fill=col, family="IBM Plex Mono"))
    out.append("</g></g>")
    return "\n".join(out)


def _edge_svg(spec: Spec, nodes: dict[str, Node], e: Edge, marker: str,
              seen: dict[str, int]) -> str:
    a, b = nodes[e.src], nodes[e.dst]
    lift = 13 * seen.get(e.dst, 0)  # stack labels when several edges enter b
    if e.label and e.src != e.dst:
        seen[e.dst] = seen.get(e.dst, 0) + 1
    ra, rb = _row_of(spec, e.src), _row_of(spec, e.dst)
    color = AMBER if e.kind == "loop" else (DIM if e.kind == "alt" else TEAL_DEEP)
    dash = ' stroke-dasharray="5 4"' if e.kind in ("loop", "alt") else ""
    lab: list[str] = []
    if ra == rb:
        row = spec.rows[ra]
        ia, ib = [i for i, n in enumerate(row) if n.id == a.id][0], [i for i, n in enumerate(row) if n.id == b.id][0]
        adjacent = abs(ia - ib) == 1
        if e.kind == "loop":
            # arc above the row from a's top back to b's top; above the group label when grouped
            g = _group_of(spec, b.id)
            ytop = (min(nodes[i].y for i in g.nodes) - 36 - 24) if g else (min(a.y, b.y) - 40)
            d = (f"M {a.cx:.0f} {a.y:.0f} L {a.cx:.0f} {ytop:.0f} L {b.cx:.0f} {ytop:.0f} "
                 f"L {b.cx:.0f} {b.y - 2:.0f}")
            if e.label:
                lab += _label((a.cx + b.cx) / 2, ytop - 5, e.label, color)
        elif adjacent:
            left, right = (a, b) if a.x < b.x else (b, a)
            x1, x2 = left.x + left.w, right.x - 2
            if a is right:  # backwards on the same row: arrow points left
                x1, x2 = right.x, left.x + left.w + 2
            d = f"M {x1:.0f} {a.cy:.0f} L {x2:.0f} {b.cy:.0f}"
            if e.label and max(len(t) for t in _bi(e.label)) * MONO_PX < abs(x2 - x1) + 24:
                lab += _label((x1 + x2) / 2, a.cy - 8, e.label, color)
        else:
            # not adjacent: go under the row so the line never crosses the boxes between
            ybot = max(a.y + a.h, b.y + b.h) + (30 if _group_of(spec, a.id) else 18)
            d = (f"M {a.cx:.0f} {a.y + a.h:.0f} L {a.cx:.0f} {ybot:.0f} L {b.cx:.0f} {ybot:.0f} "
                 f"L {b.cx:.0f} {b.y + b.h + 2:.0f}")
            if e.label:
                lab += _label((a.cx + b.cx) / 2, ybot - 5, e.label, color)
    elif rb == ra + 1:
        # downward: exit bottom of a, one bus per destination row, enter top of b
        chan = _bus_y(spec, b)
        d = (f"M {a.cx:.0f} {a.y + a.h:.0f} L {a.cx:.0f} {chan:.0f} L {b.cx:.0f} {chan:.0f} "
             f"L {b.cx:.0f} {b.y - 2:.0f}")
        if e.label:
            # grouped destination: the label sits between the bus and the box, clear of the band border
            ly = chan + 14 + lift if _group_of(spec, b.id) else chan - 8 - lift
            lab += _label(b.cx + 7, ly, e.label, color, anchor="start")
    elif rb > ra + 1:
        # skips rows: go round the side so the line never crosses a box
        chan1 = a.y + a.h + 14
        chan2 = _bus_y(spec, b) - 12
        side = 14 if b.cx < VIEW_W / 2 else VIEW_W - 14
        d = (f"M {a.cx:.0f} {a.y + a.h:.0f} L {a.cx:.0f} {chan1:.0f} L {side:.0f} {chan1:.0f} "
             f"L {side:.0f} {chan2:.0f} L {b.cx:.0f} {chan2:.0f} L {b.cx:.0f} {b.y - 2:.0f}")
        if e.label:
            lab += _label(b.cx + 8, b.y - 12, e.label, color, anchor="start")
    elif abs(a.cx - b.cx) < 6:
        # upward, same column: straight up into b from below, offset from the downward entry
        x = a.cx - 18
        d = f"M {x:.0f} {a.y:.0f} L {x:.0f} {b.y + b.h + 2:.0f}"
        if e.label:
            lab += _label(x - 8, a.y - 8, e.label, color, anchor="end")
    else:
        # upward (loop back): leave a's top, go round the side, enter b from above
        chan1 = a.y - ROW_GAP / 2 + 10
        chan2 = b.y - ROW_GAP / 2 + 10
        side = 14 if b.cx < VIEW_W / 2 else VIEW_W - 14
        d = (f"M {a.cx:.0f} {a.y:.0f} L {a.cx:.0f} {chan1:.0f} L {side:.0f} {chan1:.0f} "
             f"L {side:.0f} {chan2:.0f} L {b.cx:.0f} {chan2:.0f} L {b.cx:.0f} {b.y - 2:.0f}")
        if e.label:
            lab += _label(b.cx, chan2 - 6, e.label, color)
    order = max(ra, rb)
    path = (f'<g class="dg-edge dg-{e.kind}" style="--d:{order * 90 + 120}ms">'
            f'<path class="dg-base" d="{d}" pathLength="1" stroke="{color}" stroke-width="1.5" '
            f'fill="none"{dash} marker-end="url(#{marker})"/>'
            f'<path class="dg-packet" d="{d}" pathLength="1" stroke="{color}" stroke-width="2.5" '
            f'fill="none" stroke-linecap="round"/></g>')
    return "\n".join([path, *lab])


def _bus_y(spec: Spec, b: Node) -> float:
    """Y of the horizontal bus feeding node b: inside the group band when b is grouped."""
    grouped = any(b.id in g.nodes for g in spec.groups)
    return b.y - (22 if grouped else ROW_GAP / 2)


def _group_svg(spec: Spec, nodes: dict[str, Node], g: Group) -> str:
    ns = [nodes[i] for i in g.nodes]
    x0 = min(n.x for n in ns) - 14
    loops_in = [nodes[e.dst].cx for e in spec.edges if e.kind == "loop" and e.dst in g.nodes and e.src in g.nodes]
    lx = max(x0 + 2, max(loops_in) + 12) if loops_in else x0 + 2
    y0 = min(n.y for n in ns) - 36
    x1 = max(n.x + n.w for n in ns) + 14
    y1 = max(n.y + n.h for n in ns) + 14
    return "\n".join([
        f'<rect x="{x0:.0f}" y="{y0:.0f}" width="{x1 - x0:.0f}" height="{y1 - y0:.0f}" rx="14" '
        f'fill="rgba(0,168,132,0.035)" stroke="{g.color}" stroke-width="1" stroke-dasharray="6 4"/>',
        _bt(lx, y0 - 8, g.label, size=10, fill=g.color, family="IBM Plex Mono",
            anchor="start", extra=' letter-spacing="0.08em"'),
    ])


def render(spec: Spec) -> str:
    nodes = layout(spec)
    height = getattr(spec, "height")
    markers = "\n".join(
        f'<marker id="arr-{name}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
        f'markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" '
        f'fill="{col}"/></marker>'
        for name, col in (("flow", TEAL_DEEP), ("loop", AMBER), ("alt", DIM))
    )
    parts = [f'<svg class="dg" viewBox="0 0 {VIEW_W} {height:.0f}" xmlns="http://www.w3.org/2000/svg" '
             f'role="img" aria-label="{html.escape(spec.caption)}">', f"<defs>{markers}</defs>",
             STYLE]
    parts += [_group_svg(spec, nodes, g) for g in spec.groups]
    seen: dict[str, int] = {}
    parts += [_edge_svg(spec, nodes, e, f"arr-{e.kind}", seen) for e in spec.edges]
    order = 0
    for row in spec.rows:
        for n in row:
            parts.append(_node_svg(n, order))
            order += 1
    parts.append("</svg>")
    return "\n".join(parts)


# --------------------------------------------------------------------------- explanation + legend

LEGEND_TONES = [
    ("input", ("Entrada o salida", "Input or output")),
    ("llm", ("Paso con modelo de lenguaje", "Language-model step")),
    ("rule", ("Regla escrita en código", "Rule written in code")),
    ("tool", ("Proceso o herramienta", "Process or tool")),
    ("store", ("Almacenamiento", "Storage")),
]
LEGEND_EDGES = [
    ("flow", ("flujo principal", "main flow")),
    ("loop", ("bucle", "loop")),
    ("alt", ("ruta alternativa", "alternative path")),
]


def figure_extra(spec: Spec) -> str:
    """The HTML written under the SVG: what the diagram shows, and what the colours mean."""
    tones = {n.tone for row in spec.rows for n in row}
    if "output" in tones:
        tones.add("input")
    kinds = {e.kind for e in spec.edges}
    es, en = spec.explain
    items = [f'<span class="dg-lg dg-lg-{t}"><i></i><em class="l-es">{html.escape(a)}</em><em class="l-en">{html.escape(b)}</em></span>'
             for t, (a, b) in LEGEND_TONES if t in tones]
    items += [f'<span class="dg-lg dg-le-{k}"><i></i><em class="l-es">{html.escape(a)}</em><em class="l-en">{html.escape(b)}</em></span>'
              for k, (a, b) in LEGEND_EDGES if k in kinds]
    return ('<div class="dg-explain"><p class="l-es">' + html.escape(es) + '</p><p class="l-en">' + html.escape(en)
            + '</p></div>\n      <div class="dg-legend">' + "".join(items) + "</div>")


# --------------------------------------------------------------------------- inject

# The figure may carry an <h5> caption and a previously generated explanation + legend; both are replaced.
SVG_RE = re.compile(
    r"<div class=\"arch-figure[^\"]*\">\s*(?:<h5>.*?</h5>\s*)?<svg.*?</svg>"
    r"(?:\s*<div class=\"dg-explain\">.*?</div>\s*<div class=\"dg-legend\">.*?</div>)?",
    re.S,
)


def inject(page: Path, spec: Spec) -> None:
    src = page.read_text(encoding="utf-8")
    svg = render(spec)
    m = SVG_RE.search(src)
    if not m:
        raise SystemExit(f"{page.name}: no .arch-figure svg found")
    new = src[: m.start()] + '<div class="arch-figure reveal">\n      ' + svg + "\n      " + figure_extra(spec) + src[m.end():]
    page.write_text(new, encoding="utf-8")


def page_for(num: str) -> Path:
    matches = sorted(PROJECTS.glob(f"{num}-*.html"))
    if len(matches) != 1:
        raise SystemExit(f"project {num}: expected one page, found {matches}")
    return matches[0]


def main(argv: list[str]) -> None:
    from specs import SPECS  # noqa: PLC0415  (sibling module)

    preview = "--preview" in argv
    nums = [a for a in argv if re.fullmatch(r"\d\d", a)] or sorted(SPECS)
    for num in nums:
        spec = SPECS[num]
        inject(page_for(num), spec)
        if preview:
            out = ROOT / "scripts" / "diagrams" / f"preview-{num}.html"
            out.write_text(
                '<!doctype html><html lang="es"><meta charset="utf-8"><link rel="stylesheet" href="../../projects/_styles.css">'
                '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700'
                '&family=IBM+Plex+Mono&display=swap">'
                f'<body style="padding:24px;background:var(--bg)"><div class="arch-figure in" style="max-width:1240px">'
                f"{render(spec)}{figure_extra(spec)}</div>",
                encoding="utf-8",
            )
        print(f"{num}: ok")


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    main(sys.argv[1:])
