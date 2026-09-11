#!/usr/bin/env python3
"""Render the registered-readers page of an issue to a PDF.

  python3 tools/lib/render_brief_pdf.py 03      -> site/groundtruth/assets/GroundTruth-03_Full-Brief.pdf
"""
import asyncio, re, sys, tempfile
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[2]

PRINT_CSS = """
@page { size: Letter; margin: 14mm 12mm 16mm 12mm; }
html { font-size: 13.5px; }
body::before { display: none !important; }
.full-bar, .gate { display: none !important; }
section { break-inside: auto; }
h2, h3, .eyebrow { break-after: avoid; }
figure, table, .part-img, .callout, .sowhat, .note { break-inside: avoid; }
a { color: inherit; text-decoration: none; }
a[href^="http"]::after { content: ""; }
.wrap { max-width: none; padding-inline: 0; }
"""

async def main(n):
    src = ROOT / "site" / "groundtruth" / n / "full" / "index.html"
    out = ROOT / "site" / "groundtruth" / "assets" / f"GroundTruth-{n}_Full-Brief.pdf"
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1000, "height": 1300})
        await pg.emulate_media(media="print", color_scheme="light")
        # local fonts, so the render does not depend on Google Fonts being reachable
        html = src.read_text()
        fonts_css = (ROOT / "tools/lib/fonts-local.css").read_text().replace("url('fonts/", f"url('file://{ROOT}/tools/lib/fonts/")
        html = re.sub(r"<link[^>]+fonts\.googleapis[^>]*>", "", html).replace("</head>", f"<style>{fonts_css}</style></head>", 1)
        tmp = src.with_name("_print.html"); tmp.write_text(html)
        await pg.goto(tmp.as_uri()); await pg.wait_for_timeout(1500)
        await pg.evaluate("document.fonts && document.fonts.ready")
        await pg.add_style_tag(content=PRINT_CSS)
        await pg.wait_for_timeout(300)
        await pg.pdf(path=str(out), format="Letter", print_background=True, prefer_css_page_size=True,
                     display_header_footer=True,
                     header_template="<div></div>",
                     footer_template=f"<div style='font-family:IBM Plex Mono,Menlo,monospace;font-size:7.5px;letter-spacing:.1em;text-transform:uppercase;color:#7C8189;width:100%;padding:0 12mm;display:flex;justify-content:space-between'><span>Contact Patch Advisory &middot; Ground Truth No. {n} &middot; contactpatchadvisory.com/groundtruth/{n}/</span><span><span class='pageNumber'></span> / <span class='totalPages'></span></span></div>")
        await b.close()
    tmp.unlink(missing_ok=True)
    print(out, f"{out.stat().st_size:,} B")

asyncio.run(main(sys.argv[1]))
