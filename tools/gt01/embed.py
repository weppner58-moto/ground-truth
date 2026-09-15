#!/usr/bin/env python3
"""
No. 01 is hand-built, so its images are embedded by this script rather than a builder.

  python3 tools/gt01/embed.py

1. Brief page: every image placeholder (.phx) whose title matches a file in tools/gt01/img/ becomes
   an <img> in a crop-marked .part-img box. Works on the registered page (full/index.html) and then
   re-runs split_brief so the public page picks the change up.
2. Series page: route cards (s1-card .. s4-card, route-card) are rebuilt from tools/lib/cards.py with
   the part image on each, replacing any earlier card slides. Then re-render the PDFs:
     python3 tools/lib/render_slides.py site/groundtruth/01/series/index.html 01 \\
       "1:The-Growth" "2:The-Lineup" "3:The-Contracts" "4:The-Loan-and-Final-Word"
"""
import re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "lib"))
from cards import CARD_CSS, route_card, data_uri  # noqa: E402
from sitenav import NAV_CSS, nav_html, bottombar_html  # noqa: E402
from bands import DUO_CSS, duo  # noqa: E402
import blurbs  # noqa: E402
from logo import apply as logo_apply  # noqa: E402

IMG = ROOT / "tools" / "gt01" / "img"
D = ROOT / "site" / "groundtruth" / "01"

# placeholder title on the page -> image file, caption shown on the image
SLOTS = {
    "Juneau Avenue, Milwaukee":   ("gt01-01-juneau.jpg", "Juneau Avenue, Milwaukee. The lender's address."),
    "The Q3 2026 financing 8-K":  ("gt01-02-form.jpg",   "The Q3 2026 financing 8-K. Not filed yet."),
    "LiveWire dealer floor, 2026": ("gt01-03-floor.jpg", "An S2 and a Honcho on the same floor."),
    "LVWR on the tape":           ("gt01-04-tape.jpg",   "LVWR on the tape."),
    "LiveWire, Milwaukee":        ("gt01-05-team.jpg",   "The team that cut cost per bike 47%."),
    "STACYC":                     ("gt01-06-stacyc.jpg", "The only segment that makes money."),
}

PARTS = [("The Growth", "386% is 55 bikes to 267. The plan was 100,000. The miss is the story."),
         ("The Lineup", "$29,799 to $4,999. Premium to price. The overhead never followed."),
         ("The Contracts", "Buying bikes loses money. Not buying them costs money. Both in writing."),
         ("The Loan & the Final Word", "Nov 2025: equity backstop out, secured claim in. $85M due Dec 2027.")]
