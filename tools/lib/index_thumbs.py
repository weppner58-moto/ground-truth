#!/usr/bin/env python3
"""
Thumbnails on the Ground Truth index: each issue shows its sketch and the chart from the top of
its brief page.

  python3 tools/lib/index_thumbs.py            # capture the hero charts, then rewrite the index
  python3 tools/lib/index_thumbs.py --no-capture

Capture: the .herofig-wrap on site/groundtruth/NN/index.html, dark scheme (the index is dark),
1200 px wide, saved to tools/gtNN/img/hero.jpg. Rewrite: the .issue-img block in each #noNN
section becomes a .issue-figs column with the sketch and the chart. Idempotent.
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "lib"))
from cards import data_uri  # noqa: E402
from logo import apply as logo_apply  # noqa: E402

INDEX = ROOT / "site" / "groundtruth" / "index.html"
SKETCH = {
    "01": ("gt01/img/gt01-04-tape.jpg", "LVWR on the tape."),
    "02": ("gt02/img/gt02-04-keynote.jpg", "Back to the Bricks, 5 May 2026."),
    "03": ("gt03/img/neemrana.jpg", "Neemrana, Rajasthan. The Sprint&rsquo;s engine."),
}
CHART = {
    "01": "What Harley said for 2026, and what LiveWire did.",
    "02": "2026 guidance, added up.",
    "03": "Sixty-six years of outside moves.",
}
CSS = """/* index-thumbs */
.issue-figs{display:grid;gap:14px}
.issue-img.chart img{aspect-ratio:1200/560;object-fit:cover}
.issue-img.chart::before,.issue-img.chart::after{border-color:var(--cyan)}
a.issue-img{display:block;text-decoration:none}
.issue-img.chart .c{position:static;background:none;border-top:1px solid var(--rule);color:var(--ink-3);padding:9px 12px 8px}
a.issue-img.chart:hover .c{color:var(--cyan)}
/* /index-thumbs */"""


def capture():
    from playwright.sync_api import sync_playwright
    from PIL import Image
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1240, "height": 1200}, color_scheme="dark", device_scale_factor=1)
        for n in SKETCH:
            pg.goto((ROOT / "site" / "groundtruth" / n / "index.html").as_uri())
            pg.wait_for_timeout(900)
            el = pg.query_selector(".herofig-wrap")
            out = ROOT / "tools" / f"gt{n}" / "img" / "hero.png"
            el.screenshot(path=str(out))
            im = Image.open(out).convert("RGB")
            im = im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS)
            im.save(out.with_suffix(".jpg"), "JPEG", quality=86, optimize=True)
            out.unlink()
            print(n, "hero", im.size, (out.with_suffix(".jpg")).stat().st_size, "B")
        b.close()


def rewrite():
    h = INDEX.read_text()
    h = re.sub(r"/\* index-thumbs \*/.*?/\* /index-thumbs \*/", "", h, count=1, flags=re.S)
    h = h.replace("</style>", CSS + "</style>", 1)
    for n, (f, cap) in SKETCH.items():
        i = h.index(f'id="no{n}"')
        j = h.index('<div class="issue-figs">', i) if '<div class="issue-figs">' in h[i:h.index('<div class="cards', i)] else h.index('<div class="issue-img">', i)
        k = h.index('<div class="cards', j)
        # the block runs to the end of the .issue grid: "...</div></div>\n  <div class="cards">"
        end = h.rindex("</div>", j, k)  # closes .issue
        hero = ROOT / "tools" / f"gt{n}" / "img" / "hero.jpg"
        sketch = ROOT / "tools" / f"gt{n}" / "img" / Path(f).name
        alt = re.sub(r"&\w+;", "'", cap)
        block = (f'<div class="issue-figs"><div class="issue-img"><img src="{data_uri(sketch)}" alt="{alt}"><div class="c">{cap}</div></div>'
                 + (f'<a class="issue-img chart" href="{n}/"><img src="{data_uri(hero)}" alt="{CHART[n]}"><div class="c">{CHART[n]} &rarr;</div></a>' if hero.exists() else "")
                 + "</div>")
        h = h[:j] + block + h[end:]
    h = logo_apply(h)
    INDEX.write_text(h)
    print("index rewritten", len(h), "B")


if __name__ == "__main__":
    if "--no-capture" not in sys.argv:
        capture()
    rewrite()
