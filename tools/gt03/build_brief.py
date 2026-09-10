#!/usr/bin/env python3
"""Build groundtruth/03/index.html — Ground Truth No. 03, "Outside In".

Run from the repo root:  python3 tools/gt03/build_brief.py
Content lives in this file; CSS, bio and glyphs come from tools/lib.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "lib"))
from charts import bars, hbars, sbars, waterfall, MAG, CYAN, INK3  # noqa: E402

LIB = ROOT / "tools" / "lib"
OUT = ROOT / "groundtruth" / "03" / "index.html"
NN, REV, DATE = "03", "Rev. 1", "September 2026"
TITLE = "Harley-Davidson: Outside In"
PARTS = ["Part I", "Part II", "Part III", "Part IV", "Part V", "Part VI"]
SEC = "https://www.sec.gov/Archives/edgar/data/"

EXTRA_CSS = """
/* No. 03 additions */
.strip .s .sv{font-family:var(--f-disp);font-weight:800;font-size:clamp(28px,3.6vw,38px);line-height:.95;font-variant-numeric:tabular-nums;margin:6px 0 4px}
.strip .s .sv.m{color:var(--magenta)} .strip .s .sv.c{color:var(--cyan)}
.strip .s .sk{font-family:var(--f-mono);font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3);line-height:1.5}
.strip .s .sn{font-size:12.5px;color:var(--ink-2);line-height:1.45;margin-top:4px}
.strip .s{padding:16px 14px 16px}
.tl{list-style:none;margin:22px 0 8px;padding:0;border-top:1px solid var(--rule-2);max-width:72ch}
.tl li{display:grid;grid-template-columns:120px 1fr;gap:14px;padding:10px 0;border-bottom:1px dashed var(--rule-2);font-size:15px;line-height:1.5}
.tl li b{font-family:var(--f-mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--magenta);font-weight:600;padding-top:3px}
.tl li.h b{color:var(--cyan)}
.tbl td.q{font-size:14px}
.duo .card .big{font-family:var(--f-disp);font-weight:800;font-size:clamp(44px,6vw,72px);line-height:.9;font-variant-numeric:tabular-nums;margin:6px 0 10px}
.duo .card .big.mag{color:var(--magenta)} .duo .card .big.cy{color:var(--cyan)}
.duo .card .k{font-family:var(--f-mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3)}
.duo .card{border-top:3px solid var(--ink);padding-top:14px}
.duo .card.mag{border-color:var(--magenta)}
.glyphs .g{width:26px;height:16px;display:inline-block;margin:2px 3px 2px 0;color:var(--ink-2)}
.g-n{font-family:var(--f-disp);font-weight:800;font-size:26px;line-height:1;font-variant-numeric:tabular-nums}
.g-g{line-height:1}
.brand-txt{font-size:12px}
"""


def ev(kind):
    names = {"doc": "Documented", "calc": "Calculated", "inf": "Inferred", "ind": "Industry context", "unv": "Unverified"}
    return f"<span class='ev ev-{kind}'>{names[kind]}</span>"


def n(x):
    return f"<b class='n'>{x}</b>"


def link(url, text):
    return f"<a href='{url}' target='_blank' rel='noopener'>{text}</a>"


def brand():
    return "<div class='brand'><span class='brand-txt'>HARLEY-DAVIDSON, INC. &middot; NYSE: HOG</span></div>"


def brandrow(eyebrow):
    return f"<div class='brandrow'><div class='eyebrow'>{eyebrow}</div>{brand()}</div>"


def here(i):
    spans = " ".join(f"<span class='{'on' if j == i else ''}'>{p}</span>" for j, p in enumerate(PARTS))
    return f"<div class='here'>{spans}</div>"


IMG = ROOT / "tools" / "gt03" / "img"


def part_img(img_title, img_desc, sketch, img=None):
    """A real image if tools/gt03/img/<img> exists, else the sketch placeholder."""
    if img and (IMG / img).exists():
        import base64, mimetypes
        data = base64.b64encode((IMG / img).read_bytes()).decode()
        mime = mimetypes.guess_type(img)[0] or "image/jpeg"
        return f"<div class='part-img'><img src='data:{mime};base64,{data}' alt='{img_title}. {img_desc}'><div class='c'>{img_title}</div></div>"
    return f"<div class='part-img'><div class='phx'><span class='tag'>Image to source</span><div class='t'>{img_title}</div><div class='d'>{img_desc}</div><div class='s'>Sketch: {sketch}</div></div></div>"


def part(i, title, dek, point, why, img_title, img_desc, sketch, img=None):
    return f"""
<div class="wrap part" id="part{i+1}">
  <div class="brandrow">{here(i)}{brand()}</div>
  <div class="part-n">{PARTS[i]}</div>
  <h2 class="part-t">{title}</h2>
  <div class="part-grid">
    <div>
      <p class="part-d">{dek}</p>
      <div class="part-kv">
        <div><b>The point</b><span>{point}</span></div>
        <div><b>Why it matters</b><span>{why}</span></div>
      </div>
    </div>
    {part_img(img_title, img_desc, sketch, img)}
  </div>
