#!/usr/bin/env python3
"""
pull_edgar.py — Ground Truth primary-document puller.

Downloads SEC EDGAR filings for the Ground Truth companies (Harley-Davidson,
LiveWire by default), keeps the raw HTML, and writes a plain-text version of
every document so the corpus can go into the Claude project library.

Default pull, per company, from --since onward:
  10-K, 10-Q            primary document
  8-K                   only filings that carry Item 2.02 (Results of Operations,
                        i.e. the quarterly earnings release) unless --all-8k;
                        for those, every EX-99.* exhibit (press release, slides)
  DEF 14A               proxy (comp, board) — optional via --forms

Output tree (under --out, default data/edgar):
  raw/<TICKER>/<date>_<form>_<accession>/<file>      as filed
  text/<TICKER>/<date>_<form>_<accession>__<file>.txt plain text
  manifest.csv                                        one row per document with sizes + URL
  SIZE_REPORT.txt                                     totals

Usage:
  python3 tools/edgar/pull_edgar.py                       # HOG + LVWR since 2019-01-01
  python3 tools/edgar/pull_edgar.py --since 2021-01-01 --companies HOG LVWR PII
  python3 tools/edgar/pull_edgar.py --forms 10-K 10-Q 8-K "DEF 14A"
  python3 tools/edgar/pull_edgar.py --dry-run             # list + size estimate, no download

Requires: requests, beautifulsoup4 (pip3 install requests beautifulsoup4).
SEC fair-access rules: declared User-Agent, <= 10 requests/sec. Both handled here.
Re-runs are incremental: existing raw files are not re-fetched.
"""
import argparse
import csv
import json
import os
import re
import sys
import time
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit("pip3 install requests beautifulsoup4")

UA = "Contact Patch Advisory research tool weppner58@gmail.com"
HEADERS = {"User-Agent": UA, "Accept-Encoding": "gzip, deflate"}

# ticker -> (CIK, label). Add rows here to widen the series.
COMPANIES = {
    "HOG":  (793952,  "Harley-Davidson, Inc."),
    "LVWR": (1898795, "LiveWire Group, Inc."),
    "PII":  (931015,  "Polaris Inc."),
}

DEFAULT_FORMS = ["10-K", "10-Q", "8-K"]
MIN_INTERVAL = 0.12  # seconds between requests (~8/s, under the SEC's 10/s cap)

_last = [0.0]


def get(url, retries=7):
    for attempt in range(retries):
        wait = MIN_INTERVAL - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        r = requests.get(url, headers=HEADERS, timeout=60)
        _last[0] = time.time()
        if r.status_code == 200:
            return r
        if r.status_code in (403, 429, 503):
            pause = 5 * 2 ** attempt  # 5, 10, 20, 40, 80, 160, 320 s — SEC throttles bursts
            print(f"   ... {r.status_code} from SEC, backing off {pause}s")
            time.sleep(pause)
            continue
        r.raise_for_status()
    raise RuntimeError(f"gave up on {url} (last status {r.status_code})")


def submissions(cik):
    """All filings for a CIK: the recent block plus any paged older blocks."""
    base = get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json").json()
    blocks = [base["filings"]["recent"]]
    for f in base["filings"].get("files", []):
        blocks.append(get(f"https://data.sec.gov/submissions/{f['name']}").json())
    rows = []
    for b in blocks:
        keys = list(b.keys())
        for i in range(len(b["accessionNumber"])):
            rows.append({k: b[k][i] for k in keys})
    return base.get("name", str(cik)), rows


def filing_index(cik, acc, cache_dir):
    acc_nodash = acc.replace("-", "")
    cache = cache_dir / f"{acc_nodash}.json"
    if cache.exists():
        j = json.loads(cache.read_text())
    else:
        url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc_nodash}/index.json"
        j = get(url).json()
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps(j))
    return acc_nodash, [it["name"] for it in j["directory"]["item"]]


def html_to_text(html_bytes):
    soup = BeautifulSoup(html_bytes, "html.parser")
    # iXBRL hidden header and boilerplate
    for t in soup(["script", "style", "head", "title"]):
        t.decompose()
    for t in soup.find_all(attrs={"style": re.compile(r"display\s*:\s*none", re.I)}):
        t.decompose()
    for t in soup.find_all(["ix:header", "ix:hidden"]):
        t.decompose()
    # keep table structure readable
    for td in soup.find_all(["td", "th"]):
        td.append(" | ")
    for br in soup.find_all(["br", "p", "div", "tr", "li", "h1", "h2", "h3", "h4"]):
        br.append("\n")
    text = soup.get_text()
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"( \| )+\n", "\n", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text.strip() + "\n"