CARD_IMG = {0: "gt01-04-tape.jpg", 1: "gt01-03-floor.jpg", 2: "gt01-02-form.jpg", 3: "gt01-01-juneau.jpg", -1: "gt01-05-team.jpg"}
CARD_CAP = {0: "LVWR on the tape", 1: "An S2 and a Honcho, same floor", 2: "The paperwork", 3: "Juneau Avenue, the lender's address", -1: "LiveWire, Milwaukee"}
# Second pass (11 Sep): the photos that were on the page from the first build, keyed by a hash of their
# base64 (see key()). Each becomes the named sketch when that file exists in tools/gt01/img/.
REPLACE = {
    "95cf407c": "gt01-07-floor2019.jpg", "ccffc6da": "gt01-07-floor2019.jpg",
    "fcc6ad86": "gt01-08-stripped.jpg",  "20725b8d": "gt01-08-stripped.jpg",
    "afb2f500": "gt01-09-redshift.jpg",
    "e582679c": "gt01-10-bench.jpg",
    "dc0eaa6a": "gt01-11-kymco.jpg", "7e333a36": "gt01-11-kymco.jpg", "69430279": "gt01-11-kymco.jpg",
    "183f0211": "gt01-12-honcho-grass.jpg", "3a99c3a5": "gt01-12-honcho-grass.jpg",
    "dd1f3ae8": "gt01-13-honcho-stand.jpg", "e641700a": "gt01-13-honcho-stand.jpg",
    "b77e2c18": "gt01-14-groms.jpg", "ae5419c9": "gt01-14-groms.jpg",
    "8d29fb50": "gt01-15-dust.jpg", "7e817020": "gt01-15-dust.jpg", "7a75530c": "gt01-15-dust.jpg",
    "7df70d3c": "gt01-16-parts.jpg",
    "32d1d386": "gt01-17-chair.jpg", "50492726": "gt01-17-chair.jpg",
    # product photos on the price ladder (series and brief) -> the current studio shots
    "1080a6a8": "lib/products/one.jpg", "89552776": "lib/products/one.jpg",
    "8ab41138": "lib/products/s2.jpg", "43ce2e4f": "lib/products/s2.jpg", "6dc7e15b": "lib/products/s2.jpg", "636328e5": "lib/products/s2.jpg",
    "83ab2eea": "lib/products/honcho.jpg", "5feac193": "lib/products/honcho.jpg",
}
# Two images on one slide: a product shot beside the sketch, or two products. Left, right, captions.
SERIES_DUO = {
    "s1-3":  ("lineup.jpg", ("glyph", "0.9%", "of the plan. 923 motorcycles against 100,000"), "The lineup, $799 to $16,499", ""),
    "s1-6":  ("s2.jpg", ("glyph", "386%", "Q2 unit growth. 55 motorcycles to 267"), "S2 Del Mar: the bike behind the number", ""),
    "s1-10": ("honcho.jpg", ("glyph", "$4,999", "S4 Honcho. Built by KYMCO. Part 2"), "Next up: the Honcho", ""),
    "s2-4":  ("one.jpg", "honcho.jpg", "LiveWire ONE, $16,499", "S4 Honcho, $4,999. Nothing between them."),
    "s2-5":  ("gt01/img/gt01-13-honcho-stand.jpg", ("glyph", "+39%", "over the Grom, $3,599, the bike that owns the segment"), "Honcho on the stand", ""),
    "s4-7":  ("gt01/img/gt01-12-honcho-grass.jpg", ("glyph", "40,000", "units a year before any conclusion changes"), "2,000 Honchos in a strong first year", ""),
}
# Logos come off the page and become text pills (the page already has .brand-txt).
LOGOS = {
    "1ae5ce73": "LIVEWIRE GROUP &middot; NYSE: LVWR",
    "dd999ff3": "HARLEY-DAVIDSON, INC. &middot; NYSE: HOG",
    "53c5914d": "ALTA MOTORS",
}
# One image per page. Slide id -> (file, caption). A file that does not exist yet drops the band
# until the render lands (then re-run). Files under tools/<issue>/img/.
SERIES_ASSIGN = {
    "s1-1":  ("lib/products/one.jpg", "LiveWire ONE, 2021", "contain"),
    "s4-9":  ("lib/products/lineup.jpg", "The lineup they have", "contain"),
    "s3-5":  ("lib/products/s2.jpg", "S2 Del Mar: bought at cost-plus, written down on arrival", "contain"),
    "s1-5":  ("gt01/img/gt01-19-quarter.jpg", "Q2 2026: 267 motorcycles"),
    "s2-7":  ("gt01/img/gt01-15-dust.jpg", "Dust: the acquired programme", "", "band cmk sm"),
    "s2-6":  ("gt01/img/gt01-11-kymco.jpg", "KYMCO assembly line, Taiwan"),
    "s3-1":  ("gt01/img/gt01-18-line.jpg", "KYMCO, Taiwan"),
    "s3-7":  ("gt01/img/gt01-20-crates.jpg", "Take-or-pay"),
    "s3-9":  ("gt01/img/gt01-21-loan.jpg", "Next: the loan"),
    "s4-3":  ("gt01/img/gt01-22-lien.jpg", "Built it, badged it, sold it, lent against it"),
    "s4-7":  ("gt01/img/gt01-14-groms.jpg", "The segment it has to win"),
    "s4-8":  ("gt01/img/gt01-10-bench.jpg", "Real engineering, real sourcing"),
    "s4-11": ("gt03/img/gt03-06-juneau-dusk.jpg", "Next: the parent"),
}
# Brief clip figures keyed by their <b> label. None removes the figure for good; a file name hides
# the figure until that render exists.
BRIEF_ASSIGN = {
    "H-D LiveWire, 2019": None,
    "KYMCO assembly, Taiwan": "gt01/img/gt01-18-line.jpg",
    "Grom, $3,599": "gt01/img/gt01-23-grom-kerb.jpg",
}
TOOLS = ROOT / "tools"
KICK = "LiveWire: 5 Years In and 1% of Plan · The route"
URL = "contactpatchadvisory.com/groundtruth/01/"
ISSUE = "Ground Truth No. 01"