</div>
"""


def fig(num, title, sub, svg, tag, caption):
    return f"""
    <figure>
      <div class="fig-head"><span class="fig-n">FIG {num}</span><span class="fig-t">{title}</span><span class="fig-sub">{sub}</span></div>
      {svg}
      <figcaption>{ev(tag)}{caption}</figcaption>
    </figure>"""


def sowhat(sec, point, thesis, outlook):
    return f"""
    <div class="sowhat">
      <div class="h">So what &middot; &sect;{sec}</div>
      <div class="r"><b>The point</b><span>{point}</span></div>
      <div class="r"><b>Back to the thesis</b><span>{thesis}</span></div>
      <div class="r"><b>Outlook</b><span>{outlook}</span></div>
    </div>"""


def note(h, *ps, tag=None):
    head = (ev(tag) if tag else "") + h
    body = "".join(f"<p>{p}</p>" for p in ps)
    return f"<div class='note'><div class='h'>{head}</div>{body}</div>"


def plain(h, *ps):
    return "<div class='plain'><div class='h'>" + h + "</div>" + "".join(f"<p>{p}</p>" for p in ps) + "</div>"


def tbl(head, rows, widths=None):
    ths = []
    for i, h in enumerate(head):
        st = " style='width:%s'" % widths[i] if widths and widths[i] else ""
        ths.append("<th%s>%s</th>" % (st, h))
    th = "".join(ths)
    trs = []
    for r in rows:
        tds = []
        for c in r:
            cls = ""
            if isinstance(c, tuple):
                c, cls = c
            tds.append(f"<td class='{cls}'>{c}</td>" if cls else f"<td>{c}</td>")
        trs.append("<tr>" + "".join(tds) + "</tr>")
    return "<div class='scroll'><table class='tbl'><thead><tr>" + th + "</tr></thead><tbody>" + "".join(trs) + "</tbody></table></div>"


def section(body):
    return "<section><div class='wrap'>" + body + "</div></section>"


# ───────────────────────────── hero figure ─────────────────────────────
def herofig():
    # timeline 1960 → 2026, piecewise scale (1960–2005 = 38% of width; 2005–2028 = 62%)
    # (year, label, colour, ending, level)  level>0 above the line, <0 below
    moves = [
        (1960, "Aermacchi", MAG, "sold 1978", 1), (1986, "Holiday Rambler", MAG, "sold 1996", -1),
        (1993, "Eaglemark", CYAN, "kept: HDFS", 1), (1994.2, "Buell", MAG, "shut 2009", -2),
        (2008, "MV Agusta", MAG, "sold for €1, 2010", 1), (2013, "Street / Bawal", INK3, "built; exited 2020", -1),
        (2016, "Milwaukee-Eight", INK3, "built; kept", 2), (2018.2, "Alta", MAG, "gone in 6 months", -2),
        (2019.2, "StaCyc", CYAN, "kept: 21,633 units", 3), (2019.9, "Qianjiang", CYAN, "kept: licence", -3),
        (2020.8, "Hero", CYAN, "kept: licence", 1), (2021.6, "Rev Max", INK3, "built; kept", -1),
        (2022.4, "LiveWire SPAC", MAG, "2027?", 2), (2026.4, "Dust · Honcho", CYAN, "via LiveWire", -2),
    ]
    x0, x1 = 80, 1140
    def X(y):
        if y <= 2005:
            return x0 + (y - 1958) / (2005 - 1958) * (x1 - x0) * 0.38
        return x0 + (x1 - x0) * 0.38 + (y - 2005) / (2028 - 2005) * (x1 - x0) * 0.62
    base = 290
    o = ["<svg class='herofig' viewBox='0 0 1200 560' role='img' aria-label='Harley-Davidson outside moves 1960 to 2026: every purchased brand sold or shut; the finance company, StaCyc and the licences kept; the two engines built in-house kept.'>",
         "<rect x='0' y='0' width='1200' height='560' fill='var(--ground-2)'></rect>",
         "<text class='ax' x='80' y='44' style='font-size:12px;letter-spacing:.16em'>WHAT HARLEY-DAVIDSON REACHED OUTSIDE FOR, 1960–2026</text>",
         f"<line class='zl' x1='80' y1='{base}' x2='1140' y2='{base}'></line>"]
    for yr in [1960, 1970, 1980, 1990, 2000, 2005, 2010, 2015, 2020, 2025]:
        o.append(f"<line class='gl' x1='{X(yr):.0f}' y1='{base-8}' x2='{X(yr):.0f}' y2='{base+8}'></line>")
        o.append(f"<text class='ax' x='{X(yr):.0f}' y='{base+26}' text-anchor='middle'>{yr}</text>")
    o.append(f"<text class='ax' x='{X(2005):.0f}' y='{base+42}' text-anchor='middle' opacity='.6'>scale change</text>")
    for y, name, col, end, lv in moves:
        x = X(y)
        ly = base - 40 - 62 * (lv - 1) if lv > 0 else base + 62 + 50 * (-lv - 1)
        o.append(f"<line x1='{x:.0f}' y1='{base}' x2='{x:.0f}' y2='{ly + (12 if lv > 0 else -24)}' stroke='{col}' stroke-width='1.2' opacity='.6'></line>")
        o.append(f"<circle cx='{x:.0f}' cy='{base}' r='7' fill='{col}'></circle>")
        anchor = "middle"
        if name in ("Dust · Honcho",):
            anchor = "end"
        if name in ("Aermacchi",):
            anchor = "start"
        o.append(f"<text class='vl' x='{x:.0f}' y='{ly}' text-anchor='{anchor}' style='font-size:14px;fill:{col};font-weight:600'>{name}</text>")
        o.append(f"<text class='ax' x='{x:.0f}' y='{ly+16}' text-anchor='{anchor}'>{end}</text>")
    o.append("<g transform='translate(80,500)'>")
    o.append(f"<rect x='0' y='-8' width='12' height='12' fill='{MAG}'></rect><text class='ax' x='20' y='2'>BOUGHT A BRAND: SOLD OR SHUT</text>")
    o.append(f"<rect x='250' y='-8' width='12' height='12' fill='{CYAN}'></rect><text class='ax' x='270' y='2'>BOUGHT A CHANNEL OR A COMPONENT: KEPT</text>")
    o.append(f"<rect x='580' y='-8' width='12' height='12' fill='{INK3}'></rect><text class='ax' x='600' y='2'>BUILT IN-HOUSE</text>")
    o.append("</g>")
    o.append("<line x1='80' y1='516' x2='1140' y2='516' stroke='var(--magenta)' stroke-width='2'></line>")
    o.append("<text x='80' y='548' style='font-family:var(--f-disp);font-weight:800;font-size:27px;letter-spacing:.02em;fill:var(--ink)'>HARLEY-DAVIDSON DOESN&#8217;T WANT ELECTRIC. IT WANTS FLOOR TRAFFIC.</text>")
    o.append("</svg>")
    return "\n".join(o)


# ───────────────────────────── page ─────────────────────────────
def build():
    css = (LIB / "brief.css").read_text() + EXTRA_CSS
    bio = (LIB / "bio.html").read_text()
    bio = bio.replace("LiveWire Group, Harley-Davidson, or any company named here", "Harley-Davidson, LiveWire Group, Hero MotoCorp, KYMCO, or any company named here")
    bio = bio.replace("the fix is in the log at &sect;14", "the fix is in the log at &sect;13")
    bio = bio.replace("I have no engagement, adverse or friendly, with any of them.</p>",
                      "I have no engagement, adverse or friendly, with any of them. I know Marc Fenigstein, Alta&rsquo;s co-founder, and have worked with him since Alta closed; his account quoted in &sect;04 is public record and is identified as his.</p>")
    bio = bio.replace("the bike that still defines the segment LiveWire is walking into", "the bike that still defines the segment the Sprint is walking into")
    glyphs = (LIB / "glyphs.svg").read_text()

    H = []
    H.append(f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{TITLE}</title>
<meta name="description" content="Ground Truth No. 03. Sixty-six years of Harley-Davidson buying what it could build, read from the filings: Aermacchi, Buell, MV Agusta, Alta, StaCyc, Hero, QJ, KYMCO, Dust. What it paid, what it got, and what it was for.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@600;700;800&family=IBM+Plex+Mono:wght@400;500;600&family=Public+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap">
<style>{css}</style>
</head><body>
<header class="topbar">
  <div class="wrap">
    <div class="mark">CONTACT&nbsp;<span>PATCH</span></div>
    <div class="stamp">Ground Truth No. {NN} &middot; Draft &middot; {REV}</div>
  </div>
</header>
<main>
""")

    # ── hero
    H.append(f"""
<section class="hero">
  <div class="wrap">
    <div class="kick">Ground Truth No. {NN} &middot; Harley-Davidson, Inc. &middot; {DATE}</div>
    <div class="hero-top">
      <h1><span style="display:block;font-size:.42em;letter-spacing:.02em;color:var(--ink-2);margin-bottom:.15em">Harley-Davidson:</span>Outside<br>In</h1>
    </div>
    <p class="sub" style="font-family:var(--f-mono);font-size:clamp(13px,1.6vw,17px);letter-spacing:.14em;text-transform:uppercase;color:var(--magenta);margin:18px 0 0">Sixty-six years of buying what it could build</p>
    <div class="herofig-wrap">{herofig()}</div>
    <ul class="thesis">
      <li><b>What they said</b><span>May 2026, the new plan: &ldquo;leveraging existing powertrain, existing platforms&rdquo; and &ldquo;executing better with the platforms we already have rather than introducing entirely new ones.&rdquo; The first new bike is the Sprint, on a {n('440cc')} single Hero MotoCorp builds in Rajasthan.</span></li>
      <li><b>What it is</b><span>The sixty-sixth year of the same move. Every brand Harley ever bought was sold or shut, with the same sentence. MV Agusta: {n('$105.1M')} in, {n('$268.4M')} lost, sold back for {n('&euro;1')}. Alta: a stake too small to disclose, gone in six months. StaCyc: {n('$14.9M')}, and it outsells LiveWire {n('33 to 1')}.</span></li>
      <li><b>What decided it</b><span>Harley builds when the product carries the full brand at the full price. Everything below the big twin (a small bike, a balance bike, a battery, a loan book) gets bought, licensed or partnered. It stays when it feeds the dealer. It goes when it competes with the badge.</span></li>
    </ul>
    <p class="thesis-line">Harley doesn&rsquo;t want electric. <i>It wants floor traffic.</i></p>
    <div class="srcline">
      Sources: HOG Forms 10-K (FY1994, FY1996, FY2009, FY2010, FY2011, FY2018, FY2019, FY2020, FY2025) &middot; 10-Q (Q3 2008, Q3 2009, Q1 2018, Q3 2018, Q1 2019) &middot; 8-K (11 Jul 2008, 15 Oct 2009, 9 Aug 2010 incl. Ex. 2.1, 24 Sep 2020, 13 Dec 2021)<br>
      Faster Faster, Inc. Forms D (2016&ndash;2018) &middot; LVWR 8-K (30 Sep 2022; 22 May 2026) and 10-K (FY2022) &middot; LiveWire FY2025 and Q2 2026 results &middot; Hero MotoCorp X440 release (3 Jul 2023) &middot; H-D call transcripts Q1 2019, Q3 2021, Q2 2025, Q1 2026, Q2 2026
    </div>
  </div>
</section>
""")

    # ── strip
    H.append(f"""
<div class="strip">
  <div class="s"><div class="sk">MV Agusta &middot; loss from discontinued ops, 2008&ndash;10</div><div class="sv m">$268.4M</div><div class="sn">On $105.1M of consideration. Sold back for &euro;1 with &euro;20M of Harley cash inside.</div></div>
  <div class="s"><div class="sk">Alta Motors &middot; amount invested, per every H-D filing</div><div class="sv m">Not stated</div><div class="sn">Bounded by Alta&rsquo;s Form D: at most $5.65M. Out in six months.</div></div>
  <div class="s"><div class="sk">StaCyc &middot; total consideration, Q1 2019 10-Q</div><div class="sv c">$14.9M</div><div class="sn">$7.0M cash, a $6.5M earn-out paid in full. Every volume target hit.</div></div>
  <div class="s"><div class="sk">StaCycs per LiveWire motorcycle, 2025</div><div class="sv c">33 : 1</div><div class="sn">21,633 balance bikes. 653 motorcycles. 76% of LiveWire&rsquo;s product revenue.</div></div>
</div>
<div class="strip-cap">Four numbers from the filings. The rest of the record is in &sect;01.</div>
<div class="wrap route" id="route">
  <div class="route-h">The route &middot; six parts, one thesis</div>
  <ol>
    <li><a href="#part1"><div class="rn">Part I</div><div class="rt">The record</div><div class="rp">Sixteen moves in one table. Brands go. Channels and components stay.</div></a></li>
    <li><a href="#part2"><div class="rn">Part II</div><div class="rt">Same sentence</div><div class="rp">Buell and MV Agusta. $125M and $268M. &ldquo;Focus on the Harley-Davidson brand.&rdquo;</div></a></li>
    <li><a href="#part3"><div class="rn">Part III</div><div class="rt">Too small to say</div><div class="rp">Alta, never disclosed. StaCyc, $14.9M, and it outsells LiveWire 33 to 1.</div></a></li>
    <li><a href="#part4"><div class="rn">Part IV</div><div class="rt">What it builds</div><div class="rp">Two engines kept. One small bike lost money and left. The rule.</div></a></li>
    <li><a href="#part5"><div class="rn">Part V</div><div class="rt">The Sprint rhyme</div><div class="rp">1960: an Aermacchi. 2026: a Hero. Same hole, somebody else&rsquo;s engine.</div></a></li>
    <li><a href="#part6"><div class="rn">Part VI</div><div class="rt">The final word</div><div class="rp">Seven CEOs, one cycle. LiveWire is on the Buell script. What it was for.</div></a></li>
  </ol>
</div>
""")

    # ── §00 start here
    H.append(section(f"""
    <div class="eyebrow">00 &middot; Start here</div>
    <h2>The finding, and the trail that led to it</h2>
    <p class="lede">Harley-Davidson has spent sixty-six years buying, licensing and partnering its way into every segment below the big twin, and building from within only when the product carries the full brand at the full price. Here is how three old filings led me to that sentence.</p>
    <p>Start with what they said. May 5, 2026, the Q1 call, the new CEO explaining the plan: &ldquo;By using and leveraging existing powertrain, existing platforms, we can have a much broader assortment of motorcycles to present.&rdquo; The first new motorcycle under that plan is the Sprint. Its engine is a {n('440cc')} single that Hero MotoCorp co-developed with Harley and builds in Neemrana for the X440, a {n('&#8377;2.29 lakh')} motorcycle. On the same call: &ldquo;we&rsquo;re finalizing the specific production plans.&rdquo; A company that says it will lean on the platforms it already has is opening the plan with one it does not own.</p>
    <p>That sent me back through the record. Not the press record; the filed one. What did Harley pay each time it reached outside the building, what did it get, and how did it end?</p>
    <ul class="finds">
      <li>Open the FY2009 and FY2010 10-Ks and MV Agusta is not the &ldquo;~$163M&rdquo; everyone quotes. It is {n('$268.4M')} of net loss from discontinued operations in twenty-four months, on {n('$105.1M')} of consideration, {n('$20.1M')} of which was written off on the day it closed.</li>
      <li>Open the 8-K of August 9, 2010 and the sale agreement is attached. The shares went for {n('&euro;1')}. The U.S. company for {n('$1')}. A {n('&euro;103.8M')} receivable for another euro. Harley put {n('&euro;20.0M')} into escrow on the way out.</li>
      <li>Search every 10-Q and 10-K Harley filed in 2018 and 2019 for &ldquo;Alta.&rdquo; One hit, one sentence, in a press release. No amount. Alta&rsquo;s own Form D chain bounds it at {n('$5.65M')}.</li>
      <li>Open the Q1 2019 10-Q and StaCyc cost {n('$14.9M')}. LiveWire&rsquo;s carve-out statements show the earn-out was paid in full. In 2025 it sold {n('21,633')} units to LiveWire&rsquo;s {n('653')}.</li>
      <li>Line them up by what each one was for and the pattern writes itself: the finance company and the balance bikes were bought to feed the dealer, and they stayed. The brands were bought to be a second Harley, and they went.</li>
    </ul>
    <p>None of this is secret. All of it is in the exhibits, and most of it has not been read in a decade.</p>

    <h3 style="font-size:clamp(21px,2.6vw,28px); margin-top:40px">The trail, in five documents</h3>
    <p>The order I read them in. Each one sent me to the next.</p>
    <ol class="trail">
      <li><div><div class="doc">{link('https://www.fool.com/earnings/call-transcripts/2026/05/05/harley-davidson-hog-q1-2026-earnings-transcript/', 'Q1 2026 earnings call &middot; 5 May 2026 &rarr;')}</div><div class="what"><b>&ldquo;Existing platforms.&rdquo;</b> Starrs on the plan, and on the Sprint: &ldquo;we&rsquo;re finalizing the specific production plans.&rdquo; The engine is Hero&rsquo;s. Why does a company with the Milwaukee-Eight not build a 440?</div></div></li>
      <li><div><div class="doc">{link(SEC + '793952/000119312510037160/R9.xml', 'Form 10-K FY2009 &middot; MV Agusta note &rarr;')}</div><div class="what"><b>$115.4M.</b> The impairment, fourteen months after closing. Consideration &euro;68.3M, goodwill $85.8M, IPR&amp;D of $20.1M written off at once. The Buell decision, taken the same week, is in the 10-Q beside it.</div></div></li>
      <li><div><div class="doc">{link(SEC + '793952/000119312510183610/dex21.htm', 'Sale and Purchase Agreement &middot; Ex. 2.1 to 8-K, 9 Aug 2010 &rarr;')}</div><div class="what"><b>&euro;1.</b> &sect;2.1.1(a): the MV Agusta shares &ldquo;for a consideration of Euro 1 (one).&rdquo; &sect;7.1.1: a capital increase of &euro;20,000,000. &sect;7.2.2(a): the earn-out &ldquo;finally and irrevocably waived.&rdquo; The 10-K says &ldquo;nominal consideration.&rdquo; This is what nominal means.</div></div></li>
      <li><div><div class="doc">{link(SEC + '1620298/000162029818000001/primary_doc.xml', 'Faster Faster, Inc. &middot; Form D/A &middot; 5 Feb 2018 &rarr;')}</div><div class="what"><b>$20,843,998.</b> Alta&rsquo;s round, closed by amendment four weeks before Harley&rsquo;s announcement. Six investors and $5.65M added since July. Harley&rsquo;s own filings never give a number; this is the ceiling.</div></div></li>
      <li><div><div class="doc">{link(SEC + '793952/000079395219000021/hog-03312019x10q.htm', 'Form 10-Q Q1 2019 &middot; goodwill note &rarr;')}</div><div class="what"><b>$14.9 million.</b> StaCyc: $7.0M of cash, $9.5M of goodwill, and a stated reason: &ldquo;building the next generation of riders.&rdquo; Then LiveWire&rsquo;s FY2025 release: 21,633 of them, against 653 motorcycles.</div></div></li>
    </ol>

    <h3 style="font-size:clamp(21px,2.6vw,28px); margin-top:40px">Four instruments</h3>
    <p>The paperwork that decided each ending.</p>
    <div class="paper">
      <div class="c"><div class="n">MV Agusta &middot; sale</div><div class="t">&euro;1, &euro;1, and $1</div><div class="r"><b>Three nominal payments, &euro;20M of operating capital contributed, the 2016 earn-out waived.</b> Eleven days of drafting between the board&rsquo;s July 31 signature and the August 6 close. Harley received &ldquo;nominal consideration&rdquo; and reported &ldquo;an immaterial loss on the date of sale.&rdquo;</div><div class="k">31 Jul 2010 &middot; closed 6 Aug 2010 &middot; Ex. 2.1</div></div>
      <div class="c"><div class="n">Buell &middot; 10-Q note</div><div class="t">$125M, estimated</div><div class="r"><b>Board approval 14 Oct 2009; production ended that month.</b> ~$70M in incentives, inventory and operating costs, ~$14M of fixed assets, ~$9M of severance, ~$32M of contracts. The realized total was never broken out again.</div><div class="k">Q3 2009 10-Q &middot; Note 19</div></div>
      <div class="c"><div class="n">Alta &middot; Form D chain</div><div class="t">Five notices, no Harley</div><div class="r"><b>Alta&rsquo;s legal name. Five Reg D notices from 2016 to 2018.</b> The equity round closed 2 Feb 2018 at $20.84M. A $5.0M bridge note started selling 27 Jul 2018; $2.45M placed with four investors. Harley&rsquo;s exit leaked sixteen days later.</div><div class="k">Mar 2016 &ndash; Aug 2018 &middot; CIK 1620298</div></div>
      <div class="c"><div class="n">Dust &middot; asset purchase</div><div class="t">$375,000 cash</div><div class="r"><b>Plus $500K of stock, three annual $875K stock installments, and earn-outs up to $11.25M in stock.</b> The Alta structure, done inside LiveWire this time, where a write-off lands in a segment the parent has already told investors to look past.</div><div class="k">18 May 2026 &middot; LVWR 8-K, 22 May 2026</div></div>
    </div>

    <ul class="finds" style="margin-top:30px">
      <li><b>Why.</b> Back to the Bricks is scored on HDMC alone and opens with a licensee&rsquo;s motorcycle. Whether the Sprint and the 883 get built in Harley&rsquo;s own plants, at a price where Harley makes money, is the whole test of the plan. The record says what usually happens.</li>
      <li><b>Who for.</b> Anyone deciding whether the Sprint is a product or a channel program; anyone holding HOG into a 2027 that contains the 883, a Sprint, and a LiveWire decision; and the people at Juneau Avenue who already know this and cannot say it.</li>
      <li><b>What I did.</b> Read the acquisition, impairment and discontinued-operations notes for every outside move since 1993, the sale agreement for MV, Alta&rsquo;s Form D chain, and LiveWire&rsquo;s carve-out statements for StaCyc. Derived figures are arithmetic on filed numbers, shown in the captions. Secondary sources are used only where flagged.</li>
      <li><b>Who I am.</b> I ran product at Harley-Davidson: Touring, CVO, Trike. I have sat in the meeting where a small-bike program gets its cost target. &sect;13.</li>
    </ul>
    """))

    # ═════════ PART I — THE RECORD ═════════
    H.append(part(0, "The record", "Every time Harley-Davidson reached outside the building, 1960 to 2026, from the filings.",
                  "Sixteen moves. Every purchased brand is gone. Every purchased channel or component is still here: the finance company, the balance bikes, the licences, the assembly lines.",
                  "The pattern is the argument. Once you see what stayed and what went, the Sprint, the 883 and LiveWire stop being three decisions and become one.",
                  "Varese, 1961", "An Aermacchi-built Harley-Davidson Sprint on the line at Schiranna. The first time Harley filled the gap below the big twin with somebody else&rsquo;s motorcycle.",
                  "1961 Aermacchi Harley-Davidson Sprint 250, single-cylinder, horizontal engine, on a factory assembly line in Varese, Italy. Ink and wash, period photo feel, 3:2, no logos."))

    rows = [
        ("1960", "50% of Aermacchi&rsquo;s motorcycle division, Varese", "Out", ("~$250K", "num"), "The original <b>Harley-Davidson Sprint</b>, 250/350 singles. Full ownership early 1970s. Sold to the Castiglionis (Cagiva) 1978"),
        ("1986", "Holiday Rambler, recreational vehicles", "Out", ("~$155M", "num"), "Segment sold 1996, ~$105M, gain $22.6M, &ldquo;in order to concentrate on its core motorcycle business&rdquo;"),
        ("1993", "49% of Eaglemark Financial Services; the rest Nov 1995", "Out", ("$10M + ~$45M", "num"), "Became <span class='hi'>HDFS</span>. $248M of operating income in 2024. 9.8% sold to KKR/PIMCO at ~1.75&times; book, 2025"),
        ("1993", "49% of Buell; substantially all of the rest Feb 1998", "Out", ("~$500K; 1998 n/d", "num"), "Shut Oct 2009. Announced exit cost <span class='hi'>~$125M</span>. &ldquo;Focus both our effort and our investment on the Harley-Davidson brand&rdquo;"),
        ("2008", "MV Agusta + Cagiva", "Out", ("&euro;68.3M ($105.1M)", "num"), "Sold back to Castiglioni 6 Aug 2010 for <span class='hi'>&euro;1</span> + $1 + &euro;1, with &euro;20.0M of H-D cash contributed. Net loss from discontinued ops <span class='hi'>$268.4M</span> in 24 months"),
        ("2013", "Street 500/750, Revolution X, Bawal (India)", "<b>In</b>", ("n/d", "num"), "&ldquo;First all-new platform in 13 years.&rdquo; India manufacturing exited Sept 2020, ~$75M restructuring. &ldquo;Unprofitable,&rdquo; per the CFO, Q3 2021"),
        ("2016", "Milwaukee-Eight", "<b>In</b>", ("n/d", "num"), "Still the Big Twin"),
        ("2017", "Rayong, Thailand plant", "In, offshore", ("n/d", "num"), "Rev Max models for the U.S. moved there 2024; returning to York and Menomonee Falls before 2027"),
        ("2018", "Equity in Alta Motors (Faster Faster, Inc.) + co-development", "Out", ("<span class='hi'>never stated</span>", "num"), "H-D out by August; Alta closed 17 Oct 2018; BRP bought the IP. H-D&rsquo;s own Silicon Valley EV R&amp;D facility announced 5 Sep 2018"),
        ("2019", "StaCyc, Inc.", "Out", ("$14.9M", "num"), "LiveWire&rsquo;s only profitable unit. <span class='hi'>21,633</span> units in 2025"),
        ("2019", "Qianjiang (Geely), 338cc for China", "Out, licence", ("n/d", "num"), "X350/X500 in Asia. The X350RA is the U.S. Riding Academy bike, not for sale"),
        ("2020", "Hero MotoCorp, India distribution and brand licence", "Out, licence", ("follows ~$75M exit", "num"), "X440 launched Jul 2023, Hero-built, &#8377;2.29 lakh. <span class='hi'>The Sprint&rsquo;s engine</span>"),
        ("2021", "Revolution Max / Pan America", "<b>In</b>", ("n/d", "num"), "Pan America, Sportster S, Nightster. Thailand 2024&ndash;26; coming home"),
        ("2021", "LiveWire SPAC; KYMCO $100M", "Out, capital", ("H-D $100M; $1.77B EV", "num"), "923 units TTM; $422M of consolidated losses (No. 02)"),
        ("2025", "HDFS: 4.9% each to KKR and PIMCO; &gt;$5B of receivables; two-thirds forward flow", "Out, capital", ("~$1.25B in", "num"), "HDFS operating income guided from $490M to $55&ndash;70M (No. 02 &sect;2)"),
        ("2026", "Dust Motorcycles, Inc., via LiveWire", "Out", ("$375K cash + stock", "num"), "Pre-revenue; product &ldquo;2H 2026&rdquo;; earn-outs to $11.25M"),
        ("2026", "S4 Honcho, produced by KYMCO", "Out, contract mfg", ("$4,999 / $5,499", "num"), "KYMCO exclusive for five years on the maxi-scooter and &ldquo;any future products on which the parties may agree&rdquo;"),
        ("2026&ndash;27", "Sprint (Hero 440 single); Sportster 883", "<b>In?</b>", ("", "num"), "Sprint production &ldquo;being finalized&rdquo;; sub-$6,000 (Jul 2025) now &ldquo;less than $10,000&rdquo; (trade). The 883: first air-cooled twin program since the Evolution"),
    ]
    lost = hbars([268.4, 125, 75, 422], ["MV Agusta", "Buell", "India / Street", "LiveWire"], fills=[MAG, MAG, INK3, MAG],
                 fmt=lambda v: f"${v:,.0f}M", sublabels=["2008–10, filed", "2009, estimate", "2020, estimate", "2022–Q2 2026, filed"],
                 label="What the outside moves cost to unwind: MV Agusta $268M filed, Buell $125M estimated, India $75M estimated, LiveWire $422M consolidated.", tips=["Net loss from discontinued operations 2008–2010, FY2010 10-K", "Announced exit cost, Q3 2009 10-Q Note 19", "Restructuring for actions approved Sept 2020, 8-K", "Consolidated LiveWire operating losses, No. 02 §3"])
    H.append(section(brandrow("01 &middot; The record") + f"""
    <h2>Sixteen moves, one table</h2>
    <p class="lede">Every figure is from a filing or a company release unless marked ~, which means a secondary source and an open item. &ldquo;n/d&rdquo; means the company never disclosed it. Read the last column first.</p>
    {tbl(['Year', 'Move', 'In / out', 'Cost, as filed', 'How it ended'], rows, ['7%', '27%', '10%', '14%', '42%'])}
    <p>Two patterns fall out before any analysis. <strong>Every outside purchase that carried its own brand was sold or shut: Holiday Rambler, Buell, MV Agusta, Aermacchi. Three of the four went within two years of a CEO change, with the same sentence.</strong> Every outside move that carried no badge into a Harley segment has been kept, quietly: Eaglemark&rsquo;s balance sheet, StaCyc&rsquo;s balance bikes, Hero&rsquo;s engine, Qianjiang&rsquo;s twin, KYMCO&rsquo;s assembly line, KKR&rsquo;s capital. They feed the dealer without competing with the Harley-Davidson brand.</p>
    {fig('01', 'What the outside moves cost to unwind', '$ millions &middot; filed where available', lost, 'calc', 'MV Agusta is the filed net loss from discontinued operations, 2008&ndash;2010. Buell and India are the company&rsquo;s announced estimates; neither was ever reconciled in a later filing. LiveWire is the consolidated operating loss from the spin through Q2 2026, from No. 02. Alta is missing from this chart because there is no number to put on it.')}
    {sowhat('01', 'Harley-Davidson has gone outside for a product sixteen times in sixty-six years. The brands are gone. The channels and components stayed.', 'What survives a CEO change at Harley is whatever makes money on somebody else&rsquo;s product on a Harley dealer&rsquo;s floor.', 'The Sprint is a Hero engine, the Honcho is a KYMCO build, Dust is an option. Read the table and you know which column each is in.')}
    """))

    # ═════════ PART II — SAME SENTENCE ═════════
    H.append(part(1, "Same sentence", "Buell and MV Agusta: what the two biggest purchases cost, and the words used both times.",
                  "Buell: ~$125M to shut, sixteen years after the first stake. MV Agusta: $105.1M in, $268.4M of losses in twenty-four months, sold back for a euro with &euro;20M of Harley cash inside.",
                  "1996: &ldquo;concentrate on its core motorcycle business.&rdquo; 2009 and 2010: &ldquo;focus &hellip; on the Harley-Davidson brand.&rdquo; The words repeat because the decision does: a second brand that competes with Harley-Davidson for engineering dollars does not survive the next CEO.",
                  "East Troy, October 2009", "The last Buell on the line. Production ended at the end of the month; employment on December 18.",
                  "A single sportbike at the end of an otherwise empty assembly line, fluorescent light, workers&rsquo; jackets on hooks, Wisconsin winter through the loading door. Charcoal sketch with a blue-grey wash on a dark chalkboard ground, vignetted edges; any people seen from behind or with faces unresolved, no identifiable ethnicity; 3:2, no logos."))

    H.append(section(brandrow("02 &middot; Buell") + f"""
    <h2>Sixteen years, one paragraph, $125 million</h2>
    <p class="lede">Harley took 49% of Buell in 1993 for about half a million dollars, and &ldquo;substantially all of the remaining shares&rdquo; in February 1998. Eleven years after that, a new CEO wrote it down in one board meeting.</p>
    <p>Buell shipped {n('13,119')} motorcycles in 2008 and {n('9,572')} in 2009, on revenue of {n('$123.1M')} and {n('$46.5M')}. The 2009 number is after a Q4 of negative $4.0M, when dealers returned inventory. On October 14, 2009 the board &ldquo;committed to the discontinuation of its Buell product line.&rdquo; The subsequent-events note in the Q3 2009 10-Q put the cost at approximately {n('$125 million')}: $115M in 2009 and $10M in 2010; sales incentives, inventory write-downs and operating costs ~$70M; fixed-asset impairments ~$14M; one-time termination benefits ~$9M; contractual obligations ~$32M; about 60% of it cash. Roughly 80 hourly and 100 salaried positions, employment ending December 18.</p>
    {note('Keith Wandell, five months into the job &middot; 15 October 2009',
          '&ldquo;The fact is we must focus both our effort and our investment on the Harley-Davidson brand, as we believe this provides an optimal path to sustained, meaningful, long-term growth.&rdquo;',
          '&ldquo;We believe we can create a bright long-term future for our stakeholders through a single-minded focus on the Harley-Davidson brand.&rdquo;',
          '&ldquo;Buell and MV Agusta are great companies, with proud brands, high-quality exciting products and passionate enthusiasm for the motorcycle business.&rdquo; ' + link(SEC + '793952/000119312509208172/dex991.htm', '8-K Ex. 99.1, 15 Oct 2009'), tag='doc')}
    <p>The realized Buell cost was never reported on its own. It went into the 2009 restructuring plan, which expensed {n('$220.9M')} in 2009 and {n('$119.1M')} in 2010, and the FY2010 10-K closes the file in one sentence: &ldquo;The Company ceased production of Buell motorcycles at the end of October 2009.&rdquo; Buell&rsquo;s own statement said it had built &ldquo;more than 135,000 motorcycles&rdquo; since 1983. Erik Buell, eighteen months later: &ldquo;They didn&rsquo;t shut down Buell because they were mean.&rdquo; He was right. They shut it because it was a second brand in a building that has room for one.</p>
    {sowhat('02', 'Buell cost about $125M to close and was never reconciled. It was the first purchased brand a new CEO killed inside a year.', 'The sentence Wandell used is the one the company has used for every brand exit since 1996. It is not a Buell sentence. It is a Harley sentence.', 'LiveWire has a new CEO who did not start it, and the sentence has already been said: &ldquo;we leaned heavily into Touring and Electric.&rdquo;')}
    """))

    mvw = hbars([105.1, 20.1, 115.4, 111.8, 268.4, 217.4],
                ["Consideration", "IPR&D written off", "2009 impairment", "2010 impairment", "Net loss, 2008–10", "After 2011 tax reversal"],
                fills=[INK3, MAG, MAG, MAG, MAG, MAG], fmt=lambda v: f"${v:,.1f}M", vb=(720, None), row_h=36, left=190,
                sublabels=["€68.3M, Aug 2008", "day one", "FY2009 10-K", "FY2010 10-K", "discontinued ops, net of tax", "+$51.0M, Q4 2011"],
                label="MV Agusta: $105.1M of consideration; $20.1M of IPR&D written off; impairments of $115.4M and $111.8M; net loss from discontinued operations $268.4M, $217.4M after the 2011 tax reversal.",
                tips=["Total consideration €68.3M ($105.1M), incl. €47.5M of bank debt", "In-process R&D written off subsequent to the acquisition", "Goodwill $85.5M, fixed assets $19.8M, intangibles $10.1M", "Receivables $32.3M, inventory $25.2M, fixed assets $26.9M, intangibles $15.8M, other", "$29.5M + $125.8M + $113.1M", "Reversal of tax reserves on IRS agreement"])
    mv_rows = [
        ("2008 (8 Aug &ndash; 31 Dec)", ("$15.9M", "num"), ("$(31.9)M", "num"), ("<span class='hi'>$(29.5)M</span>", "num")),
        ("2009", ("$56.7M", "num"), ("$(165.4)M", "num"), ("<span class='hi'>$(125.8)M</span>", "num")),
        ("2010 (to 6 Aug)", ("$48.6M", "num"), ("$(131.0)M", "num"), ("<span class='hi'>$(113.1)M</span>", "num")),
        ("<b>Total, 24 months</b>", ("$121.2M", "num"), ("$(328.4)M", "num"), ("<span class='hi'><b>$(268.4)M</b></span>", "num")),
        ("2011: tax reserves reversed on IRS agreement", ("", "num"), ("$(0.4)M", "num"), ("+$51.0M", "num")),
        ("<b>Net</b>", ("", "num"), ("", "num"), ("<b>$(217.4)M</b>", "num")),
    ]
    H.append(section(brandrow("03 &middot; MV Agusta") + f"""
    <h2>$105 million in. $268 million out. Sold for a euro.</h2>
    <p class="lede">Announced July 11, 2008 under Jim Ziemer, closed August 8, committed for sale October 2009, gone August 6, 2010. The whole thing fits inside one Harley-Davidson CEO transition, and the filings record every dollar of it.</p>
    <p>The announcement: &ldquo;total consideration of approximately 70 million euros ($109 million), which includes the satisfaction of existing bank debt for approximately 45 million euros ($70 million),&rdquo; plus a contingent payment to Claudio Castiglioni in 2016. Ziemer: &ldquo;Motorcycles are the heart, soul and passion of Harley-Davidson, Buell and MV Agusta.&rdquo; The final allocation in the FY2009 10-K: consideration {n('&euro;68.3M ($105.1M)')}, of which &euro;47.5M ($73.2M) retired bank debt; net assets acquired {n('$95.6M')}; goodwill {n('$85.8M')}; intangibles $52.8M, of which {n('$20.1M')} was in-process research and development &ldquo;written off subsequent to the acquisition.&rdquo; A fifth of the purchase price, expensed on arrival.</p>
    {fig('02', 'MV Agusta: what went in, what was written off, what was lost', '$ millions &middot; FY2009, FY2010 and FY2011 10-Ks', mvw, 'calc', 'The first bar is what Harley paid. The next three are the filed write-offs: $20.1M of IPR&amp;D on arrival; $115.4M in 2009 (goodwill $85.5M, fixed assets $19.8M, intangibles $10.1M); $111.8M in 2010 (receivables $32.3M, inventory $25.2M, fixed assets $26.9M, intangibles $15.8M, other). The last two are the filed net loss from discontinued operations ($29.5M + $125.8M + $113.1M = $268.4M) and the same figure after the $51.0M tax-reserve reversal of Q4 2011. Impairments alone were $227.2M pre-tax, more than double the purchase price.')}
    {tbl(['Discontinued operations, as filed', 'Revenue', 'Loss before tax', 'Net loss'], mv_rows, ['40%', '20%', '20%', '20%'])}
    <p>On $105.1M of consideration that is {n('2.55 times')} the purchase price lost, or {n('$11.2M')} a month for every month Harley owned the company. The impairments alone, $115.4M in 2009 and $111.8M in 2010, come to {n('$227.2M')} pre-tax. More than double what was paid.</p>

    <h3 style="font-size:clamp(21px,2.6vw,28px); margin-top:46px">The sale, and the &euro;1 / &euro;2 / &euro;3 question</h3>
    <p>The FY2010 10-K says only that &ldquo;the Company received nominal consideration in return for the transfer of MV and related assets.&rdquo; The Sale and Purchase Agreement, filed as Exhibit 2.1 to the 8-K of August 9, 2010, is where the number lives.</p>
    <div class="kn">
      <div class="kn-row"><div class="kn-l">{ev('doc')}The shares</div><div class="kn-t">&sect;2.1.1(a): H-D Varese Holding transfers &ldquo;all rights, title and interest &hellip; in the MV Agusta Shares&rdquo; (all 120,000 ordinary shares, the entire capital of MV Agusta Motor S.p.A.) &ldquo;for a consideration of Euro 1 (one).&rdquo;</div></div>
      <div class="kn-row"><div class="kn-l">{ev('doc')}The U.S. company</div><div class="kn-t">The membership interests in MV Agusta USA LLC, for US$1.</div></div>
      <div class="kn-row"><div class="kn-l">{ev('doc')}The receivable</div><div class="kn-t">An intercompany receivable of &euro;103,789,617.60, the money Harley had lent its own subsidiary, for &euro;1.</div></div>
      <div class="kn-row"><div class="kn-l">{ev('doc')}The cash left inside</div><div class="kn-t">&sect;7.1.1: a capital increase of &ldquo;Euro 20,000,000 (twenty million)&rdquo; less sums already received, paid into escrow. The 8-K: &ldquo;the Company contributed 20 million Euros to MV as operating capital.&rdquo;</div></div>
      <div class="kn-row"><div class="kn-l">{ev('doc')}The earn-out</div><div class="kn-t">&sect;7.2.2(a): Castiglioni&rsquo;s right to the 2016 earn-out &ldquo;will be finally and irrevocably waived and dismissed with prejudice.&rdquo;</div></div>
      <div class="kn-row"><div class="kn-l">{ev('calc')}Therefore</div><div class="kn-t">&ldquo;&euro;1&rdquo; is the share price. &ldquo;&euro;3&rdquo; is the press adding the three nominal payments. &ldquo;&euro;2&rdquo; counts only the euros. All three are right. The 10-K&rsquo;s &ldquo;immaterial loss on the date of sale&rdquo; is also right: by August 2010 there was nothing left to lose.</div></div>
    </div>
    {note('Keith Wandell &middot; 6 August 2010', '&ldquo;Our decision to divest MV Agusta reflects our strategy to focus our efforts and our investment on the Harley-Davidson brand, as we believe this provides an optimal path to long-term growth.&rdquo;', tag='doc')}
    <p class="pull">In 1996 the sentence was &ldquo;core motorcycle business.&rdquo; In 2009 and 2010 it was &ldquo;the Harley-Davidson brand.&rdquo; The words repeat because the decision does.</p>
    {sowhat('03', 'MV Agusta cost $105.1M and lost $268.4M in twenty-four months. It went back to the seller for three nominal payments and &euro;20M of Harley cash.', 'It is the one time Harley bought big, and it is the reason every outside move since has been sized to be forgettable.', 'The Castiglionis got the factory back in 2010 the way they got Aermacchi&rsquo;s in 1978. Harley is now buying a 440 single from Hero. See Part V.')}
    """))

    # ═════════ PART III — TOO SMALL TO SAY ═════════
    H.append(part(2, "Too small to say", "Alta, which Harley never put a number on, and StaCyc, the one purchase that has hit every target it was given.",
                  "Alta: one sentence in one press release, no amount in any filing, bounded by Alta&rsquo;s own Form D at $5.65M, gone in six months. StaCyc: $14.9M, earn-out paid in full, 21,633 units in 2025 to LiveWire&rsquo;s 653.",
                  "Together they show what Harley actually wanted from electric. Not a motorcycle company. A battery it could learn from, and a $649 product that puts a family on a dealer floor.",
                  "Brisbane, California, 2018", "Alta Motors&rsquo; Redshift on a Harley dealer floor, one of 44 that carried it. Six months later the building was empty.",
                  "A small electric dirt bike on a polished dealership floor between two large cruisers, price tag hanging, morning light through showroom glass. Charcoal sketch with a blue-grey wash on a dark chalkboard ground, vignetted edges; any people seen from behind or with faces unresolved, no identifiable ethnicity; 3:2, no logos."))

    fd_rows = [
        ("7 Mar 2016", "$7.0M convertible notes", ("$1.77M", "num"), ("18", "num"), "Marc Fenigstein, CEO"),
        ("2 Jun 2017", "$26.1M equity (first sale 18 May 2017)", ("$12.4M", "num"), ("42", "num"), "Fenigstein, CEO"),
        ("3 Jul 2017", "$20.3M equity + debt (first sale 20 Jun 2017)", ("$15.2M", "num"), ("24", "num"), "Derek Dorresteyn, Secretary"),
        ("<b>5 Feb 2018</b> (D/A)", "Same round, amended and closed: <span class='hi'>$20,843,998</span>", ("<span class='hi'>$20.84M</span>", "num"), ("<span class='hi'>30</span>", "num"), "Arno Harris, CEO &middot; signed 2 Feb"),
        ("<b>13 Aug 2018</b>", "<span class='hi'>$5.0M debt</span> (first sale 27 Jul 2018)", ("<span class='hi'>$2.45M</span>", "num"), ("<span class='hi'>4</span>", "num"), "Harris, CEO &middot; signed 10 Aug"),
    ]
    inv = sbars([1.083, -1.106, -1.679], ["Q3 2017", "Q3 2018", "Q4 2018"], fills=[CYAN, MAG, MAG],
                fmt=lambda v: ("+" if v > 0 else "\u2212") + f"${abs(v):.1f}M",
                label="Investment income: plus $1.1M in Q3 2017; minus $1.1M in Q3 2018; minus $1.7M in Q4 2018.", vb=(720, 260),
                tips=["Q3 2017: +$1,083K", "Q3 2018: −$1,106K", "Q4 2018: −$1,679K"])
    H.append(section(brandrow("04 &middot; Alta Motors") + f"""
    <h2>One sentence, no number, six months</h2>
    <p class="lede">March 1, 2018: &ldquo;Harley-Davidson Invests In Alta Motors; Companies Will Collaborate On Future Electric Motorcycle Product Development.&rdquo; Search every filing Harley made in 2018 and 2019 for what it paid, and this is what you find.</p>
    <p>Matt Levatich, in the release: &ldquo;Alta has demonstrated innovation and expertise in EV and their objectives align closely with ours. We each have strengths and capabilities that will be mutually beneficial as we work together to develop cutting-edge electric motorcycles.&rdquo; No amount. No percentage. The Q1 2018 earnings release, filed as an 8-K exhibit on April 24, is the only Harley-Davidson SEC filing that has ever contained the word &ldquo;Alta&rdquo;: <em>&ldquo;Invested in a collaborative agreement with Alta Motors, an innovator in lightweight electric vehicles, supporting Harley-Davidson&rsquo;s commitment to lead in the electrification of the sport of motorcycling.&rdquo;</em></p>
    <p>That is the whole disclosure. A full-text search of every 10-Q and 10-K from April 2018 through December 2019 finds no equity investment, no carrying value, no impairment of an investment, no write-off, no &ldquo;privately held,&rdquo; no &ldquo;readily determinable fair value.&rdquo; The stake sat below the threshold at which a $5.7 billion company has to tell anyone what it paid. The only footprint is one line on the income statement.</p>
    {fig('03', 'Investment (loss) income, the quarter before and the two quarters after', '$ millions &middot; Q3 2018 10-Q, Q4 2018 release', inv, 'inf', 'The line ran at roughly +$1M a quarter and went to &minus;$1.1M in Q3 2018 and &minus;$1.7M in Q4 2018; full-year investment income fell from $3.58M to $0.95M. No filing attributes the swing, and the FY2018 10-K paragraph that would explain it was not retrieved (open item 1). The inference is mine: this is where a small, un-named equity stake would go when it is written to zero.')}
    <h3 style="font-size:clamp(21px,2.6vw,28px); margin-top:46px">Alta&rsquo;s own paperwork bounds it</h3>
    <p>Alta Motors was the trade name. The company was <strong>Faster Faster, Inc.</strong>, Brisbane, California, CIK 1620298, and it filed a Form D for every round it raised.</p>
    {tbl(['Filed', 'Offering', 'Sold', 'Investors', 'Signed by'], fd_rows, ['14%', '38%', '12%', '10%', '26%'])}
    <p>The round Harley joined was closed by amendment on February 2, 2018, four weeks before the announcement. Between the July 2017 notice and the February 2018 amendment the round grew by {n('$5.65M')} and {n('six')} investors. No Form D reports an equity sale after that. If Harley&rsquo;s money is in that round, and there is nowhere else in the record for it to be, the check was inside $5.65M. {ev('inf')} Harley has never stated the figure.</p>
    <ul class="tl">
      <li><b>2 Feb 2018</b><span>Alta closes its equity round at $20,843,998 (Form D/A, filed 5 Feb).</span></li>
      <li><b>1 Mar 2018</b><span>Harley announces the investment and co-development. &ldquo;We intend to be the world leader in the electrification of motorcycles.&rdquo;</span></li>
      <li><b>30 Jul 2018</b><span>&ldquo;More Roads to Harley-Davidson&rdquo;: LiveWire in 2019, &ldquo;additional models through 2022,&rdquo; $450&ndash;550M of operating investment. Alta is not mentioned.</span></li>
      <li><b>27 Jul 2018</b><span>Alta begins selling a $5.0M bridge note; $2.45M placed with four investors (Form D, filed 13 Aug).</span></li>
      <li><b>29 Aug 2018</b><span>Asphalt &amp; Rubber, sourced: Harley &ldquo;has all but removed itself from its joint motorcycle project with Alta.&rdquo; No company statement. {ev('unv')}</span></li>
      <li class="h"><b>5 Sep 2018</b><span>Harley announces &ldquo;a new advanced technology R&amp;D facility in Silicon Valley&rdquo;: about 25 staff, &ldquo;battery, power electronics, and e-machine design and development.&rdquo; Alta&rsquo;s specialty, one exit away from Alta&rsquo;s building.</span></li>
      <li><b>17 Oct 2018</b><span>Alta ceases operations. Harley to TechCrunch: &ldquo;Our collaborative efforts with Alta Motors were productive and we were pleased with the development work we partnered on.&rdquo;</span></li>
      <li><b>20 Feb 2019</b><span>BRP buys &ldquo;certain intellectual property, patents and some limited physical assets&rdquo; and says it has &ldquo;no interest in restarting operations of Alta Motors.&rdquo;</span></li>
    </ul>
    {note('The other side of the story &middot; on the record, unverified',
          'Marc Fenigstein, Alta&rsquo;s co-founder and first CEO, told RideApart in 2024 that the deal was to &ldquo;split development costs right down the line&rdquo; on Alta&rsquo;s second-generation platform, with Alta &ldquo;effectively &hellip; a supplier of [Harley&rsquo;s] next platform,&rdquo; and that when LiveWire&rsquo;s S2 Del Mar appeared, &ldquo;our drawings, our engineering CAD and our concept sketches from early 2018&rdquo; matched it &ldquo;almost one for one.&rdquo;',
          'That is his account. It is public, Harley has not answered it, and no filing supports or contradicts it. <strong>Disclosure: I know Marc Fenigstein and have worked with him since Alta closed. The quote is here because it is public and material. Weigh it knowing that.</strong>', tag='unv')}
    {sowhat('04', 'Harley paid a sum too small to disclose, learned what it needed about batteries and e-machines, and opened its own lab a week after the split leaked. Six months, one press release, no number.', 'Alta is the cleanest case in the table: the technology without the partner, at a price that never had to be explained.', 'Dust Motorcycles, May 2026: $375,000 in cash, the rest in LiveWire stock and earn-outs. The same shape, one level down, where a write-off is already priced in.')}
    """))

    units = bars([653, 21633], ["LiveWire motorcycles", "StaCyc"], fills=[MAG, CYAN], fmt=lambda v: f"{v:,.0f}", vb=(720, 280), ymax=25000, ticks=5,
                 label="2025 units: 653 LiveWire motorcycles; 21,633 StaCyc balance bikes.", tips=["Electric motorcycles, FY2025: 653", "STACYC, FY2025: 21,633"])
    glyph_rows = "".join(
        f"<div class='g-row {cls}'><div class='g-l'>{lab}</div><div class='g-n'>{val:,}</div><div class='g-g'>" + "".join("<svg class='g'><use href='#moto'/></svg>" for _ in range(max(1, round(val / 500)))) + "</div></div>"
        for lab, val, cls in [("LiveWire motorcycles, 2025", 653, "hi"), ("StaCyc, 2025", 21633, "")])
    eo_rows = [
        ("At acquisition, 4 Mar 2019", ("$14.9M", "num"), "Total consideration; $7.0M cash; goodwill $9.5M (tax-deductible); intangibles $5.3M"),
        ("Earn-out, fair value at close", ("$4.98M", "num"), "Maximum $6.537M, &ldquo;based on the achievement of sales volume targets&rdquo; over three twelve-month periods from June 2019"),
        ("Paid 2020", ("$2.18M", "num"), "First performance period met"),
        ("Paid 2021", ("$2.18M", "num"), "Second period met"),
        ("Paid 24 Jun 2022", ("$2.18M", "num"), "&ldquo;the final earnout payment.&rdquo; Third period met"),
        ("<b>Total paid</b>", ("<b>$6.54M</b>", "num"), "Effectively the maximum. Every volume milestone hit"),
    ]
    H.append(section(brandrow("05 &middot; StaCyc") + f"""
    <h2>$14.9 million, and it outsells LiveWire 33 to 1</h2>
    <p class="lede">The Q1 2019 10-Q: &ldquo;On March 4, 2019, the Company purchased certain assets and liabilities of StaCyc, Inc. for total consideration of $14.9 million including cash paid at acquisition of $7.0 million.&rdquo; The stated reason was not electrification. It was the next customer.</p>
    <p>Harley&rsquo;s filing never explains the other $7.9M. LiveWire&rsquo;s carve-out financials, filed when the SPAC closed, do: a contingent earn-out with a fair value of {n('$4.98M')} at acquisition and a maximum of $6.537M, paid {n('$2.18M')} in each of 2020, 2021 and 2022. StaCyc hit every volume target it was given.</p>
    {tbl(['StaCyc consideration', '$', 'Source: Q1 2019 10-Q; LVWR 8-K 30 Sep 2022; LVWR 10-K FY2022 R71'], eo_rows, ['30%', '14%', '56%'])}
    {note('What it was bought for &middot; their words',
          'Heather Malenshek, SVP Marketing and Brand, 5 March 2019: &ldquo;The StaCyc team shares the same vision we have for building the next generation of riders globally.&rdquo;',
          'Matt Levatich, Q1 2019 call: &ldquo;kids who are enjoying two-wheeled freedom with their families, connecting through Harley Davidson dealerships and events. Starting at $649, StaCyc products further broaden the spectrum we&rsquo;ve promised in the electric two-wheel space.&rdquo;', tag='doc')}
    <div class="duo">
      <div class="card mag"><div class="k">LiveWire electric motorcycles &middot; 2025</div><div class="big mag">653</div><p>{n('$6.1M')} of revenue, down 28%. $9,342 a unit. The company sold to the public at a $1.77B enterprise value.</p></div>
      <div class="card"><div class="k">StaCyc &middot; 2025</div><div class="big cy">21,633</div><p>{n('$19.6M')} of revenue, up 7%. $906 a unit. {n('76%')} of LiveWire&rsquo;s product revenue, from a $14.9M purchase.</p></div>
    </div>
    {glyphs}
    <div class="glyphs">
      <div class="g-h">Units, not percentages &middot; one glyph = 500 vehicles</div>
      {glyph_rows}
    </div>
    {fig('04', 'LiveWire Group unit sales by product, 2025', 'LiveWire FY2025 results, 10 Feb 2026', units, 'doc', 'Thirty-three StaCycs for every LiveWire motorcycle. Three-quarters of the product revenue of the company Harley sold to the public at $1.77 billion comes from a $14.9M purchase of a company that makes $649 balance bikes for three-year-olds.')}
    <h3 style="font-size:clamp(21px,2.6vw,28px); margin-top:46px">The older precedent: Eaglemark</h3>
    <p>In January 1993 Harley &ldquo;invested $10 million for a 49% interest in Eaglemark Financial Services,&rdquo; which financed dealers&rsquo; floor plans and customers&rsquo; motorcycles. In November 1995 it bought the rest for &ldquo;approximately $45 million.&rdquo; {n('$55M')} for the business that became HDFS, made {n('$248M')} of operating income in 2024, and that KKR and PIMCO paid roughly 1.75 times book for a tenth of in 2025.</p>
    <p class="pull">The two outside purchases that were kept and made money are the two that make money on somebody else&rsquo;s product on a Harley dealer&rsquo;s floor. Neither has ever been asked to build a motorcycle.</p>
    {sowhat('05', 'StaCyc is the only piece of Harley&rsquo;s electric decade that has ever met a volume target, and the targets it met are the ones a dealer can see from the service counter.', 'A family, a kid, a first purchase, a reason to come back. That is what Harley bought in 2019. The motorcycle company came with it.', 'If LiveWire is sold, merged or wound down, watch whether StaCyc comes back into the motor company. That is the tell.')}
    """))

    # ═════════ PART IV — WHAT IT BUILDS ═════════
    H.append(part(3, "What it builds", "Three in-house programs, two outcomes, and the rule that falls out of them.",
                  "The Milwaukee-Eight and the Revolution Max got built and kept. The Street, the one time Harley built its own small bike in its own plants, lost money, closed the Indian plant, and handed the segment to Hero.",
                  "Harley develops from within when the product carries the full brand at the full price. Below that line it has never once succeeded on its own, and it stopped trying in 2020.",
                  "Bawal, Haryana, 2014", "The Street 750 line at Harley&rsquo;s own Indian plant. Closed September 2020; one month later the Hero agreements were signed.",
                  "A liquid-cooled middleweight cruiser being assembled in a bright modern Indian plant, workers in blue, monsoon sky outside. Charcoal sketch with a blue-grey wash on a dark chalkboard ground, vignetted edges; any people seen from behind or with faces unresolved, no identifiable ethnicity; 3:2, no logos."))
    H.append(section(brandrow("06 &middot; Built in-house") + f"""
    <h2>Two engines kept. One small bike lost money and left.</h2>
    <p class="lede">The table has three things Harley built rather than bought in the last fifteen years. Two are still the engines of its highest-priced lines. The third is the reason the Sprint is a Hero.</p>
    <p><strong>Street 500/750, 2013.</strong> &ldquo;The first all-new platform from Harley-Davidson in 13 years,&rdquo; liquid-cooled Revolution X, for &ldquo;young adults in cities around the world,&rdquo; built in Kansas City for North America and in Bawal, India, for everywhere else. On September 24, 2020 Harley filed an 8-K &ldquo;discontinuing its sales and manufacturing operations in India&rdquo;: about 70 employees, &ldquo;approximately {n('$75 million')}&rdquo; of restructuring expense for the actions approved that month, of which &ldquo;contract termination and other costs of approximately $67 million.&rdquo; One month later it signed the Hero agreements. The verdict came from the CFO, Gina Goetter, on the Q3 2021 call: &ldquo;the decision to exit the unprofitable Street and Legacy Sportster bikes.&rdquo;</p>
    <p><strong>Milwaukee-Eight, 2016, and Revolution Max, 2021.</strong> &ldquo;The ninth Big Twin in its history&rdquo; and &ldquo;a clean-sheet, advanced-design effort.&rdquo; Neither release gives a program cost or a development time. Both are still the engines of the two lines that carry the company. The Pan America is the one genuinely new segment Harley has entered in twenty years by building rather than buying, and it is a $20,000 motorcycle.</p>
    {plain('The rule, in one sentence', 'Harley-Davidson develops from within when the product will carry the full brand at the full price, and reaches outside for everything below it.', 'The one time it built its own small bike in its own plants, it lost money, closed the plant, and licensed the segment to the partner who could build the engine for &#8377;2.29 lakh.')}
    {note('Industry context, not a filing', 'York builds Touring and Softail with an IAM workforce and a cost base built for $25,000 motorcycles. A 440 single at a York burden rate is not a $6,000 motorcycle and everyone in the planning office knows it. That is the calculation behind &ldquo;finalizing the specific production plans.&rdquo; I have run it.', tag='ind')}
    {sowhat('06', 'In-house works above the big-twin price line and has never worked below it.', 'Everything below the line gets bought, licensed or partnered. That is not a strategy statement; it is the record.', 'The 883 is the first air-cooled twin program since the Evolution and the first time since Street that Harley has tried to build below the line. Part V.')}
    """))

    # ═════════ PART V — THE SPRINT RHYME ═════════
    H.append(part(4, "The Sprint rhyme", "1960, an Aermacchi. 2026, a Hero. The same hole below the big twin, and somebody else&rsquo;s engine in it both times.",
                  "The first Sprint was built in Varese by a company Harley half-owned. The new one runs a 440 single Hero co-developed and builds in Neemrana for a &#8377;2.29 lakh motorcycle. Where the Sprint is built and what it costs are undecided.",
                  "Those two facts are the test of the rule. Hero-built means the rule held and the plan&rsquo;s &ldquo;existing platforms&rdquo; include a licensee&rsquo;s. York-built means it is not a $6,000 motorcycle, and Street says what happens next.",
                  "Neemrana, Rajasthan, 2023", "The X440 on Hero&rsquo;s line at the Garden Factory. Co-developed at Hero&rsquo;s CIT, priced at &#8377;2,29,000. The Sprint&rsquo;s engine.",
                  "A 440cc single-cylinder roadster, oil-cooled engine exposed, on a stand in a clean Indian factory with trees visible through open bays. Charcoal sketch with a blue-grey wash on a dark chalkboard ground, vignetted edges; any people seen from behind or with faces unresolved, no identifiable ethnicity; 3:2, no logos.", img="neemrana.jpg"))
    H.append(section(brandrow("07 &middot; Aermacchi to Hero") + f"""
    <h2>Same hole, somebody else&rsquo;s engine</h2>
    <p class="lede">The first Harley-Davidson Sprint was an Aermacchi. Harley bought half of the Varese motorcycle division in 1960, for about a quarter of a million dollars by the accounts that survive, because the 125cc Hummer left a gap between it and the big twins that Japan was about to fill.</p>
    <p>It sold the Sprint for fourteen years, won three 250cc world championships (1974&ndash;76) and a 350 title with Walter Villa on Aermacchi-built Harleys, and then in 1978 AMF sold the factory and the rights to the Castiglioni brothers. Thirty years later Harley bought MV Agusta from the same family, and sold it back to them for a euro. {ev('unv')} Prices and dates for Aermacchi are secondary-sourced; open item 3.</p>
    <p>Sixty-six years on the Sprint returns, into the same hole, on somebody else&rsquo;s engine. Hero&rsquo;s July 3, 2023 release: the X440&rsquo;s 440cc single was &ldquo;co-developed by Hero MotoCorp and Harley-Davidson at the Hero Center for Innovation and Technology,&rdquo; built at the &ldquo;Garden Factory at Neemrana, Rajasthan,&rdquo; and priced from {n('&#8377;2,29,000')}, about {n('$2,760')}. Trade reporting puts X440 sales at 8,974 units in the nine months to December 2024. {ev('unv')}</p>
    <ul class="tl">
      <li><b>Jul 2025</b><span>Zeitz, Q2 call: the Sprint has &ldquo;been in development since 2021,&rdquo; is &ldquo;targeting an entry price below $6,000,&rdquo; and will be &ldquo;not only highly accessible, but also profitable.&rdquo;</span></li>
      <li><b>Nov 2025</b><span>Starrs, Q3 call: &ldquo;a bike that&rsquo;s lighter and easier to maneuver &hellip; a bike that&rsquo;s more affordable.&rdquo;</span></li>
      <li><b>May 2026</b><span>Starrs, Q1 call: &ldquo;returning to a space that we haven&rsquo;t been in since the 1960s.&rdquo; On production: &ldquo;we&rsquo;re finalizing the specific production plans.&rdquo; Trade reporting the same day: the target is now &ldquo;less than $10,000&rdquo; and the build location is undecided. {ev('unv')}</span></li>
      <li><b>Jun 2026</b><span>Hero&rsquo;s CEO: &ldquo;If Harley finds suitability for the product in its global markets, it can take it from Hero to sell elsewhere; that decision rests with Harley.&rdquo; {ev('unv')} A dealer letter: order X350 RAs now, &ldquo;well in advance of availability of Sprint.&rdquo;</span></li>
      <li><b>Jul 2026</b><span>Starrs, Q2 call: &ldquo;we expect to ship Sprint end of this year.&rdquo; No price, no plant, no mention of Hero.</span></li>
    </ul>
    <p>Nobody at Harley has said where the Sprint will be built or what it will cost. Both facts are the test. If the Sprint ships from Neemrana at a Hero cost base, the rule held and the &ldquo;existing platforms&rdquo; in Starrs&rsquo;s plan include one that belongs to a licensee in Rajasthan. If it ships from York at a York cost base, it will not be a $6,000 motorcycle, and the Street&rsquo;s history says what happens next.</p>
    {sowhat('07', 'The company has been trying to fill the space below the big twin with somebody else&rsquo;s motorcycle since Eisenhower. It has never once filled it with its own.', 'The Sprint is a channel product for a dealer network with 554 U.S. stores and half the retail volume it had in 2014. It will be called &ldquo;accessible&rdquo; and never core.', 'The two facts that decide it, plant and MSRP, are both due before the end of 2026. Watch the Q3 call.')}
    """))

    H.append(section(brandrow("08 &middot; The 883") + f"""
    <h2>The other half of the test</h2>
    <p class="lede">&ldquo;Our iconic Harley-Davidson Sportster will be returning in 2027.&rdquo; Air-cooled, &ldquo;middleweight,&rdquo; &ldquo;accessible starting price point,&rdquo; &ldquo;the most requested motorcycle from both our riders and our dealers.&rdquo;</p>
    <p>Starrs, May 2026: &ldquo;we have the cost at a place where we are comfortable against the expected MSRP.&rdquo; Trade reporting: an 883cc air-cooled twin, about $10,000, built in York. {ev('unv')} It is the first air-cooled twin program since the Evolution and, if the reporting holds, the first time in the record that the space below the big twin is being filled from Harley&rsquo;s own plant, at a price where Harley has never made money. Raymond James, on the same call: &ldquo;there&rsquo;s a reason why Sportster was discontinued, right? It was hard to make money.&rdquo;</p>
    <div class="duo">
      <div class="card"><div class="k">If the 883 is built in York and makes money at ~$10,000</div><div class="big cy">Rule breaks</div><p>The plan has a second lever, and Starrs is the first CEO in the record to fill the hole from inside.</p></div>
      <div class="card mag"><div class="k">If the Sprint is Hero-built and the 883 slips or moves</div><div class="big mag">Rule holds</div><p>Back to the Bricks is a Touring and Softail plan with a licensee&rsquo;s motorcycle at the bottom, and the undecided Sprint plant was the tell.</p></div>
    </div>
    {sowhat('08', 'Plant and price, for both bikes. Everything else about the small-bike strategy is a press release.', 'A Sportster built in York that makes money at $10,000 would be the first time since 1960 that Harley filled the space below the big twin with its own motorcycle.', 'No. 02 carried the volume arithmetic: the 883 has to deliver most of the plan&rsquo;s growth on its own. The build decision is the plan.')}
    """))

    # ═════════ PART VI — THE FINAL WORD ═════════
    H.append(part(5, "The final word", "Seven CEOs, one cycle, and what every purchase was actually for.",
                  "Each CEO&rsquo;s outside moves are the next CEO&rsquo;s focus story. LiveWire is eleven months into a CEO who did not start it, with the sentence already said and the cheapest unwind in the table.",
                  "The parent never wanted the electric motorcycle. It wanted the floor traffic. Read that way, the whole record is one decision.",
                  "Juneau Avenue", "The headquarters, where every one of these decisions was signed. The building has room for one brand.",
                  "A red-brick industrial headquarters block on a Milwaukee street at dusk, one lit window, wet pavement. Charcoal sketch with a blue-grey wash on a dark chalkboard ground, vignetted edges; any people seen from behind or with faces unresolved, no identifiable ethnicity; 3:2, no signage."))
    ceo_rows = [
        ("Richard Teerlink", "&ndash;1997", "Eaglemark 49% and 100%; Buell 49%", "Holiday Rambler"),
        ("Jeffrey Bleustein", "1997&ndash;2005", "Buell to ~100%", "none"),
        ("James Ziemer", "2005&ndash;2009", "MV Agusta", "none"),
        ("Keith Wandell", "2009&ndash;2015", "none", "<span class='hi'>Buell; MV Agusta</span>"),
        ("Matt Levatich", "2015&ndash;2020", "Thailand plant; Alta; StaCyc; Qianjiang; Silicon Valley R&amp;D; LiveWire as a brand", "Alta"),
        ("Jochen Zeitz", "2020&ndash;2025", "Hero licence; LiveWire SPAC; KYMCO; HDFS to KKR/PIMCO", "<span class='hi'>India manufacturing; Street; Sportster; Bronx</span>; Rev Max to Thailand"),
        ("Artie Starrs", "Oct 2025&ndash;", "Sprint; Sportster 883 return; Dust (via LiveWire)", "Rev Max back from Thailand; &ldquo;leaned heavily into Touring and Electric&rdquo;"),
    ]
    H.append(section(brandrow("09 &middot; The cycle") + f"""
    <h2>Each CEO&rsquo;s purchases are the next CEO&rsquo;s focus story</h2>
    <p class="lede">Bleustein bought Buell; Wandell shut it. Ziemer bought MV; Wandell sold it. Levatich bought Alta, StaCyc, the QJ deal and the Thailand plant; Zeitz kept the two that fill dealer floors and reversed the one that built motorcycles offshore. Zeitz spun LiveWire and sold the finance company; Starrs brought Rev Max home and brought back a motorcycle discontinued four years earlier.</p>
    {tbl(['CEO', 'Tenure', 'Bought or started', 'Sold, shut or reversed'], ceo_rows, ['18%', '12%', '38%', '32%'])}
    <p>Buell lasted sixteen years under Harley ownership and eleven months into a new CEO. MV lasted fourteen months into one. LiveWire is eleven months into Starrs. That is not a strategy; it is a cycle, and the table is its record.</p>
    {sowhat('09', 'Seven CEOs, and the outside moves reset every five to seven years, with the same sentence.', 'What survives the reset is whatever makes money on somebody else&rsquo;s product on a dealer&rsquo;s floor: HDFS, StaCyc, the licences.', 'The next reset is LiveWire&rsquo;s, and it has a date: cash to about May 2027, the $75M note due December 15, 2027.')}
    """))

    H.append(section(brandrow("10 &middot; Analysis, not reporting") + f"""
    <h2>What it was for</h2>
    <p class="lede">Everything above this line is filed. This section is judgment, and says so.</p>
    <div class="kn">
      <div class="kn-row"><div class="kn-l">{ev('inf')}LiveWire</div><div class="kn-t">It is following the Buell and MV Agusta script, and the script has four lines. A CEO who did not start it. The focus sentence, already written: &ldquo;Over the last several years, we leaned heavily into Touring and Electric. Going forward, we are shifting to a more rider-centric portfolio.&rdquo; A cheap unwind: the public minority is roughly $28M at recent prices, the assets are pledged to Harley under the $75M secured note, and Harley &ldquo;does not plan to make additional investments&rdquo; (No. 02 &sect;3). And a date: cash to about May 2027, the note due December 15, 2027. Buell cost $125M to shut. MV cost $268M. LiveWire&rsquo;s losses are already consolidated; the unwind costs Harley a write-down on a note it holds against collateral it built. It is the cheapest exit in the table.</div></div>
      <div class="kn-row"><div class="kn-l">{ev('inf')}StaCyc and Dust</div><div class="kn-t">The two pieces of LiveWire with a future are the two that were never electric motorcycles. StaCyc is a dealer-traffic product with a margin and a five-year record of hitting volume targets. Dust is an option on off-road electric that cost $375,000 in cash and $3.5M all-in before earn-outs. It is the Alta structure, done inside a subsidiary this time, so the write-off, if it comes, lands in a segment Harley has already told investors to look past. If LiveWire is sold, merged or wound down, watch whether these two are carved back into the motor company. That would be the tell.</div></div>
      <div class="kn-row"><div class="kn-l">{ev('ind')}The Sprint</div><div class="kn-t">Hero-built or Hero-engined; a channel product for a dealer network with 554 U.S. stores and half the retail it had in 2014; described as &ldquo;accessible&rdquo; and never as core; kept as long as it does not carry a Harley badge into a Harley segment. Volume will matter more than margin because the margin is Hero&rsquo;s.</div></div>
      <div class="kn-row"><div class="kn-l">{ev('ind')}The 883</div><div class="kn-t">The one that decides whether Starrs is different. Build location and MSRP are the two facts that matter; both were open items in No. 02 and both are still open.</div></div>
    </div>
    <div class="final">
      <div class="h">{ev('inf')}The final word &middot; Harley-Davidson</div>
      <h3>Harley doesn&rsquo;t want electric. It wants floor traffic.</h3>
      <p>The Milwaukee-Eight and the Revolution Max got built because a Touring bike and a Pan America carry a $25,000 price that pays for an engine program. A 440 single, a balance bike, a battery and a consumer loan book do not, and every one of them was bought, licensed or partnered. Kept when it feeds the dealer. Dropped when it competes with the badge.</p>
      <p>Read the electric decade that way and it stops looking like a series of mistakes. Alta was a battery lesson bought for a sum too small to disclose. LiveWire was an option on a category, sold to the public so the losses would sit somewhere else until consolidation brought them home. StaCyc was the only part of it Harley ever wanted for its own sake: a <b class="n">$649</b> product that puts a family on a dealer floor and brings them back in ten years for a Sportster. <strong>It is the one part of the electric decade the company has never had to write down, and it is the one that was never an electric motorcycle.</strong></p>
      <p>I ran product at Harley. I know the meeting where a program gets its cost target, and I know which programs never get one because the answer is already known. The Sprint got one in 2021 and is still &ldquo;finalizing production plans&rdquo; in 2026. That is the answer.</p>
      <p>Ground Truth No. 02 ended by asking which brick LiveWire is under. This one ends with the question underneath that. <strong>The record says Harley keeps what fills the dealer floor and sells what competes with the badge. Which of those is the Sprint?</strong></p>
    </div>
    """))

    # ═════════ SOURCES ═════════
    src = [
        ("Form 10-K, FY1994", "Harley-Davidson, Inc.", "Mar 1995", "Eaglemark $10M for 49%; Buell 49%; Holiday Rambler acquired Dec 1986", SEC + "793952/0000950131-95-000813.txt", "0000950131-95-000813"),
        ("Form 10-K, FY1996", "Harley-Davidson, Inc.", "Mar 1997", "Eaglemark remainder ~$45M (Nov 1995); Transportation Vehicles segment sold ~$105M, gain $22.6M, &ldquo;core motorcycle business&rdquo;", SEC + "793952/000091205797011157/0000912057-97-011157.txt", "0000912057-97-011157"),
        ("8-K, MV Agusta announcement", "Harley-Davidson, Inc.", "11 Jul 2008", "~&euro;70M ($109M) incl. ~&euro;45M of bank debt; contingent payment 2016; Ziemer quote", SEC + "793952/000089706908001146/cmw3628a.htm", "0000897069-08-001146"),
        ("Form 10-Q, Q3 2008", "Harley-Davidson, Inc.", "30 Oct 2008", "MV closing 8 Aug 2008; &euro;68.3M ($105.1M); initial goodwill $87.9M, IPR&amp;D $16.6M", SEC + "793952/000119312508220204/d10q.htm", "0001193125-08-220204"),
        ("8-K Ex. 99.1, Q3 2009 results", "Harley-Davidson, Inc.", "15 Oct 2009", "Buell discontinuation, ~$125M; MV divestiture; Wandell &ldquo;focus&rdquo; sentences; Q3 impairments $14.2M / $18.9M", SEC + "793952/000119312509208172/dex991.htm", "0001193125-09-208172"),
        ("Form 10-Q, Q3 2009 &middot; Note 19", "Harley-Davidson, Inc.", "30 Oct 2009", "Buell exit cost by category; MV goodwill $85.6M; earn-out terms", SEC + "793952/000119312509218615/R22.xml", "0001193125-09-218615"),
        ("Form 10-K, FY2009 &middot; MV note", "Harley-Davidson, Inc.", "23 Feb 2010", "Final allocation; goodwill $85.75M; IPR&amp;D $20.1M; 2009 impairment $115.4M; discontinued ops 2008&ndash;09", SEC + "793952/000119312510037160/R9.xml", "0001193125-10-037160"),
        ("8-K, MV sale &middot; Ex. 2.1 Sale and Purchase Agreement", "Harley-Davidson, Inc.", "9 Aug 2010", "&euro;1 / $1 / &euro;1; &euro;20.0M capital increase; earn-out waived; prior write-downs $162.6M net", SEC + "793952/000119312510183610/dex21.htm", "0001193125-10-183610"),
        ("Form 10-K, FY2010 &middot; discontinued operations", "Harley-Davidson, Inc.", "24 Feb 2011", "2010 impairment $111.8M; &ldquo;nominal consideration&rdquo;; loss table 2008&ndash;10; Buell production ceased Oct 2009", SEC + "793952/000119312511045258/R10.xml", "0001193125-11-045258"),
        ("8-K Ex. 99.1, Q4 2011 results", "Harley-Davidson, Inc.", "24 Jan 2012", "$51.0M benefit on discontinued operations; IRS agreement; &ldquo;no further financial adjustments related to MV Agusta&rdquo;", SEC + "793952/000119312512021080/d287412dex991.htm", "0001193125-12-021080"),
        ("Form 10-K, FY2014", "Harley-Davidson, Inc.", "Feb 2015", "694 U.S. dealerships; 2014 retail", SEC + "793952/000079395215000009/hog12-31x201410xk.htm", "0000793952-15-000009"),
        ("8-K Ex. 99.1, Q1 2018 results", "Harley-Davidson, Inc.", "24 Apr 2018", "The only &ldquo;Alta&rdquo; sentence in any H-D filing", SEC + "793952/000079395218000017/a8kq12018exhibit991.htm", "0000793952-18-000017"),
        ("8-K Ex. 99.1, More Roads", "Harley-Davidson, Inc.", "30 Jul 2018", "LiveWire 2019; models through 2022; $450&ndash;550M opex, $225&ndash;275M capex; Asia small-displacement alliance", SEC + "793952/000079395218000046/exhibit991-strategypressre.htm", "0000793952-18-000046"),
        ("Form 10-Q, Q3 2018", "Harley-Davidson, Inc.", "8 Nov 2018", "Investment (loss) income &minus;$1,106K; no Alta, no equity-investment note", SEC + "793952/000079395218000057/R2.htm", "0000793952-18-000057"),
        ("Form D / D/A chain", "Faster Faster, Inc. (Alta Motors)", "2016&ndash;2018", "Five Reg D notices; round closed $20,843,998 (D/A, 5 Feb 2018); $5.0M bridge (13 Aug 2018)", SEC + "1620298/000162029818000001/primary_doc.xml", "0001620298-18-000001 &middot; -18-000002"),
        ("Form 10-Q, Q1 2019 &middot; goodwill note", "Harley-Davidson, Inc.", "9 May 2019", "StaCyc: $14.9M total; $7.0M cash; goodwill $9.5M; intangibles $5.3M", SEC + "793952/000079395219000021/hog-03312019x10q.htm", "0000793952-19-000021"),
        ("Form 10-K, FY2019 &middot; R80&ndash;R82", "Harley-Davidson, Inc.", "19 Feb 2020", "StaCyc XBRL details; goodwill roll-forward +$9,520K", SEC + "793952/000079395220000008/R80.htm", "0000793952-20-000008"),
        ("8-K, India exit", "Harley-Davidson, Inc.", "24 Sep 2020", "Discontinuing India sales and manufacturing; ~70 employees; ~$75M; $67M contract termination", SEC + "793952/000079395220000097/hog-20200923.htm", "0000793952-20-000097"),
        ("8-K Ex. 99.1, LiveWire / ABIC", "Harley-Davidson, Inc.", "13 Dec 2021", "$1.77B EV; H-D $100M; KYMCO $100M; StaCyc included in LiveWire", SEC + "793952/000119312521354631/d262169dex991.htm", "0001193125-21-354631"),
        ("8-K Ex. 99.1, carve-out financial statements", "LiveWire Group, Inc.", "30 Sep 2022", "StaCyc earn-out: $4,978K fair value; $0&ndash;$6,537K; $2,180K paid 2020, 2021, 2022", SEC + "1898795/000119312522255710/d378827dex991.htm", "0001193125-22-255710"),
        ("Form 10-K, FY2022 &middot; R71", "LiveWire Group, Inc.", "6 Mar 2023", "Contingent consideration roll-forward; goodwill $8,327K", SEC + "1898795/000189879523000023/R71.htm", "0001898795-23-000023"),
        ("8-K, Dust Motorcycles APA and KYMCO agreement", "LiveWire Group, Inc.", "22 May 2026", "$375K cash; $500K stock; 3 &times; $875K stock; earn-outs to $11.25M; KYMCO five-year exclusivity", SEC + "1898795/000119312526237206/d128514d8k.htm", "0001193125-26-237206"),
        ("8-K Ex. 99.1, Q2 2026 results", "LiveWire Group, Inc.", "23 Jul 2026", "267 motorcycles; 5,223 StaCyc; Honcho production; Dust closed", SEC + "1898795/000189879526000064/lvwrexhibit9916-30x2026.htm", "0001898795-26-000064"),
        ("Form 10-K, FY2025", "Harley-Davidson, Inc.", "26 Feb 2026", "554 U.S. dealerships; HDFS 9.8% to KKR/PIMCO; Thailand", SEC + "793952/000079395226000011/hog-20251231.htm", "0000793952-26-000011"),
    ]
    src_rows = [(f"<strong>{d}</strong><br><span style='color:var(--ink-3)'>{who}</span>", when, what, (f"{link(url, 'Open on EDGAR &rarr;')}<br><span style='color:var(--ink-3);font-size:10px'>{acc}</span>", "num")) for d, who, when, what, url, acc in src]
    rel = [
        ("H-D release &middot; Alta investment", "1 Mar 2018", "https://investor.harley-davidson.com/news/news-details/2018/HARLEY-DAVIDSON-INVESTS-IN-ALTA-MOTORS-COMPANIES-WILL-COLLABORATE-ON-FUTURE-ELECTRIC-MOTORCYCLE-PRODUCT-DEVELOPMENT/default.aspx"),
        ("H-D release &middot; Silicon Valley R&amp;D facility", "5 Sep 2018", "https://investor.harley-davidson.com/news/news-details/2018/Harley-Davidson-Creates-New-Advanced-Technology-RD-Facility-In-Silicon-Valley/default.aspx"),
        ("H-D release &middot; StaCyc acquisition", "5 Mar 2019", "https://investor.harley-davidson.com/news/news-details/2019/Harley-Davidson-Acquires-StaCyc-Inc.-Maker-Of-Electric-Powered-Two-Wheelers-For-Kids/default.aspx"),
        ("H-D release &middot; Qianjiang", "19 Jun 2019", "https://investor.harley-davidson.com/news/news-details/2019/Harley-Davidson-To-Build-Riders-By-Expanding-Access-In-Asia-With-Small-Displacement-Motorcycle/default.aspx"),
        ("H-D release &middot; Hero MotoCorp agreements", "27 Oct 2020", "https://investor.harley-davidson.com/news/news-details/2020/Harley-Davidson--Hero-Motocorp-Announce-Agreements-For-India-Market/default.aspx"),
        ("H-D release &middot; MV Agusta sale", "6 Aug 2010", "https://www.prnewswire.com/news-releases/harley-davidson-finalizes-sale-of-mv-agusta-100125319.html"),
        ("H-D release &middot; Street platform", "4 Nov 2013", "https://www.prnewswire.com/news-releases/harley-davidson-announces-new-motorcycle-platform-230577261.html"),
        ("H-D release &middot; Milwaukee-Eight", "23 Aug 2016", "https://www.prnewswire.com/news-releases/harley-davidson-launches-all-new-milwaukee-eight-engine-300316973.html"),
        ("H-D Media Kit &middot; Revolution Max 1250", "22 Feb 2021", "https://h-dmediakit.com/us/news-articles/harley-davidson-revolution-max-1250-engine-is-tuned-for-adventure.html"),
        ("H-D release &middot; KKR / PIMCO", "30 Jul 2025", "https://investor.harley-davidson.com/news/news-details/2025/Harley-Davidson-Announces-Strategic-Partnership-with-KKR-and-PIMCO/default.aspx"),
        ("H-D release &middot; Rev Max returns to U.S.", "9 Jun 2026", "https://investor.harley-davidson.com/news/news-details/2026/HarleyDavidson-Announces-Return-of-Revolution-Max-Production-to-U-S--Facilities/default.aspx"),
        ("Hero MotoCorp release &middot; X440", "3 Jul 2023", "https://www.heromotocorp.com/content/dam/hero-aem-website/in/media-center/press-release/press-release-harley-davidson-x440-jul3-23.pdf"),
        ("LiveWire release &middot; FY2025 results", "10 Feb 2026", "https://investor.livewire.com/news-events-1/news/news-details/2026/LiveWire-Group-Inc--Reports-2025-Fourth-Quarter-and-Full-Year-Financial-Results/default.aspx"),
        ("LiveWire release &middot; Dust Moto", "19 May 2026", "https://www.businesswire.com/news/home/20260519308777/en/LiveWire-Group-Inc.-Acquires-Dust-Moto"),
        ("LiveWire release &middot; S4 Honcho production", "8 Jun 2026", "https://www.businesswire.com/news/home/20260608727335/en/LiveWire-Group-Inc.-Commences-Production-of-AllNew-S4-Honcho-MiniMoto-Models"),
        ("BRP release &middot; Alta assets", "20 Feb 2019", "https://ir.brp.com/news-releases/news-release-details/brp-purchases-select-assets-alta-motors-part-its-ongoing"),
        ("Transcript &middot; Q1 2019 call (Levatich on StaCyc)", "23 Apr 2019", "https://www.fool.com/earnings/call-transcripts/2019/04/23/harley-davidson-hog-q1-2019-earnings-call-transcri.aspx"),
        ("Transcript &middot; Q3 2021 call (Goetter on Street)", "27 Oct 2021", "https://www.fool.com/earnings/call-transcripts/2021/10/28/harley-davidson-inc-hog-q3-2021-earnings-call-tran/"),
        ("Transcript &middot; Q2 2025 call (Zeitz on Sprint)", "30 Jul 2025", "https://www.investing.com/news/transcripts/earnings-call-transcript-harleydavidson-sees-19-revenue-drop-in-q2-2025-93CH-4160744"),
        ("Transcript &middot; Q1 2026 call (Starrs)", "5 May 2026", "https://www.fool.com/earnings/call-transcripts/2026/05/05/harley-davidson-hog-q1-2026-earnings-transcript/"),
        ("Transcript &middot; Q2 2026 call (Starrs)", "23 Jul 2026", "https://www.benzinga.com/news/26/07/60642023/transcript-harley-davidson-q2-2026-earnings-conference-call"),
    ]
    rel_rows = [(d, when, (link(url, 'Open &rarr;'), "num")) for d, when, url in rel]
    sec_rows = [
        ("Asphalt &amp; Rubber &middot; Alta break-up (sourced report)", "29 Aug 2018", (link("https://www.asphaltandrubber.com/rumors/harley-davidson-alta-motors-break-up/", "Open &rarr;"), "num")),
        ("TechCrunch &middot; Alta closure; H-D statement", "18 Oct 2018", (link("https://techcrunch.com/2018/10/18/e-moto-startup-alta-motors-reportedly-powers-down/", "Open &rarr;"), "num")),
        ("RideApart &middot; Fenigstein interview", "2024", (link("https://www.rideapart.com/features/760044/alta-motors-ceo-talks-acquisition-dissolving-harley-davidson/", "Open &rarr;"), "num")),
        ("Motorcycle.com &middot; Sprint price and plant (deck paraphrase)", "5 May 2026", (link("https://www.motorcycle.com/bikes/new-model-preview/2027-harley-davidson-sprint-wont-reach-sub-6-000-target-price-44664607", "Open &rarr;"), "num")),
        ("Motorcycle.com &middot; Sportster 883 (deck paraphrase)", "5 May 2026", (link("https://www.motorcycle.com/bikes/new-model-preview/harley-davidson-is-bringing-back-the-air-cooled-sportster-for-2027-44664601", "Open &rarr;"), "num")),
        ("Autocar Professional &middot; X440 volumes", "30 Jan 2025", (link("https://www.autocarpro.in/analysis-sales/hero-motocorp-sells-12188-harley-x440-and-mavrick-440-bikes-in-april-december-2024-up-77-124662", "Open &rarr;"), "num")),
        ("motorcycles.news &middot; Hero CEO on Sprint", "23 Jun 2026", (link("https://www.motorcycles.news/en/harley-davidson-sprint-hero-alliance-global-market/", "Open &rarr;"), "num")),
        ("Powersports Business &middot; dealer letter, X350 RA and Sprint", "25 Jun 2026", (link("https://powersportsbusiness.com/news/harley-davidson/2026/06/25/rumored-sprint-gains-momentum-as-harley-dealer-letter-revealed/", "Open &rarr;"), "num")),
        ("Roadracing World &middot; Buell statement, 135,000 units", "15 Oct 2009", (link("https://www.roadracingworld.com/news/updated-again-harley-davidson-shuts-down-buell-plans-to-sell-mv-agusta/", "Open &rarr;"), "num")),
        ("Powersports Business &middot; Erik Buell", "14 Mar 2011", (link("https://powersportsbusiness.com/features/2011/03/14/3142011-putting-his-sport-bike-theory-to-test/", "Open &rarr;"), "num")),
        ("Deseret News / AP &middot; Holiday Rambler sale", "26 Jan 1996", (link("https://www.deseret.com/1996/1/26/19221303/harley-to-sell-its-rambler-unit/", "Open &rarr;"), "num")),
        ("Family RVing &middot; Holiday Rambler $155M", "Oct 2003", (link("https://familyrvingmag.com/2003/10/01/fifty-years-of-holiday-rambler/", "Open &rarr;"), "num")),
        ("Curbside Classic; Classic Bike Hub; Motorcycle Classics; Rider &middot; Aermacchi", "various", (link("https://www.curbsideclassic.com/blog/two-wheelers/harley-davidson-sprint-the-spaghetti-hoglet/", "Open &rarr;"), "num")),
    ]
    H.append(section(f"""
    <div class="eyebrow">11 &middot; Sources</div>
    <h2>Every document, linked</h2>
    <p class="lede">Each row in the first table opens the filing on EDGAR. The second is company releases and full call transcripts. The third is secondary, and nothing rests on it that is not marked Unverified in the text.</p>
    {tbl(['Document', 'Filed', 'What it supports', 'Link'], src_rows, ['24%', '11%', '45%', '20%'])}
    <h3 style="font-size:clamp(21px,2.6vw,28px); margin-top:40px">Releases and transcripts</h3>
    {tbl(['Document', 'Date', 'Link'], rel_rows, ['64%', '18%', '18%'])}
    <h3 style="font-size:clamp(21px,2.6vw,28px); margin-top:40px">Secondary, used only where flagged</h3>
    {tbl(['Source', 'Date', 'Link'], sec_rows, ['64%', '18%', '18%'])}
    """))

    # ═════════ METHOD & STANDING ═════════
    open_rows = [
        ("1", "Alta investment amount", "Not in any H-D filing (full-text search, 2018&ndash;2019). The bound in &sect;04 is inferred from Faster Faster, Inc.&rsquo;s Form D chain. The FY2018 10-K MD&amp;A paragraph on investment income was not retrieved. It is the one place an unnamed write-off might be described."),
        ("2", "&ldquo;Alta Motors&rdquo; in LiveWire&rsquo;s 10-Ks", "LiveWire&rsquo;s FY2024 and FY2025 10-Ks contain the string (EDGAR full-text hit); location not retrieved, probably an officer biography."),
        ("3", "Aermacchi", "1960 price (~$250K), 1978 sale price, Sprint volumes and the year of full ownership (1972&ndash;74) are secondary only."),
        ("4", "Holiday Rambler purchase price", "$155M is trade press (Family RVing, 2003); the 1986 annual report is not on EDGAR."),
        ("5", "Buell 1993 price and cumulative units", "~$500K and 135,000+ / 136,923 are secondary."),
        ("6", "Hero X440 volumes; Sprint build source", "8,974 (Apr&ndash;Dec 2024) is Autocar Professional&rsquo;s. Neither Harley nor Hero has confirmed Hero builds the Sprint. Check the dealer-meeting materials and the Q3 call."),
        ("7", "Sprint price; 883 price and plant", "&ldquo;Less than $10,000&rdquo; and &ldquo;~$10,000 / York&rdquo; are press paraphrases of the 5 May 2026 investor deck. Fetch the deck."),
        ("8", "Milwaukee-Eight and Rev Max program costs", "Not in either release; check capex commentary 2014&ndash;2020."),
        ("9", "LiveWire TTM units", "923 to June 2026 is from No. 01; the Q1 2026 release was not re-pulled."),
        ("10", "Realized India exit charge", "$75M is the estimate for actions approved September 2020; FY2020 restructuring was $130.0M for all 2020 actions and does not break India out."),
    ]
    corr_rows = [
        ("MV Agusta: &ldquo;~$163M of losses in 24 months.&rdquo;", "That is the 8-K&rsquo;s &ldquo;prior write-downs of $162.6 million, net of tax,&rdquo; which is impairments only. The filed net loss from discontinued operations is <strong>$268.4M</strong> (2008&ndash;10), $217.4M after the Q4 2011 tax reversal."),
        ("MV sale: &ldquo;&euro;1 with &euro;20M of H-D cash inside.&rdquo;", "Right but incomplete: three nominal payments (&euro;1 shares, $1 U.S. LLC, &euro;1 for a &euro;103.8M receivable), &euro;20.0M into escrow, earn-out waived."),
        ("StaCyc 2025 units: 21,141.", "<strong>21,633</strong> (LiveWire FY2025 release). Ratio to motorcycles 32 &rarr; 33."),
        ("HDFS: &ldquo;9.8% to KKR/PIMCO, ~$6B book sold.&rdquo;", "4.9% each to KKR and PIMCO (9.8% collectively, FY2025 10-K) and &ldquo;over $5 billion&rdquo; of receivables (30 Jul 2025 release)."),
        ("Thailand plant, 2018.", "Announced 25 May 2017; producing 2018."),
        ("&ldquo;Zeitz, 2025: unprofitable&rdquo; on Street.", "The on-the-record statement is CFO Gina Goetter&rsquo;s, Q3 2021 call. Zeitz said &ldquo;prune unprofitable motorcycles&rdquo; without naming Street."),
        ("Buell exit cost $125M, stated as fact.", "It is the October 2009 estimate (Q3 2009 10-Q, Note 19). No filing reports a realized Buell-only total."),
        ("Holiday Rambler sold 1996 for ~$50M.", "The whole Transportation Vehicles segment went for ~$105M, gain $22.6M (FY1996 10-K); ~$50M was the RV division per wire reports."),
        ("Alta: H-D &ldquo;would instead build its own R&amp;D center in Silicon Valley.&rdquo;", "Paraphrase. The facility was announced in a separate release, 5 Sep 2018."),
        ("Dust: cost undisclosed.", "Terms are in LiveWire&rsquo;s 22 May 2026 8-K."),
        ("S4 Honcho $4,999.", "$4,999 Trail; $5,499 Street."),
        ("Aermacchi full ownership 1974.", "Sources split 1972/1973/1974; stated as &ldquo;early 1970s.&rdquo;"),
    ]
    H.append(section(f"""
    <span id="method"></span><div class="eyebrow">12 &middot; Method &amp; standing</div>
    <h2>Who wrote this, and how</h2>
    {bio}
    <div class="duo" style="margin-top:30px">
      <div class="card">
        <div class="k">Method</div>
        <p style="font-size:15px; color:var(--ink)"><strong>Primary documents first.</strong> Every dollar figure on MV Agusta, Buell, StaCyc, Eaglemark, India, Dust and LiveWire is from a filing, linked in &sect;11. Alta&rsquo;s bound is from Alta&rsquo;s own Form D chain, and is marked as an inference.</p>
        <p><strong>Derived figures are labelled.</strong> Loss-to-consideration multiples, loss per month, units per unit, revenue per unit and the Form D increment are arithmetic on filed numbers; the script is in the repo at <code>tools/gt03/calc.py</code>.</p>
        <p><strong>Fact and opinion are separated.</strong> &sect;&sect;01&ndash;09 are sourced. &sect;10 is judgment and says so. Where a reading rests on my time in the industry (the York cost base, the planning-office calculation) it is tagged Industry context.</p>
        <p><strong>No inside sources.</strong> Nothing here rests on anything I was told. The public record carries every claim.</p>
      </div>
      <div class="card">
        <div class="evlegend">
          <div class="evlegend-h">Evidence status</div>
          <p style="margin:6px 0 10px">Major findings carry one of five tags, so a reader can see at a glance what kind of claim is being made and how to attack it.</p>
          <div class="evlegend-r">{ev('doc')}<span>Stated in a filing, contract, release or transcript, and linked to it.</span></div>
          <div class="evlegend-r">{ev('calc')}<span>Arithmetic on documented numbers, with the computation shown.</span></div>
          <div class="evlegend-r">{ev('inf')}<span>A conclusion supported by more than one documented fact, but stated by none of them.</span></div>
          <div class="evlegend-r">{ev('ind')}<span>My professional experience or established industry practice, not a document.</span></div>
          <div class="evlegend-r">{ev('unv')}<span>Plausible, and not independently establishable from public information.</span></div>
        </div>
      </div>
    </div>
    """))
    H.append(section(f"""
    <div class="eyebrow">13 &middot; Open items &amp; corrections</div>
    <h2>What is not yet nailed down, and what Rev. 0 got wrong</h2>
    <p class="lede">Ten open items. Anything in this list is tagged Unverified where it appears above. The corrections log is public policy: nothing is fixed silently.</p>
    {tbl(['#', 'Item', 'Status'], open_rows, ['5%', '28%', '67%'])}
    <h3 style="font-size:clamp(21px,2.6vw,28px); margin-top:46px">Corrections log</h3>
    <p>Rev. 0 (8 September 2026) was an outline built from secondary sources. Rev. 1 (9 September 2026) corrects it on reading the filings.</p>
    {tbl(['What was claimed', 'What the document said'], corr_rows, ['42%', '58%'])}
    """))

    # ── footer
    H.append(f"""
<footer class="foot">
  <div class="wrap">
    <div class="tape">Method &amp; limitations</div>
    <h4>What this brief does and does not claim</h4>
    <p>Every figure is drawn from SEC filings, company releases, or full call transcripts, except where marked Unverified. Derived figures (loss multiples, per-unit revenue, the Form D increment) are arithmetic on filed numbers and are identified as such in the captions.</p>
    <p><strong>This brief does not assert, and no filing states, that Harley-Davidson intends to sell, wind down, reabsorb or otherwise change its relationship with LiveWire, StaCyc or Dust, or that the Sprint will be built by Hero MotoCorp.</strong> &sect;10 is an enumeration of what the record has done before, identified as judgment. The Alta investment amount has never been disclosed by Harley-Davidson; the bound in &sect;04 is an inference from Faster Faster, Inc.&rsquo;s Regulation D notices and is labelled as such.</p>
    <p>Marc Fenigstein&rsquo;s account of the Alta&ndash;Harley collaboration is quoted from a published interview, is his, and is unverified. The author knows him and has worked with him. That relationship is disclosed in &sect;12 and here.</p>
    <p>Prior issues: <a href="../02/">No. 02, Harley-Davidson: Back to the Bricks</a> &middot; <a href="../01/">No. 01, LiveWire: 5 Years In and 1% of Plan</a> &middot; <a href="../../">Index</a></p>
    <p style="margin-top:26px; font-family:var(--f-mono); font-size:10.5px; letter-spacing:.1em; text-transform:uppercase; color:var(--ink-3)">
      Contact Patch Advisory &middot; Ground Truth No. {NN} &middot; {REV} &middot; William Weppner &middot; {DATE}
    </p>
  </div>
</footer>
</main>
<div id="tip" role="status" aria-live="polite"></div>
<script>
(function(){{
  var tip=document.getElementById('tip');
  document.querySelectorAll('[data-tip]').forEach(function(el){{
    el.addEventListener('mouseenter',function(e){{ tip.textContent=el.getAttribute('data-tip'); tip.style.opacity='1'; }});
    el.addEventListener('mousemove',function(e){{
      var x=e.clientX+14, y=e.clientY+16;
      if(x+tip.offsetWidth>window.innerWidth-10) x=e.clientX-tip.offsetWidth-14;
      tip.style.left=x+'px'; tip.style.top=y+'px';
    }});
    el.addEventListener('mouseleave',function(){{ tip.style.opacity='0'; }});
  }});
}})();
</script>
</body></html>
""")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("".join(H))
    print("wrote", OUT, OUT.stat().st_size, "bytes")


if __name__ == "__main__":
    build()