def wanted_docs(form, names, all_8k):
    """Pick which files in a filing directory to keep."""
    keep = []
    for n in names:
        low = n.lower()
        if not low.endswith((".htm", ".html", ".txt", ".pdf")):
            continue
        if low.endswith("-index.htm") or low.endswith("-index.html"):
            continue
        if low.startswith("r") and re.fullmatch(r"r\d+\.htm", low):
            continue  # XBRL viewer pages
        if form.startswith("8-K"):
            if re.search(r"ex[-_]?99", low) or low.startswith("d") or "8k" in low or "8-k" in low:
                keep.append(n)
        else:
            keep.append(n)
    return keep


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--companies", nargs="+", default=["HOG", "LVWR"], help=f"tickers from {list(COMPANIES)}")
    ap.add_argument("--forms", nargs="+", default=DEFAULT_FORMS)
    ap.add_argument("--since", default="2019-01-01", help="earliest filing date, YYYY-MM-DD")
    ap.add_argument("--until", default="2099-12-31")
    ap.add_argument("--out", default="data/edgar")
    ap.add_argument("--all-8k", action="store_true", help="keep every 8-K, not just Item 2.02 earnings releases")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    out = Path(args.out)
    raw_root, text_root = out / "raw", out / "text"
    manifest_path = out / "manifest.csv"
    out.mkdir(parents=True, exist_ok=True)

    rows_out = []
    for tk in args.companies:
        if tk not in COMPANIES:
            sys.exit(f"unknown ticker {tk}; add it to COMPANIES")
        cik, label = COMPANIES[tk]
        name, filings = submissions(cik)
        print(f"\n== {tk}  {name}  CIK {cik}: {len(filings)} filings on record")

        picked = []
        for f in filings:
            form = f["form"]
            if form not in args.forms and form.replace("/A", "") not in args.forms:
                continue
            if not (args.since <= f["filingDate"] <= args.until):
                continue
            if form.startswith("8-K") and not args.all_8k:
                if "2.02" not in (f.get("items") or ""):
                    continue
            picked.append(f)
        print(f"   {len(picked)} filings match forms={args.forms} since {args.since}")

        for f in picked:
            acc = f["accessionNumber"]
            form = f["form"]
            date = f["filingDate"]
            tag = f"{date}_{form.replace('/', '-').replace(' ', '')}_{acc}"
            acc_nodash, names = filing_index(cik, acc, out / ".index-cache")
            primary = f.get("primaryDocument")
            if form.startswith("8-K"):
                # earnings 8-K: the EX-99 exhibits (release, slides); fall back to the 8-K body
                docs = wanted_docs(form, names, args.all_8k)
                ex = [d for d in docs if re.search(r"ex[-_]?99", d.lower())]
                docs = ex or ([primary] if primary in names else docs)
            else:
                # 10-K / 10-Q / proxy: the primary document only (no ex31/ex32/ex10 boilerplate)
                docs = [primary] if primary and primary in names else wanted_docs(form, names, args.all_8k)[:1]
            for d in docs:
                url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc_nodash}/{d}"
                raw_path = raw_root / tk / tag / d
                txt_path = text_root / tk / f"{tag}__{Path(d).stem}.txt"
                if args.dry_run:
                    print(f"   [dry] {tag}  {d}")
                    rows_out.append(dict(ticker=tk, form=form, filed=date, period=f.get("reportDate", ""),
                                         accession=acc, file=d, raw_bytes="", text_bytes="", url=url))
                    continue
                if raw_path.exists():
                    data = raw_path.read_bytes()
                else:
                    data = get(url).content
                    raw_path.parent.mkdir(parents=True, exist_ok=True)
                    raw_path.write_bytes(data)
                if d.lower().endswith(".pdf"):
                    text_bytes = 0
                else:
                    text = html_to_text(data) if d.lower().endswith((".htm", ".html")) else data.decode("utf-8", "replace")
                    txt_path.parent.mkdir(parents=True, exist_ok=True)
                    txt_path.write_text(text, encoding="utf-8")
                    text_bytes = len(text.encode("utf-8"))
                print(f"   {tag}  {d}  raw {len(data)/1024:8.0f} KB  text {text_bytes/1024:7.0f} KB")
                rows_out.append(dict(ticker=tk, form=form, filed=date, period=f.get("reportDate", ""),
                                     accession=acc, file=d, raw_bytes=len(data), text_bytes=text_bytes, url=url))

    with open(manifest_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows_out[0].keys()) if rows_out else ["ticker"])
        w.writeheader()
        w.writerows(rows_out)

    if not args.dry_run:
        lines = ["Ground Truth EDGAR corpus — size report", f"since {args.since}  forms {args.forms}", ""]
        tot_raw = tot_txt = 0
        for tk in args.companies:
            for form in sorted({r["form"] for r in rows_out if r["ticker"] == tk}):
                sel = [r for r in rows_out if r["ticker"] == tk and r["form"] == form]
                rb = sum(r["raw_bytes"] for r in sel)
                tb = sum(r["text_bytes"] for r in sel)
                tot_raw += rb
                tot_txt += tb
                lines.append(f"{tk:5} {form:8} {len(sel):3} docs   raw {rb/1e6:7.2f} MB   text {tb/1e6:7.2f} MB")
        lines += ["", f"TOTAL {len(rows_out)} docs   raw {tot_raw/1e6:.2f} MB   text {tot_txt/1e6:.2f} MB"]
        (out / "SIZE_REPORT.txt").write_text("\n".join(lines) + "\n")
        print("\n" + "\n".join(lines))
    print(f"\nmanifest: {manifest_path}")


if __name__ == "__main__":
    main()
