"""Image bands shared by the three carousel builders and the placement scripts.

duo(): two images side by side on one slide, a product photo (white, contained) beside a sketch
(dark, cropped), or two products. Product photos live in tools/lib/products/.
"""
from pathlib import Path
from cards import data_uri

LIB = Path(__file__).resolve().parent
PRODUCTS = LIB / "products"

DUO_CSS = """
/* bands.py */
.band.duo{display:grid;grid-template-columns:1fr 1fr;gap:12px;background:none;border:0}
.band.duo .cell{position:relative;border:1px solid var(--rule);background:#15171A;overflow:hidden}
.dk .band.duo .cell{border-color:var(--drule)}
.band.duo .cell.white{background:#fff}
.band.duo .cell img{display:block;width:100%;height:260px;object-fit:cover}
.band.duo .cell.white img{object-fit:contain;padding:14px 18px 34px}
.band.duo .cell .c{position:absolute;left:0;right:0;bottom:0;padding:8px 12px;font-family:var(--mono);font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:#E7E9EB;background:linear-gradient(transparent,rgba(11,12,14,.85))}
.band.duo .cell.white .c{color:#4A4E54;background:none;border-top:1px solid #E3E0D8;padding:7px 12px 6px}
.band.duo .cell::before,.band.duo .cell::after{content:"";position:absolute;width:12px;height:12px;border:1.5px solid var(--mag);pointer-events:none}
.band.duo .cell::before{top:-1px;left:-1px;border-right:0;border-bottom:0}
.band.duo .cell::after{bottom:-1px;right:-1px;border-left:0;border-top:0}
.band.product{background:#fff}
.band.product img{object-fit:contain;padding:14px 18px 34px;height:300px}
.band.product .c{color:#4A4E54;background:none;border-top:1px solid #E3E0D8;padding:7px 12px 6px}
/* /bands.py */"""


def _src(f):
    p = Path(f)
    if not p.is_absolute():
        p = (PRODUCTS / f) if (PRODUCTS / f).exists() else (LIB.parent / f)
    return p


def is_product(f):
    return (PRODUCTS / Path(f).name).exists() and str(f).count("/") == 0


def cell(f, cap):
    p = _src(f)
    white = " white" if p.parent == PRODUCTS else ""
    return f'<div class="cell{white}"><img src="{data_uri(p)}" alt="{cap}"><div class="c">{cap}</div></div>'


def duo(left, right, cap_l, cap_r, extra=""):
    return f'<div class="band duo{(" " + extra) if extra else ""}">{cell(left, cap_l)}{cell(right, cap_r)}</div>'


def product(f, cap):
    return f'<div class="band cmk product"><img src="{data_uri(_src(f))}" alt="{cap}"><div class="c">{cap}</div></div>'
