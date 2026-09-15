"""
Inline SVG figures for carousel slides that would otherwise be text alone: bars, ranges, timelines,
route strips, the brick wall, sorted chips, chains, forks, a filing page, coins, a hub. Each one is
drawn from the numbers on the slide, in the slide's own palette (currentColor, --cyan, --mag), so it
renders on light and dark slides and survives the PDF render.

  from figs import FIG_CSS, hbars, ranges, timeline, route, bricks, chips, chain, fork, doc, coins, hub,
                   threshold, span, numberline, proportion, stamps

Every function returns a <div class="fig ..."> holding one <svg viewBox="0 0 904 H">. 904 is the slide's
content width (1080 less 2 x 88 padding).
"""
import html as H

W = 904

FIG_CSS = """
/* figs.py */
.fig{margin:6px 0 22px;flex:0 0 auto}
.fig svg{display:block;width:100%;height:auto;overflow:visible}
.fig .mono{font-family:var(--mono);font-size:18px;letter-spacing:.05em}
.fig .mono.sm{font-size:15px;letter-spacing:.1em;text-transform:uppercase}
.fig .disp{font-family:var(--disp);font-weight:800;letter-spacing:.005em}
.fig .body{font-family:var(--body);font-size:18px}
.fig .ink{fill:currentColor}.fig .mute{fill:var(--ink3)}.slide.dk .fig .mute{fill:var(--dink3)}
.fig .cy{fill:var(--cyan)}.slide.dk .fig .cy{fill:var(--dcyan)}
.fig .mg{fill:var(--mag)}.slide.dk .fig .mg{fill:var(--dmag)}
.fig .rule{stroke:var(--rule2);fill:none}.slide.dk .fig .rule{stroke:var(--drule)}
.fig .rule2{stroke:var(--rule2);stroke-width:2;fill:none}.slide.dk .fig .rule2{stroke:#3A4046}
.fig .inkline{stroke:currentColor;fill:none;stroke-width:2}
.fig .cyline{stroke:var(--cyan);fill:none;stroke-width:2.5}.slide.dk .fig .cyline{stroke:var(--dcyan)}
.fig .mgline{stroke:var(--mag);fill:none;stroke-width:2.5}.slide.dk .fig .mgline{stroke:var(--dmag)}
.fig .paper{fill:var(--paper2)}.slide.dk .fig .paper{fill:#15181C}
.fig .hatch{fill:url(#gt-hatch)}
.fig .cap{font-family:var(--mono);font-size:14px;letter-spacing:.14em;text-transform:uppercase;fill:var(--ink3)}
.slide.dk .fig .cap{fill:var(--dink3)}
.fig .c{position:static;background:none;font-family:var(--mono);font-size:14px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink3);padding:10px 0 0;border:0}
.slide.dk .fig .c{color:var(--dink3)}
/* /figs.py */"""

HATCH = ('<defs><pattern id="gt-hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
         '<line x1="0" y1="0" x2="0" y2="8" stroke="currentColor" stroke-width="1.5" opacity=".55"/></pattern></defs>')


def e(s):
    return H.escape(str(s), quote=True)


def t(x, y, s, cls="mono ink", anchor="start", size=None, extra=""):
    st = f' style="font-size:{size}px"' if size else ""
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}"{st}{extra}>{e(s)}</text>'


def svg(h, body, cls="", cap=None):
    c = f'<div class="c cap-line">{e(cap)}</div>' if cap else ""
    return (f'<div class="fig {cls}"><svg viewBox="0 0 {W} {h}" width="{W}" height="{h}" xmlns="http://www.w3.org/2000/svg" role="img">'
            f'{HATCH}{body}</svg>{c}</div>')


def _wrap(s, n):
    out, line = [], ""
    for w in str(s).split():
        if len(line) + len(w) + 1 > n and line:
            out.append(line); line = w
        else:
            line = (line + " " + w).strip()
    if line:
        out.append(line)
    return out


# ---------------------------------------------------------------- bars and ranges

