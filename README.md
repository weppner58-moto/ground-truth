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

A Cloudflare Worker with static assets, Git-connected to this repo: every push to `main` runs `npx wrangler deploy`.
`wrangler.toml` points the Worker at `src/index.js` and the assets at `site/`; the Worker runs first for
`/groundtruth/*` and serves everything else straight from `site/`. Custom domain: contactpatchadvisory.com
(Worker > Settings > Domains & Routes).

| Setting | Where | Purpose |
|---|---|---|
| `GT_LIST` | KV namespace, id in `wrangler.toml` | one record per registered email |
| `GATE_SECRET` | secret, Worker > Settings > Variables and secrets | signs the reader cookie (`gt_reader`, one year, `/groundtruth` only) |
| `ADMIN_TOKEN` | secret | `curl -H "Authorization: Bearer $ADMIN_TOKEN" https://contactpatchadvisory.com/groundtruth/registrations` returns the list as CSV |
| `TURNSTILE_SITEKEY`, `TURNSTILE_SECRET` | variable, secret | optional bot check on the form |
| `NOTIFY` + `NOTIFY_TO` | send_email binding, variable | optional email to you on each registration (needs Email Routing on the zone) |

Without `GATE_SECRET` nothing is gated. Gated paths: `/groundtruth/NN/full/` (the complete brief) and
`/groundtruth/assets/GroundTruth-NN_Full-Brief.pdf`. The public page of each issue is the hero, Start here and
section 01, then the register panel; the series pages and carousel PDFs stay open. Short links `/01`, `/02`,
`/03`, `/gt` and the old GitHub Pages paths are in `site/_redirects`.

Local run: `wrangler dev --var GATE_SECRET:x --var ADMIN_TOKEN:y`.

GitHub Pages (weppner58-moto.github.io/ground-truth) serves the `gh-pages` branch, which is the `site/` tree
(`git subtree split --prefix=site -b gh-pages`), no gate. Once the Cloudflare domain is live that branch goes
back to redirect stubs.

## Method

Figures come from filed financial statements or are computed from them, with the computation shown. Derived figures are labelled. Sourced analysis and judgment are kept in separate sections. Corrections are published in a dated log rather than made silently. No positions are held in any company covered.

Built against a complete local archive of both companies' SEC filings: 260 documents, reconciled against EDGAR.

---

William Weppner · Contact Patch Advisory · independent expert witness and litigation consultant, EV and powersports product liability.

No. 02 images: drop renders into `tools/gt02/img/` as `gt02-01-juneau.jpg`, `gt02-02-hdfs-desk.jpg`, `gt02-03-delmar-floor.jpg`, `gt02-04-keynote.jpg`, `gt02-05-883.jpg`, `gt02-06-bricks.jpg` (1200 wide, q80). `build_brief.py` puts each on its part when the file exists; `build_series.py` puts them on the route cards. Then `split_brief.py 02`, render_slides with "1:The-Arithmetic" "2:The-Sale" "3:The-Subsidiary" "4:The-Bricks", and `render_brief_pdf.py 02`.

Index thumbnails: `python3 tools/lib/index_thumbs.py` captures each brief's hero chart (dark, 1200 wide) to `tools/gtNN/img/hero.jpg` and rewrites the index so every issue shows its sketch and its chart. Run it after any hero chart changes.

Sketches through the body of Nos. 02 and 03: `python3 tools/lib/place.py NN` after the builders and before render. Slots are listed in the file (section number or slide id -> file, caption); a missing file leaves the slot empty. Unfilled part images are hidden, not shown as placeholder boxes.

Charts as images: `python3 tools/lib/figcap.py NN` captures the hero chart and every FIG of a brief (dark, 1200 wide) into `tools/gtNN/img/`; place.py puts them on the part covers. Re-run after a chart changes.

Product photos: `tools/lib/products/` (one, s2, honcho, lineup, stacyc). `tools/lib/bands.py` gives the two-up band (product beside sketch); slots are `SERIES_DUO` in `tools/gt01/embed.py` and the `duo` tables in `tools/lib/place.py`. Product photos may repeat across slides; sketches stay once per page.

Build order for a carousel: builder (or `tools/gt01/embed.py`) -> `tools/lib/place.py NN` (Nos. 02, 03) -> `tools/lib/fit.py NN` (shrinks bands, then content, on any slide that runs past 1350 px) -> `tools/lib/render_slides.py`. `tools/lib/blurbs.py` holds the one-line captions under every picture, keyed by file name; both pipelines apply it.

Gate, one URL per issue: `/groundtruth/NN/` serves the whole brief to a browser with the reader cookie and the public page (opening sections plus the register panel) to everyone else; `/NN/full/` redirects there. The full-brief PDF needs the cookie; part PDFs and route cards are open. `GATE_KEY` in wrangler.toml signs the cookie until `tools/setup-gate.sh` (run once on the Mac) creates the KV list and sets `GATE_SECRET` and `ADMIN_TOKEN`; the list is then at `/groundtruth/registrations?token=<ADMIN_TOKEN>` as CSV.

Logo: `tools/site/img/logo-*.png`; `tools/lib/logo.py` swaps it into every `.mark` (practice site, index, briefs, slides, cards); `src/logo.js` carries it for the register page.
