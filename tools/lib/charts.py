"""Ground Truth house charts — SVG emitters in the site's classes.

Classes: .gl gridline · .zl zero line · .ax axis label · .bar · .vl value label.
Fills:   var(--magenta) = the bad or highlighted number · var(--cyan) = healthy or reference · var(--ink-3) = history.
Both the brief (brief.css) and the series (series.css) define these classes; svg_theme() remaps the
CSS variables for the series' dark slides.
"""
from html import escape

MAG, CYAN, INK3, INK = "var(--magenta)", "var(--cyan)", "var(--ink-3)", "var(--ink)"


def _fmt(v, fmt):
    return fmt(v) if callable(fmt) else (fmt % v if fmt else f"{v:,.0f}")


def bars(values, labels, *, fills=None, tips=None, fmt=None, vb=(720, 280), label="",
         ymax=None, ticks=4, tickfmt=None, left=56, bar_w=None, opacities=None, vl_neg=False, scale=1.0):
    """Vertical bars. values are magnitudes (>=0). fills per bar; tips per bar (data-tip)."""
    W, H = vb
    n = len(values)
    top, bottom = 40 * scale, H - 50 * scale
    plot_h = bottom - top
    ymax = ymax or max(values) * 1.12
    fills = fills or [MAG] * n
    opacities = opacities or [None] * n
    tips = tips or [None] * n
    inner_l = left
    inner_w = W - inner_l - 20 * scale
    slot = inner_w / n
    bw = bar_w or min(80 * scale, slot * 0.62)
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{escape(label)}">']
    for i in range(1, ticks + 1):
        y = bottom - plot_h * i / ticks
        out.append(f'<line class="gl" x1="{inner_l}" y1="{y:.1f}" x2="{W-20*scale}" y2="{y:.1f}"></line>')
        tv = ymax * i / ticks
        out.append(f'<text class="ax" x="0" y="{y+4*scale:.1f}">{escape(_fmt(tv, tickfmt or fmt))}</text>')
    out.append(f'<line class="zl" x1="{inner_l}" y1="{bottom}" x2="{W-20*scale}" y2="{bottom}"></line>')
    out.append(f'<text class="ax" x="0" y="{bottom+4*scale:.1f}">0</text>')
    for i, v in enumerate(values):
        cx = inner_l + slot * (i + 0.5)
        h = plot_h * v / ymax
        x = cx - bw / 2
        op = f' opacity="{opacities[i]}"' if opacities[i] else ""
        tip = f' data-tip="{escape(str(tips[i]))}"' if tips[i] else ""
        out.append(f'<rect class="bar" x="{x:.1f}" y="{bottom-h:.1f}" width="{bw:.1f}" height="{h:.1f}" fill="{fills[i]}"{op}{tip}></rect>')
        cls = "vl vl-neg" if (vl_neg and fills[i] == MAG) else "vl"
        out.append(f'<text class="{cls}" x="{cx:.1f}" y="{bottom-h-7*scale:.1f}" text-anchor="middle">{escape(_fmt(v, fmt))}</text>')
        out.append(f'<text class="ax" x="{cx:.1f}" y="{bottom+20*scale:.1f}" text-anchor="middle">{escape(str(labels[i]))}</text>')
    out.append("</svg>")
    return "\n".join(out)


def hbars(values, labels, *, fills=None, tips=None, fmt=None, vb=(720, None), label="", xmax=None,
          row_h=34, left=150, scale=1.0, sublabels=None):
    """Horizontal bars, one row per item — for ranked lists (costs, units)."""
    W = vb[0]
    n = len(values)
    rh = row_h * scale
    H = vb[1] or int(rh * n + 30 * scale)
    fills = fills or [INK3] * n
    tips = tips or [None] * n
    xmax = xmax or max(values) * 1.15
    inner_l, inner_r = left * scale, W - 90 * scale
    inner_w = inner_r - inner_l
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{escape(label)}">']
    out.append(f'<line class="zl" x1="{inner_l}" y1="{10*scale}" x2="{inner_l}" y2="{H-14*scale}"></line>')
    for i, v in enumerate(values):
        y = 14 * scale + rh * i
        bh = rh * 0.58
        w = inner_w * v / xmax
        tip = f' data-tip="{escape(str(tips[i]))}"' if tips[i] else ""
        out.append(f'<text class="ax" x="{inner_l-10*scale:.1f}" y="{y+bh*0.7:.1f}" text-anchor="end">{escape(str(labels[i]))}</text>')
        if sublabels and sublabels[i]:
            out.append(f'<text class="ax" x="{inner_l-10*scale:.1f}" y="{y+bh*0.7+12*scale:.1f}" text-anchor="end" opacity=".7">{escape(str(sublabels[i]))}</text>')
        out.append(f'<rect class="bar" x="{inner_l}" y="{y:.1f}" width="{max(w,1.5):.1f}" height="{bh:.1f}" fill="{fills[i]}"{tip}></rect>')
        out.append(f'<text class="vl" x="{inner_l+w+8*scale:.1f}" y="{y+bh*0.72:.1f}">{escape(_fmt(v, fmt))}</text>')
    out.append("</svg>")
    return "\n".join(out)


