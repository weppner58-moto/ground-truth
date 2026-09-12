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
}
# Logos come off the page and become text pills (the page already has .brand-txt).
LOGOS = {
    "1ae5ce73": "LIVEWIRE GROUP &middot; NYSE: LVWR",
    "dd999ff3": "HARLEY-DAVIDSON, INC. &middot; NYSE: HOG",
    "53c5914d": "ALTA MOTORS",
}
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
        if f and (IMG / f).exists():
            n["img"] += 1
            return re.sub(r'src="data:[^"]+"', f'src="{data_uri(IMG / f)}"', tag, count=1)
        return tag
    html = re.sub(r'<img[^>]*src="data:image/(\w+);base64,([^"]+)"[^>]*>', repl, html)
    # the Alta logo clip figure in §05 goes entirely once the Redshift sketch is in
    if (IMG / "gt01-09-redshift.jpg").exists():
        html, c = re.subn(r'<figure class="clip"[^>]*><span class="cm"></span><img [^>]*alt="Alta Motors logo"[^>]*>.*?</figure>', "", html, count=1, flags=re.S)
        n["logo"] += c
    return html, n


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
    html = sitenav(html)
    if full.exists():
        # write back as the raw full page, then split
        (D / "full" / "index.html").write_text("<!-- gt:full -->\n" + html if not html.startswith("<!-- gt:full -->") else html)
        # split_brief reads full/ when index.html is public; make sure index.html is marked public
        if not src.read_text().startswith("<!-- gt:public -->"):
            src.write_text(html)
    else:
        src.write_text(html)
    subprocess.run([sys.executable, str(ROOT / "tools" / "lib" / "split_brief.py"), "01"], check=True)
    print(f"brief: {n} placeholder(s) filled, {sw['img']} photo(s) swapped for sketches, {sw['logo']} logo(s) replaced")


def rebuild_cards():
    p = D / "series" / "index.html"
    s = p.read_text()
    s, sw = swap(s)
    s = sitenav(s, series=True)
    print(f"series: {sw['img']} photo(s) swapped for sketches, {sw['logo']} logo(s) replaced")
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
    p.write_text(s)
    print("series: 5 route cards rebuilt")


if __name__ == "__main__":
    embed_brief()
    rebuild_cards()
