# Contact Patch Advisory

The practice site (contactpatchadvisory.com) and Ground Truth, its primary-document research series on the motorcycle industry. `site/` is the deploy root on Cloudflare Pages; `site/groundtruth/` is the series.

**No. 03: Harley-Davidson: Outside In** (Draft · Rev. 1)

- [The full brief](site/groundtruth/03/: sixty-six years of buying what it could build; 14 sections, 4 figures, linked source index, open items, corrections log
- [The four-part series](site/groundtruth/03/series/: 42 slides plus route cards
- Carousel PDFs: [Part 1](site/groundtruth/assets/GroundTruth-03_Part1_The-Record.pdf) · [Part 2](site/groundtruth/assets/GroundTruth-03_Part2_Same-Sentence.pdf) · [Part 3](site/groundtruth/assets/GroundTruth-03_Part3_Too-Small-to-Say.pdf) · [Part 4](site/groundtruth/assets/GroundTruth-03_Part4_The-Sprint-and-Final-Word.pdf) · [Route card](site/groundtruth/assets/GroundTruth-03_Card_The-Route.pdf)

**No. 02: Harley-Davidson: Back to the Bricks, Down to Breakeven** (Rev. 2 draft)

- [The full brief](site/groundtruth/02/: 16 sections in six parts, 8 figures, linked source index, open items and corrections log
- [The four-part series](site/groundtruth/02/series/: 37 slides
- Carousel PDFs: [Part 1](site/groundtruth/assets/GroundTruth-02_Part1_The-Arithmetic.pdf) · [Part 2](site/groundtruth/assets/GroundTruth-02_Part2_The-Sale.pdf) · [Part 3](site/groundtruth/assets/GroundTruth-02_Part3_The-Subsidiary.pdf) · [Part 4](site/groundtruth/assets/GroundTruth-02_Part4_The-Bricks.pdf)

**No. 01: LiveWire Group: The 386% Problem**

- [The full brief](site/groundtruth/01/: 13 sections, 11 figures, linked source index, corrections log
- [The three-part series](site/groundtruth/01/series/: 28 slides
- Carousel PDFs: [Part 1](site/groundtruth/assets/GroundTruth-01_Part1_The-Number.pdf) · [Part 2](site/groundtruth/assets/GroundTruth-01_Part2_The-Contracts.pdf) · [Part 3](site/groundtruth/assets/GroundTruth-01_Part3_The-Clock.pdf)

## Building the practice site

```
python3 build.py        # site.tpl.html + posts/*.py -> site/index.html, site/news/, sitemap, feed
```

## Building an issue

```
python3 tools/gt03/build_brief.py                     # site/groundtruth/03/index.html
python3 tools/gt03/build_series.py                    # site/groundtruth/03/series/index.html
python3 tools/lib/render_slides.py site/groundtruth/03/series/index.html 03 \
  "1:The-Record" "2:Same-Sentence" "3:Too-Small-to-Say" "4:The-Sprint-and-Final-Word"   # PNGs + PDFs
python3 tools/gt03/calc.py                            # every derived figure, reproduced
python3 tools/lib/split_brief.py 03                   # public page + full/ (registered readers); safe to re-run
python3 tools/lib/render_brief_pdf.py 03              # site/groundtruth/assets/GroundTruth-03_Full-Brief.pdf

No. 02 builds the same way from `tools/gt02/` (its chart/render helpers live in `tools/gt02/lib/`).
No. 01 is hand-built: `python3 tools/gt01/embed.py` embeds the images in `tools/gt01/img/` and rebuilds its route cards
(from `tools/lib/cards.py`), then render_slides with "1:The-Growth" "2:The-Lineup" "3:The-Contracts" "4:The-Loan-and-Final-Word".
```

`tools/lib/` holds the house CSS (`brief.css`, `series.css`), the bio block, the chart emitters (`charts.py`), the slide renderer, and the local fonts used for rendering. Needs Playwright (Chromium), Pillow and img2pdf.

## Deploying

Cloudflare Pages, Git-connected to this repo, build output `site/`, no build command (built output is committed).
Custom domain: contactpatchadvisory.com. The registration gate is in `functions/` and needs these project settings:

| Setting | Type | Purpose |
|---|---|---|
| `GT_LIST` | KV namespace binding | one record per registered email |
| `GATE_SECRET` | secret | signs the reader cookie (`gt_reader`, one year, `/groundtruth` only) |
| `ADMIN_TOKEN` | secret | `curl -H "Authorization: Bearer $ADMIN_TOKEN" https://contactpatchadvisory.com/groundtruth/registrations` returns the list as CSV |
| `TURNSTILE_SITEKEY`, `TURNSTILE_SECRET` | plain text, secret | optional bot check on the form |
| `NOTIFY` + `NOTIFY_TO` | send_email binding, plain text | optional email to you on each registration (needs Email Routing on the zone) |

Without `GATE_SECRET` nothing is gated, so a preview deploy serves the whole site. Gated paths: `/groundtruth/NN/full/` (the complete brief) and `/groundtruth/assets/GroundTruth-NN_Full-Brief.pdf`. The public page of each issue is the hero, Start here and section 01, then the register panel; the series pages and carousel PDFs stay open.
Short links `/01`, `/02`, `/03`, `/gt` and the old GitHub Pages paths are in `site/_redirects`.

Local run: `wrangler pages dev site --kv GT_LIST --binding GATE_SECRET=x --binding ADMIN_TOKEN=y`.

## Method

Figures come from filed financial statements or are computed from them, with the computation shown. Derived figures are labelled. Sourced analysis and judgment are kept in separate sections. Corrections are published in a dated log rather than made silently. No positions are held in any company covered.

Built against a complete local archive of both companies' SEC filings: 260 documents, reconciled against EDGAR.

---

William Weppner · Contact Patch Advisory · independent expert witness and litigation consultant, EV and powersports product liability.
