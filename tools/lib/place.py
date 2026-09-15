#!/usr/bin/env python3
"""
Put sketches through the body of a brief and its carousel, beyond the one image per part the
builders place. Nos. 02 and 03 only (No. 01 is hand-built; tools/gt01/embed.py does the same job).

  python3 tools/lib/place.py 02      # after build_brief.py and build_series.py, before split/render

Every slot names a file under tools/; a file that does not exist yet leaves the slot empty, so
renders can land in any order. Rule: an image appears once per page. Idempotent.

Brief: a crop-marked strip (.gt-fig) under the lede of the numbered section.
Series: a band (.gt-band) under the top header of the slide; route cards get an image band in
place of their dek, as on the No. 02 cards.
"""
import re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "lib"))
from cards import data_uri, CARD_CSS  # noqa: E402
from bands import DUO_CSS, duo  # noqa: E402

TOOLS = ROOT / "tools"

PLACES = {
    "02": {
        "brief": {  # section number -> (file, caption)
            "02": ("gt02/img/gt02-07-dealer-closed.jpg", "Half the motorcycles, three-quarters of the dealers"),
            "04": ("gt02/img/gt02-08-loan-files.jpg", "The loan book, sold"),
            "06": ("gt02/img/gt02-09-handshake.jpg", "From equity backstop to senior secured creditor"),
            "07": ("gt02/img/gt02-10-clock.jpg", "Cash to May 2027"),
            "09": ("gt02/img/gt02-11-banner.jpg", "Hardwire, scored"),
            "10": ("gt02/img/gt02-12-investor-room.jpg", "$1.6 billion of buybacks"),
            "12": ("gt02/img/gt02-13-york-line.jpg", "2027, if it works"),
        },
        "series": {  # slide id -> (file, caption)
            "s1-2": ("gt02/img/gt02-14-call.jpg", "5 May 2026, the call"),
            "s1-6": ("gt02/img/gt02-07-dealer-closed.jpg", "Half the motorcycles"),
            "s2-3": ("gt02/img/gt02-08-loan-files.jpg", "What was sold"),
            "s3-4": ("gt02/img/gt02-09-handshake.jpg", "The seat change"),
            "s3-5": ("gt02/img/gt02-10-clock.jpg", "The clock"),
            "s4-5": ("gt02/img/gt02-11-banner.jpg", "Hardwire, promised vs delivered"),
            "s4-6": ("gt02/img/gt02-12-investor-room.jpg", "Capital returned"),
            "s4-7": ("gt02/img/gt02-05-883.jpg", "The bet"),
            "s4-8": ("gt02/img/gt02-13-york-line.jpg", "2027, if every target lands"),
        },
        "cards": {},  # No. 02's builder already puts images on its cards
        "duo": {  # slide id -> (left, right, caption, caption); product photos by bare name from tools/lib/products/
            "s3-3": ("s2.jpg", "honcho.jpg", "S2 Del Mar, $15,499", "S4 Honcho, $4,999: the subsidiary's lineup"),
        },
        "covers": {  # part cover -> (file, caption); charts come from tools/lib/figcap.py
            "s1-1": ("gt02/img/hero.jpg", "2026 guidance, added up"),
            "s2-1": ("gt02/img/fig-04.jpg", "HDFS operating income, $ millions: the cliff after the sale"),
            "s3-1": ("gt02/img/fig-05.jpg", "LiveWire\'s share of the drag on consolidated operating income"),
            "s4-1": ("gt02/img/fig-08.jpg", "Consolidated operating income, actual and on the plan, $ millions"),
        },
    },
    "03": {
        "brief": {
            "01": ("gt03/img/gt03-07-museum.jpg", "Sixteen moves, one table"),
            "03": ("gt03/img/gt03-08-mv.jpg", "MV Agusta, sold for a euro"),
            "05": ("gt03/img/gt03-09-stacyc-race.jpg", "StaCyc: thirty-three to one"),
            "06": ("gt03/img/gt03-10-engine.jpg", "Two engines kept"),
            "07": ("gt03/img/gt03-11-x440.jpg", "The Hero X440, the Sprint&rsquo;s engine"),
            "08": ("gt03/img/gt03-12-883.jpg", "The 883"),
            "09": ("gt03/img/gt03-13-frames.jpg", "Each CEO&rsquo;s purchases, the next CEO&rsquo;s focus story"),
        },
        "series": {
            "s1-3": ("gt03/img/gt03-11-x440.jpg", "The engine it does not own"),
            "s1-7": ("gt03/img/gt03-13-frames.jpg", "Same sentence, three CEOs"),
            "s2-4": ("gt03/img/gt03-08-mv.jpg", "MV Agusta, 2008"),
            "s3-10": ("gt02/img/gt02-02-hdfs-desk.jpg", "Eaglemark, 1993"),
            "s4-2": ("gt03/img/gt03-10-engine.jpg", "Built in-house"),
            "s4-4": ("gt03/img/gt03-01-varese.jpg", "Varese, 1961"),
            "s4-5": ("gt03/img/neemrana.jpg", "Neemrana, 2023"),
            "s4-7": ("gt03/img/gt03-12-883.jpg", "The 883, 2027"),
        },
        "cards": {
            "s1-card": ("gt03/img/gt03-07-museum.jpg", "Sixty-six years of outside moves"),
            "s2-card": ("gt03/img/gt03-02-easttroy.jpg", "East Troy, October 2009"),
            "s3-card": ("gt03/img/gt03-03-redshift-floor.jpg", "Brisbane, California, 2018"),
            "s4-card": ("gt03/img/fig-01.jpg", "What the outside moves cost to unwind, $ millions"),
            "route-card": ("gt03/img/gt03-06-juneau-dusk.jpg", "Juneau Avenue, Milwaukee"),
        },
        "duo": {
            "s1-8": ("stacyc.jpg", "gt03/img/gt03-09-stacyc-race.jpg", "StaCyc, from $799", "21,633 in 2025"),
            "s3-7": ("stacyc.jpg", "gt01/img/gt01-06-stacyc.jpg", "StaCyc, bought March 2019", "$14.9 million"),
        },
        "covers": {
            "s1-1": ("gt03/img/hero.jpg", "Sixty-six years of outside moves"),
            "s2-1": ("gt03/img/fig-02.jpg", "MV Agusta: what went in, what was written off, what was lost"),
            "s3-1": ("gt03/img/fig-04.jpg", "2025: thirty-three StaCycs for every LiveWire motorcycle"),
            "s4-1": ("gt03/img/gt03-04-bawal.jpg", "Bawal, 2014: built in-house, closed 2020"),
        },
    },
}

