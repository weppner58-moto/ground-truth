"""Route cards for the carousel series, with an optional image band.

A route card is the second page of every part's carousel PDF and ships alone as
GroundTruth-NN_Card_PartN_<Name>.pdf; the stand-alone one (id route-card) is the series card.
Used by the No. 02 and No. 03 builders and by tools/gt01/embed.py for the hand-built No. 01.
"""
import base64, mimetypes
from pathlib import Path

CARD_CSS = """
.slide.card h1{font-size:80px}
.slide.card .cband{margin:22px 0 0}
.slide.card .cband img{height:330px}
.rgrid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:26px}
.rgrid .c{border:1px solid var(--rule);padding:16px;position:relative}
.dk .rgrid .c{border-color:var(--drule)}
.rgrid .c.on{border-color:var(--mag)} .dk .rgrid .c.on{border-color:var(--dmag)}
.rgrid .n{font-family:var(--mono);font-size:13px;letter-spacing:.18em;text-transform:uppercase;color:var(--mag)}
.dk .rgrid .n{color:var(--dmag)}
.rgrid .t{font-family:var(--disp);font-weight:800;text-transform:uppercase;font-size:36px;line-height:.95;margin:8px 0 10px}
.rgrid .d{font-size:20px;line-height:1.4;color:var(--ink2)}
.dk .rgrid .d{color:var(--dink3)}
.slide.card.img h1{font-size:64px}
.slide.card.img .rgrid .t{font-size:30px}
.slide.card.img .rgrid .d{font-size:18px}
.slide.card.img .rgrid .c{padding:12px 14px}
body.web .slide.card{display:none}
"""


def data_uri(path):
    p = Path(path)
    mime = mimetypes.guess_type(p.name)[0] or "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"


def route_card(sid, n_on, *, kick, title, dek, parts, url, issue, img=None, caption="", dark=True, quote="'"):
    """parts: list of (name, one-line description). n_on: index highlighted, or -1 for the series card."""
    q = quote
    cells = "".join(
        f"<div class={q}c{' on' if i == n_on else ''}{q}><div class={q}n{q}>Part {i+1} of {len(parts)}{' · this post' if i == n_on else ''}</div>"
        f"<div class={q}t{q}>{t}</div><div class={q}d{q}>{d}</div></div>"
        for i, (t, d) in enumerate(parts))
    band = ""
    if img:
        cap = f"<div class={q}c{q}>{caption}</div>" if caption else ""
        band = f"<div class={q}band cmk cband{q}><img src={q}{data_uri(img)}{q} alt={q}{caption}{q}>{cap}</div>"
    dek_color = "var(--dink3)" if dark else "var(--ink2)"
    hdr = f"<div class={q}tophdr{q}><div class={q}mark{q}>CONTACT&nbsp;<i>PATCH</i></div><div class={q}tag{q}>Route card</div></div>"
    body = f"""
  <div class={q}kick{q}>{kick}</div>
  <h1>{title}</h1>
  {band if img else f"<p class={q}wide{q} style={q}font-size:26px;margin-top:22px;color:{dek_color}{q}>{dek}</p>"}
  <div class={q}rgrid{q}>{cells}</div>
  <div class={q}spacer{q}></div>
  <div class={q}foot{q}><span>{url}</span><span>{issue}</span></div>"""
    cls = "card img" if img else "card"
    return f"<div class={q}slide{' dk' if dark else ''} {cls}{q} id={q}{sid}{q}>{hdr}{body}</div>\n"
