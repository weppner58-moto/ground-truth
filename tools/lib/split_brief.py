#!/usr/bin/env python3
"""
Split a built brief into the public page and the registered-readers page.

  python3 tools/lib/split_brief.py 03 [--free 2]

Reads  site/groundtruth/NN/index.html   (the full page a builder writes)
Writes site/groundtruth/NN/full/index.html   the whole brief, served only with the reader cookie
       site/groundtruth/NN/index.html        the public page: hero, the first --free numbered
                                             sections, the register panel, Method & standing, footer

Idempotent: if index.html is already a public page (marked <!-- gt:public -->), the full page is
read back from full/index.html, so builders and this script can run in any order.
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MARK = "<!-- gt:public -->"

def main():
    n = sys.argv[1]
    free = int(sys.argv[sys.argv.index("--free") + 1]) if "--free" in sys.argv else 2  # 00 Start here + 01
    d = ROOT / "site" / "groundtruth" / n
    src = d / "index.html"
    html = src.read_text()
    if html.startswith(MARK):
        html = (d / "full" / "index.html").read_text()
        html = unshift(html.replace("<!-- gt:full -->", "", 1).lstrip("\n"))

    secs = [m.start() for m in re.finditer(r"<section[^>]*>", html)]
    foot = html.index("<footer")
    method = max(i for i in secs if "Method &amp; standing" in html[i:i + 600] or "Method & standing" in html[i:i + 600])
    # sections: [hero, 00, 01, ..., method, ...]; the public page keeps hero + the first `free` after it
    cut = secs[1 + free]
    kept = html[:cut]
    gated = html[cut:method]
    tail = html[method:foot]
    footer = html[foot:]

    # what is behind the form: the eyebrows of the gated sections
    eyebrows = [strip(t) for t in re.findall(r"<div class=[\"']eyebrow[\"']>(.*?)</div>", gated)]
    eyebrows = [e for e in eyebrows if not e.startswith("Method")]
    figs = len(re.findall(r"<figure", gated))
    pdf = f"../assets/GroundTruth-{n}_Full-Brief.pdf"
    full_url = f"/groundtruth/{n}/full/"

    panel = f"""
<section class="gate"><div class="wrap">
  <div class="gate-box">
    <span class="tape">Registered readers continue here</span>
    <h2>{len(eyebrows)} more sections behind one form.</h2>
    <p>Name and email, once, and this browser is through for a year: the rest of the brief, every figure linked to its filing, the source index, and the whole thing as a PDF. The open items and the corrections log stay public; that is the method.</p>
    <p class="gate-list">{" &nbsp;&middot;&nbsp; ".join(eyebrows)}</p>
    <div class="gate-row">
      <a class="gate-btn" href="/groundtruth/register/?next={full_url}">Register and continue</a>
      <a class="gate-alt" href="full/">Already registered? Continue</a>
    </div>
  </div>
</div></section>
"""
    css = """
<style>
.gate{padding:clamp(40px,6vw,72px) 0;border-bottom:1px solid var(--rule)}
.gate-box{position:relative;border:1px solid var(--ink);padding:clamp(26px,4vw,44px)}
.gate-box::before,.gate-box::after{content:"";position:absolute;width:14px;height:14px;border:solid var(--ink-3);pointer-events:none}
.gate-box::before{left:-15px;top:-15px;border-width:0 1px 1px 0}
.gate-box::after{right:-15px;bottom:-15px;border-width:1px 0 0 1px}
.gate .tape{display:inline-block;background:var(--tape,var(--ink));color:var(--tape-ink,var(--ground));font-family:var(--f-mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;padding:5px 10px 4px}
.gate h2{margin-top:16px}
.gate-list{font-family:var(--f-mono);font-size:12px;letter-spacing:.04em;text-transform:uppercase;color:var(--ink-3);line-height:2;max-width:none}
.gate-row{display:flex;gap:18px;align-items:center;flex-wrap:wrap;margin-top:18px}
.gate-btn{font-family:var(--f-mono);font-size:12.5px;letter-spacing:.14em;text-transform:uppercase;background:var(--tape,var(--ink));color:var(--tape-ink,var(--ground));padding:14px 20px;text-decoration:none}
.gate-btn:hover{background:var(--cyan);color:var(--ground);text-decoration:none}
.gate-alt{font-family:var(--f-mono);font-size:12px;letter-spacing:.06em;color:var(--cyan)}
.full-bar{font-family:var(--f-mono);font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;border-bottom:1px solid var(--rule);background:var(--ground-2)}
.full-bar .wrap{display:flex;gap:18px;align-items:center;justify-content:space-between;flex-wrap:wrap;padding-block:10px}
.full-bar a{color:var(--cyan)}
</style>
"""
    public = kept + panel + tail + footer
    if ".gate-box{" not in public: public = public.replace("</head>", css + "</head>", 1)
    # anchors that now live behind the gate go to the full page
    kept_ids = set(re.findall(r'id="([^"]+)"', kept + tail))
    public = re.sub(r'href="#([^"]+)"', lambda m: m.group(0) if m.group(1) in kept_ids else f'href="full/#{m.group(1)}"', public)
    public = MARK + "\n" + public

    bar = f"""<div class="full-bar"><div class="wrap"><span>Registered reader &middot; the complete brief</span><span><a href="../">Public page</a> &nbsp;&middot;&nbsp; <a href="{pdf}">Download the PDF</a></span></div></div>
"""
    fullp = shift(html)
    if ".gate-box{" not in fullp: fullp = fullp.replace("</head>", css + "</head>", 1)
    fullp = re.sub(r"(<body[^>]*>)", r"\1\n" + bar.replace("\\", "\\\\"), fullp, count=1)
    fullp = "<!-- gt:full -->\n" + fullp

    (d / "full").mkdir(exist_ok=True)
    (d / "full" / "index.html").write_text(fullp)
    src.write_text(public)
    print(f"{n}: public keeps {free} sections, {len(eyebrows)} gated; full/index.html {len(fullp):,} B, index.html {len(public):,} B")

def strip(t): return re.sub(r"<[^>]+>", "", t).replace("&middot;", "·").strip()

def shift(h):
    """Relative links one level deeper for full/."""
    h = re.sub(r'href="\.\./', 'href="../../', h)
    h = re.sub(r'href="(0\d/)', r'href="../\1', h)
    h = h.replace('href="series/"', 'href="../series/"').replace("href='series/'", "href='../series/'")
    return h

def unshift(h):
    h = h.replace('href="../series/"', 'href="series/"').replace("href='../series/'", "href='series/'")
    h = re.sub(r'href="\.\./(0\d/)', r'href="\1', h)
    h = re.sub(r'href="\.\./\.\./', 'href="../', h)
    h = re.sub(r'<div class="full-bar">.*?</div></div>\n', "", h, count=1, flags=re.S)
    return h

if __name__ == "__main__":
    main()