FIG_CSS = """
/* place.py */
.gt-fig{margin:26px 0 8px}
.gt-fig img{height:300px}
.gt-fig .c{font-size:10.5px}
/* /place.py */"""
BAND_CSS = """
/* place.py */
.gt-band{margin:0 0 28px}
.gt-band img{height:230px}
.gt-band.chart img{object-fit:contain;height:auto;max-height:440px;background:#0B0C0E}
.gt-band.cover img{height:330px}
.gt-band.chart .c{position:static;background:none;border-top:1px solid var(--drule);color:var(--dink3);padding:9px 12px 8px}
.slide.gt-cover h1{font-size:92px!important}
.slide.gt-cover .spacer:first-of-type{flex:0 0 12px}
.slide.card.img .rgrid .t{font-size:30px}
/* /place.py */"""


def q(s):
    """Match an attribute value in either quote style."""
    return r"[\"']" + s + r"[\"']"


def brief(n):
    d = ROOT / "site" / "groundtruth" / n
    src = d / "index.html"
    public = src.read_text().startswith("<!-- gt:public -->")
    target = d / "full" / "index.html" if public else src
    h = target.read_text()
    h = re.sub(r"\n?/\* place\.py \*/.*?/\* /place\.py \*/", "", h, count=1, flags=re.S)
    h = h.replace("</style>", FIG_CSS + "\n</style>", 1)
    h = re.sub(r'\s*<div class="part-img gt-fig"[^>]*>.*?</div></div>', "", h, flags=re.S)  # previous run
    n_set = 0
    for sec, (f, cap) in PLACES[n]["brief"].items():
        m = re.search(r"<div class=%s>%s &middot;" % (q("eyebrow"), sec), h)
        if not m or not (TOOLS / f).exists():
            continue
        lede = re.search(r"<p class=%s>.*?</p>" % q("lede"), h[m.end():], re.S)
        if not lede:
            continue
        at = m.end() + lede.end()
        fig = f'\n    <div class="part-img gt-fig"><img src="{data_uri(TOOLS / f)}" alt="{re.sub("&[a-z]+;", "", cap)}"><div class="c">{cap}</div></div>'
        h = h[:at] + fig + h[at:]
        n_set += 1
    target.write_text(h)
    if public:
        subprocess.run([sys.executable, str(ROOT / "tools" / "lib" / "split_brief.py"), n], check=True)
    print(f"{n} brief: {n_set} section figure(s) placed")


