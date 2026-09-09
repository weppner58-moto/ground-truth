#!/usr/bin/env python3
"""Render a Ground Truth series page to carousel PDFs and route-card PDFs.

Usage (from repo root):
  python3 tools/lib/render_slides.py groundtruth/02/series/index.html 02 \
      "1:The-Arithmetic" "2:The-Sale" "3:The-Subsidiary" "4:The-Bricks"

Each ".slide" in DOM order is screenshotted at 1080x1350 (device scale 1) with body.web removed,
so cards (hidden on the web view) render. Slides are grouped by id prefix "s<part>-". A slide whose
id ends in "-card" is the route card: it becomes page 2 of that part's carousel PDF and its own
GroundTruth-NN_Card_PartN_<Name>.pdf. A slide with id "route-card" becomes GroundTruth-NN_Card_The-Route.pdf.
PDF page size is 1080x1350 px at 150 dpi = 518.4 x 648 pt, matching No. 01.

Fonts: tools/lib/fonts-local.css is injected so renders do not depend on Google Fonts being reachable.
Requires: playwright (python) with chromium, img2pdf.
"""
import asyncio, os, sys, re, io
import img2pdf
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LIB = os.path.join(ROOT, "tools", "lib")
ASSETS = os.path.join(ROOT, "assets")


async def shoot(html_path, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    font_css = open(os.path.join(LIB, "fonts-local.css")).read().replace("url('fonts/", "url('file://%s/fonts/" % LIB)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1180, "height": 1450}, device_scale_factor=1)
        await pg.goto("file://" + os.path.abspath(html_path))
        await pg.add_style_tag(content=font_css)
        await pg.evaluate("document.body.classList.remove('web')")
        await pg.evaluate("document.fonts.ready")
        await pg.wait_for_timeout(1200)
        ids = await pg.evaluate("Array.from(document.querySelectorAll('.slide')).map(e=>e.id)")
        shots = []
        for sid in ids:
            el = await pg.query_selector("#" + sid)
            path = os.path.join(out_dir, sid + ".png")
            await el.screenshot(path=path)
            shots.append((sid, path))
        await b.close()
    return shots


def to_pdf(png_paths, out_path):
    layout = img2pdf.get_layout_fun((img2pdf.in_to_pt(1080 / 150), img2pdf.in_to_pt(1350 / 150)))
    with open(out_path, "wb") as f:
        f.write(img2pdf.convert(png_paths, layout_fun=layout))


def main():
    html_path, issue, *parts = sys.argv[1:]
    out_dir = os.path.join(ROOT, "build", "slides-%s" % issue)
    shots = asyncio.run(shoot(html_path, out_dir))
    os.makedirs(ASSETS, exist_ok=True)
    by_part = {}
    route_card = None
    for sid, path in shots:
        if sid == "route-card":
            route_card = path
            continue
        m = re.match(r"s(\d+)-", sid)
        if not m:
            continue
        by_part.setdefault(m.group(1), []).append((sid, path))
    for spec in parts:
        num, name = spec.split(":", 1)
        slides = by_part.get(num, [])
        cover = [p for s, p in slides if s == f"s{num}-1"]
        card = [p for s, p in slides if s.endswith("-card")]
        rest = [p for s, p in slides if s != f"s{num}-1" and not s.endswith("-card")]
        pages = cover + card + rest
        out = os.path.join(ASSETS, f"GroundTruth-{issue}_Part{num}_{name}.pdf")
        to_pdf(pages, out)
        print(out, len(pages), "pages")
        if card:
            outc = os.path.join(ASSETS, f"GroundTruth-{issue}_Card_Part{num}_{name}.pdf")
            to_pdf(card, outc)
            print(outc)
    if route_card:
        outr = os.path.join(ASSETS, f"GroundTruth-{issue}_Card_The-Route.pdf")
        to_pdf([route_card], outr)
        print(outr)


if __name__ == "__main__":
    main()
