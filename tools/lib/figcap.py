#!/usr/bin/env python3
"""
Capture a brief's charts as images for the carousel covers: the hero chart and every FIG NN.

  python3 tools/lib/figcap.py 02      -> tools/gt02/img/hero.jpg, fig-01.jpg, fig-02.jpg ...

Dark scheme (the slides are dark), 1200 px wide, JPEG q86. Run after build_brief.py.
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main(n):
    from playwright.sync_api import sync_playwright
    from PIL import Image
    page = ROOT / "site" / "groundtruth" / n / "full" / "index.html"
    if not page.exists():
        page = ROOT / "site" / "groundtruth" / n / "index.html"
    out = ROOT / "tools" / f"gt{n}" / "img"
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1240, "height": 1400}, color_scheme="dark", device_scale_factor=1)
        pg.goto(page.as_uri())
        pg.wait_for_timeout(900)
        targets = [("hero", ".herofig-wrap")]
        for i, el in enumerate(pg.query_selector_all("figure")):
            t = el.query_selector(".fig-n")
            if t:
                num = re.sub(r"\D", "", t.inner_text())
                el.evaluate(f"el => el.setAttribute('data-figcap', 'fig-{num}')")
                targets.append((f"fig-{num}", f"figure[data-figcap='fig-{num}']"))
        for name, sel in targets:
            el = pg.query_selector(sel)
            if not el:
                continue
            if name != "hero":
                el = el.query_selector("svg") or el  # the chart alone; the head and note are too small at band size
            png = out / f"{name}.png"
            el.screenshot(path=str(png))
            im = Image.open(png).convert("RGB")
            im = im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS)
            im.save(png.with_suffix(".jpg"), "JPEG", quality=86, optimize=True)
            png.unlink()
            print(n, name, im.size)
        b.close()


if __name__ == "__main__":
    main(sys.argv[1])