def series(n):
    p = ROOT / "site" / "groundtruth" / n / "series" / "index.html"
    s = p.read_text()
    s = re.sub(r"\n?/\* place\.py \*/.*?/\* /place\.py \*/", "", s, count=1, flags=re.S)
    if "body.web .slide.card" not in s:
        s = s.replace("</style>", CARD_CSS + "</style>", 1)
    s = re.sub(r"\n?/\* bands\.py \*/.*?/\* /bands\.py \*/", "", s, count=1, flags=re.S)
    s = s.replace("</style>", BAND_CSS + DUO_CSS + "\n</style>", 1)
    s = re.sub(r"\s*<div class=\"band duo[^\"]*\">.*?</div></div></div>", "", s, flags=re.S)
    s = re.sub(r"\s*<div class=[\"']band cmk gt-band[^\"']*[\"']>.*?</div></div>", "", s, flags=re.S)
    n_set = 0
    for sid, (f, cap) in PLACES[n]["series"].items():
        if not (TOOLS / f).exists():
            continue
        m = re.search(r"<div class=[\"']slide[^\"']*[\"'] id=%s>\s*<div class=%s>" % (q(sid), q("tophdr")), s, re.S)
        if not m:
            continue
        # the top header holds .mark and .tag; the band goes after its closing tag
        tag = re.search(r"<div class=%s>.*?</div>\s*</div>" % q("tag"), s[m.end():], re.S)
        if not tag:
            continue
        at = m.end() + tag.end()
        band = f'\n  <div class="band cmk gt-band"><img src="{data_uri(TOOLS / f)}" alt="{cap}"><div class="c">{cap}</div></div>'
        s = s[:at] + band + s[at:]
        n_set += 1
    n_duo = 0
    for sid, (lf, rf, cl, cr) in PLACES[n].get("duo", {}).items():
        m = re.search(r"<div class=[\"']slide[^\"']*[\"'] id=%s>\s*<div class=%s>" % (q(sid), q("tophdr")), s, re.S)
        if not m:
            continue
        tag = re.search(r"<div class=%s>.*?</div>\s*</div>" % q("tag"), s[m.end():], re.S)
        if not tag:
            continue
        at = m.end() + tag.end()
        s = s[:at] + "\n  " + duo(lf, rf, cl, cr) + s[at:]
        n_duo += 1
    n_cov = 0
    for sid, (f, cap) in PLACES[n].get("covers", {}).items():
        if not (TOOLS / f).exists():
            continue
        m = re.search(r"<div class=([\"'])(slide[^\"']*)\1 id=%s>(.*?)(?=<div class=[\"']slide|\s*</div>\s*<script)" % q(sid), s, re.S)
        if not m:
            continue
        blk = m.group(0)
        cls = m.group(2) if "gt-cover" in m.group(2) else m.group(2) + " gt-cover"
        blk = re.sub(r"<div class=([\"'])slide[^\"']*\1 id=", lambda mm: f"<div class={mm.group(1)}{cls}{mm.group(1)} id=", blk, count=1)
        kind = "chart" if ("fig-" in f or "hero" in f) else "cover"
        band = f'\n  <div class="band cmk gt-band {kind}"><img src="{data_uri(TOOLS / f)}" alt="{cap}"><div class="c">{cap}</div></div>'
        dek = re.search(r"</h1>\s*<p class=[\"']wide[\"'][^>]*>.*?</p>", blk, re.S)
        at = dek.end() if dek else blk.index("</h1>") + 5
        blk = blk[:at] + band + blk[at:]
        s = s[:m.start()] + blk + s[m.end():]
        n_cov += 1
    n_card = 0
    for sid, (f, cap) in PLACES[n]["cards"].items():
        if not (TOOLS / f).exists():
            continue
        m = re.search(r"<div class=([\"'])(slide[^\"']*card[^\"']*)\1 id=%s>(.*?)(?=<div class=[\"']slide|\s*</div>\s*<script)" % q(sid), s, re.S)
        if not m:
            continue
        blk = m.group(0)
        cls = m.group(2) if " img" in m.group(2) else m.group(2) + " img"
        blk = re.sub(r"<div class=([\"'])slide[^\"']*\1 id=", lambda mm: f"<div class={mm.group(1)}{cls}{mm.group(1)} id=", blk, count=1)
        body = m.group(3)
        # the dek paragraph after the h1 gives way to the band
        body2 = re.sub(r"(</h1>)\s*<p class=[\"']wide[\"'][^>]*>.*?</p>", r"\1", body, count=1, flags=re.S)
        body2 = re.sub(r"(</h1>)\s*<div class=[\"']band cmk gt-band[^\"']*[\"']>.*?</div></div>", r"\1", body2, count=1, flags=re.S)
        band = f'\n  <div class="band cmk gt-band cband"><img src="{data_uri(TOOLS / f)}" alt="{cap}"><div class="c">{cap}</div></div>'
        body2 = body2.replace("</h1>", "</h1>" + band, 1)
        blk = blk.replace(body, body2, 1)
        s = s[:m.start()] + blk + s[m.end():]
        n_card += 1
    p.write_text(s)
    print(f"{n} series: {n_set} band(s), {n_duo} duo(s), {n_cov} cover(s), {n_card} card image(s)")


if __name__ == "__main__":
    n = sys.argv[1]
    brief(n)
    series(n)