def hbars(rows, cap=None, unit="", row_h=90, label_w=0, hi=None):
    """rows: (label, value, shown, cls[, sub]). value: number, (lo, hi) range, or a list of segments.
    Bars share one scale from the largest magnitude; a zero axis appears when anything is negative."""
    vals = []
    for r in rows:
        v = r[1]
        if isinstance(v, tuple):
            vals += list(v)
        elif isinstance(v, list):
            vals.append(sum(v))
        else:
            vals.append(v)
    lo, hi_v = min(0, min(vals)), max(0, max(vals))
    if hi is not None:
        hi_v = max(hi_v, hi)
    span = (hi_v - lo) or 1
    x0, x1 = 0, W - 150  # room for the shown value at the right
    def X(v):
        return x0 + (v - lo) / span * (x1 - x0)
    y = 8
    body = []
    if lo < 0:
        body.append(f'<line x1="{X(0):.1f}" y1="0" x2="{X(0):.1f}" y2="{len(rows) * row_h}" class="rule2"/>')
    for r in rows:
        label, v, shown, cls = r[0], r[1], r[2], r[3]
        sub = r[4] if len(r) > 4 else ""
        body.append(t(0, y + 16, label, "mono sm mute"))
        by = y + 28
        bh = row_h - 50
        if isinstance(v, list):  # segments
            cx = X(0)
            for i, sv in enumerate(v):
                w = (sv / span) * (x1 - x0)
                body.append(f'<rect x="{cx:.1f}" y="{by}" width="{max(w - 3, 1):.1f}" height="{bh}" class="{cls}"/>')
                cx += w
            end = cx
        elif isinstance(v, tuple):
            a, b = X(v[0]), X(v[1])
            body.append(f'<rect x="{min(a, b):.1f}" y="{by}" width="{max(abs(b - a), 3):.1f}" height="{bh}" class="{cls}"/>')
            end = max(a, b)
        else:
            a, b = X(0), X(v)
            body.append(f'<rect x="{min(a, b):.1f}" y="{by}" width="{max(abs(b - a), 3):.1f}" height="{bh}" class="{cls}"/>')
            end = max(a, b) if v >= 0 else X(0)
        body.append(t(end + 16, by + bh - 6, shown, "disp ink", size=38))
        if sub:
            body.append(t(0, by + bh + 20, sub, "cap"))
        y += row_h
    return svg(y, "".join(body), "bars", cap)


