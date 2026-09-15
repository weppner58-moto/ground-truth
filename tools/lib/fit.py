#!/usr/bin/env python3
"""
Keep every carousel slide inside its 1080 x 1350 box. Measures each slide in a browser and,
where the content runs past the bottom, adds a fit class that first shortens the image bands and
then scales the slide's content down a step at a time. Idempotent; run after placing images and
before render_slides.

  python3 tools/lib/fit.py 02
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEVELS = ["fit1", "fit2", "fit3", "fit4", "fit5"]
CSS = """
/* fit.py */
.slide.fit1 .band img,.slide.fit1 .gt-band img,.slide.fit1 .band.duo .cell img{height:180px}
.slide.fit1 .band.duo .cell.glyph{min-height:180px}
.slide.fit1 .band.duo .cell.glyph .g-big{font-size:72px}
.slide.fit1 .gt-band.chart img{max-height:300px}
.slide.fit1 .cband img,.slide.fit1 .slide.card.img .cband img{height:230px}
.slide.fit2 > *{zoom:.93}
.slide.fit2 .band img,.slide.fit2 .gt-band img,.slide.fit2 .band.duo .cell img{height:170px}
.slide.fit2 .band.duo .cell.glyph{min-height:170px}
.slide.fit2 .band.duo .cell.glyph .g-big{font-size:68px}
.slide.fit2 .gt-band.chart img{max-height:280px}
.slide.fit2 .cband img{height:210px}
.slide.fit3 > *{zoom:.87}
.slide.fit3 .band img,.slide.fit3 .gt-band img,.slide.fit3 .band.duo .cell img{height:160px}
.slide.fit3 .band.duo .cell.glyph{min-height:160px}
.slide.fit3 .band.duo .cell.glyph .g-big{font-size:64px}
.slide.fit3 .gt-band.chart img{max-height:260px}
.slide.fit3 .cband img{height:200px}
.slide.fit4 > *{zoom:.8}
.slide.fit4 .band img,.slide.fit4 .gt-band img,.slide.fit4 .band.duo .cell img{height:150px}
.slide.fit4 .band.duo .cell.glyph{min-height:150px}
.slide.fit4 .band.duo .cell.glyph .g-big{font-size:60px}
.slide.fit4 .gt-band.chart img{max-height:240px}
.slide.fit4 .cband img{height:190px}
.slide.fit5 > *{zoom:.72}
.slide.fit5 .band img,.slide.fit5 .gt-band img,.slide.fit5 .band.duo .cell img{height:140px}
.slide.fit5 .gt-band.chart img{max-height:220px}
.slide.fit5 .cband img{height:180px}
/* /fit.py */"""

MEASURE = """() => [...document.querySelectorAll('.slide')].map(s => {
    const r = s.getBoundingClientRect(); let maxb = 0;
    for (const el of s.querySelectorAll('*')) { const b = el.getBoundingClientRect().bottom - r.top; if (b > maxb) maxb = b; }
    return [s.id, Math.round(maxb)]; })"""


def main(n, limit=1350):
    from playwright.sync_api import sync_playwright
    page = ROOT / "site" / "groundtruth" / n / "series" / "index.html"
    h = page.read_text()
    h = re.sub(r"\n?/\* fit\.py \*/.*?/\* /fit\.py \*/", "", h, count=1, flags=re.S)
    h = re.sub(r"(<div class=[\"']slide[^\"']*?) fit\d([\"'])", r"\1\2", h)
    h = h.replace("</style>", CSS + "\n</style>", 1)
    page.write_text(h)
    levels = {}
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1400, "height": 1500})
        for _ in range(len(LEVELS) + 1):
            pg.goto(page.as_uri()); pg.wait_for_timeout(600)
            pg.evaluate("document.body.classList.remove('web')")
            pg.wait_for_timeout(150)
            over = [sid for sid, maxb in pg.evaluate(MEASURE) if maxb > limit]
            if not over:
                break
            changed = False
            for sid in over:
                cur = levels.get(sid, 0)
                if cur >= len(LEVELS):
                    continue
                levels[sid] = cur + 1
                changed = True
                h = page.read_text()
                h = re.sub(r"(<div class=[\"']slide[^\"']*?)( fit\d)?([\"'] id=[\"']%s[\"'])" % re.escape(sid),
                           lambda m: m.group(1) + " " + LEVELS[levels[sid] - 1] + m.group(3), h, count=1)
                page.write_text(h)
            if not changed:
                break
        b.close()
    print(n, "fit:", {k: LEVELS[v - 1] for k, v in levels.items()} or "all slides fit")


if __name__ == "__main__":
    main(sys.argv[1])