def waterfall(steps, *, fmt=None, vb=(720, 300), label="", scale=1.0, left=56):
    """steps: list of (label, delta, fill) — running bars from 0; a final ('Total', None, fill) draws the total."""
    W, H = vb
    top, bottom = 40 * scale, H - 50 * scale
    run = 0
    vals = []
    for lab, d, f in steps:
        if d is None:
            vals.append((lab, 0, run, f, True))
        else:
            vals.append((lab, run, run + d, f, False))
            run += d
    lo = min(0, min(min(a, b) for _, a, b, _, _ in vals))
    hi = max(max(a, b) for _, a, b, _, _ in vals) * 1.1
    span = hi - lo
    n = len(vals)
    inner_l = left
    inner_w = W - inner_l - 20 * scale
    slot = inner_w / n
    bw = min(80 * scale, slot * 0.62)
    Y = lambda v: bottom - (v - lo) / span * (bottom - top)
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{escape(label)}">']
    for i in range(1, 5):
        v = lo + span * i / 4
        out.append(f'<line class="gl" x1="{inner_l}" y1="{Y(v):.1f}" x2="{W-20*scale}" y2="{Y(v):.1f}"></line>')
        out.append(f'<text class="ax" x="0" y="{Y(v)+4*scale:.1f}">{escape(_fmt(v, fmt))}</text>')
    out.append(f'<line class="zl" x1="{inner_l}" y1="{Y(0):.1f}" x2="{W-20*scale}" y2="{Y(0):.1f}"></line>')
    prev_top = None
    for i, (lab, a, b, f, total) in enumerate(vals):
        cx = inner_l + slot * (i + 0.5)
        x = cx - bw / 2
        y0, y1 = Y(max(a, b)), Y(min(a, b))
        out.append(f'<rect class="bar" x="{x:.1f}" y="{y0:.1f}" width="{bw:.1f}" height="{max(y1-y0,1.5):.1f}" fill="{f}"></rect>')
        if prev_top is not None and not total:
            out.append(f'<line class="gl" x1="{x-slot*0.38:.1f}" y1="{Y(a):.1f}" x2="{x:.1f}" y2="{Y(a):.1f}"></line>')
        val = b if total else b - a
        out.append(f'<text class="vl" x="{cx:.1f}" y="{y0-7*scale:.1f}" text-anchor="middle">{escape(_fmt(val, fmt))}</text>')
        out.append(f'<text class="ax" x="{cx:.1f}" y="{bottom+20*scale:.1f}" text-anchor="middle">{escape(lab)}</text>')
        prev_top = b
    out.append("</svg>")
    return "\n".join(out)


def svg_theme(svg, dark):
    """Remap brief CSS variables to the series palette (series.css names)."""
    m = {"var(--magenta)": "var(--dmag)" if dark else "var(--mag)",
         "var(--cyan)": "var(--dcyan)" if dark else "var(--cyan)",
         "var(--ink-3)": "var(--dink3)" if dark else "var(--ink3)",
         "var(--ink)": "var(--dink)" if dark else "var(--ink)"}
    for k, v in m.items():
        svg = svg.replace(k, v)
    return svg


def sbars(values, labels, *, fills=None, tips=None, fmt=None, vb=(720, 280), label="", scale=1.0, left=56):
    """Signed vertical bars around a zero line (positive up, negative down)."""
    W, H = vb
    n = len(values)
    top, bottom = 34 * scale, H - 46 * scale
    lo, hi = min(0, min(values)), max(0, max(values))
    span = (hi - lo) * 1.15 or 1
    Y = lambda v: bottom - (v - lo * 1.075) / span * (bottom - top)
    fills = fills or [MAG] * n
    tips = tips or [None] * n
    inner_l = left
    inner_w = W - inner_l - 20 * scale
    slot = inner_w / n
    bw = min(80 * scale, slot * 0.62)
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{escape(label)}">']
    for v in [hi, hi / 2, lo / 2, lo]:
        if v == 0:
            continue
        out.append(f'<line class="gl" x1="{inner_l}" y1="{Y(v):.1f}" x2="{W-20*scale}" y2="{Y(v):.1f}"></line>')
        out.append(f'<text class="ax" x="0" y="{Y(v)+4*scale:.1f}">{escape(_fmt(v, fmt))}</text>')
    out.append(f'<line class="zl" x1="{inner_l}" y1="{Y(0):.1f}" x2="{W-20*scale}" y2="{Y(0):.1f}"></line>')
    out.append(f'<text class="ax" x="0" y="{Y(0)+4*scale:.1f}">0</text>')
    for i, v in enumerate(values):
        cx = inner_l + slot * (i + 0.5)
        x = cx - bw / 2
        y0, y1 = (Y(v), Y(0)) if v >= 0 else (Y(0), Y(v))
        tip = f' data-tip="{escape(str(tips[i]))}"' if tips[i] else ""
        out.append(f'<rect class="bar" x="{x:.1f}" y="{y0:.1f}" width="{bw:.1f}" height="{max(y1-y0,1.5):.1f}" fill="{fills[i]}"{tip}></rect>')
        ly = y0 - 7 * scale if v >= 0 else y1 + 15 * scale
        out.append(f'<text class="vl{" vl-neg" if v < 0 else ""}" x="{cx:.1f}" y="{ly:.1f}" text-anchor="middle">{escape(_fmt(v, fmt))}</text>')
        out.append(f'<text class="ax" x="{cx:.1f}" y="{bottom+20*scale:.1f}" text-anchor="middle">{escape(str(labels[i]))}</text>')
    out.append("</svg>")
    return "\n".join(out)