def key(b64):
    import hashlib
    return hashlib.md5(b64[:20000].encode()).hexdigest()[:8]


def swap(html):
    """Replace first-build photos with the sketches that exist, and logos with text pills."""
    n = {"img": 0, "logo": 0}
    def repl(m):
        tag = m.group(0); k = key(m.group(2))
        if k in LOGOS:
            n["logo"] += 1
            return f'<span class="brand-txt">{LOGOS[k]}</span>'
        f = REPLACE.get(k)
        fp = (TOOLS / f) if f and "/" in f else (IMG / f) if f else None
        if fp and fp.exists():
            n["img"] += 1
            return re.sub(r'src="data:[^"]+"', f'src="{data_uri(fp)}"', tag, count=1)
        return tag
    html = re.sub(r'<img[^>]*src="data:image/(\w+);base64,([^"]+)"[^>]*>', repl, html)
    # the Alta logo clip figure in §05 goes entirely once the Redshift sketch is in
    if (IMG / "gt01-09-redshift.jpg").exists():
        html, c = re.subn(r'<figure class="clip"[^>]*><span class="cm"></span><img [^>]*alt="Alta Motors logo"[^>]*>.*?</figure>', "", html, count=1, flags=re.S)
        n["logo"] += c
    # logos drawn inside the SVG charts (hero and the final-word chart) become wordmark text
    def svglogo(m):
        a = dict(re.findall(r'(\w+)="([^"]*)"', m.group(0)))
        x, y, w, hh = float(a["x"]), float(a["y"]), float(a["width"]), float(a["height"])
        name = "LIVEWIRE GROUP" if w >= 200 else "HARLEY-DAVIDSON"
        if x + w > 1000: ax, anchor = x + w, "end"
        elif x < 100: ax, anchor = x, "start"
        else: ax, anchor = x + w / 2, "middle"
        n["logo"] += 1
        return (f'<text x="{ax:g}" y="{y + hh * 0.68:g}" text-anchor="{anchor}" style="fill:var(--ink)" font-family="Big Shoulders Display,Impact,sans-serif" '
                f'font-weight="800" font-size="{min(30, hh * 0.6):g}" letter-spacing="2">{name}</text>')
    html = re.sub(r'<image class="logo"[^>]*/>', svglogo, html)
    # a band that letterboxed a logo-ish photo on white ("contain") should fill with the sketch
    sk = {key(__import__("base64").b64encode((IMG / f).read_bytes()).decode()) for f in set(REPLACE.values()) if (IMG / f).exists()}
    def unbox(m):
        return m.group(0).replace(" contain", "", 1) if key(m.group(2)) in sk else m.group(0)
    html = re.sub(r'<div class="band[^"]* contain"[^>]*>\s*<img[^>]*src="data:image/(\w+);base64,([^"]+)"', unbox, html)
    return html, n


HEAD = '<!doctype html>\n<meta charset="utf-8">\n'
def skeleton(html):
    """No. 01 was hand-built without a head; give it a doctype and a charset so Safari stops guessing Latin-1."""
    if '<meta charset' in html:
        return html
    lead = ""
    if html.startswith("<!-- gt:"):
        lead, html = html.split("\n", 1)
        lead += "\n"
    if '<meta name="viewport"' not in html:
        html = '<meta name="viewport" content="width=device-width,initial-scale=1">\n' + html
    return lead + HEAD + html


