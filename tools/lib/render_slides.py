#!/usr/bin/env python3
"""Render a Ground Truth series page to 1080x1350 PNGs and pack the carousel PDFs.

Usage:
  python3 tools/lib/render_slides.py groundtruth/NN/series/index.html NN "1:The-Name" "2:The-Name" ...

For each part N: assets/GroundTruth-NN_PartN_<Name>.pdf = cover (sN-1) + route card (sN-card) + slides.
Each route card also ships alone as assets/GroundTruth-NN_Card_PartN_<Name>.pdf, and the stand-alone
route card (id route-card) as assets/GroundTruth-NN_Card_The-Route.pdf.
PNGs land in build/slides-NN/ (gitignored). 150 dpi → 518.4 × 648 pt, matching No. 01.
"""
import os, re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]


def main():
    html_path, nn, parts = Path(sys.argv[1]), sys.argv[2], sys.argv[3:]
    names = dict(p.split(":", 1) for p in parts)
    out = ROOT / "build" / f"slides-{nn}"
    out.mkdir(parents=True, exist_ok=True)
    assets = ROOT / "site" / "groundtruth" / "assets"
    assets.mkdir(exist_ok=True)

    html = html_path.read_text()
    fonts_css = (ROOT / "tools/lib/fonts-local.css").read_text()
    fonts_css = fonts_css.replace("url('fonts/", f"url('file://{ROOT}/tools/lib/fonts/")
    html = html.replace('<body class="web">', "<body>").replace("<body class='web'>", "<body>")
    html = html.replace('<script>document.body.classList.add("web");</script>', "")  # No. 01 adds it by script
    html = re.sub(r'<link[^>]+fonts\.googleapis[^>]*>', "", html)
    html = html.replace("</head>", f"<style>{fonts_css}</style></head>", 1)
    tmp = out / "_render.html"
    tmp.write_text(html)

    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1240, "height": 1500}, device_scale_factor=1)
        pg.goto(tmp.as_uri())
        pg.wait_for_timeout(600)
        pg.evaluate("document.body.classList.remove('web')")
        pg.evaluate("document.fonts && document.fonts.ready")
        pg.wait_for_timeout(400)
        ids = pg.evaluate("Array.from(document.querySelectorAll('.slide')).map(e=>e.id)")
        for sid in ids:
            el = pg.query_selector(f"#{sid}")
            el.scroll_into_view_if_needed()
            el.screenshot(path=str(out / f"{sid}.png"))
        b.close()

    def pdf(png_ids, name):
        imgs = [Image.open(out / f"{i}.png").convert("RGB") for i in png_ids]
        for k, im in enumerate(imgs):
            if im.size != (1080, 1350):
                imgs[k] = im.crop((0, 0, 1080, 1350)) if im.size[0] >= 1080 and im.size[1] >= 1350 else im.resize((1080, 1350))
        # 150 dpi → 518.4 × 648 pt, matching No. 01. PNG pages (lossless), via img2pdf.
        import io, img2pdf
        pages = []
        for im in imgs:
            buf = io.BytesIO(); im.save(buf, format="PNG"); pages.append(buf.getvalue())
        (assets / name).write_bytes(img2pdf.convert(pages, layout_fun=img2pdf.get_fixed_dpi_layout_fun((150, 150))))
        print("wrote", name, len(imgs), "pages")

    for n, name in names.items():
        slides = [i for i in ids if re.fullmatch(rf"s{n}-\d+", i)]
        slides.sort(key=lambda s: int(s.split("-")[1]))
        card = f"s{n}-card"
        seq = [slides[0]] + ([card] if card in ids else []) + slides[1:]
        pdf(seq, f"GroundTruth-{nn}_Part{n}_{name}.pdf")
        if card in ids:
            pdf([card], f"GroundTruth-{nn}_Card_Part{n}_{name}.pdf")
    if "route-card" in ids:
        pdf(["route-card"], f"GroundTruth-{nn}_Card_The-Route.pdf")
    print("PNGs in", out)


if __name__ == "__main__":
    main()
