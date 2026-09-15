#!/usr/bin/env python3
"""Report carousel slides whose content runs past the 1350 px slide: python3 tools/lib/overflow.py 02"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[2]
n = sys.argv[1]
page = ROOT / "site" / "groundtruth" / n / "series" / "index.html"
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1400, "height": 1500})
    pg.goto(page.as_uri()); pg.wait_for_timeout(800)
    pg.evaluate("document.body.classList.remove('web')")
    pg.wait_for_timeout(200)
    rows = pg.evaluate("""() => [...document.querySelectorAll('.slide')].map(s => {
        const r = s.getBoundingClientRect(); let maxb = 0;
        for (const el of s.querySelectorAll('*')) { const b = el.getBoundingClientRect().bottom - r.top; if (b > maxb) maxb = b; }
        return [s.id, Math.round(s.scrollHeight), Math.round(maxb)]; })""")
    bad = [r for r in rows if r[1] > 1352 or r[2] > 1352]
    print(n, "slides:", len(rows), "overflowing:", bad)
    b.close()