def assign_series(html):
    """Apply SERIES_ASSIGN: swap or drop the band on each listed slide."""
    n = {"set": 0, "drop": 0, "duo": 0}
    html = re.sub(r"\n?/\* bands\.py \*/.*?/\* /bands\.py \*/", "", html, count=1, flags=re.S)
    html = html.replace("</style>", DUO_CSS + "</style>", 1)
    html = re.sub(r'\s*<div class="band duo[^"]*">.*?</div></div></div>', "", html, flags=re.S)  # previous run
    for sid, (lf, rf, cl, cr) in SERIES_DUO.items():
        m = re.search(r'<div class="slide[^"]*" id="%s">.*?(?=<div class="slide|\s*</div>\s*<script)' % sid, html, re.S)
        if not m:
            continue
        blk = m.group(0)
        blk = re.sub(r'\n?[ \t]*<div class="band[^"]*">.*?</div>\s*</div>(?=\s*<div class="(?:kick|quote|h|src|spacer|grid|row|foot|stat|k)|\s*<h|\s*<p|\s*<img)', "", blk, count=1, flags=re.S) if '<div class="band duo' in blk else re.sub(r'\n?[ \t]*<div class="band[^"]*">\s*<img[^>]*>\s*(?:<div class="c">.*?</div>\s*)?</div>', "", blk, count=1, flags=re.S)
        hdr = re.search(r'<div class="tophdr">.*?</div>\s*</div>', blk, re.S)
        if not hdr:
            continue
        blk = blk[:hdr.end()] + "\n  " + duo(lf, rf, cl, cr, extra="sm") + blk[hdr.end():]
        html = html[:m.start()] + blk + html[m.end():]
        n["duo"] += 1
    for sid, spec in SERIES_ASSIGN.items():
        if sid in SERIES_DUO:
            continue
        f, cap = spec[0], spec[1]
        extra = spec[2] if len(spec) > 2 else ""
        m = re.search(r'<div class="slide[^"]*" id="%s">.*?(?=<div class="slide|\s*</div>\s*<script)' % sid, html, re.S)
        if not m:
            continue
        blk = m.group(0)
        full = re.search(r'<img class="imgfull"[^>]*>', blk)
        if full:
            # a full-width image slide: swap its source, and drop any band a previous run added
            blk2 = re.sub(r'\n?[ \t]*<div class="band[^"]*">\s*<img[^>]*>\s*(?:<div class="c">.*?</div>\s*)?</div>', "", blk, count=1, flags=re.S)
            if (TOOLS / f).exists():
                blk2 = re.sub(r'(<img class="imgfull"[^>]*?src=")data:[^"]+(")', lambda mm: mm.group(1) + data_uri(TOOLS / f) + mm.group(2), blk2, count=1)
                n["set"] += 1
            html = html[:m.start()] + blk2 + html[m.end():]
            continue
        band = re.search(r'\n?[ \t]*<div class="band[^"]*">\s*<img[^>]*>\s*(?:<div class="c">.*?</div>\s*)?</div>', blk, re.S)
        if not band:
            # a band dropped on an earlier run comes back under the top header once its file exists
            if not (TOOLS / f).exists():
                continue
            hdr = re.search(r'<div class="tophdr">.*?</div>\s*</div>', blk, re.S)
            if not hdr:
                continue
            cls = spec[3] if len(spec) > 3 else "band cmk sm" + (f" {extra}" if extra else "")
            new = f'\n  <div class="{cls}"><img src="{data_uri(TOOLS / f)}" alt="{cap}"><div class="c">{cap}</div></div>'
            blk2 = blk[:hdr.end()] + new + blk[hdr.end():]
            html = html[:m.start()] + blk2 + html[m.end():]
            n["set"] += 1
            continue
        if (TOOLS / f).exists():
            new = re.sub(r'src="data:[^"]+"', f'src="{data_uri(TOOLS / f)}"', band.group(0), count=1)
            new = re.sub(r'<div class="c">.*?</div>', f'<div class="c">{cap}</div>', new, count=1, flags=re.S) if '<div class="c">' in new else new.replace("</div>", f'<div class="c">{cap}</div></div>')
            if extra and f' {extra}' not in new[:60]:
                new = new.replace('<div class="band', f'<div class="band {extra}', 1)
            if len(spec) > 3:
                new = re.sub(r'<div class="band[^"]*"', f'<div class="{spec[3]}"', new, count=1)
            n["set"] += 1
        else:
            new = ""
            n["drop"] += 1
        blk2 = blk[:band.start()] + new + blk[band.end():]
        html = html[:m.start()] + blk2 + html[m.end():]
    return html, n


