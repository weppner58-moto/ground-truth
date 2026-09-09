# Ground Truth — Contact Patch Advisory

Primary-document research on the motorcycle industry.

**No. 03 — Harley-Davidson: Outside In** (Draft · Rev. 1)

- [The full brief](groundtruth/03/) — sixty-six years of buying what it could build; 14 sections, 4 figures, linked source index, open items, corrections log
- [The four-part series](groundtruth/03/series/) — 42 slides plus route cards
- Carousel PDFs — [Part 1](assets/GroundTruth-03_Part1_The-Record.pdf) · [Part 2](assets/GroundTruth-03_Part2_Same-Sentence.pdf) · [Part 3](assets/GroundTruth-03_Part3_Too-Small-to-Say.pdf) · [Part 4](assets/GroundTruth-03_Part4_The-Sprint-and-Final-Word.pdf) · [Route card](assets/GroundTruth-03_Card_The-Route.pdf)

**No. 02 — Harley-Davidson: Back to the Bricks, Down to Breakeven** (Rev. 2 draft)

- [The full brief](groundtruth/02/) — 16 sections in six parts, 8 figures, linked source index, open items and corrections log
- [The four-part series](groundtruth/02/series/) — 37 slides
- Carousel PDFs — [Part 1](assets/GroundTruth-02_Part1_The-Arithmetic.pdf) · [Part 2](assets/GroundTruth-02_Part2_The-Sale.pdf) · [Part 3](assets/GroundTruth-02_Part3_The-Subsidiary.pdf) · [Part 4](assets/GroundTruth-02_Part4_The-Bricks.pdf)

**No. 01 — LiveWire Group: The 386% Problem**

- [The full brief](groundtruth/01/) — 13 sections, 11 figures, linked source index, corrections log
- [The three-part series](groundtruth/01/series/) — 28 slides
- Carousel PDFs — [Part 1](assets/GroundTruth-01_Part1_The-Number.pdf) · [Part 2](assets/GroundTruth-01_Part2_The-Contracts.pdf) · [Part 3](assets/GroundTruth-01_Part3_The-Clock.pdf)

## Building an issue

```
python3 tools/gt03/build_brief.py                     # groundtruth/03/index.html
python3 tools/gt03/build_series.py                    # groundtruth/03/series/index.html
python3 tools/lib/render_slides.py groundtruth/03/series/index.html 03 \
  "1:The-Record" "2:Same-Sentence" "3:Too-Small-to-Say" "4:The-Sprint-and-Final-Word"   # PNGs + PDFs
python3 tools/gt03/calc.py                            # every derived figure, reproduced

No. 02 builds the same way from `tools/gt02/` (its chart/render helpers live in `tools/gt02/lib/`).
```

`tools/lib/` holds the house CSS (`brief.css`, `series.css`), the bio block, the chart emitters (`charts.py`), the slide renderer, and the local fonts used for rendering. Needs Playwright (Chromium), Pillow and img2pdf.

## Method

Figures come from filed financial statements or are computed from them, with the computation shown. Derived figures are labelled. Sourced analysis and judgment are kept in separate sections. Corrections are published in a dated log rather than made silently. No positions are held in any company covered.

Built against a complete local archive of both companies' SEC filings — 260 documents, reconciled against EDGAR.

---

William Weppner · Contact Patch Advisory · independent expert witness and litigation consultant, EV and powersports product liability.
