"""The Contact Patch Advisory logo (CP brush mark with the wordmark), swapped in for every text mark.

  from logo import apply; html = apply(html)          # brief pages, index, practice site
  from logo import apply; html = apply(html, slides=True)   # carousel pages (dark slides show the paper version)

Both versions ride along as data URIs; CSS shows the ink one on light grounds and the paper one on dark.
"""
import base64, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
IMG = ROOT / "tools" / "site" / "img"
INK = "data:image/png;base64," + base64.b64encode((IMG / "logo-ink-600.png").read_bytes()).decode()
PAPER = "data:image/png;base64," + base64.b64encode((IMG / "logo-paper-600.png").read_bytes()).decode()

CSS = """
/* logo.py */
.mark{display:flex;align-items:center}
.mark .lg{display:block;height:var(--logo-h,56px);width:auto}
.mark .lg-paper{display:none}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .mark .lg-ink{display:none}:root:not([data-theme="light"]) .mark .lg-paper{display:block}}
:root[data-theme="dark"] .mark .lg-ink{display:none}:root[data-theme="dark"] .mark .lg-paper{display:block}
.dk .mark .lg-ink,.dark .mark .lg-ink,body.dark .mark .lg-ink{display:none}
.dk .mark .lg-paper,.dark .mark .lg-paper,body.dark .mark .lg-paper{display:block}
.slide .mark .lg{height:var(--logo-h,54px)}
.topbar .mark .lg{height:var(--logo-h,56px)}
header.site .mark .lg,.site-head .mark .lg,.nav .mark .lg{height:var(--logo-h,64px)}
/* /logo.py */"""

TAG = f'<img class="lg lg-ink" src="{INK}" alt="Contact Patch Advisory"><img class="lg lg-paper" src="{PAPER}" alt="">'


def apply(html, force_dark=False):
    """Replace the text inside every .mark with the logo images (idempotent)."""
    html = re.sub(r"\n?/\* logo\.py \*/.*?/\* /logo\.py \*/", "", html, count=1, flags=re.S)
    css = CSS
    if force_dark:
        css += "\n.mark .lg-ink{display:none!important}.mark .lg-paper{display:block!important}\n"
    if "</style>" in html:
        html = html.replace("</style>", css + "\n</style>", 1)
    else:
        html = html.replace("</head>", "<style>" + css + "\n</style>\n</head>", 1)
    def swap(m):
        open_tag = m.group(1)
        return open_tag + TAG + m.group(3)
    # <div class="mark">...</div> and <a class="mark" ...>...</a>, either quote style, any inner text
    html = re.sub(r'(<(?:div|a) class=["\']mark["\'][^>]*>)(.*?)(</(?:div|a)>)', swap, html, flags=re.S)
    return html