BLANK = "data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="

def assign_brief(html):
    """Apply BRIEF_ASSIGN to the clip figures on the brief; mark sketch figures' source line."""
    n = {"set": 0, "hide": 0, "rm": 0}
    for lab, f in BRIEF_ASSIGN.items():
        m = re.search(r'<figure class="clip"[^>]*>(?:(?!</figure>).)*?<b>%s</b>.*?</figure>' % re.escape(lab), html, re.S)
        if not m:
            continue
        fig = m.group(0)
        if f is None:
            new = ""
            n["rm"] += 1
        elif (TOOLS / f).exists():
            new = re.sub(r'src="data:[^"]+"', f'src="{data_uri(TOOLS / f)}"', fig, count=1).replace(" hidden", "")
            n["set"] += 1
        else:
            new = re.sub(r'src="data:[^"]+"', f'src="{BLANK}"', fig, count=1)
            if " hidden" not in new[:40]:
                new = new.replace('<figure class="clip"', '<figure class="clip" hidden', 1)
            n["hide"] += 1
        html = html[:m.start()] + new + html[m.end():]
    return html, n


CREDITS_OLD = re.compile(r"Image credits: LiveWire ONE, S2 Del Mar and S4 Honcho photographs &copy; LiveWire Group, Inc\., from the company's own product pages; Dust Model_1 &copy; Dust Moto; Alta Redshift &copy; Alta Motors \(archived press image\)\. Honda Grom photographs &copy; American Honda, product and lifestyle imagery\. Reproduced here for editorial comment; confirm rights before any commercial distribution\.")
CREDITS_NEW = ("Image credits: the scene illustrations are charcoal sketches by William Weppner, drawn for this series. "
               "Product photographs on the price ladder: LiveWire ONE, S2 Del Mar and S4 Honcho &copy; LiveWire Group, Inc., from the company's own product pages; "
               "Dust Model_1 &copy; Dust Moto. Reproduced for editorial comment; confirm rights before any commercial distribution.")

def credits(html):
    return CREDITS_OLD.sub(CREDITS_NEW, html, count=1)


def mark_sketch_sources(html):
    """Clip figures that now hold a sketch say so on their source line instead of naming a photo."""
    sk = set()
    for f in IMG.glob("*.jpg"):
        sk.add(key(__import__("base64").b64encode(f.read_bytes()).decode()))
    def fix(m):
        fig = m.group(0)
        im = re.search(r'src="data:image/\w+;base64,([^"]+)"', fig)
        if not im or key(im.group(1)) not in sk:
            return fig
        return re.sub(r'(<div class="src"><b>[^<]*</b>)<span>[^<]*</span>', r'\1<span>Sketch</span>', fig, count=1)
    return re.sub(r'<figure class="clip"[^>]*>.*?</figure>', fix, html, flags=re.S)


def sitenav(html, series=False):
    """Practice-site links in the sticky header and the bar pinned to the bottom (idempotent)."""
    if ".sitenav{" not in html:
        html = html.replace("</style>", NAV_CSS + ("body.web .bottombar{display:block}.bottombar{display:none}" if series else "") + "</style>", 1)
    if 'class="sitenav"' not in html and not series:
        html = re.sub(r'(<header class="topbar">\s*<div class="wrap">\s*<div class="mark">.*?</div>)', lambda m: m.group(1) + "\n    " + nav_html(), html, count=1, flags=re.S)
    if 'class="bottombar"' not in html:
        if "</body>" in html:
            html = html.replace("</body>", bottombar_html() + "\n</body>", 1)
        elif '<script>document.body.classList.add("web");</script>' in html:
            html = html.replace('<script>document.body.classList.add("web");</script>', bottombar_html() + '\n<script>document.body.classList.add("web");</script>', 1)
        else:
            html = html.rstrip() + "\n" + bottombar_html() + "\n"
    return html