def numberline(lo, hi, marks, cap=None, offscale=None):
    """A number line with ranges and points. marks: (kind, a, b, label, cls) kind in range|point."""
    x0, x1, y = 20, W - 40, 70
    span = hi - lo
    X = lambda v: x0 + (v - lo) / span * (x1 - x0)
    body = [f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" class="rule2"/>']
    step = 50 if span <= 400 else 100
    v = lo
    while v <= hi:
        body.append(f'<line x1="{X(v):.1f}" y1="{y - 6}" x2="{X(v):.1f}" y2="{y + 6}" class="rule2"/>')
        body.append(t(X(v), y + 28, ("$" + str(v) + "M") if v >= 0 else f"$({-v})M", "mono sm mute", "middle"))
        v += step
    body.append(f'<line x1="{X(0):.1f}" y1="{y - 22}" x2="{X(0):.1f}" y2="{y + 10}" class="inkline"/>')
    for i, (kind, a, b, label, cls) in enumerate(marks):
        yy = y - 44 - i * 52
        if kind == "range":
            body.append(f'<rect x="{X(a):.1f}" y="{yy - 10}" width="{X(b) - X(a):.1f}" height="20" class="{cls}"/>')
            body.append(t((X(a) + X(b)) / 2, yy - 20, label, "mono sm ink", "middle"))
        else:
            body.append(f'<circle cx="{X(a):.1f}" cy="{yy}" r="9" class="{cls}"/>')
            body.append(t(X(a) + 16, yy + 5, label, "mono sm ink"))
    if offscale:
        body.append(f'<path d="M{x1 - 74} {y + 46} h58 l14 12 l-14 12 h-58 z" class="mg"/>')
        body.append(t(x1 - 84, y + 63, offscale, "mono sm ink", "end"))
    h = y + 80
    top = min([y - 44 - i * 52 - 34 for i in range(len(marks))] + [y - 84])
    return svg(h - top, f'<g transform="translate(0 {-top})">' + "".join(body) + "</g>", "nline", cap)


def proportion(rows, cap=None):
    """Thin full-width bars with a sliver: (label, pct, shown, cls). pct > 100 draws an arrow off the end."""
    body, y = [], 6
    for label, pct, shown, cls in rows:
        body.append(t(0, y + 14, label, "mono sm mute"))
        by = y + 24
        body.append(f'<rect x="0" y="{by}" width="{W - 170}" height="32" class="paper"/>')
        body.append(f'<rect x="0" y="{by}" width="{W - 170}" height="32" class="rule" style="stroke-width:1"/>')
        if pct > 100:
            body.append(f'<rect x="0" y="{by}" width="{W - 170}" height="32" class="{cls}"/>')
            body.append(f'<path d="M{W - 170} {by - 6} l28 22 l-28 22 z" class="{cls}"/>')
        else:
            body.append(f'<rect x="0" y="{by}" width="{max((W - 170) * pct / 100, 5):.1f}" height="32" class="{cls}"/>')
        body.append(t(W - 126, by + 29, shown, "disp ink", size=38))
        y += 90
    return svg(y, "".join(body), "prop", cap)


# ---------------------------------------------------------------- time

def timeline(events, cap=None, h=None, start=None, end=None):
    """events: (pos 0..1 or None, date, label, cls). Labels alternate above and below the line."""
    n = len(events)
    y = 160
    x0, x1 = 40, W - 40
    body = [f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" class="rule2"/>']

    for i, (pos, date, label, cls) in enumerate(events):
        x = x0 + (pos if pos is not None else i / max(n - 1, 1)) * (x1 - x0)
        up = i % 2 == 0
        body.append(f'<circle cx="{x:.1f}" cy="{y}" r="9" class="{cls}"/>')
        ly = y - 34 if up else y + 44
        body.append(f'<line x1="{x:.1f}" y1="{y - 9 if up else y + 9}" x2="{x:.1f}" y2="{y - 24 if up else y + 24}" class="inkline" style="stroke-width:1.5"/>')
        lines = _wrap(label, 18)
        if up:
            ly = y - 34 - (len(lines) - 1) * 21 - 26
            body.append(t(x, ly, date, "mono sm " + ("cy" if "cy" in cls else "mg" if "mg" in cls else "ink"), "middle"))
            for k, ln in enumerate(lines):
                body.append(t(x, ly + 23 + k * 21, ln, "body ink", "middle", size=17))
        else:
            body.append(t(x, ly, date, "mono sm " + ("cy" if "cy" in cls else "mg" if "mg" in cls else "ink"), "middle"))
            for k, ln in enumerate(lines):
                body.append(t(x, ly + 23 + k * 21, ln, "body ink", "middle", size=17))
    return svg(h or 330, "".join(body), "tl", cap)


def span(total_label, segments, marks, cap=None, note=None):
    """One bar for a period, with shaded segments and labelled marks. segments: (a, b, cls, label); marks: (pos, label, cls)."""
    x0, x1, y, bh = 0, W - 20, 70, 34
    body = [t(0, -30, total_label, "mono sm mute"),
            f'<rect x="{x0}" y="{y}" width="{x1 - x0}" height="{bh}" class="paper"/>',
            f'<rect x="{x0}" y="{y}" width="{x1 - x0}" height="{bh}" class="rule" style="stroke-width:1"/>']
    for a, b, cls, label in segments:
        body.append(f'<rect x="{x0 + a * (x1 - x0):.1f}" y="{y}" width="{(b - a) * (x1 - x0):.1f}" height="{bh}" class="{cls}"/>')
        if label:
            body.append(t(x0 + (a + b) / 2 * (x1 - x0), y + bh + 24, label, "mono sm ink", "middle"))
    for i, (pos, label, cls) in enumerate(marks):
        x = x0 + pos * (x1 - x0)
        lvl = i % 2
        body.append(f'<line x1="{x:.1f}" y1="{y - 16 - lvl * 30}" x2="{x:.1f}" y2="{y + bh + 8}" class="{cls}"/>')
        anchor = "start" if pos < 0.7 else "end"
        body.append(t(x + (8 if pos < 0.7 else -8), y - 24 - lvl * 30, label, "mono sm ink", anchor))
    if note:
        body.append(t(0, y + bh + 62, note, "cap"))
    return svg(y + bh + 104, f'<g transform="translate(0 60)">' + "".join(body) + "</g>", "span", cap)


# ---------------------------------------------------------------- structure

def route(parts, current, cap=None):
    """Four boxes, the current one filled, the ones behind it ticked."""
    n = len(parts)
    gap = 14
    bw = (W - gap * (n - 1)) / n
    body = []
    for i, (num, title) in enumerate(parts):
        x = i * (bw + gap)
        done, now = i < current, i == current
        cls = "cy" if now else "paper"
        body.append(f'<rect x="{x:.1f}" y="0" width="{bw:.1f}" height="112" class="{cls}"/>')
        body.append(f'<rect x="{x:.1f}" y="0" width="{bw:.1f}" height="112" class="rule" style="stroke-width:1.5"/>')
        tc = "ink" if not now else "ink"
        body.append(t(x + 16, 36, f"Part {num}" + ("  ✓" if done else ""), "mono sm " + ("mute" if done else tc)))
        lines = _wrap(title, 13)
        for k, ln in enumerate(lines[:2]):
            body.append(t(x + 16, 70 + k * 28, ln, "disp " + ("mute" if done else "ink"), size=26))
        if i < n - 1:
            body.append(f'<path d="M{x + bw + 2:.1f} 48 l10 8 l-10 8" class="inkline" style="stroke-width:1.5"/>')
    return svg(112, "".join(body), "route", cap)


def bricks(labels, under=None, cap=None):
    """A running-bond wall with one numbered brick per label; `under` draws a brick beneath the footing."""
    bw, bh, gap = 292, 84, 8
    rows = [[0, 1, 2], [3, 4]]
    body, y = [], 0
    for r, idx in enumerate(rows):
        off = 0 if r == 0 else (bw + gap) / 2
        for k, i in enumerate(idx):
            x = off + k * (bw + gap)
            body.append(f'<rect x="{x:.1f}" y="{y}" width="{bw}" height="{bh}" class="paper"/>')
            body.append(f'<rect x="{x:.1f}" y="{y}" width="{bw}" height="{bh}" class="rule" style="stroke-width:1.5"/>')
            body.append(t(x + 14, y + 52, str(i + 1), "disp ink", size=44))
            lines = _wrap(labels[i], 21)
            for j, ln in enumerate(lines[:2]):
                body.append(t(x + 54, y + 36 + j * 22, ln, "body ink", size=17))
        y += bh + gap
    body.append(f'<line x1="0" y1="{y + 4}" x2="{W}" y2="{y + 4}" class="inkline"/>')
    body.append(t(0, y + 28, "footing: HDMC, the motor company", "cap"))
    y += 34
    if under:
        y += 16
        x = (W - bw) / 2
        body.append(f'<rect x="{x:.1f}" y="{y}" width="{bw}" height="{bh}" class="hatch"/>')
        body.append(f'<rect x="{x:.1f}" y="{y}" width="{bw}" height="{bh}" class="mgline" style="stroke-dasharray:6 5"/>')
        body.append(t(x + bw / 2, y + 36, under[0], "disp mg", "middle", size=32))
        body.append(t(x + bw / 2, y + 64, under[1], "mono sm mg", "middle"))
        y += bh
    return svg(y + 8, "".join(body), "bricks", cap)


def chips(left, right, centre=None, cap=None):
    """Two labelled columns of chips: (header, sub, cls, [items]). centre: (label, sub) sits between them."""
    colw = 350 if centre else 436
    body, maxy = [], 0
    for ci, (header, sub, cls, items) in enumerate([left, right]):
        x = 0 if ci == 0 else W - colw
        body.append(t(x, 18, header, "mono sm " + cls))
        body.append(t(x, 40, sub, "cap"))
        y = 60
        cx, cy = x, y
        for it in items:
            w = 28 + len(it) * 11.2
            if cx + w > x + colw and cx > x:
                cx, cy = x, cy + 50
            body.append(f'<rect x="{cx:.1f}" y="{cy}" width="{w:.1f}" height="40" rx="20" class="{cls}" opacity=".16"/>')
            body.append(f'<rect x="{cx:.1f}" y="{cy}" width="{w:.1f}" height="40" rx="20" class="{cls}line"/>')
            body.append(t(cx + w / 2, cy + 26, it, "mono ink", "middle"))
            cx += w + 10
        maxy = max(maxy, cy + 40)
    if centre:
        x, yc = W / 2, max(maxy / 2 + 30, 90)
        body.append(f'<circle cx="{x:.1f}" cy="{yc}" r="60" class="hatch"/>')
        body.append(f'<circle cx="{x:.1f}" cy="{yc}" r="60" class="inkline" style="stroke-dasharray:6 5"/>')
        body.append(t(x, yc - 4, centre[0], "disp ink", "middle", size=24))
        body.append(t(x, yc + 36, centre[1], "disp ink", "middle", size=44))
        body.append(f'<path d="M{x - 66:.1f} {yc} h-30 m6 -6 l-6 6 l6 6" class="inkline" style="stroke-dasharray:4 4"/>')
        body.append(f'<path d="M{x + 66:.1f} {yc} h30 m-6 -6 l6 6 l-6 6" class="inkline" style="stroke-dasharray:4 4"/>')
        maxy = max(maxy, yc + 60)
    return svg(maxy + 8, "".join(body), "chips", cap)


def chain(steps, cap=None, cls="cy"):
    """Boxes joined by arrows: (head, sub). The last box carries the outcome in `cls`."""
    n = len(steps)
    gap = 26
    bw = (W - gap * (n - 1)) / n
    body = []
    for i, (head, sub) in enumerate(steps):
        x = i * (bw + gap)
        last = i == n - 1
        op = ' opacity=".18"' if last else ""
        body.append(f'<rect x="{x:.1f}' + f'" y="0" width="{bw:.1f}" height="120" class="{"paper" if not last else cls}"{op}/>')
        body.append(f'<rect x="{x:.1f}" y="0" width="{bw:.1f}" height="120" class="{"rule" if not last else cls + "line"}" style="stroke-width:1.5"/>')
        for k, ln in enumerate(_wrap(head, 16)[:2]):
            body.append(t(x + 14, 36 + k * 24, ln, "disp ink", size=24))
        for k, ln in enumerate(_wrap(sub, 22)[:2]):
            body.append(t(x + 14, 86 + k * 17, ln, "body ink", size=14))
        if i < n - 1:
            body.append(f'<path d="M{x + bw + 4:.1f} 60 h16 m-6 -7 l7 7 l-7 7" class="inkline"/>')
    return svg(122, "".join(body), "chain", cap)


def fork(head, branches, cap=None):
    """One head box and two branches: (title, result, cls)."""
    body = []
    hw = 420
    body.append(f'<rect x="{(W - hw) / 2:.1f}" y="0" width="{hw}" height="64" class="paper"/>')
    body.append(f'<rect x="{(W - hw) / 2:.1f}" y="0" width="{hw}" height="64" class="rule" style="stroke-width:1.5"/>')
    body.append(t(W / 2, 40, head, "disp ink", "middle", size=26))
    bw = 430
    for i, (title, result, cls) in enumerate(branches):
        x = 0 if i == 0 else W - bw
        cx = x + bw / 2
        body.append(f'<path d="M{W / 2} 64 V 90 H {cx:.1f} V 112" class="inkline" style="stroke-width:1.5"/>')
        body.append(f'<rect x="{x}" y="112" width="{bw}" height="128" class="{cls}" opacity=".14"/>')
        body.append(f'<rect x="{x}" y="112" width="{bw}" height="128" class="{cls}line" style="stroke-width:1.5"/>')
        body.append(t(x + 16, 146, title, "mono sm " + cls))
        for k, ln in enumerate(_wrap(result, 34)[:3]):
            body.append(t(x + 16, 176 + k * 22, ln, "body ink", size=16))
    return svg(244, "".join(body), "fork", cap)


def doc(title, lines, hot, redact=None, cap=None, stamp=None):
    """A page from a filing. lines: strings; `hot` is the index drawn in full; the rest are ruled grey.
    redact: (index, chars) blacks out a word on that line."""
    pw, x0 = 620, (W - 620) / 2
    body = [f'<rect x="{x0}" y="0" width="{pw}" height="{56 + len(lines) * 30}" class="paper"/>',
            f'<rect x="{x0}" y="0" width="{pw}" height="{56 + len(lines) * 30}" class="rule" style="stroke-width:1.5"/>',
            t(x0 + 26, 34, title, "mono sm mute")]
    y = 74
    for i, ln in enumerate(lines):
        if i == hot:
            body.append(f'<rect x="{x0 + 14}" y="{y - 20}" width="{pw - 28}" height="30" class="cy" opacity=".18"/>')
            body.append(t(x0 + 26, y, ln, "body ink", size=16))
            if redact:
                body.append(f'<rect x="{x0 + 26 + redact[0]}" y="{y - 16}" width="{redact[1]}" height="22" class="ink"/>')
        else:
            w = min(pw - 52, 40 + (len(ln) * 7.4 if ln else 0))
            body.append(f'<rect x="{x0 + 26}" y="{y - 12}" width="{w:.1f}" height="8" class="mute" opacity=".35"/>')
        y += 30
    if stamp:
        cx, cy = x0 + pw - 150, 56 + len(lines) * 15
        body.append(f'<g transform="rotate(-12 {cx} {cy})"><rect x="{cx - 120}" y="{cy - 26}" width="240" height="52" class="mgline" style="stroke-width:3"/>'
                    + t(cx, cy + 9, stamp, "disp mg", "middle", size=26) + "</g>")
    return svg(56 + len(lines) * 30 + 4, "".join(body), "doc", cap)


def coins(items, cap=None):
    """Circles with a face value and a label: (face, label, sub)."""
    n = len(items)
    body = []
    for i, (face, label, sub) in enumerate(items):
        cx = (i + .5) * W / n
        body.append(f'<circle cx="{cx:.1f}" cy="70" r="58" class="paper"/>')
        body.append(f'<circle cx="{cx:.1f}" cy="70" r="58" class="rule2"/>')
        body.append(f'<circle cx="{cx:.1f}" cy="70" r="48" class="rule" style="stroke-dasharray:3 4"/>')
        body.append(t(cx, 88, face, "disp ink", "middle", size=54))
        body.append(t(cx, 158, label, "mono sm ink", "middle"))
        body.append(t(cx, 180, sub, "cap", "middle"))
    return svg(190, "".join(body), "coins", cap)


def hub(centre, spokes, cap=None):
    """A centre and spokes: (label, sub, cls). Kept items (cy) sit on the ring; dropped ones (mg) outside it."""
    import math
    cx, cy, r = W / 2, 210, 130
    body = [f'<circle cx="{cx}" cy="{cy}" r="{r}" class="rule" style="stroke-dasharray:6 6"/>',
            f'<circle cx="{cx}" cy="{cy}" r="56" class="ink"/>',
            t(cx, cy - 4, centre[0], "mono sm", "middle", extra=' style="fill:var(--paper)"'),
            t(cx, cy + 16, centre[1], "mono sm", "middle", extra=' style="fill:var(--paper)"')]
    n = len(spokes)
    for i, (label, sub, cls) in enumerate(spokes):
        a = -math.pi / 2 + (i + .5) * 2 * math.pi / n
        inside = "cy" in cls
        d = r - 4 if inside else r + 48
        x, y = cx + d * math.cos(a), cy + d * math.sin(a)
        body.append(f'<line x1="{cx + 56 * math.cos(a):.1f}" y1="{cy + 56 * math.sin(a):.1f}" x2="{x:.1f}" y2="{y:.1f}" class="{cls}line" style="stroke-width:2{"" if inside else ";stroke-dasharray:4 5"}"/>')
        body.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" class="{cls}"/>')
        right = math.cos(a) > 0
        lx = x + (18 if right else -18)
        anchor = "start" if right else "end"
        ly = y + (-8 if math.sin(a) < 0 else 22)
        body.append(t(lx, ly, label, "mono " + cls, anchor))
        body.append(t(lx, ly + 20, sub, "cap", anchor))
    return svg(cy + r + 90, "".join(body), "hub", cap)


def threshold(line_label, above, below, cap=None):
    """Items above and below a horizontal rule: (label, sub, cls)."""
    y = 120
    body = [f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" class="inkline"/>',
            t(W, y - 10, line_label, "mono sm ink", "end")]
    def row(items, yy, tag):
        n = len(items)
        bw = min(260, W / n - 14)
        for i, (label, sub, cls) in enumerate(items):
            x = (i + .5) * W / n
            body.append(f'<rect x="{x - bw / 2:.1f}" y="{yy}" width="{bw:.1f}" height="60" class="{cls}" opacity=".14"/>')
            body.append(f'<rect x="{x - bw / 2:.1f}" y="{yy}" width="{bw:.1f}" height="60" class="{cls}line" style="stroke-width:1.5"/>')
            body.append(t(x, yy + 27, label, "disp ink", "middle", size=23))
            body.append(t(x, yy + 48, sub, "cap", "middle"))
        body.append(t(0, yy + (-8 if yy < y else 80), tag, "mono sm mute"))
    row(above, y - 84, "built in Milwaukee, kept")
    row(below, y + 22, "bought, licensed or partnered")
    return svg(y + 110, "".join(body), "thr", cap)


def stamps(items, cap=None):
    """Dated tapes carrying the same words: (year, phrase, cls)."""
    body, y = [], 0
    for year, phrase, cls in items:
        body.append(f'<rect x="0" y="{y}" width="{W}" height="54" class="{cls}" opacity=".12"/>')
        body.append(f'<rect x="0" y="{y}" width="150" height="54" class="{cls}"/>')
        body.append(t(75, y + 36, year, "disp", "middle", size=30, extra=' style="fill:var(--paper)"'))
        body.append(t(172, y + 34, phrase, "mono ink", size=16))
        y += 66
    return svg(y - 8, "".join(body), "stamps", cap)


def ranges(rows, cap=None, **kw):
    return hbars(rows, cap, **kw)
