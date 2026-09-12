#!/usr/bin/env python3
"""Build groundtruth/02/index.html — Ground Truth No. 02, Harley-Davidson.

Run from the repo root:  python3 tools/gt02/build_brief.py
Uses tools/lib/brief.css (the No. 01 stylesheet, portraits included) and tools/lib/charts.py.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "tools", "lib")); from sitenav import nav_html, bottombar_html
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools", "gt02", "lib"))  # No. 02 chart/render API; tools/lib is the current one
from charts import bars, hbars, waterfall, MAG, CYAN, INK3

CSS = open(os.path.join(ROOT, "tools", "lib", "brief.css")).read()
OUT = os.path.join(ROOT, "site", "groundtruth", "02", "index.html")

ISSUE = "Ground Truth No. 02"
DATE = "September 2026"
SITE = "https://contactpatchadvisory.com/groundtruth/02/"

def n(x):  # highlighted number
    return f'<b class="n">{x}</b>'

def ev(kind):
    names = {"doc": "Documented", "calc": "Calculated", "inf": "Inferred", "ind": "Industry context", "unv": "Unverified"}
    return f'<span class="ev ev-{kind}">{names[kind]}</span>'

def fig(num, title, sub, svg, cap_kind, cap):
    return f'''
    <figure>
      <div class="fig-head"><span class="fig-n">FIG {num:02d}</span><span class="fig-t">{title}</span><span class="fig-sub">{sub}</span></div>
      {svg}
      <figcaption>{ev(cap_kind)}{cap}</figcaption>
    </figure>'''

def sowhat(sec, point, thesis, outlook):
    return f'''
    <div class="sowhat">
      <div class="h">So what &middot; &sect;{sec}</div>
      <div class="r"><b>The point</b><span>{point}</span></div>
      <div class="r"><b>Back to the thesis</b><span>{thesis}</span></div>
      <div class="r"><b>Outlook</b><span>{outlook}</span></div>
    </div>'''

def brandrow(eyebrow):
    return f'<div class="brandrow"><div class="eyebrow">{eyebrow}</div><div class="brand"><span style="font-family:var(--f-disp);font-weight:800;text-transform:uppercase;font-size:14px;letter-spacing:.06em;color:var(--ink-3)">Harley-Davidson, Inc. &middot; HOG</span></div></div>'

def here(on):
    parts = ["Part I", "Part II", "Part III", "Part IV", "Part V", "Part VI"]
    return '<div class="here">' + " ".join(f'<span class="{"on" if p==on else ""}">{p}</span>' for p in parts) + "</div>"

def part(pid, roman, title, dek, point, why, img_title, img_desc, img_src):
    return f'''
<div class="wrap part" id="{pid}">
  <div class="brandrow">{here(roman)}<div class="brand"><span style="font-family:var(--f-disp);font-weight:800;text-transform:uppercase;font-size:14px;letter-spacing:.06em;color:var(--ink-3)">Harley-Davidson, Inc.</span></div></div>
  <div class="part-n">{roman}</div>
  <h2 class="part-t">{title}</h2>
  <div class="part-grid">
    <div>
      <p class="part-d">{dek}</p>
      <div class="part-kv">
        <div><b>The point</b><span>{point}</span></div>
        <div><b>Why it matters</b><span>{why}</span></div>
      </div>
    </div>
    <div class="part-img"><div class="phx" style="height:240px;aspect-ratio:auto;border:0"><span class="tag">Image to source</span><div class="t">{img_title}</div><div class="d">{img_desc}</div><div class="s">{img_src}</div></div></div>
  </div>
</div>'''

def phx(title, desc, src, style=""):
    return f'<div class="phx" style="{style}"><span class="tag">Image to source</span><div class="t">{title}</div><div class="d">{desc}</div><div class="s">{src}</div></div>'

def table(head, rows, widths=None, cls_map=None):
    ths = []
    for i, h in enumerate(head):
        style = ' style="width:%s"' % widths[i] if widths and widths[i] else ""
        ths.append("<th%s>%s</th>" % (style, h))
    th = "".join(ths)
    body = []
    for r in rows:
        tds = []
        for j, c in enumerate(r):
            cls = ""
            if cls_map and j in cls_map:
                cls = f' class="{cls_map[j]}"'
            tds.append(f"<td{cls}>{c}</td>")
        body.append("<tr>" + "".join(tds) + "</tr>")
    return f'<div class="scroll"><table class="tbl"><thead><tr>{th}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'

# ───────────────────────────── HERO FIGURE ─────────────────────────────
def hero_svg():
    # Guidance stack: HDMC 10..50, HDFS 55..70, LiveWire -80..-70, Sum -15..50 ; scale: 1 $M = 2.2px, zero at y=300
    z = 300; k = 2.2
    def y(v): return z - v * k
    cols = [(230, "HDMC", 10, 50, "var(--cyan)", "THE MOTOR COMPANY"),
            (470, "HDFS", 55, 70, "var(--cyan)", "THE FINANCE COMPANY"),
            (710, "LIVEWIRE", -80, -70, "var(--magenta)", "THE SUBSIDIARY"),
            (950, "HARLEY-DAVIDSON, INC.", -15, 50, "var(--ink)", "ADDED UP")]
    s = ['<svg class="herofig" viewBox="0 0 1200 560" role="img" aria-label="Harley-Davidson 2026 guidance: HDMC operating income $10 to $50 million, HDFS $55 to $70 million, LiveWire loss $70 to $80 million; consolidated implied $(15) to $50 million.">',
         '<rect width="1200" height="560" style="fill:var(--ground-2)"/>',
         '<text x="48" y="60" style="fill:var(--ink-2)" font-family="IBM Plex Mono,ui-monospace,monospace" font-size="12" letter-spacing="2">2026 OPERATING INCOME GUIDANCE · RAISED 23 JULY 2026 · $ MILLIONS</text>',
         '<text x="1152" y="60" style="fill:var(--ink-2)" font-family="IBM Plex Mono,ui-monospace,monospace" font-size="12" letter-spacing="2" text-anchor="end">LOW END TO HIGH END OF EACH RANGE</text>',
         '<line x1="48" y1="78" x2="1152" y2="78" style="stroke:var(--rule)"/>']
    for gv in (100, 50, -50, -100):
        s.append(f'<line x1="120" y1="{y(gv):.0f}" x2="1080" y2="{y(gv):.0f}" style="stroke:var(--rule)" stroke-dasharray="2 4"/>')
        s.append(f'<text x="108" y="{y(gv)+4:.0f}" style="fill:var(--ink-3)" font-family="IBM Plex Mono,ui-monospace,monospace" font-size="11" text-anchor="end">{gv:+d}</text>')
    s.append(f'<line x1="120" y1="{z}" x2="1080" y2="{z}" style="stroke:var(--ink)" stroke-width="1.5"/>')
    s.append(f'<text x="108" y="{z+4}" style="fill:var(--ink)" font-family="IBM Plex Mono,ui-monospace,monospace" font-size="11" text-anchor="end">0</text>')
    for cx, lab, lo, hi, col, sub in cols:
        w = 150
        top, bot = y(max(lo, hi, 0)), y(min(lo, hi, 0))
        # faint full range from 0 to the far end; solid from 0 to the near end
        far, near = (hi, lo) if hi >= 0 and lo >= 0 else ((lo, hi) if hi <= 0 else (None, None))
        if far is not None:
            s.append(f'<rect x="{cx-w/2}" y="{min(y(far),y(0)):.0f}" width="{w}" height="{abs(y(far)-y(0)):.0f}" style="fill:{col}" opacity=".32"/>')
            s.append(f'<rect x="{cx-w/2}" y="{min(y(near),y(0)):.0f}" width="{w}" height="{abs(y(near)-y(0)):.0f}" style="fill:{col}"/>')
        else:  # straddles zero (consolidated)
            s.append(f'<rect x="{cx-w/2}" y="{y(hi):.0f}" width="{w}" height="{abs(y(hi)-y(0)):.0f}" style="fill:{col}" opacity=".32"/>')
            s.append(f'<rect x="{cx-w/2}" y="{y(0):.0f}" width="{w}" height="{abs(y(lo)-y(0)):.0f}" style="fill:var(--magenta)" opacity=".85"/>')
        rng = f"${lo} to ${hi}M" if lo >= 0 else (f"$({-hi}) to $({-lo})M" if hi < 0 else f"$({-lo}) to ${hi}M")
        ty = top - 14 if (hi > 0) else y(0) - 14
        s.append(f'<text x="{cx}" y="{ty:.0f}" style="fill:{"var(--magenta)" if lab=="LIVEWIRE" else "var(--ink)"}" font-family="Big Shoulders Display,Impact,sans-serif" font-weight="800" font-size="34" text-anchor="middle">{rng}</text>')
        s.append(f'<text x="{cx}" y="470" style="fill:var(--ink)" font-family="IBM Plex Mono,ui-monospace,monospace" font-size="12" letter-spacing="2" text-anchor="middle">{lab}</text>')
        s.append(f'<text x="{cx}" y="490" style="fill:var(--ink-3)" font-family="IBM Plex Mono,ui-monospace,monospace" font-size="10" letter-spacing="2" text-anchor="middle">{sub}</text>')
    s.append('<path d="M120 520 L1080 520" style="stroke:var(--magenta)" stroke-width="1"/><path d="M120 514 L120 526 M1080 514 L1080 526" style="stroke:var(--magenta)" stroke-width="1"/>')
    s.append('<text x="600" y="548" style="fill:var(--magenta)" font-family="Big Shoulders Display,Impact,sans-serif" font-weight="800" font-size="22" letter-spacing="2" text-anchor="middle">THE SUBSIDIARY IS GUIDED TO LOSE MORE THAN THE MOTOR COMPANY IS GUIDED TO MAKE</text>')
    s.append("</svg>")
    return "\n".join(s)

# ───────────────────────────── FIGURES ─────────────────────────────
FIG_RETAIL = bars([267999, 218273, 180248, 194256, 178451, 162771, 151229, 132535],
                  ["2014", "2019", "2020", "2021", "2022", "2023", "2024", "2025"],
                  colors=[INK3, INK3, INK3, INK3, INK3, INK3, MAG, MAG], opacities=[.55, .7, .55, .7, .7, .8, .85, None],
                  ymax=280000, ticks=[0, 100000, 200000], tick_fmt=lambda v: f"{v/1000:.0f}K", val_fmt=lambda v: f"{v/1000:.0f}K",
                  aria="Worldwide retail motorcycle sales: 267,999 in 2014 falling to 132,535 in 2025.")

FIG_HDMC = bars([289.6, -186.1, 408.6, 677.1, 661.2, 277.8, -28.7],
                ["2019", "2020", "2021", "2022", "2023", "2024", "2025"],
                colors=[CYAN, MAG, CYAN, CYAN, CYAN, CYAN, MAG], opacities=[.6, .7, .7, .85, None, .85, None],
                ymax=720, ymin=-220, ticks=[-200, 0, 200, 400, 600], tick_fmt=lambda v: f"${v:,.0f}M", val_fmt=lambda v: f"{v:,.0f}",
                aria="HDMC operating income by year: $290M 2019, $(186)M 2020, $409M 2021, $677M 2022, $661M 2023, $278M 2024, $(29)M 2025.")

FIG_SEG = waterfall([("HDMC", -28.7, MAG), ("LiveWire", -75.0, MAG), ("HDFS", 490.4, CYAN), ("Consolidated", None, "var(--ink)")],
                    ymin=-130, ymax=520, ticks=[-100, 0, 100, 200, 300, 400, 500], val_fmt="{:+,.1f}",
                    aria="2025 operating income bridge: HDMC minus $28.7M, LiveWire minus $75.0M, HDFS plus $490.4M, consolidated $386.6M.")

FIG_HDFS = bars([234.7, 248.4, 490.4, 62.5, 137.5],
                ["2023", "2024", "2025", "2026 guide", "2029 target"],
                colors=[CYAN, CYAN, CYAN, MAG, INK3], opacities=[.7, .85, None, None, .7],
                ymax=520, ticks=[0, 100, 200, 300, 400, 500], tick_fmt=lambda v: f"${v:,.0f}M", val_fmt=lambda v: f"{v:,.0f}",
                tips=["2023: $234.7M", "2024: $248.4M", "2025: $490.4M (transaction year)", "2026 guidance: $55–70M, midpoint shown", "2029 target: $125–150M, midpoint shown"],
                aria="HDFS operating income: $235M 2023, $248M 2024, $490M 2025, guided $55–70M for 2026, targeted $125–150M by 2029.")

FIG_LW = bars([15.0, 26.3, 19.4, 33.8], ["2023", "2024", "2025", "TTM Jun 2026"],
              colors=[MAG]*4, opacities=[.55, .75, .85, None], ymax=40, ticks=[0, 10, 20, 30, 40], tick_fmt="{:.0f}%", val_fmt="{:.1f}%",
              aria="LiveWire operating loss as a percentage of Harley-Davidson consolidated operating income: 15% 2023, 26% 2024, 19% 2025, 34% trailing twelve months.")

FIG_BUY = bars([38.6, 34.3, 36.0, 26.5, 20.0, 28.30], ["2022", "2023", "2024", "2025", "H1 2026", "HOG 4 Sep 2026"],
               colors=[INK3, INK3, INK3, INK3, INK3, MAG], opacities=[.7, .7, .7, .7, .7, None], ymax=44, ticks=[0, 10, 20, 30, 40],
               tick_fmt="${:.0f}", val_fmt="${:.2f}",
               aria="Average repurchase price by year: $38.6 2022, $34.3 2023, $36.0 2024, $26.5 2025, $20.0 H1 2026; share price $28.30 on 4 September 2026.")

FIG_SPORT = hbars([("Plan: +5% a year", 6600, CYAN, None, "motorcycles"),
                   ("Sportster, low", 35000, MAG, .8, "Starrs: “35,000–40,000+ … on a global basis”"),
                   ("Sportster, high", 40000, MAG, None, "")],
                  xmax=44000, val_fmt="{:,.0f}", aria="The plan needs about 6,600 incremental units a year; the Sportster historically sold 35,000 to 40,000 globally.")

FIG_2027 = bars([779.1, 416.6, 386.6, 17.5, 210, 280], ["2023", "2024", "2025", "2026 guide", "2027 w/ LiveWire", "2027 w/o"],
                colors=[CYAN, CYAN, CYAN, MAG, INK3, INK3], opacities=[None, .85, .7, None, .7, .5], ymax=820, ticks=[0, 200, 400, 600, 800],
                tick_fmt=lambda v: f"${v:,.0f}M", val_fmt=lambda v: f"{v:,.0f}",
                tips=["2023: $779.1M", "2024: $416.6M", "2025: $386.6M (HDFS transaction year)", "2026 guidance midpoint: about $17M", "2027 if the plan lands and LiveWire still loses $70M: about $210M", "2027 if the plan lands and LiveWire is gone: about $280M"],
                aria="Consolidated operating income: $779M 2023, $417M 2024, $387M 2025, guided about $17M midpoint for 2026, roughly $210–280M in 2027 if Back to the Bricks delivers.", label_fs=9.5)

# ───────────────────────────── PAGE ─────────────────────────────
def build():
    H = []
    H.append(f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Harley-Davidson: Back to the Bricks, Down to Breakeven</title>
<meta name="description" content="Ground Truth No. 02. What LiveWire costs Harley-Davidson, what Back to the Bricks actually commits to, and what a 2027 Harley looks like on the company's own numbers. Every figure linked to its filing.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@600;700;800&family=IBM+Plex+Mono:wght@400;500;600&family=Public+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap">
<style>{CSS}</style>
</head><body>

<header class="topbar">
  <div class="wrap">
    <div class="mark">CONTACT&nbsp;<span>PATCH</span></div>
    {nav_html()}
    <div class="stamp">{ISSUE} &middot; Draft &middot; Rev. 2</div>
  </div>
</header>

<main>

<section class="hero" style="border-bottom:1px solid var(--rule)">
  <div class="wrap">
    <div class="kick">{ISSUE} &middot; Harley-Davidson, Inc. &middot; {DATE}</div>
    <div class="hero-top">
      <h1><span style="display:block;font-size:.42em;letter-spacing:.02em;color:var(--ink-2);margin-bottom:.15em">Harley-Davidson:</span>Back to<br>the Bricks.<br>Down to<br>Breakeven.</h1>
    </div>
    <p class="sub" style="font-family:var(--f-mono);font-size:clamp(13px,1.6vw,17px);letter-spacing:.14em;text-transform:uppercase;color:var(--magenta);margin:18px 0 0">What LiveWire costs the parent, and what the plan leaves out</p>
    <div class="herofig-wrap">{hero_svg()}</div>
    <ul class="thesis">
      <li><b>What they said</b><span>May 2026, introducing the new plan: &ldquo;Over the last several years, we leaned heavily into Touring and Electric.&rdquo; Five pillars, six targets, {n("$350 million")} of HDMC EBITDA in 2027.</span></li>
      <li><b>What it is</b><span>Add up the company&rsquo;s own 2026 guidance and Harley-Davidson, Inc. lands between a {n("$15 million")} loss and a {n("$50 million")} profit. It made {n("$779 million")} in 2023. Its electric subsidiary is guided to lose {n("$70&ndash;80 million")}; its motor company to make {n("$10&ndash;50 million")}.</span></li>
      <li><b>What decided it</b><span>A finance company sold for cash, a five-year strategy that missed every quantified target, and a subsidiary that sits inside the income statement and outside the plan.</span></li>
    </ul>
    <p class="thesis-line">The plan is scored on the motor company. <i>The income statement is not.</i></p>
    <div class="srcline">
      Sources: HOG Form 10-K (FY2025) &middot; HOG Form 10-Q (Q2 2026) &middot; HOG Forms 8-K (Q4 2025, Q1 2026, Q2 2026 results) &middot; &ldquo;Back to the Bricks&rdquo; release (5 May 2026)<br>
      Hardwire release (2 Feb 2021) &middot; Hardwire Stage II investor day (10 May 2022) &middot; KKR/PIMCO partnership releases (30 Jul, 25 Aug 2025) &middot; LVWR Form 10-K (FY2025), 10-Q (Q2 2026) &middot; Ground Truth No. 01</div>
  </div>
</section>

<div class="strip">
  <div class="s"><div class="l"><b>Worldwide retail</b><span>2014 &rarr; 2025 &middot; 267,999 &rarr; 132,535</span><span style="color:var(--magenta);font-size:22px;font-family:var(--f-disp);font-weight:800;letter-spacing:0">&minus;51%</span></div></div>
  <div class="s"><div class="l"><b>HDMC operating margin</b><span>2023 &rarr; 2025 &middot; 13.6% &rarr; (0.8%)</span><span style="color:var(--magenta);font-size:22px;font-family:var(--f-disp);font-weight:800;letter-spacing:0">&minus;14.4 pts</span></div></div>
  <div class="s"><div class="l"><b>LiveWire losses consolidated</b><span>2022 &rarr; Jun 2026 &middot; H-D segment basis</span><span style="color:var(--magenta);font-size:22px;font-family:var(--f-disp);font-weight:800;letter-spacing:0">$422M</span></div></div>
  <div class="s"><div class="l"><b>Dealerships</b><span>2019 &rarr; 2025 &middot; 1,569 &rarr; 1,174</span><span style="color:var(--magenta);font-size:22px;font-family:var(--f-disp);font-weight:800;letter-spacing:0">&minus;25%</span></div></div>
</div>
<div class="strip-cap">The company the plan inherits. Each line is sourced in Part I.</div>

<div class="wrap route" id="route">
  <div class="route-h">The route &middot; six parts, one thesis</div>
  <ol>
    <li><a href="#part1"><div class="rn">Part I</div><div class="rt">The arithmetic</div><div class="rp">Add up the guidance: about zero. The subsidiary&rsquo;s loss exceeds the motor company&rsquo;s profit.</div></a></li>
    <li><a href="#part2"><div class="rn">Part II</div><div class="rt">The sale</div><div class="rp">2025&rsquo;s profit was the finance company, sold. $180M a year of earnings traded for $1.25B once.</div></a></li>
    <li><a href="#part3"><div class="rn">Part III</div><div class="rt">The subsidiary</div><div class="rp">$422M consolidated. 0.6% of revenue, a third of the profit drag. Cash to May 2027; note due December.</div></a></li>
    <li><a href="#part4"><div class="rn">Part IV</div><div class="rt">The plan</div><div class="rp">Five pillars, six targets. The 2027 number is a 5% margin, below the year Hardwire was written to fix.</div></a></li>
    <li><a href="#part5"><div class="rn">Part V</div><div class="rt">The bet</div><div class="rp">$1.6B of buybacks, and one motorcycle carrying the growth target: the 883.</div></a></li>
    <li><a href="#part6"><div class="rn">Part VI</div><div class="rt">The final word</div><div class="rp">LiveWire didn&rsquo;t break Harley. It is what the new Harley can&rsquo;t afford. The decision has a date.</div></a></li>
  </ol>
</div>
''')

    # ───── §00
    H.append(f'''
<section>
  <div class="wrap">
    <div class="eyebrow">00 &middot; Start here</div>
    <h2>The finding, and the trail that led to it</h2>
    <p class="lede">Ground Truth No. 01 read LiveWire&rsquo;s filings. This one reads the parent&rsquo;s, and asks what the electric bet cost, what the new plan promises, and what Harley-Davidson looks like if the plan works.</p>

    <p>Start with the sentence the new CEO used to bury the old strategy. Artie Starrs, 5 May 2026, introducing Back to the Bricks: <em>&ldquo;Over the last several years, we leaned heavily into Touring and Electric. Going forward, we are shifting to a more rider-centric portfolio.&rdquo;</em> Fourteen words. That is the parent company&rsquo;s verdict on Hardwire, on LiveWire and on five years of product decisions, delivered on an earnings call and never expanded on.</p>
    <p>Then add up the guidance the same company published eleven weeks later. HDMC, the motor company: {n("$10&ndash;50 million")} of operating income. HDFS, the finance company: {n("$55&ndash;70 million")}. LiveWire: a {n("$70&ndash;80 million")} loss. Segment operating income sums to the consolidated line in Harley-Davidson&rsquo;s reporting. 2025 proves it: $(28.7)M + $490.4M + $(75.0)M = $386.6M, to the decimal. So the sum is the company&rsquo;s own forecast: <strong>Harley-Davidson, Inc. is guided to somewhere between a $15 million loss and a $50 million profit for 2026.</strong> Three years ago the number was $779 million.</p>
    <p>That is the finding. Inside it sits the sentence this brief is built on: <strong>the electric subsidiary is guided to lose more than the motor company is guided to make.</strong> At every point in both ranges.</p>

    <ul class="finds">
      <li>Open the FY2025 10-K segment note and the motor company lost {n("$28.7M")} in 2025, the first HDMC operating loss outside the pandemic year in the modern history of the company. The whole consolidated profit came from HDFS, and HDFS&rsquo;s profit came from selling its loan book.</li>
      <li>Ask what that sale did to earnings power and HDFS goes from a {n("$248M")} run rate to a {n("$55&ndash;70M")} guide. The company&rsquo;s steadiest earner was converted to cash, once.</li>
      <li>Read LiveWire as H-D reports it and the consolidated losses run to {n("$422M")} since 2022: a fifth of the 2025 profit drag, a third of the trailing one, from 0.6% of revenue.</li>
      <li>Read Back to the Bricks and there is no LiveWire target, no electric anything, and a 2027 EBITDA number that translates to roughly a {n("5%")} operating margin, below where HDMC stood in 2019, the year Hardwire was written to fix.</li>
      <li>Read Hardwire next to it: every quantified target missed. 15% margin promised for 2025; (0.8%) delivered.</li>
    </ul>

    <p>None of that is a secret. All of it is in the filings, and almost none of it is in the coverage, which has been about Sportsters and dealer sentiment. Those matter; Part V is about them. But the arithmetic comes first.</p>

    <h3 style="font-size:clamp(21px,2.6vw,28px); margin-top:40px">The trail, in five documents</h3>
    <p>The order I read them in. Each one sent me to the next.</p>
    <ol class="trail">
      <li><div><div class="doc"><a href="https://www.sec.gov/Archives/edgar/data/793952/000079395226000058/a8kq22026exhibit991v2.htm" target="_blank" rel="noopener">Q2 2026 results &middot; 8-K Ex. 99.1 &middot; 23 Jul 2026 &rarr;</a></div><div class="what"><b>The guidance.</b> Raised across the board, and still adds to roughly zero. Nobody added it up on the call.</div></div></li>
      <li><div><div class="doc"><a href="https://www.sec.gov/Archives/edgar/data/793952/000079395226000011/R27.htm" target="_blank" rel="noopener">Form 10-K FY2025 &middot; segment note &rarr;</a></div><div class="what"><b>Where the profit came from.</b> HDMC $(28.7)M. LiveWire $(75.0)M. HDFS $490.4M. One of these three is not like the others, and it is the one that was sold.</div></div></li>
      <li><div><div class="doc"><a href="https://investor.harley-davidson.com/news/news-details/2025/Harley-Davidson-Announces-Strategic-Partnership-with-KKR-and-PIMCO/default.aspx" target="_blank" rel="noopener">KKR / PIMCO strategic partnership &middot; 30 Jul 2025 &rarr;</a></div><div class="what"><b>The sale.</b> $5B+ of receivables, 9.8% of HDFS, two-thirds of future originations forward-sold. &ldquo;Unlocks ~$1.25 billion.&rdquo; Announced three months before the CEO who did it left.</div></div></li>
      <li><div><div class="doc"><a href="https://investor.harley-davidson.com/news/news-details/2026/Harley-Davidson-Announces-Back-to-the-Bricks-Strategic-Plan-to-Restore-Performance-and-Deliver-Profitable-Growth/default.aspx" target="_blank" rel="noopener">&ldquo;Back to the Bricks&rdquo; &middot; 5 May 2026 &rarr;</a></div><div class="what"><b>The plan.</b> Five pillars, one dated target, five medium-term ranges. LiveWire appears only in the forward-looking factors. The word &ldquo;electric&rdquo; does not appear.</div></div></li>
      <li><div><div class="doc"><a href="https://investor.harley-davidson.com/news/news-details/2022/Harley-Davidson-2022-Investor-Day-Update-Hardwire-Stage-II/default.aspx" target="_blank" rel="noopener">Hardwire Stage II &middot; investor day &middot; 10 May 2022 &rarr;</a></div><div class="what"><b>The benchmark.</b> &ldquo;HDMC Operating Margin: 15% by 2025.&rdquo; &ldquo;+5% to +7% CAGR.&rdquo; The plan the new plan replaces, in its own words.</div></div></li>
    </ol>

    <h3 style="font-size:clamp(21px,2.6vw,28px); margin-top:40px">The paperwork, on one screen</h3>
    <p>Four documents. Read the cards and you can skip the rest; every section below is the arithmetic they imply.</p>
    <div class="paper">
      <div class="c"><div class="n">Guidance &middot; 23 Jul 2026</div><div class="t">Three ranges that sum to zero</div><div class="r">HDMC <b>$10&ndash;50M</b>. HDFS <b>$55&ndash;70M</b>. LiveWire <b>$(70&ndash;80)M</b>. Implied consolidated: <b>$(15)M to $50M</b>.</div><div class="k">8-K Ex. 99.1 &middot; raised from Feb 2026</div></div>
      <div class="c"><div class="n">KKR / PIMCO &middot; Jul&ndash;Oct 2025</div><div class="t">The finance company, sold forward</div><div class="r">~$6B of receivables sold. 9.8% of HDFS equity. Two-thirds of future loans forward-sold for five years. <b>$1.0B dividend</b> to the parent. HDFS earnings <b>&minus;75%</b> going forward.</div><div class="k">Releases 30 Jul, 25 Aug 2025 &middot; 10-K FY2025</div></div>
      <div class="c"><div class="n">Term loan &middot; Nov&ndash;Dec 2025</div><div class="t">$75M, secured, due Dec 2027</div><div class="r">Convertible feature removed. Lien on substantially all of LiveWire&rsquo;s assets. SOFR + 4%, compounding to maturity. H-D: no further investment planned.</div><div class="k">LVWR 10-K FY2025 &middot; HOG 10-K FY2025</div></div>
      <div class="c"><div class="n">Back to the Bricks &middot; 5 May 2026</div><div class="t">Five pillars, no subsidiary</div><div class="r">HDMC EBITDA <b>&gt;$350M in 2027</b>. Mid-single-digit retail CAGR. 25&ndash;30% gross margin. 10&ndash;12% EBITDA margin. <b>$150M</b> of fixed cost out. LiveWire: not scored.</div><div class="k">Release &middot; Q1 2026 call</div></div>
    </div>

    <ul class="finds">
      <li><strong>Why Harley-Davidson.</strong> No. 01 followed the subsidiary&rsquo;s money. It leads here: to the only company in American motorcycling whose filings carry the whole industry&rsquo;s weight, in the first year of a new CEO and a new plan.</li>
      <li><strong>Who this is for.</strong> Dealers weighing the next allocation. Suppliers sizing the York ramp. Investors deciding whether &ldquo;transition year&rdquo; is a floor. Anyone at LiveWire wondering what the parent&rsquo;s numbers say about their runway.</li>
      <li><strong>What I did.</strong> Read H-D&rsquo;s FY2025 10-K and Q2 2026 10-Q line by line, the last five years of results releases and calls, the two strategy documents, the KKR/PIMCO releases, and the governance filings from the 2025 fight. Every figure links to its source. Twelve open items are listed in &sect;16, not hidden.</li>
      <li><strong>Who I am.</strong> Ex-Harley-Davidson product manager: Touring, CVO, Trike. Ex-Honda. Independent now. &sect;16 has the rest, and the disclosure.</li>
    </ul>
  </div>
</section>''')

    # ───── PART I
    H.append(part("part1", "Part I", "The arithmetic",
                  "The company&rsquo;s own 2026 guidance, added up, and the five-year line it sits at the bottom of.",
                  "Harley-Davidson, Inc. is guided to roughly breakeven operating income in 2026, and the subsidiary&rsquo;s guided loss is larger than the motor company&rsquo;s guided profit.",
                  "Every argument about Sportsters, dealers and tariffs happens inside that arithmetic. Growth from here is measured from a base near zero.",
                  "Juneau Avenue", "The Milwaukee headquarters, reopened for return-to-office in March 2026. Exterior, brick.", "Sketch: The Harley-Davidson headquarters on Juneau Avenue, Milwaukee, a long red-brick factory facade with tall windows, present day, overcast morning light. Charcoal sketch with a blue-grey wash on a dark chalkboard ground, vignetted edges; any people seen from behind or with faces unresolved, no identifiable ethnicity; 3:2, no logos."))

    H.append(f'''
<section>
  <div class="wrap">
    {brandrow("01 &middot; The guidance")}
    <h2>Three ranges that add up to about nothing</h2>
    <p class="lede">All three numbers come from the same release, the same day, the same table. No outside denominator, nothing to argue about. I add them; the company does not.</p>

    <div class="duo">
      <div class="card">
        <div class="k">HDMC operating income &middot; 2026 guidance</div>
        <div class="big">$10&ndash;50M</div>
        <p>The motor company. Raised on 23 July from a range of <b class="n">$(40)M to $10M</b>.</p>
      </div>
      <div class="card mag">
        <div class="k">LiveWire operating loss &middot; 2026 guidance</div>
        <div class="big mag">$(70&ndash;80)M</div>
        <p>The subsidiary. Unchanged since February. <b class="n">0.6%</b> of revenue.</p>
      </div>
    </div>

    {table(["2026 guidance, 23 Jul 2026", "Low", "High"],
           [["HDMC operating income", "$10M", "$50M"],
            ["HDFS operating income", "$55M", "$70M"],
            ["LiveWire operating loss", '<span class="hi">$(80)M</span>', '<span class="hi">$(70)M</span>'],
            ["<strong>Implied consolidated operating income</strong>", "<strong>$(15)M</strong>", "<strong>$50M</strong>"],
            ["<em>For reference: consolidated operating income, 2023</em>", "", "<em>$779.1M</em>"]],
           widths=["56%", "22%", "22%"], cls_map={1: "num", 2: "num"})}

    <div class="note">
      <div class="h">Two qualifications, stated before anyone else states them</div>
      <p>{ev("doc")}H1 2026 consolidated operating income was <b class="n">$99.5M</b>, so the full-year guidance implies a second-half loss. Q4 is seasonally the weak quarter: HDMC lost <b class="n">$260M</b> in Q4 2025 on a gross margin of <b class="n">(8.0%)</b>. Management has also beaten its own ranges twice this year. The guidance may be conservative. It is still the number they chose to publish.</p>
      <p>{ev("calc")}&ldquo;Segment operating income sums to the consolidated line&rdquo; is checked against 2025 to the decimal, and against 2024 ($277.8M + $248.4M &minus; $109.6M = $416.6M). No corporate eliminations sit between the segments and the total.</p>
    </div>

    <p class="pull">The subsidiary is guided to lose more than the motor company is guided to make.</p>

    {sowhat("01",
            "Added up, the 2026 plan is a breakeven year for the enterprise. LiveWire&rsquo;s $70&ndash;80M loss is the swing between a profit and a loss.",
            "Back to the Bricks scores itself on HDMC EBITDA. That is a legitimate management metric. It is also the one metric that excludes the line that turns the year negative.",
            "If H2 tracks H1, the company beats this. If Q4 looks like Q4 2025, it does not. Either way the range is the floor the new strategy is being measured from.")}
  </div>
</section>''')

    H.append(f'''
<section>
  <div class="wrap">
    {brandrow("02 &middot; The five-year line")}
    <h2>Half the motorcycles, three-quarters of the dealers</h2>
    <p class="lede">The company Back to the Bricks inherits, against the company Hardwire inherited, against the company of a decade ago.</p>

    {table(["", "2014", "2019", "2023", "2024", "2025", "2019&rarr;25"],
           [["Consolidated revenue", "~$6.23B", "$5,361M", "$5,836M", "$5,187M", "<strong>$4,473M</strong>", "&minus;17%"],
            ["Worldwide retail (units)", "267,999", "218,273", "162,771", "151,229", "<strong>132,535</strong>", "&minus;39%"],
            ["U.S. retail", "171,079", "125,960", "98,468", "94,930", "<strong>82,698</strong>", "&minus;34%"],
            ["Motorcycle shipments", "270,726", "213,939", "179,984", "148,862", "<strong>124,477</strong>", "&minus;42%"],
            ["HDMC operating margin", "18.0%", "6.3%", "13.6%", "6.7%", '<span class="hi">(0.8%)</span>', "&minus;7.1 pts"],
            ["U.S. 601cc+ share (MIC)", "n/a", "n/a", "37.9%", "37.3%", "<strong>34.5%</strong>", "n/a"],
            ["Dealerships worldwide", "n/a", "1,569", "n/a", "1,224", "<strong>1,174</strong>", "&minus;25%"],
            ["U.S. dealerships", "n/a", "698", "n/a", "570", "<strong>554</strong>", "&minus;21%"],
            ["Diluted EPS", "$3.88", "$2.68", "$4.87", "$3.44", "<strong>$2.78</strong>", "+4%"]],
           widths=["28%", "12%", "12%", "12%", "12%", "12%", "12%"], cls_map={1: "num", 2: "num", 3: "num", 4: "num", 5: "num", 6: "num"})}

    {fig(1, "Worldwide retail motorcycle sales", "units &middot; company releases", FIG_RETAIL, "doc",
         "Retail is down <b class='n'>51%</b> from 2014 and has fallen every year since 2021. U.S. retail is down 52% over the same span; shipments 54%. The 2025 figure is the lowest in the modern reporting history of the company. Sources: FY2014, FY2019&ndash;FY2025 results releases (8-K Ex. 99.1).")}

    <p>Revenue fell less than volume because price rose and because HDFS is in the consolidated line. EPS held up because of the buyback and because of what HDFS did in 2025. Those are Parts II and V. Strip those out and the motor company&rsquo;s trajectory is the unit line: <strong>a business that sells half the motorcycles it sold eleven years ago, through a quarter fewer stores, and in 2025 did it at a loss.</strong></p>

    {fig(2, "HDMC operating income", "$ millions &middot; Motorcycles segment; LiveWire separated from 2022", FIG_HDMC, "doc",
         "2025 was the first HDMC operating loss since the pandemic year, and the first in a normal year on record. Q4 2025 gross margin was <b class='n'>(8.0%)</b>: for one quarter the company sold motorcycles for less than they cost to build. Segment definitions changed in 2022 when LiveWire was split out; 2019&ndash;2021 are the Motorcycles segment as then reported.")}

    {sowhat("02",
            "This is not a company in a down year. It is a company at the end of an eleven-year decline in volume, with margin now following volume down.",
            "Every Back to the Bricks target is measured from this base. A 5% margin in 2027 would be a recovery. It would also be below 2019.",
            "The plan&rsquo;s mid-single-digit retail growth reverses a &minus;8% CAGR. That is not incremental; it is a change of direction the company has not managed since 2021.")}
  </div>
</section>''')

    # ───── PART II
    H.append(part("part2", "Part II", "The sale",
                  "Where the 2025 profit came from, and what it cost to get it.",
                  "In 2025 the motor company lost money and the subsidiary lost more. The year was profitable because the finance company sold its loan book and paid a $1 billion dividend to the parent. That does not happen twice.",
                  "HDFS earned about a quarter-billion a year before the sale and is guided to $55&ndash;70M after it. The company traded a recurring earner for a one-time cheque.",
                  "HDFS, Plano", "Harley-Davidson Financial Services offices, Plano, Texas. Or a dealer finance desk.", "Sketch: A dealership finance desk, a rider signing loan papers across from a finance manager, cruisers blurred on the showroom floor behind them, present day, flat fluorescent light. Charcoal sketch with a blue-grey wash on a dark chalkboard ground, vignetted edges; any people seen from behind or with faces unresolved, no identifiable ethnicity; 3:2, no logos."))

    H.append(f'''
<section>
  <div class="wrap">
    {brandrow("03 &middot; Where the 2025 profit came from")}
    <h2>Two segments lost money. The third was sold.</h2>
    <p class="lede">Consolidated operating income of $386.6M looks like a profitable company. The segment note says which company.</p>

    {fig(3, "2025 operating income by segment", "$ millions &middot; bridge to the consolidated line", FIG_SEG, "doc",
         "HDMC $(28.7)M. LiveWire $(75.0)M. HDFS $490.4M, described in the release as &ldquo;record-high earnings, driven by the HDFS transaction.&rdquo; The motorcycle company and its subsidiary together lost $103.7M; the finance company covered it four times over, once. FY2025 10-K, segment note.")}

    <p>What HDFS sold, in the company&rsquo;s own description: <em>&ldquo;a back book sale, sale of approximately $6 billion of existing HDFS loan receivables, forward flow agreements, the sale of future HDFS loan originations, and the sale of equity interest, sale of a 9.8% common equity interest in HDFS to KKR and PIMCO.&rdquo;</em> The receivables went at a premium to par. The equity went at an agreed <b class="n">$1.8B</b> valuation, 4.9% to each partner. The forward-flow agreement commits HDFS to sell roughly <b class="n">two-thirds</b> of its future retail originations for five years.</p>
    <p>The accounting follows: the provision for credit losses swung from a <b class="n">$247M</b> expense in 2024 to a <b class="n">$191M</b> <em>credit</em> in 2025 as reserves on the sold loans were released. The HDFS allowance fell from $399M at mid-year to <b class="n">$2.2M</b> at year-end. HDFS paid a <b class="n">$1.0 billion</b> dividend up to the parent in Q4. Total debt fell from $6.96B to $2.97B as the securitization debt left with the receivables. Cash rose to <b class="n">$3.09 billion</b>.</p>

    <div class="plain"><div class="h">In plain English</div><p>Harley-Davidson&rsquo;s finance arm used to lend riders the money to buy the bikes, hold the loans, and earn the interest for years. It sold most of those loans, and most of the future ones, for cash now. The balance sheet got much cleaner. The income statement lost its steadiest line.</p></div>

    {sowhat("03",
            "The 2025 profit is real and it is non-recurring. The recurring picture is a motor company at a loss and a subsidiary at a larger one.",
            "This is why 2025 EPS was $2.78 and not something near zero, and why the 2026 guidance looks like a cliff. It is not a cliff. It is the ground.",
            "The transaction was announced 30 July 2025 by the departing CEO. The incoming one inherited the cash and the lower run rate together.")}
  </div>
</section>''')

    H.append(f'''
<section>
  <div class="wrap">
    {brandrow("04 &middot; The HDFS trade")}
    <h2>$180 million a year, exchanged for $1.25 billion, once</h2>
    <p class="lede">Whether the KKR/PIMCO deal was good depends on what the cash does. Here is what was given up.</p>

    {fig(4, "HDFS operating income", "$ millions &middot; 2026 and 2029 shown at range midpoints", FIG_HDFS, "doc",
         "HDFS earned $235M and $248M in the two years before the sale: <b class='n'>60%</b> of consolidated operating income in 2024. It is guided to $55&ndash;70M for 2026 and targeted at $125&ndash;150M by 2029. The 2025 spike is the transaction. Sources: FY2025 10-K; Q1 and Q2 2026 calls.")}

    {table(["What H-D got", "What H-D gave"],
           [["~$1.25B of &ldquo;discretionary cash&rdquo; (management&rsquo;s figure), of which $450M to debt reduction and ~$500M earmarked for shareholders", "~$180M a year of operating income at the 2024 run rate, rebuilding to perhaps half that by 2029"],
            ["$1.0B dividend from HDFS to the parent in Q4 2025", "9.8% of HDFS, with a right to buy back up to a third a year"],
            ["Balance sheet: total debt $6.96B &rarr; $2.97B; cash $1.59B &rarr; $3.09B", "Two-thirds of future originations, forward-sold for five years"],
            ["A capital-light HDFS with, management says, &ldquo;significantly higher ROE&rdquo;", "The CECL reserve release ($191M) that made 2025 look normal"]],
           widths=["50%", "50%"])}

    <p>{ev("calc")}At the 2024 run rate the foregone earnings are roughly <b class="n">$180M</b> a year. $1.25B of cash buys back about <b class="n">seven years</b> of them, before the 2029 rebuild is counted. That is not a bad trade if the cash is deployed into something that earns more than HDFS did. So far it has gone into a <b class="n">$200M</b> accelerated repurchase (November 2025) at an average of about $26.50, and a balance sheet that now holds $1.9B of cash against a business guided to breakeven.</p>
    <p>{ev("doc")}The trade is already visible in cash. H1 2026 operating cash flow was <b class="n">$(59)M</b> against $509M a year earlier; free cash flow <b class="n">$(104)M</b> against $444M, a $548M swing the Q2 deck attributes &ldquo;in part, due to 67% reduction in HDFS operating income after sale of retail finance receivables in 2H &rsquo;25&rdquo; and to forward-flow timing. The managed retail book is $6.1B: $1.6B owned, <b class="n">$4.5B</b> off balance sheet with KKR and PIMCO. HDMC alone is net cash $933M; HDFS is net debt $(1,848)M; Harley-Davidson, Inc. is net debt $(862)M.</p>
    <p>{ev("ind")}The other thing HDFS did was floor the dealers and finance the riders in downturns when banks would not. A forward-flow partner has a contract; a captive had a reason. Whether KKR and PIMCO buy the two-thirds in 2028 at the same terms they bought it in 2025 is a question the filings cannot answer.</p>

    {sowhat("04",
            "HDFS was Harley&rsquo;s annuity. It has been converted to a lump sum and a smaller annuity.",
            "The plan&rsquo;s $350M HDMC EBITDA target has to carry the enterprise now in a way it did not have to before the sale. The margin for error left with the loan book.",
            "Watch the 2029 HDFS target ($125&ndash;150M). If it slips, the enterprise is a motorcycle company with a service arm, and the motorcycle company is at 5%.")}
  </div>
</section>''')

    # ───── PART III
    H.append(part("part3", "Part III", "The subsidiary",
                  "What LiveWire costs the parent, in the parent&rsquo;s own numbers, and the date on which that stops being a line item and becomes a decision.",
                  "$422M of consolidated operating losses since 2022; a fifth of the 2025 profit drag and a third of the trailing one; from 0.6% of revenue and 2.7% of headcount. Cash runs out around May 2027. The note is due in December 2027.",
                  "Because LiveWire is consolidated, no ownership change short of deconsolidation improves Harley-Davidson&rsquo;s reported operating income. Back to the Bricks handles this by not counting it.",
                  "S2 Del Mar on a Harley floor", "A LiveWire on a Harley-Davidson dealer floor, or the LiveWire space at Harley-Davidson headquarters.", "Sketch: A single electric motorcycle on a display stand at the edge of a dealer showroom, hemmed in by larger cruisers and touring bikes, present day, hard overhead spotlights. Charcoal sketch with a blue-grey wash on a dark chalkboard ground, vignetted edges; any people seen from behind or with faces unresolved, no identifiable ethnicity; 3:2, no logos."))

    H.append(f'''
<section>
  <div class="wrap">
    {brandrow("05 &middot; What LiveWire costs")}
    <h2>Nought point six percent of revenue. A third of the drag.</h2>
    <p class="lede">H-D consolidates LiveWire and reports it as a segment. Every dollar LiveWire loses appears in Harley-Davidson&rsquo;s operating income; only the ~11% belonging to LiveWire&rsquo;s public minority comes back out, below the line.</p>

    {table(["LiveWire segment (H-D basis)", "Operating loss", "As % of H-D consolidated operating income"],
           [["2023", "$(116.8)M", "15.0%"],
            ["2024", "$(109.6)M", '<span class="hi">26.3%</span>'],
            ["2025", "$(75.0)M", "19.4%"],
            ["TTM to 30 Jun 2026", "$(72.1)M", '<span class="hi">33.8%</span>']],
           widths=["40%", "30%", "30%"], cls_map={1: "num", 2: "num"})}

    {fig(5, "LiveWire&rsquo;s share of the drag", "LiveWire operating loss &divide; H-D consolidated operating income", FIG_LW, "calc",
         "Both figures from H-D&rsquo;s segment note. TTM = FY2025 &minus; H1 2025 + H1 2026 for each line. The 2025 figure is flattered by the HDFS transaction in the denominator; on a normalised HDFS the share would be far higher. Loss attributable to noncontrolling interests was $9.6M in 2025; Harley-Davidson shareholders bear roughly <b class='n'>89%</b> of LiveWire&rsquo;s losses.")}

    <p>{ev("calc")}Cumulative LiveWire operating losses consolidated into Harley-Davidson: <b class="n">$337.0M</b> from January 2023 through June 2026, and <b class="n">$422.3M</b> including 2022 (the spin closed 27 September 2022; the stand-alone post-spin Q4 2022 figure is open item 3 in &sect;16). Against the December 2021 plan of 100,000 units and $1.8B of revenue by 2026, LiveWire delivered 923 units and $31.3M trailing. <a href="../01/">Ground Truth No. 01</a> has that story in full.</p>
    <p>{ev("doc")}For scale, in 2025 LiveWire was <b class="n">0.6%</b> of Harley-Davidson&rsquo;s revenue ($25.7M of $4,473M), <b class="n">2.7%</b> of its headcount (about 150 of about 5,500), and <b class="n">19%</b> of the drag on its operating income. In 2026 it is guided to be the difference between a profit and a loss.</p>

    {sowhat("05",
            "A $75M loss did not take Harley-Davidson from $779M to zero. But when the motor company is guided to make $10&ndash;50M, a $75M loss on 0.6% of revenue is no longer a rounding error.",
            "The plan solves this by scoring HDMC. The consolidated income statement, the share count and the dividend do not have that option.",
            "The $150M fixed-cost target is stated as &ldquo;not including LiveWire.&rdquo; LiveWire&rsquo;s own cost cuts (real: 18% less cash used) are the only thing moving this line.")}
  </div>
</section>''')

    H.append(f'''
<section>
  <div class="wrap">
    {brandrow("06 &middot; The seat change")}
    <h2>From equity backstop to senior secured creditor</h2>
    <p class="lede">H-D&rsquo;s remaining direct exposure to LiveWire is one instrument. What changed in it says what the parent intends.</p>

    <div class="clip stack"><span class="cm"></span>
      <div class="row"><div class="lab"><span class="tag">Feb 2024 &middot; original</span><span class="res">Convertible Delayed Draw Term Loan &middot; up to $100M</span></div>
        <div class="hl">Harley-Davidson could convert the loan to LiveWire equity at maturity if LiveWire lacked the capacity to repay. A parent&rsquo;s instrument: if the subsidiary cannot pay, the parent owns more of it. Never drawn.</div>
        <div class="src"><b>LVWR 8-K Ex. 10.1</b><span>14 Feb 2024</span><a href="https://www.sec.gov/Archives/edgar/data/1898795/000189879524000037/executedconvertibleloana.htm" target="_blank" rel="noopener">Open on EDGAR &rarr;</a></div></div>
      <div class="row"><div class="lab"><span class="tag">Nov 2025 &middot; amended &amp; restated</span><span class="res">Delayed Draw Term Loan &middot; $75M &middot; secured</span></div>
        <div class="hl">Conversion feature <strong>removed</strong>. Security interest over <strong>substantially all</strong> of LiveWire&rsquo;s assets added. Six-month SOFR + 4.00%, compounding, all due at maturity, <strong>15 December 2027</strong>. Effective rate 7.64%. The first $10M of any ATM proceeds goes to the lender. Negative covenants on debt, liens, asset sales, investments and affiliate transactions. Drawn in full 15 December 2025.</div>
        <div class="src"><b>LVWR 10-K FY2025 &middot; related-party note</b><span>Filed Feb 2026</span><a href="https://www.sec.gov/Archives/edgar/data/1898795/000189879526000028/R24.htm" target="_blank" rel="noopener">Open on EDGAR &rarr;</a></div></div>
    </div>

    <p>{ev("inf")}Read the two together and the parent moved from prospective equity holder to senior secured creditor of its own subsidiary, twelve months before it published a strategy with no subsidiary in it. On the Q4 2025 call Starrs said: <em>&ldquo;LiveWire is now working diligently to attract its own sources of capital to continue to finance its operations and future plans.&rdquo;</em> The FY2025 10-K risk factors name &ldquo;the ability of LiveWire to obtain sufficient funding from sources other than the Company.&rdquo;</p>
    <p>{ev("unv")}Ground Truth No. 01 quoted the FY2025 10-K as stating H-D &ldquo;does not plan to make additional investments in LiveWire beyond the amount outstanding under the Term Loan.&rdquo; This revision could not re-locate the sentence in the fetched text of the filing (the MD&amp;A liquidity section was truncated in retrieval). It is carried here as unverified until the page and paragraph are confirmed (open item 1, &sect;16). The Q4 call language above is the verified equivalent.</p>

    {sowhat("06",
            "A convertible loan says: if this fails, we own it. A secured loan says: if this fails, we get paid first.",
            "That is the paper behind &ldquo;working diligently to attract its own sources of capital.&rdquo; The parent has chosen its seat.",
            "Any third-party capital LiveWire raises now sits behind H-D&rsquo;s lien. That is a hard pitch to a new investor, which is the point.")}
  </div>
</section>''')

    H.append(f'''
<section>
  <div class="wrap">
    {brandrow("07 &middot; The clock")}
    <h2>Cash to May 2027. A note due in December. A plan scored on 2027.</h2>
    <p class="lede">LiveWire&rsquo;s own 10-Q supplies the runway. H-D&rsquo;s filings supply the constraint. The calendar supplies the collision.</p>

    <div class="duo">
      <div class="card mag">
        <div class="k">LiveWire cash &middot; 30 Jun 2026</div>
        <div class="big mag">$52.9M</div>
        <p>From <b class="n">$82.8M</b> at year-end. Burn <b class="n">$29.9M</b> in six months. At that rate: about <b class="n">ten and a half months</b>.</p>
      </div>
      <div class="card">
        <div class="k">Owed to Harley-Davidson &middot; due 15 Dec 2027</div>
        <div class="big">$76.8M</div>
        <p>And compounding at SOFR + 4%. Roughly <b class="n">$85M</b> at maturity. Secured on substantially everything.</p>
      </div>
    </div>

    <p>{ev("calc")}Straight-line the H1 2026 burn and LiveWire&rsquo;s cash reaches zero around <b class="n">May 2027</b>. The note is due seven months later. Back to the Bricks&rsquo; only dated target, $350M of HDMC EBITDA, is for 2027. Harley-Davidson will make its LiveWire decision in the same year it has promised to prove the new strategy works, and it has not said what the decision is.</p>

    <h3 style="font-size:clamp(21px,2.6vw,28px)">The options, as they stand on the filings</h3>
    <p>This is an enumeration, not a prediction. H-D has stated no intention to fund, acquire, divest or wind down LiveWire, and none is asserted here.</p>
    {table(["Option", "What it costs H-D", "What it does to H-D&rsquo;s P&amp;L"],
           [["<strong>Fund LiveWire again</strong>", "Reverses the stated position; cash", "Nothing; the losses are already consolidated"],
            ["<strong>Buy out the minority</strong> (~23.3M public shares)", "~$28M at $1.20. The 4 Aug 2026 severance amendment already carves an H-D acquisition out of &ldquo;change in control&rdquo;", "Nothing; already consolidated. Removes public-company cost and the NCI line"],
            ["<strong>Let LiveWire raise from third parties</strong>", "Dilution below ~89%. At $1.20 a $60M raise is ~50M shares, taking H-D to ~70%. New money sits behind H-D&rsquo;s lien", "Still consolidated above 50%"],
            ["<strong>Let it fail / foreclose</strong>", "Write-down of the $75M note against the collateral; wind-down costs; the contracts in No. 01 unwind", "Losses stop. Deconsolidation gain or loss"],
            ["<strong>Sell or merge it</strong>", "Depends on the buyer. H-D keeps the manufacturing and services agreements either way", "Deconsolidation"]],
           widths=["26%", "40%", "34%"])}

    <p>{ev("calc")}Note what every row shares. <strong>Because LiveWire is already consolidated, no ownership change short of deconsolidation improves Harley-Davidson&rsquo;s reported operating income.</strong> The $70&ndash;80M a year comes out of H-D&rsquo;s numbers only when LiveWire stops losing it or stops being H-D&rsquo;s. Buying the minority for $28M would be the cheapest corporate action in the company&rsquo;s recent history and would change the operating line by exactly nothing.</p>

    {sowhat("07",
            "The decision has a date, and it is inside the plan&rsquo;s window.",
            "Back to the Bricks does not mention it. The Q1 and Q2 2026 calls treated LiveWire operationally: Honcho, Dust, cash used. No 2026 statement from Starrs or Root uses &ldquo;strategic alternatives,&rdquo; &ldquo;divestiture&rdquo; or &ldquo;wind-down.&rdquo;",
            "LiveWire&rsquo;s 10-Q says it will pursue financing &ldquo;during the third quarter of 2026.&rdquo; That quarter ends in three weeks.")}
  </div>
</section>''')

    # ───── PART IV
    H.append(part("part4", "Part IV", "The plan",
                  "What Back to the Bricks actually commits to, and what the plan it replaces committed to.",
                  "Five pillars and six targets, all HDMC. The 2027 EBITDA number translates to roughly a 5% operating margin, below 2019. Hardwire promised 15% by 2025 and delivered (0.8%).",
                  "A stabilisation plan with a growth target attached is a reasonable thing to publish after 2025. Calling it ambitious is not.",
                  "Back to the Bricks", "The 5 May 2026 webcast title slide, or Starrs at a dealer meeting.", "Sketch: A chief executive at a lectern addressing a hall of motorcycle dealers, a wide blank screen behind him, 2026 corporate meeting, cool stage lighting. Charcoal sketch with a blue-grey wash on a dark chalkboard ground, vignetted edges; any people seen from behind or with faces unresolved, no identifiable ethnicity; 3:2, no logos."))

    H.append(f'''
<section>
  <div class="wrap">
    {brandrow("08 &middot; Back to the Bricks")}
    <h2>Five pillars, six targets, and what is not in it</h2>
    <p class="lede">The release is short. I quote the pillars in full because the paraphrases in circulation are more ambitious than the document.</p>

    <div class="paper">
      <div class="c"><div class="n">Pillar 1</div><div class="t">Competitive advantages and legacy</div><div class="r">&ldquo;The Company&rsquo;s iconic brand, diversified and powerful revenue channels, and best-in-class dealer network provide a powerful foundation for growth.&rdquo;</div></div>
      <div class="c"><div class="n">Pillar 2</div><div class="t">Exclusive dealer network</div><div class="r">&ldquo;The Company is planning actions to enable dealers to <b>double profitability in 2026</b> and then <b>double it again by 2029</b>.&rdquo;</div></div>
      <div class="c"><div class="n">Pillar 3</div><div class="t">Recapture share where H-D has &ldquo;right to win&rdquo;</div><div class="r">&ldquo;&hellip;new motorcycles, used motorcycles, Parts &amp; Accessories, and Apparel &amp; Licensing.&rdquo; Not electric.</div></div>
      <div class="c"><div class="n">Pillar 4</div><div class="t">Strong financial position</div><div class="r">&ldquo;Cost and restructuring actions already underway support a path to stronger free cash flow and EBITDA margin over time.&rdquo;</div></div>
      <div class="c"><div class="n">Pillar 5</div><div class="t">Bolstered management team</div><div class="r">&ldquo;&hellip;a number of leadership appointments that support the Company as it leverages its innate strengths.&rdquo;</div></div>
    </div>

    {table(["Target", "Stated", "Against the record"],
           [["HDMC EBITDA", "<strong>&gt; $350M in 2027</strong>, the only dated number", f"{ev('calc')}The Q2 2026 deck&rsquo;s reconciliation gives HDMC D&amp;A of $40M for the quarter and $81M for the half, about $160M a year (restructuring adjustments of $3M / $17M are separate). <strong>$350M of EBITDA implies roughly $190M of operating income, about a 5% margin</strong> on 2025 revenue. HDMC made $290M in 2019 and $661M in 2023."],
            ["Retail unit growth", "Mid-single-digit CAGR, &ldquo;medium term&rdquo; (Starrs: three to five years)", "~5% on 132,535 is about <strong>6,600 motorcycles a year</strong>. The 2019&ndash;2025 CAGR was <strong>&minus;8%</strong>. Retail has fallen every year since 2021."],
            ["HDMC gross margin", "25&ndash;30%", "2025: 24.2%. 2024: 28.0%. 2023: 32.3%. This is a return to 2024."],
            ["HDMC opex", "&lt; 20% of sales", "2025: 25.0% ($895M / $3,578M). Needs the $150M cost take-out <em>and</em> revenue growth."],
            ["HDMC EBITDA margin", "10&ndash;12%", "Hardwire Stage II targeted <strong>15% operating margin by 2025</strong>. Delivered: (0.8%)."],
            ["P&amp;A and Apparel/Licensing", "Mid-single-digit CAGR", "P&amp;A revenue: $652M (2024) &rarr; $614M (2025). Some 30% of eliminated SKUs being reinstated."],
            ["Fixed cost", "&ldquo;at least $150 million&hellip; impacting 2027 and beyond versus 2025 levels&rdquo;", "&ldquo;Not including LiveWire.&rdquo; Restructuring expense so far: $17M for H1 2026 per the Q2 deck. A March 2026 reduction in force, size undisclosed."]],
           widths=["18%", "30%", "52%"])}

    <div class="note">
      <div class="h">What is not in it</div>
      <p>No revenue target in dollars. No EPS target. No free-cash-flow number. No HDFS target beyond the separately stated 2029 range. No volume for Sportster or Sprint. No capital-return commitment. Starrs, February 2026: &ldquo;we expect to be measured in our approach to share repurchases.&rdquo; <strong>No LiveWire target. The word &ldquo;electric&rdquo; does not appear.</strong> LiveWire is in the forward-looking factors only: &ldquo;the demand for and consumer willingness to adopt two- and three-wheeled electric vehicles,&rdquo; and the ability to &ldquo;realize the desired business benefits from LiveWire operating as a separate public company.&rdquo;</p>
    </div>

    <p class="pull">The 2027 target is below where the company stood the year before the strategy it replaces was written.</p>

    {sowhat("08",
            "Back to the Bricks is a plan to get HDMC to roughly 2019 profitability on 60% of 2019&rsquo;s volume, by 2027. A stabilisation plan with growth attached for years three to five.",
            "It scores itself on the one metric that excludes the subsidiary. Consolidated, the enterprise is a 5% motor company plus a shrunken HDFS minus $70M.",
            "The dealer-profitability doubling is the most concrete promise and the most checkable. Starrs in July: &ldquo;we expect domestic dealer profitability to double in 2026.&rdquo; Hold him to it.")}
  </div>
</section>''')

    H.append(f'''
<section>
  <div class="wrap">
    {brandrow("09 &middot; Hardwire, scored")}
    <h2>Every quantified target missed, most by the full amount</h2>
    <p class="lede">Back to the Bricks replaces Hardwire (announced 2 February 2021; Stage II targets set 10 May 2022). The company set this benchmark for itself. I use it as written.</p>

    {table(["Hardwire commitment", "Target", "Delivered, FY2025"],
           [["HDMC revenue growth", "&ldquo;+5% to +7% CAGR 2021&ndash;2025&rdquo; &rarr; ~$5.5&ndash;5.9B", '<span class="hi">$3,578M</span>, down 21% from 2021'],
            ["HDMC operating margin", "<strong>&ldquo;15% by 2025&rdquo;</strong>", '<span class="hi">(0.8%)</span>'],
            ["Diluted EPS", "&ldquo;low double-digit growth&rdquo;", "$4.19 (2021) &rarr; <strong>$2.78</strong>"],
            ["HDFS operating income", "&ldquo;double-digit growth&rdquo; (2021); +3&ndash;5% CAGR (2022)", "$490M via a one-time sale; 2026 guided $55&ndash;70M"],
            ["Cost productivity", "&ldquo;$400 million&hellip; for HDMC by 2025&rdquo;", "New plan requires a further $150M"],
            ["Profit focus", "&ldquo;Touring, large Cruiser and Trike&rdquo;", "Touring inventory overhang; Q4 2025 HDMC gross margin (8.0%); U.S. share 37.9% &rarr; 34.5%"],
            ["Selective expansion", "Pan America; &ldquo;profitable middleweight offerings&rdquo;", "Rev Max moved to Thailand (Aug 2024), now moving back to York (Jun 2026); Sportster discontinued, now returning"],
            ["<strong>&ldquo;Lead in Electric&rdquo;</strong>", "&ldquo;Electric motorcycles are important to Harley-Davidson&rsquo;s future&rdquo;; separate division; 100,000 LiveWire units a year from 2026", '<span class="hi">923 units TTM. $422M of consolidated losses.</span> &ldquo;We leaned heavily into&hellip; Electric.&rdquo;']],
           widths=["22%", "36%", "42%"])}

    <p>{ev("doc")}The one structural Hardwire commitment that was executed, separating LiveWire into a public company, is the one that produced the $422M. The shareholder record of the rest is the 2025 annual meeting: <b class="n">over 48%</b> of votes cast were withheld from Zeitz, and over 40% from the presiding director and one other, on H Partners&rsquo; campaign. The board committed that all three would leave before the 2026 meeting; all three did. Starrs was appointed 4 August 2025 from Topgolf, before that Pizza Hut. At the 2026 meeting the withhold vote against him was 1.5%. <em>(Open item 9: the 2025 tallies are from press reports of preliminary results; pull the Item 5.07 8-K.)</em></p>

    {sowhat("09",
            "The company&rsquo;s last five-year plan missed every number it published. The new one publishes fewer numbers.",
            "That is not cynicism; it may be wisdom. But the fairest test of Back to the Bricks is the one Hardwire failed: what was said, what was delivered, in the company&rsquo;s own units.",
            "Ground Truth will score it the same way, on the same table, in 2027.")}
  </div>
</section>''')

    # ───── PART V
    H.append(part("part5", "Part V", "The bet",
                  "What the capital did, and the one motorcycle the growth target is riding on.",
                  "$1.63B of buybacks at an average of $31 for a stock at $28. A mid-single-digit growth target that needs about 6,600 units a year, and a Sportster that once sold 35,000&ndash;40,000.",
                  "The plan has one volume lever. It was discontinued four years ago because it did not make money. Starrs says the cost is now right. Nothing else in the lineup has that kind of volume in it.",
                  "Sportster 883", "An Evolution-engined 883: Iron 883 or a customised example. The bike the plan is betting on.", "Sketch: An air-cooled Sportster 883 with a peanut tank and low bars, parked at a kerb on a city street, late 2010s, low evening sun. Charcoal sketch with a blue-grey wash on a dark chalkboard ground, vignetted edges; any people seen from behind or with faces unresolved, no identifiable ethnicity; 3:2, no logos."))

    H.append(f'''
<section>
  <div class="wrap">
    {brandrow("10 &middot; Capital returned")}
    <h2>$1.6 billion of buybacks, and the stock where it started</h2>
    <p class="lede">The share count fell 25%. The price did not follow. What the company paid, against what the shares are worth.</p>

    {table(["Year", "Repurchased", "Shares", "Average price"],
           [["2022", "$324M", "8.4M", "$38.6"], ["2023", "$350M", "10.2M", "$34.3"], ["2024", "$450M", "12.5M", "$36.0"],
            ["2025", "$347M", "13.1M", "$26.5"], ["H1 2026", "$158M", "7.9M", "$20.0"],
            ["<strong>Total</strong>", "<strong>$1,629M</strong>", "<strong>52.1M</strong>", "<strong>$31.3</strong>"]],
           widths=["25%", "25%", "25%", "25%"], cls_map={1: "num", 2: "num", 3: "num"})}

    {fig(6, "Average repurchase price by year, against the share price today", "$ per share", FIG_BUY, "calc",
         "Averages are annual dollars divided by annual shares from the results releases; ASR settlement timing may shift the 2025/2026 split slightly (open item 11). HOG closed at <b class='n'>$28.30</b> on 4 September 2026. The 52.1M shares bought for $1.63B are worth about <b class='n'>$1.47B</b> at that price.")}

    <p>{ev("doc")}Diluted shares: 145.1M (2023) &rarr; 108.6M (Q2 2026). Market capitalisation about <b class="n">$2.9B</b>, for a company that made $779M of operating income three years ago and holds $1.9B of cash today. HOG was <b class="n">$30.47</b> the day Zeitz took the job in February 2020. It is $28.30. Six and a half years, $1.6B of buybacks, a $1.25B balance-sheet transaction and a new CEO, and the shares are where they started. Consensus target as of 4 September: $27, rated Hold.</p>

    {sowhat("10",
            "The buyback shrank the denominator and the business shrank faster.",
            "The $1.25B from HDFS is the last large pool of discretionary cash. &ldquo;Measured&rdquo; repurchases is the right word; it is also an admission that the last $1.6B did not work.",
            "If the plan lands, the share count makes every dollar of 2027 EBITDA worth more per share. If it does not, the company has spent its cushion buying its own decline.")}
  </div>
</section>''')

    H.append(f'''
<section>
  <div class="wrap">
    {brandrow("11 &middot; The Sportster arithmetic")}
    <h2>One motorcycle carries the growth target</h2>
    <p class="lede">Two bikes and a return. Here is why the second one matters more than everything else in the announced lineup combined.</p>

    <div class="paper">
      <div class="c"><div class="n">Sprint &middot; ships end-2026</div><div class="t">The entry bike</div><div class="r">Zeitz, July 2025: &ldquo;targeting an entry price below $6,000.&rdquo; Starrs to Reuters, May 2026: &ldquo;approximately $6,000.&rdquo; Motorcycle.com, same day: the sub-$6,000 language is gone from the filings and the target is &ldquo;less than $10,000.&rdquo; Trade reporting describes a 440cc single derived from the Hero MotoCorp X440, built in India. <b>None of platform, plant or price is confirmed in a primary source.</b></div><div class="k">Open item 5 &middot; UBS&rsquo;s first Q1 question: will it be tariffed?</div></div>
      <div class="c"><div class="n">Sportster 883 &middot; 2027</div><div class="t">The bet</div><div class="r">Starrs, Q1 call: &ldquo;what we&rsquo;re talking about today is the 883.&rdquo; Air-cooled, &ldquo;middleweight,&rdquo; &ldquo;accessible starting price point.&rdquo; Q2: &ldquo;the return of the Sportster 883 in 2027, which our European dealers are particularly excited about.&rdquo; Price and plant (~$10,000; York) are trade reporting only.</div><div class="k">Open item 6</div></div>
      <div class="c"><div class="n">Rev Max &middot; announced 10 Jun 2026</div><div class="t">Comes home</div><div class="r">Pan America, Sportster S and Nightster production returns from Rayong, Thailand to York and Menomonee Falls before 2027, reversing the August 2024 move. York to build &ldquo;over 100,000 motorcycles&rdquo; in 2027. Tariffs cost $67M in 2025; guided $75&ndash;90M for 2026.</div><div class="k">Company statement &middot; Q2 call</div></div>
    </div>

    {fig(7, "What the growth target needs, against what the Sportster used to sell", "motorcycles per year", FIG_SPORT, "calc",
         "A mid-single-digit CAGR on 132,535 units is about <b class='n'>6,600</b> incremental motorcycles a year. Starrs on the Q1 call: the Sportster market &ldquo;as recently as five, six years ago&hellip; was 35,000&ndash;40,000+ on a global basis&rdquo; (the transcript renders it with a dollar sign; it is units). A Sportster that recovers a third of that delivers two years of the plan&rsquo;s entire growth target on its own.")}

    <p>{ev("ind")}Nothing else in the announced lineup has that kind of volume in it. Twenty &ldquo;new models and trims&rdquo; over three years, per the strategy slides, are mostly Touring and Softail variants and price-point trims: Street Bob $14,999, Low Rider S $18,999, Road Glide Solo $25,999. Those defend share; they do not add 6,600 units a year. The Sportster does, if it works.</p>
    <p>{ev("doc")}And the risk was stated on the call by Raymond James: <em>&ldquo;there&rsquo;s a reason why Sportster was discontinued, right? It was hard to make money.&rdquo;</em> Starrs: <em>&ldquo;We have the cost at a place that we&rsquo;re extremely comfortable against the expected MSRP.&rdquo;</em> Used values, per Starrs, are &ldquo;at or above original MSRP&rdquo;; that is a real demand signal. So the plan&rsquo;s growth is, in practice, a bet that a motorcycle discontinued because it could not make money can come back at a price where it does, into a market a third smaller than when it left, through a dealer network 21% smaller. Not an unreasonable bet. But one bet, and the plan does not have a second.</p>
    <p>{ev("doc")}Europe is where it is most needed. EMEA retail fell 11% in 2025 and 9% in Q2 2026; share moved &ldquo;from 4% to 3%.&rdquo; Starrs: &ldquo;We are not satisfied with our performance there.&rdquo;</p>

    {sowhat("11",
            "Back to the Bricks has one volume lever, and it is the 883.",
            "That lever is also the answer to Hardwire&rsquo;s abandonment of the entry rider, and to the question LiveWire was created to answer. The company&rsquo;s accessible bike is a $10,000 air-cooled twin, not an electric.",
            "The 883&rsquo;s first full year is 2027, the same year as the EBITDA target and the LiveWire note. Everything lands at once.")}
  </div>
</section>''')

    H.append(f'''
<section>
  <div class="wrap">
    {brandrow("12 &middot; 2027, if it works")}
    <h2>Take every target at face value</h2>
    <p class="lede">Assume Back to the Bricks lands exactly as written and on time. This is the company it describes.</p>

    {table(["2027, plan delivered", ""],
           [["Worldwide retail", "~143,000 (2026 guidance midpoint plus 5%): <strong>66% of 2019, 53% of 2014</strong>"],
            ["HDMC revenue", "~$3.8B (flat pricing; Sportster/Sprint mix dilutes ASP)"],
            ["HDMC EBITDA / operating income", "$350M+ / ~$190M: <strong>~5% margin, below 2019&rsquo;s 6.3%</strong>"],
            ["HDFS operating income", "~$80&ndash;100M on the path to $125&ndash;150M by 2029: <strong>a third of 2024</strong>"],
            ["LiveWire", "Unaddressed. Loss guided $70&ndash;80M for 2026; cash exhausted mid-2027; $85M owed to the parent in December"],
            ["Consolidated operating income", "<strong>~$210M</strong> if LiveWire is still losing $70M; <strong>~$280M</strong> if it is gone"],
            ["Dealers", "~1,150, &ldquo;twice as profitable as 2025&rdquo;"],
            ["Share count", "~100M at a &ldquo;measured&rdquo; pace"]],
           widths=["32%", "68%"])}

    {fig(8, "Consolidated operating income, actual and implied", "$ millions &middot; 2026 at guidance midpoint; 2027 on the plan&rsquo;s own targets", FIG_2027, "calc",
         "2023&ndash;2025 from the 10-K. 2026 is the midpoint of the guidance sum in &sect;01. 2027 assumes ~$190M of HDMC operating income (from the $350M EBITDA target and ~$160M of D&amp;A), ~$90M of HDFS, and LiveWire either at a $70M loss or deconsolidated. Every 2027 input is the company&rsquo;s, not mine; the arithmetic is.")}

    <p>Even in the success case, Harley-Davidson in 2027 is a company earning about a quarter of what it earned in 2023, selling about two-thirds of the motorcycles it sold in 2019, through three-quarters of the dealers, with its finance company deliberately shrunk and its electric subsidiary either wound up or still consuming a third of the profit. <strong>That is the plan, working.</strong></p>
    <p>The plan not working looks like 2025 again: a Touring overhang, promotional spend, a negative gross margin in the fourth quarter, and a consolidated profit that depends on a non-recurring event. Except that the non-recurring event has already been used.</p>

    {sowhat("12",
            "The upside case is a smaller, slightly profitable Harley-Davidson. The downside case is 2025 without the HDFS sale to cover it.",
            "This is the read-through No. 01 promised: what LiveWire is doing to the parent&rsquo;s numbers. The answer is that it is the difference between the two 2027 columns, and the plan does not choose between them.",
            "Q3 2026 results, late October, are the first test: whether H2 tracks H1 or tracks Q4 2025.")}
  </div>
</section>''')

    # ───── PART VI
    H.append(part("part6", "Part VI", "The final word",
                  "Three things that are true at once, and the question the plan leaves open.",
                  "LiveWire did not break Harley-Davidson. LiveWire is exactly what the new Harley-Davidson cannot afford. And the decision about it has a date inside the plan&rsquo;s own window.",
                  "Anyone telling you the electric bet sank Harley is choosing the flattering villain. Anyone telling you it does not matter is not adding up the guidance.",
                  "The bricks", "Headquarters brickwork, close. Or a York assembly line.", "Sketch: A motorcycle assembly line in York, Pennsylvania, workers lowering an engine into a frame on a moving conveyor, present day, high skylight factory light. Charcoal sketch with a blue-grey wash on a dark chalkboard ground, vignetted edges; any people seen from behind or with faces unresolved, no identifiable ethnicity; 3:2, no logos."))

    H.append(f'''
<section class="final-sec">
  <div class="wrap">
    {brandrow("13 &middot; Analysis, not reporting")}
    <h2>Which brick is LiveWire under?</h2>
    <p class="lede">Sections 01&ndash;12 are sourced. This one is judgment, and says so.</p>

    <div class="kn">
      <div class="kn-row"><div class="kn-l">{ev("inf")}One</div><div class="kn-t"><strong>LiveWire is not what broke Harley-Davidson.</strong> A $75M annual loss does not take a company from $779M of operating income to breakeven. The Touring overhang, a 12% retail decline in 2025, $67M of tariffs, a negative-gross-margin quarter and the deliberate shrinking of HDFS did that. The electric bet is the flattering villain: it lets everyone else off.</div></div>
      <div class="kn-row"><div class="kn-l">{ev("calc")}Two</div><div class="kn-t"><strong>LiveWire is exactly what the new plan cannot afford.</strong> When the motor company is guided to make $10&ndash;50M, a $70&ndash;80M loss on 0.6% of revenue is the difference between a profitable year and a losing one. The plan solves this by not counting it. The income statement does not have that option.</div></div>
      <div class="kn-row"><div class="kn-l">{ev("doc")}Three</div><div class="kn-t"><strong>The decision has a date.</strong> LiveWire&rsquo;s cash lasts to roughly May 2027 at the current burn. Its note to the parent is due 15 December 2027. Back to the Bricks&rsquo; one dated target is 2027. Harley-Davidson will make its LiveWire decision in the year it has promised to prove the new strategy works, and it has not yet said what the decision is.</div></div>
    </div>

    <div class="final">
      <div class="h">The final word</div>
      <h3>Back to the Bricks has five pillars, six targets and a two-year clock.</h3>
      <p>The plan is a reasonable one. Stabilise the motor company, fix the dealers, bring back the bike people actually ask for, take $150M of cost out, and get to a 5% margin by 2027. After 2025, that is not timid; it is honest. But it is scored on HDMC, and Harley-Davidson, Inc. is not HDMC. It is HDMC plus a finance company that has been sold forward, minus a subsidiary that is guided to lose more than the motor company is guided to make, with a note coming due in the plan&rsquo;s own target year.</p>
      <p><strong>No. 01 asked: congrats on what. This one asks something simpler. Which brick is LiveWire under, and who is going to lift it?</strong></p>
    </div>
  </div>
</section>''')

    # ───── SOURCES
    src_rows = [
        ("Form 10-K, FY2025", "Harley-Davidson, Inc.", "26 Feb 2026", "Segment note (HDMC/LiveWire/HDFS); MIC share; dealer counts; debt; repurchases; LiveWire risk factors; HDFS transaction accounting", "https://www.sec.gov/Archives/edgar/data/793952/000079395226000011/0000793952-26-000011-index.html", "0000793952-26-000011"),
        ("Form 10-Q, Q2 2026", "Harley-Davidson, Inc.", "5 Aug 2026", "Q2 and H1 segment results; cash; debt; repurchases; noncontrolling interest", "https://www.sec.gov/Archives/edgar/data/793952/000079395226000061/0000793952-26-000061-index.htm", "0000793952-26-000061"),
        ("Form 8-K: Q2 2026 results", "Harley-Davidson, Inc.", "23 Jul 2026", "Ex. 99.1. Raised 2026 guidance: HDMC $10&ndash;50M, HDFS $55&ndash;70M, LiveWire $(70&ndash;80)M; retail; dealer inventory", "https://www.sec.gov/Archives/edgar/data/793952/000079395226000058/a8kq22026exhibit991v2.htm", "0000793952-26-000058"),
        ("Form 8-K: Q1 2026 results", "Harley-Davidson, Inc.", "5 May 2026", "Ex. 99.1. Q1 results; original 2026 guidance reaffirmed; Back to the Bricks introduced", "https://www.sec.gov/Archives/edgar/data/793952/000079395226000029/a8kq12026exhibit991.htm", "0000793952-26-000029"),
        ("&ldquo;Back to the Bricks&rdquo; release", "Harley-Davidson, Inc.", "5 May 2026", "Five pillars verbatim; $350M 2027 HDMC EBITDA; medium-term targets; forward-looking factors naming LiveWire and Sportster", "https://investor.harley-davidson.com/news/news-details/2026/Harley-Davidson-Announces-Back-to-the-Bricks-Strategic-Plan-to-Restore-Performance-and-Deliver-Profitable-Growth/default.aspx", "Investor site"),
        ("Q4/FY2025 results and 2026 outlook", "Harley-Davidson, Inc.", "10 Feb 2026", "FY2025 results; original 2026 guidance; HDFS &ldquo;record-high earnings, driven by the HDFS transaction&rdquo;; $1B HDFS dividend", "https://investor.harley-davidson.com/news/news-details/2026/Harley-Davidson-Delivers-Fourth-Quarter-and-Full-Year-Financial-Results-and-2026-Outlook/default.aspx", "Investor site"),
        ("Q4 2025 earnings call", "Harley-Davidson, Inc.", "10 Feb 2026", "Starrs on LiveWire &ldquo;working diligently to attract its own sources of capital&rdquo;; Root on tariffs ($67M 2025) and the HDFS sale", "https://www.fool.com/earnings/call-transcripts/2026/02/10/harley-davidson-hog-q4-2025-earnings-transcript/", "Transcript"),
        ("Q1 2026 earnings call", "Harley-Davidson, Inc.", "5 May 2026", "&ldquo;Leaned heavily into Touring and Electric&rdquo;; Sportster 883 and the 35,000&ndash;40,000 figure; Raymond James on Sportster economics; $150M cost target", "https://www.fool.com/earnings/call-transcripts/2026/05/05/harley-davidson-hog-q1-2026-earnings-transcript/", "Transcript"),
        ("Q2 2026 earnings call", "Harley-Davidson, Inc.", "23 Jul 2026", "Raised guidance; &ldquo;dealer profitability to double in 2026&rdquo;; Sprint end-2026, Sportster 883 in 2027; EMEA share; LiveWire operational update", "https://www.benzinga.com/news/26/07/60642023/transcript-harley-davidson-q2-2026-earnings-conference-call", "Transcript"),
        ("KKR / PIMCO strategic partnership", "Harley-Davidson, Inc.", "30 Jul 2025", "Deal structure: $5B+ receivables, 9.8% of HDFS, forward flow; &ldquo;~$1.25 billion discretionary cash&rdquo;; $450M debt, ~$500M to shareholders", "https://investor.harley-davidson.com/news/news-details/2025/Harley-Davidson-Announces-Strategic-Partnership-with-KKR-and-PIMCO/default.aspx", "Investor site"),
        ("KKR / PIMCO: residual interests sale", "Harley-Davidson, Inc.", "25 Aug 2025", "Step one completed; ~$2B VIEs and $1.8B of debt removed; &gt;$230M proceeds; $1.8B HDFS valuation", "https://investor.harley-davidson.com/news/news-details/2025/Harley-Davidson-Achieves-Milestone-in-Strategic-Partnership-with-KKR-and-PIMCO-with-Completion-of-Sale-of-Residual-Interests-in-Securitized-Consumer-Loan-Receivables/default.aspx", "Investor site"),
        ("Hardwire strategic plan", "Harley-Davidson, Inc.", "2 Feb 2021", "Six priorities including &ldquo;Lead in Electric&rdquo;; 2021&ndash;25 targets: MSD revenue growth, margin improvement, low-double-digit EPS growth", "https://investor.harley-davidson.com/news/news-details/2021/Harley-Davidson-Unveils-The-Hardwire-Five-Year-Strategic-Plan-Targets-Profitable-Growth-And-Brand-Desirability/default.aspx", "Investor site"),
        ("Hardwire Stage II: investor day", "Harley-Davidson, Inc.", "10 May 2022", "&ldquo;HDMC Operating Margin: 15% by 2025&rdquo;; +5&ndash;7% revenue CAGR; $400M cost productivity", "https://investor.harley-davidson.com/news/news-details/2022/Harley-Davidson-2022-Investor-Day-Update-Hardwire-Stage-II/default.aspx", "Investor site"),
        ("Form 8-K: CEO appointment", "Harley-Davidson, Inc.", "4 Aug 2025", "Starrs appointed effective 1 Oct 2025; compensation terms; Zeitz transition", "https://www.sec.gov/Archives/edgar/data/793952/000079395225000166/hog-20250730.htm", "0000793952-25-000166"),
        ("Form 8-K Ex. 17.1 / 17.2: Dourdeville letters", "Harley-Davidson, Inc.", "Apr 2025", "Director resignation; TSR under current leadership; call for Zeitz, Linebarger and Levinson to resign", "https://sec.gov/Archives/edgar/data/793952/000079395225000085/dourdevillelettertoharle.htm", "0000793952-25-000085"),
        ("H Partners: withhold campaign and result", "H Partners Management", "16 Apr / 14 May 2025", "Campaign against three directors; &ldquo;nearly 50% of overall shares voted withhold&rdquo;; board commitments", "https://www.businesswire.com/news/home/20250514503704/en/", "Business Wire"),
        ("Form 8-K: 2026 annual meeting", "Harley-Davidson, Inc.", "21 May 2026", "Certified director votes; Starrs 70.0M for / 1.1M withheld", "https://www.stocktitan.net/sec-filings/HOG/8-k-harley-davidson-inc-reports-material-event-4b5e29845596.html", "Item 5.07"),
        ("Form 10-K, FY2019", "Harley-Davidson, Inc.", "Feb 2020", "2019 dealer counts (698 U.S.; 1,569 worldwide); headcount", "https://www.sec.gov/Archives/edgar/data/793952/000079395220000008/hog10-k12x31x2019.htm", "0000793952-20-000008"),
        ("Results releases FY2014, FY2019&ndash;FY2023", "Harley-Davidson, Inc.", "2015&ndash;2024", "Trend table: retail, shipments, Motorcycles segment operating income, revenue", "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000793952&type=8-K", "EDGAR 8-K index"),
        ("Form 10-K, FY2025", "LiveWire Group, Inc.", "Feb 2026", "Term loan terms (A&amp;R Nov 2025; drawn 15 Dec 2025; due 15 Dec 2027; SOFR + 4%; secured); shares outstanding; cash", "https://www.sec.gov/Archives/edgar/data/1898795/000189879526000028/0001898795-26-000028-index.htm", "0001898795-26-000028"),
        ("Form 10-Q, Q2 2026", "LiveWire Group, Inc.", "5 Aug 2026", "Cash $52.9M; H1 burn; going-concern-adjacent language; Item 5 severance amendment carving out an H-D acquisition", "https://www.sec.gov/Archives/edgar/data/1898795/000189879526000085/0001898795-26-000085-index.htm", "0001898795-26-000085"),
        ("Form 8-K Ex. 10.1: Convertible Delayed Draw Term Loan", "LiveWire Group, Inc.", "14 Feb 2024", "Original $100M convertible instrument, for comparison with the Nov 2025 restatement", "https://www.sec.gov/Archives/edgar/data/1898795/000189879524000037/executedconvertibleloana.htm", "0001898795-24-000037"),
        ("Rev Max production returns to York", "Harley-Davidson, Inc.", "10 Jun 2026", "Pan America, Sportster S, Nightster production from Thailand to York/Menomonee Falls; &ldquo;over 100,000 motorcycles at York in 2027&rdquo;", "https://ultimatemotorcycling.com/2026/06/10/harley-davidson-bringing-revolution-max-production-back-to-u-s/", "Company statement via trade press"),
        ("Reuters: Back to the Bricks", "Reuters", "5 May 2026", "Starrs: Sprint &ldquo;approximately $6,000&rdquo;", "https://www.globalbankingandfinance.com/harley-davidson-bets-affordable-models-dealer-network-latest/", "Secondary"),
        ("Motorcycle.com: Sprint pricing; Sportster 883; plan slides", "Motorcycle.com", "5&ndash;7 May 2026", "Sub-$6,000 language dropped; ~$10,000 883; 20 models/trims; price-point trims", "https://www.motorcycle.com/bikes/features/harley-davidson-announces-back-to-the-bricks-business-plan-44664700", "Secondary"),
        ("Ground Truth No. 01", "Contact Patch Advisory", "Sep 2026", "LiveWire operating detail, contracts, the loan, the 2021 plan of record", "../01/", "This site"),
    ]
    rows_html = []
    for doc, who, filed, what, url, acc in src_rows:
        rows_html.append(f'''<tr>
          <td><strong>{doc}</strong><br><span style="color:var(--ink-3)">{who}</span></td>
          <td>{filed}</td>
          <td>{what}</td>
          <td class="num"><a href="{url}" target="_blank" rel="noopener">Open &rarr;</a><br><span style="color:var(--ink-3);font-size:10px">{acc}</span></td>
        </tr>''')
    H.append(f'''
<section>
  <div class="wrap">
    <div class="eyebrow">14 &middot; Sources</div>
    <h2>Every document, linked</h2>
    <p class="lede">Each row opens the filing or release. Where a row is a transcript or trade report rather than a filing, it is labelled, and the brief uses it only for quotations and for the three product facts flagged as open items.</p>
    <div class="scroll"><table class="tbl">
      <thead><tr><th style="width:24%">Document</th><th style="width:12%">Filed</th><th style="width:44%">What it supports</th><th style="width:20%">Link</th></tr></thead>
      <tbody>{"".join(rows_html)}</tbody>
    </table></div>
  </div>
</section>''')

    # ───── METHOD
    bio = open(os.path.join(ROOT, "tools", "lib", "bio.html")).read().replace("&sect;14", "&sect;16")
    open_items = [
        ("&ldquo;Does not plan to make additional investments in LiveWire&rdquo;", "No. 01 quotes this from H-D&rsquo;s FY2025 10-K. This pass could not re-locate it in the fetched text (MD&amp;A/liquidity truncated). Confirm page and section; until then it is tagged Unverified in &sect;06."),
        ("Post-spin Q4 2022 LiveWire loss", "Needed to state the &ldquo;since spin&rdquo; cumulative precisely instead of bracketing $337M&ndash;$422M."),
        ("H-D ownership of LiveWire", "~88.6% is computed from share counts (181M of 204.3M); neither 10-K prints it. Confirm from the most recent LiveWire proxy."),
        ("Sprint platform, plant and price", "Hero X440 derivation and India build are trade reporting; the $6,000 vs &ldquo;under $10,000&rdquo; conflict is unresolved. Check the August 2026 dealer-meeting materials and the Q3 call."),
        ("Sportster 883 price and plant", "~$10,000 and York are trade reporting only. The 883 designation itself is Starrs&rsquo;s, on the record."),
        ("HDMC vs HDFS debt split", "Inferred by instrument at 12/31/25; read the consolidating balance sheet (10-K R131)."),
        ("2025 annual meeting certified votes", "&ldquo;Over 48% withheld&rdquo; is from press reports of preliminary results; pull the Item 5.07 8-K."),
        ("Back to the Bricks &ldquo;phases&rdquo;", "One summary described reset/growth/acceleration phases; the release does not contain that language. Not cited here; do not add unless found in the deck."),
        ("Buyback average prices", "Computed from annual $ and share totals; ASR settlement timing may shift the 2025/2026 split slightly."),
        ("Rider demographics", "No 2025/2026 company-disclosed median age located; the last is &ldquo;45 years old&rdquo; for 2023. Omitted."),
    ]
    oi = "".join(f"<tr><td><strong>{i+1}.</strong> {a}</td><td>{b}</td></tr>" for i, (a, b) in enumerate(open_items))
    H.append(f'''
<section>
  <div class="wrap">
    <span id="method"></span><div class="eyebrow">15 &middot; Method &amp; standing</div>
    <h2>Who wrote this, and how</h2>
    {bio}
    <div class="duo" style="margin-top:30px">
      <div class="card">
        <div class="k">Method</div>
        <p style="font-size:15px; color:var(--ink)"><strong>Primary documents first.</strong> Figures come from filed financial statements or are computed from them, and the computation is shown.</p>
        <p><strong>Derived figures are labelled.</strong> The guidance sum, LiveWire&rsquo;s share of the drag, the EBITDA-to-operating-income translation, the buyback averages and the 2027 picture are arithmetic on filed numbers, identified in the captions.</p>
        <p><strong>Fact and opinion are separated.</strong> Sections 01&ndash;12 are sourced. Section 13 is judgment, and says so. Where an interpretation rests on my time in the industry, it carries the Industry context tag.</p>
        <div class="evlegend">
          <div class="evlegend-h">Evidence status</div>
          <p style="margin:6px 0 10px">Major findings carry one of five tags, so a reader can see what kind of claim is being made and how to attack it.</p>
          <div class="evlegend-r"><span class="ev ev-doc">Documented</span><span>Stated in a filing, release or transcript, and linked to it.</span></div>
          <div class="evlegend-r"><span class="ev ev-calc">Calculated</span><span>Arithmetic on documented numbers, with the computation shown.</span></div>
          <div class="evlegend-r"><span class="ev ev-inf">Inferred</span><span>A conclusion supported by more than one documented fact, but stated by none of them.</span></div>
          <div class="evlegend-r"><span class="ev ev-ind">Industry context</span><span>My professional experience or established industry practice, not a document.</span></div>
          <div class="evlegend-r"><span class="ev ev-unv">Unverified</span><span>Plausible, and not yet independently establishable from a document in hand.</span></div>
        </div>
      </div>
    </div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="eyebrow">16 &middot; Open items &amp; corrections</div>
    <h2>What is not yet nailed down</h2>
    <p class="lede">Rev. 2 is a working draft. These ten items are flagged in the text where they bite and will be closed or corrected here, dated, before the brief is called final. Two closed on reading the Q2 2026 deck; the corrections are logged below.</p>
    <div class="scroll"><table class="tbl">
      <thead><tr><th style="width:38%">Open item</th><th style="width:62%">What is needed</th></tr></thead>
      <tbody>{oi}</tbody>
    </table></div>
    <h3 style="font-size:clamp(21px,2.6vw,28px); margin-top:46px">Corrections log</h3>
    <div class="scroll"><table class="tbl">
      <thead><tr><th style="width:46%">What was claimed</th><th style="width:54%">What the document said</th></tr></thead>
      <tbody>
        <tr><td><span style="color:var(--ink-3)">8 Sep 2026 &middot; Rev. 2</span><br>$350M of HDMC EBITDA translated to ~$180M of operating income using inferred &ldquo;D&amp;A and adjustments&rdquo; of ~$43M a quarter.</td><td>The Q2 2026 deck gives HDMC D&amp;A directly: $40M for Q2, $81M for H1, ~$160M a year. Restated to <strong>~$190M</strong>; the ~5% conclusion is unchanged; 2027 consolidated moved from ~$200&ndash;270M to ~$210&ndash;280M.</td></tr>
        <tr><td><span style="color:var(--ink-3)">8 Sep 2026 &middot; Rev. 2</span><br>An apparent conflict on Q2 U.S. 601cc+ share (32% vs 38%) was listed as an open item.</td><td>Seasonality, not error: 34% FY2025, 38% Q1 2026, 32% Q2 2026, 34% YTD (deck slide 6). Closed.</td></tr>
        <tr><td><span style="color:var(--ink-3)">8 Sep 2026 &middot; Rev. 2</span><br>Restructuring expense stated as $15M (Q1) + $3M (Q2).</td><td>$17M for H1 2026 per the deck.</td></tr>
        <tr><td colspan="2" style="color:var(--ink-3)">If something here is wrong, tell me; it will appear on this list with the date.</td></tr>
      </tbody>
    </table></div>
  </div>
</section>

</main>

<footer class="foot">
  <div class="wrap">
    <div class="tape">Method &amp; limitations</div>
    <h4>What this brief does and does not claim</h4>
    <p>Every figure is drawn from SEC filings, company releases or call transcripts, or is arithmetic on them identified as such. Segment figures are on Harley-Davidson&rsquo;s reporting basis; LiveWire&rsquo;s own filings report slightly different segment totals ($75.5M vs $75.0M for FY2025) and are used only for LiveWire&rsquo;s cash and loan terms.</p>
    <p><strong>This brief does not assert, and no filing states, that Harley-Davidson intends to fund, acquire, divest or wind down LiveWire.</strong> The options in &sect;07 are an enumeration of what the filings permit, not a forecast. The 2027 picture in &sect;12 uses the company&rsquo;s own targets as inputs and is labelled Calculated.</p>
    <p>Product facts about the Sprint and the Sportster 883 beyond what management said on the record are trade reporting and are flagged as open items. The 883 designation is management&rsquo;s own.</p>
    <p style="margin-top:22px">Contact Patch Advisory &middot; {ISSUE} &middot; William Weppner &middot; {DATE} &middot; Rev. 2 &middot; <a href="../01/">No. 01</a> &middot; <a href="../../">Index</a></p>
  </div>
</footer>
{bottombar_html()}
</body></html>''')

    html = "\n".join(H)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write(html)
    print(OUT, len(html), "bytes")

if __name__ == "__main__":
    build()