def embed_brief():
    full = D / "full" / "index.html"
    src = D / "index.html"
    html = full.read_text() if full.exists() and src.read_text().startswith("<!-- gt:public -->") else src.read_text()
    n = 0
    def repl(m):
        nonlocal n
        blk = m.group(0)
        t = re.search(r"class=[\"']t[\"']>(.*?)<", blk)
        if not t or t.group(1) not in SLOTS: return blk
        f, cap = SLOTS[t.group(1)]
        if not (IMG / f).exists(): return blk
        n += 1
        return f"<div class=\"part-img\"><img src=\"{data_uri(IMG / f)}\" alt=\"{cap}\"><div class=\"c\">{t.group(1)}</div></div>"
    # bare .phx blocks (inside .ph-grid) and .phx already wrapped in .part-img
    html = re.sub(r"<div class=[\"']part-img[\"']>\s*<div class=[\"']phx[\"']>.*?</div>\s*</div>\s*</div>", repl, html, flags=re.S)
    html = re.sub(r"<div class=[\"']phx[\"']>.*?<div class=[\"']s[\"']>.*?</div>\s*</div>", repl, html, flags=re.S)
    html, sw = swap(html)
    html, ba = assign_brief(html)
    html = credits(mark_sketch_sources(html))
    html, nb = blurbs.apply(html)
    html = logo_apply(skeleton(sitenav(html)))
    if full.exists():
        # write back as the raw full page, then split
        (D / "full" / "index.html").write_text("<!-- gt:full -->\n" + html if not html.startswith("<!-- gt:full -->") else html)
        # split_brief reads full/ when index.html is public; make sure index.html is marked public
        if not src.read_text().startswith("<!-- gt:public -->"):
            src.write_text(html)
    else:
        src.write_text(html)
    subprocess.run([sys.executable, str(ROOT / "tools" / "lib" / "split_brief.py"), "01"], check=True)
    print(f"brief: {n} placeholder(s) filled, {sw['img']} photo(s) swapped for sketches, {sw['logo']} logo(s) replaced; clips: {ba}")


def rebuild_cards():
    p = D / "series" / "index.html"
    s = p.read_text()
    s, sw = swap(s)
    s, sa = assign_series(s)
    s = skeleton(sitenav(s, series=True))
    print(f"series: {sw['img']} photo(s) swapped for sketches, {sw['logo']} logo(s) replaced; bands {sa}")
    s = re.sub(r"<div class=\"slide[^\"]*card[^\"]*\" id=\"(s\d-card|route-card)\">.*?</div>\n(?=\s*<div class=\"slide|\s*</div>\s*<script)", "", s, flags=re.S)
    if "body.web .slide.card" not in s:
        s = s.replace("</style>", CARD_CSS + "</style>", 1)
    def card(sid, n):
        return route_card(sid, n, kick=KICK, title="Four parts.<br>One thesis.",
                          dek="Five years in, one percent of plan. How a percentage led to the contracts, and the contracts to the loan.",
                          parts=PARTS, url=URL, issue=ISSUE, img=IMG / CARD_IMG[n], caption=CARD_CAP[n], quote='"')
    for n in range(4):
        cover_end = re.search(rf"<div class=\"slide[^\"]*\" id=\"s{n+1}-1\">.*?</div>\n(?=\s*<div class=\"slide)", s, re.S)
        s = s[:cover_end.end()] + card(f"s{n+1}-card", n) + s[cover_end.end():]
    s = s.replace("\n</div>\n<script>", "\n" + card("route-card", -1) + "</div>\n<script>", 1)
    s, nb = blurbs.apply(s)
    s = logo_apply(s)
    print(f"series: {nb} blurb(s)")
    p.write_text(s)
    print("series: 5 route cards rebuilt")


if __name__ == "__main__":
    embed_brief()
    rebuild_cards()
