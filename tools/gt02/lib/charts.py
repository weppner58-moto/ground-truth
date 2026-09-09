"""SVG chart helpers matching the Ground Truth brief CSS (.gl .zl .ax .bar .vl classes).

Every helper returns an SVG string sized for the brief column (viewBox 720 wide) or a
custom width. Colors are CSS variables so the charts follow the page theme.
"""

MAG = "var(--magenta)"
CYAN = "var(--cyan)"
INK3 = "var(--ink-3)"


def _fmt(v, fmt):
    return fmt.format(v) if isinstance(fmt, str) else fmt(v)


def bars(values, labels, *, colors=None, opacities=None, ymax=None, ymin=0, ticks=None,
         tick_fmt="{:,.0f}", val_fmt="{:,.0f}", aria="", width=720, height=280,
         pad_l=64, pad_r=20, pad_t=18, pad_b=50, tips=None, zero_line=True,
         label_fs=None):
    """Vertical bar chart with a zero line. Negative values hang below zero."""
    n = len(values)
    if ymax is None:
        ymax = max(max(values), 0)
    if ymin is None:
        ymin = min(min(values), 0)
    lo = min(ymin, min(values))
    hi = max(ymax, max(values))
    span = hi - lo or 1
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b
    gap = plot_w / n
    bw = gap * 0.62

    def y(v):
        return pad_t + (hi - v) / span * plot_h

    out = [f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{aria}">']
    if ticks is None:
        ticks = []
    for t in ticks:
        yy = y(t)
        cls = "zl" if (t == 0 and zero_line) else "gl"
        out.append(f'<line class="{cls}" x1="{pad_l-8}" y1="{yy:.1f}" x2="{width-pad_r}" y2="{yy:.1f}"></line>')
        out.append(f'<text class="ax" x="0" y="{yy+4:.1f}">{_fmt(t, tick_fmt)}</text>')
    if 0 not in ticks and zero_line and lo < 0 < hi:
        yy = y(0)
        out.append(f'<line class="zl" x1="{pad_l-8}" y1="{yy:.1f}" x2="{width-pad_r}" y2="{yy:.1f}"></line>')
    for i, v in enumerate(values):
        x = pad_l + gap * i + (gap - bw) / 2
        y0, y1 = y(max(v, 0)), y(min(v, 0))
        h = max(y1 - y0, 1.5)
        col = (colors[i] if colors else MAG)
        op = f' opacity="{opacities[i]}"' if opacities and opacities[i] is not None else ""
        tip = tips[i] if tips else f"{labels[i]} — {_fmt(v, val_fmt)}"
        out.append(f'<rect class="bar" x="{x:.1f}" y="{y0:.1f}" width="{bw:.1f}" height="{h:.1f}" fill="{col}"{op} data-tip="{tip}"></rect>')
        vy = y0 - 7 if v >= 0 else y1 + 15
        out.append(f'<text class="vl" x="{x+bw/2:.1f}" y="{vy:.1f}" text-anchor="middle">{_fmt(v, val_fmt)}</text>')
        fs = f' font-size="{label_fs}"' if label_fs else ""
        out.append(f'<text class="ax" x="{x+bw/2:.1f}" y="{height-pad_b+22}" text-anchor="middle"{fs}>{labels[i]}</text>')
    out.append("</svg>")
    return "\n".join(out)


def hbars(rows, *, xmax, width=720, row_h=38, pad_l=190, pad_r=90, val_fmt="{:,.0f}", aria=""):
    """Horizontal bars. rows = [(label, value, color, opacity, note)]."""
    height = row_h * len(rows) + 16
    plot_w = width - pad_l - pad_r
    out = [f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{aria}">']
    for i, (label, v, col, op, note) in enumerate(rows):
        yy = 8 + i * row_h
        w = max(plot_w * v / xmax, 1.5)
        opa = f' opacity="{op}"' if op is not None else ""
        out.append(f'<text class="ax" x="0" y="{yy+row_h*0.55:.1f}">{label}</text>')
        out.append(f'<rect class="bar" x="{pad_l}" y="{yy+6}" width="{w:.1f}" height="{row_h-14}" fill="{col}"{opa} data-tip="{label} — {_fmt(v,val_fmt)}"></rect>')
        out.append(f'<text class="vl" x="{pad_l+w+8:.1f}" y="{yy+row_h*0.55:.1f}">{_fmt(v,val_fmt)}{(" · "+note) if note else ""}</text>')
    out.append("</svg>")
    return "\n".join(out)


def waterfall(steps, *, ymin, ymax, ticks, width=720, height=300, pad_l=64, pad_r=20, pad_t=18, pad_b=56,
              val_fmt="{:+,.0f}", aria=""):
    """Bridge chart. steps = [(label, delta or None for total, color)]. A None delta draws the running total."""
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b
    span = ymax - ymin
    n = len(steps)
    gap = plot_w / n
    bw = gap * 0.6

    def y(v):
        return pad_t + (ymax - v) / span * plot_h

    out = [f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{aria}">']
    for t in ticks:
        cls = "zl" if t == 0 else "gl"
        out.append(f'<line class="{cls}" x1="{pad_l-8}" y1="{y(t):.1f}" x2="{width-pad_r}" y2="{y(t):.1f}"></line>')
        out.append(f'<text class="ax" x="0" y="{y(t)+4:.1f}">{t:,.0f}</text>')
    run = 0
    for i, (label, d, col) in enumerate(steps):
        x = pad_l + gap * i + (gap - bw) / 2
        if d is None:
            top, bot, shown = max(run, 0), min(run, 0), run
            txt = f"{run:,.0f}"
        else:
            a, b = run, run + d
            top, bot = max(a, b), min(a, b)
            run = b
            txt = _fmt(d, val_fmt)
        h = max(y(bot) - y(top), 1.5)
        out.append(f'<rect class="bar" x="{x:.1f}" y="{y(top):.1f}" width="{bw:.1f}" height="{h:.1f}" fill="{col}" data-tip="{label} — {txt}"></rect>')
        out.append(f'<text class="vl" x="{x+bw/2:.1f}" y="{y(top)-7:.1f}" text-anchor="middle">{txt}</text>')
        out.append(f'<text class="ax" x="{x+bw/2:.1f}" y="{height-pad_b+22}" text-anchor="middle">{label}</text>')
    out.append("</svg>")
    return "\n".join(out)
