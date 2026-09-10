#!/usr/bin/env python3
"""Build groundtruth/02/series/index.html — the four-part LinkedIn carousel for Ground Truth No. 02.

Slides are 1080x1350 (.slide). Route cards carry class "card" and are rendered as the
second page of each carousel PDF and as stand-alone card PDFs by tools/lib/render_slides.py.
Run from the repo root:  python3 tools/gt02/build_series.py
"""
import os, sys, re
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools", "gt02", "lib"))  # No. 02 chart/render API; tools/lib is the current one
from charts import bars, hbars, waterfall, MAG, CYAN, INK3

CSS = open(os.path.join(ROOT, "tools", "lib", "series.css")).read()
OUT = os.path.join(ROOT, "groundtruth", "02", "series", "index.html")
URL = "weppner58-moto.github.io/ground-truth/groundtruth/02"
TITLE = "Harley-Davidson: Back to the Bricks, Down to Breakeven"

ROUTE = [("Part I", "The arithmetic", "Add up the guidance: about zero. The subsidiary's loss exceeds the motor company's profit."),
         ("Part II", "The sale", "2025's profit was the finance company, sold. $180M a year traded for $1.25B once."),
         ("Part III", "The subsidiary", "$422M consolidated. A third of the profit drag from 0.6% of revenue. Cash to May 2027."),
         ("Part IV", "The plan", "Five pillars, six targets. The 2027 number is a 5% margin, below 2019."),
         ("Part V", "The bet", "$1.6B of buybacks, and one motorcycle carrying the growth target: the 883."),
         ("Part VI", "The final word", "LiveWire didn't break Harley. It is what the new Harley can't afford.")]

EXTRA_CSS = """
.routegrid{display:grid;grid-template-columns:1fr 1fr;gap:2px;background:var(--drule);margin-top:auto}
.routegrid div{background:#101215;padding:16px 18px 18px}
.routegrid .rn{font-family:var(--mono);font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--dmag)}
.routegrid .rt{font-family:var(--disp);font-weight:800;text-transform:uppercase;font-size:30px;line-height:.95;margin:6px 0 8px;color:var(--dink)}
.routegrid .rp{font-size:15.5px;line-height:1.38;color:var(--dink3)}
.routegrid div.on{outline:2px solid var(--dmag);outline-offset:-2px}
.routegrid div.on .rt{color:var(--dmag)}
.routegrid:not(.all) div:not(.on) .rt{opacity:.55}
.tbl{width:100%;border-collapse:collapse;font-size:24px}
.tbl th{font-family:var(--mono);font-size:14px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink3);text-align:left;padding:0 10px 12px 0;border-bottom:2px solid var(--rule2);font-weight:500}
.dk .tbl th{color:var(--dink3);border-color:#343A40}
.tbl td{padding:16px 10px 16px 0;border-bottom:1px solid var(--rule);vertical-align:top;line-height:1.35}
.dk .tbl td{border-color:var(--drule)}
.tbl td.num{text-align:right;font-family:var(--mono);font-size:22px;white-space:nowrap}
.tbl .hi{color:var(--mag);font-weight:600}
.dk .tbl .hi{color:var(--dmag)}
.pillars{list-style:none;padding:0;margin:0}
.pillars li{display:grid;grid-template-columns:70px 1fr;gap:18px;border-top:1px solid var(--rule);padding:18px 0;max-width:none;font-size:24px;line-height:1.4}
.pillars li:last-child{border-bottom:1px solid var(--rule)}
.pillars li b{font-family:var(--disp);font-weight:800;font-size:44px;line-height:1;color:var(--mag)}
.pillars li span small{display:block;font-family:var(--mono);font-size:14px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink3);margin-top:6px}
.brand{font-family:var(--disp);font-weight:800;text-transform:uppercase;font-size:16px;letter-spacing:.08em;color:var(--ink3)}
.dk .brand{color:var(--dink3)}
"""

def svg_theme(svg, dark):
    svg = svg.replace("var(--magenta)", "var(--dmag)" if dark else "var(--mag)")
    svg = svg.replace("var(--cyan)", "var(--dcyan)" if dark else "var(--cyan)")
    svg = svg.replace("var(--ink-3)", "var(--dink3)" if dark else "var(--ink3)")
    svg = svg.replace("var(--ink)", "var(--dink)" if dark else "var(--ink)")
    return svg

def slide(body, *, dark=False, tag="", sid="", foot_l="Harley-Davidson, Inc. · HOG", foot_r="Contact Patch Advisory", extra_cls=""):
    cls = "slide" + (" dk" if dark else "") + (" " + extra_cls if extra_cls else "")
    return f'''<div class="{cls}" id="{sid}">
  <div class="tophdr"><div class="mark">CONTACT&nbsp;<i>PATCH</i></div><div class="tag">{tag}</div></div>
  {body}
  <div class="foot"><span>{foot_l}</span><span>{foot_r}</span></div>
</div>'''

def cover(part_n, part_title, h1, dek, sid):
    return slide(f'''
  <div class="spacer"></div>
  <div class="kick">{TITLE} · Part {part_n} of 4</div>
  <h1 style="font-size:112px">{h1}</h1>
  <p class="wide" style="margin-top:36px;color:var(--dink3);font-size:30px">{dek}</p>
  <div class="spacer"></div>
  <p class="wide" style="font-family:var(--mono);font-size:16px;letter-spacing:.14em;text-transform:uppercase;color:var(--dink3);margin:0">Part {part_n} · {part_title}</p>''',
  dark=True, tag="Ground Truth No. 02", sid=sid, foot_l="Harley-Davidson, Inc. · HOG", foot_r="September 2026")

def route_card(on_index, sid, heading=None, dek=None):
    cells = []
    for i, (rn, rt, rp) in enumerate(ROUTE):
        cells.append(f'<div class="{"on" if i == on_index else ""}"><div class="rn">{rn}</div><div class="rt">{rt}</div><div class="rp">{rp}</div></div>')
    heading = heading or ROUTE[on_index][1]
    dek = dek or "What Harley-Davidson's own filings say about the plan, the subsidiary, and 2027."
    return slide(f'''
  <div class="kick">{TITLE} · The route</div>
  <h1 style="font-size:80px;max-width:12ch">{heading}</h1>
  <p class="wide" style="margin-top:22px;color:var(--dink3);font-size:24px;margin-bottom:30px">{dek}</p>
  <div class="routegrid{" all" if on_index < 0 else ""}" style="margin-bottom:34px">{"".join(cells)}</div>''',
  dark=True, tag="Ground Truth No. 02", sid=sid, foot_l="Contact Patch · Ground Truth No. 02", foot_r=URL, extra_cls="card")

def stat(k, v, sub, mag=True, size=84):
    return f'<div class="col stat {"m" if mag else ""}"><div class="k">{k}</div><div class="v {"m" if mag else ""}" style="font-size:{size}px">{v}</div><div class="sub">{sub}</div></div>'

def tbl(head, rows, nums=()):
    th = "".join(f"<th>{h}</th>" for h in head)
    body = "".join("<tr>" + "".join(f'<td class="{"num" if j in nums else ""}">{c}</td>' for j, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<table class="tbl"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table>'

def closer(next_line, sid, tag):
    return slide(f'''
  <div class="spacer"></div>
  <h2 style="font-size:60px;max-width:16ch">{next_line}</h2>
  <div class="spacer"></div>
  <p class="wide" style="font-size:26px;color:var(--dcyan)">Full brief: 16 sections in six parts, every figure linked to its filing, open items and corrections published.<br>{URL}</p>''',
  dark=True, tag=tag, sid=sid, foot_l="Former H-D product manager · Independent analyst", foot_r="No position held")

def build():
    S = []
    # ═══════════ PART 1 — THE ARITHMETIC ═══════════
    P = []
    P.append(cover(1, "The arithmetic", "BACK TO<br>THE BRICKS.<br>DOWN TO<br>BREAKEVEN.", "What LiveWire costs Harley-Davidson, what the new plan leaves out, and what 2027 looks like on the company's own numbers.", "s1-1"))
    P.append(route_card(0, "s1-card"))
    P.append(slide('''
  <div class="kick">What they said · 5 May 2026 · introducing the plan</div>
  <p class="wide" style="font-size:26px;color:var(--dink3);margin-bottom:44px">Harley-Davidson's new CEO, on the call that replaced the old five-year strategy:</p>
  <div class="quote" style="font-size:40px;max-width:22ch">"Over the last several years, we leaned heavily into Touring and Electric."</div>
  <div class="spacer"></div>
  <p class="wide" style="font-size:26px;margin:0">Fourteen words. The parent company's verdict on Hardwire, on LiveWire, and on five years of product decisions.</p>''',
      dark=True, tag="01 / 09", sid="s1-2", foot_l="Q1 2026 earnings call · Artie Starrs"))
    P.append(slide(f'''
  <div class="kick">What they guided · 23 July 2026 · $ millions, operating income</div>
  <h2 style="font-size:62px">Three ranges from one release.</h2>
  <div class="row" style="margin-top:10px">
    {stat("HDMC · the motor company", "$10–50M", "raised from $(40)M to $10M", mag=False, size=62)}
    {stat("HDFS · the finance company", "$55–70M", "raised from $45–60M", mag=False, size=62)}
    {stat("LiveWire · the subsidiary", "$(70–80)M", "unchanged since February", mag=True, size=62)}
  </div>
  <div class="spacer"></div>
  <p class="wide" style="font-size:27px;margin:0">Segment operating income sums to the consolidated line in H-D's reporting. 2025 proves it to the decimal: $(28.7)M + $490.4M + $(75.0)M = $386.6M.</p>''',
      tag="02 / 09", sid="s1-3", foot_l="Source: HOG 8-K Ex. 99.1 · 23 Jul 2026 · 10-K FY2025"))
    P.append(slide('''
  <div class="kick">Added up</div>
  <h2 style="font-size:58px;max-width:15ch">Harley-Davidson, Inc., 2026, on its own guidance:</h2>
  <div class="big mag" style="font-size:150px;margin-top:30px">$(15)M<br>to $50M</div>
  <div class="sub" style="font-size:20px;margin-top:30px">CONSOLIDATED OPERATING INCOME · IMPLIED</div>
  <div class="spacer"></div>
  <p class="wide" style="font-size:28px;margin:0">It made <strong>$779 million</strong> in 2023. Roughly breakeven is the floor the new strategy is being measured from.</p>''',
      dark=True, tag="03 / 09", sid="s1-4", foot_l="Calculated from company guidance · 23 Jul 2026"))
    P.append(slide('''
  <div class="spacer"></div>
  <h2 style="font-size:66px;max-width:15ch;color:var(--mag)">The subsidiary is guided to lose more than the motor company is guided to make.</h2>
  <p class="wide" style="font-size:28px;margin-top:30px">At every point in both ranges. LiveWire's $70–80M loss exceeds HDMC's $10–50M profit. LiveWire is 0.6% of revenue.</p>
  <div class="spacer"></div>''',
      tag="04 / 09", sid="s1-5", foot_l="HOG 2026 guidance · 23 Jul 2026"))
    fig_retail = bars([267999, 218273, 194256, 162771, 151229, 132535], ["2014", "2019", "2021", "2023", "2024", "2025"],
                      colors=[INK3, INK3, INK3, INK3, MAG, MAG], opacities=[.55, .7, .7, .8, .85, None], ymax=280000,
                      ticks=[0, 100000, 200000], tick_fmt=lambda v: f"{v/1000:.0f}K", val_fmt=lambda v: f"{v/1000:.0f}K", width=900, height=420, pad_l=80)
    P.append(slide(f'''
  <div class="kick">The line the plan inherits · worldwide retail, units</div>
  <h2 style="font-size:60px">Half the motorcycles.</h2>
  {svg_theme(fig_retail, True)}
  <div class="spacer"></div>
  <p class="wide" style="font-size:26px;margin:0">267,999 in 2014. 132,535 in 2025. Down <strong>51%</strong>, and down every year since 2021. U.S. retail: down 52%. Shipments: down 54%.</p>''',
      dark=True, tag="05 / 09", sid="s1-6", foot_l="Source: HOG results releases FY2014–FY2025"))
    P.append(slide(f'''
  <div class="kick">2019 → 2025 · the company Hardwire inherited vs the one it left</div>
  {tbl(["", "2019", "2025", "Change"], [
      ["Worldwide retail", "218,273", "132,535", "−39%"],
      ["U.S. retail", "125,960", "82,698", "−34%"],
      ["Shipments", "213,939", "124,477", "−42%"],
      ["HDMC operating margin", "6.3%", '<span class="hi">(0.8%)</span>', "−7.1 pts"],
      ["U.S. 601cc+ share", "n/a", "34.5%", "37.9% in 2023"],
      ["Dealerships worldwide", "1,569", "1,174", "−25%"],
      ["U.S. dealerships", "698", "554", "−21%"],
      ["Diluted EPS", "$2.68", "$2.78", "+4%"]], nums=(1, 2, 3))}
  <div class="spacer"></div>
  <p class="wide" style="font-size:25px;margin:0">EPS held up. That is the buyback and the finance company: Parts 2 and 4.</p>''',
      tag="06 / 09", sid="s1-7", foot_l="Source: HOG 10-K FY2019, FY2025 · results releases"))
    fig_hdmc = bars([289.6, 408.6, 677.1, 661.2, 277.8, -28.7], ["2019", "2021", "2022", "2023", "2024", "2025"],
                    colors=[CYAN, CYAN, CYAN, CYAN, CYAN, MAG], opacities=[.6, .7, .85, None, .85, None], ymax=720, ymin=-120,
                    ticks=[0, 200, 400, 600], tick_fmt=lambda v: f"${v:,.0f}M", val_fmt=lambda v: f"{v:,.0f}", width=900, height=420, pad_l=90)
    P.append(slide(f'''
  <div class="kick">HDMC operating income · $ millions</div>
  <h2 style="font-size:58px;max-width:16ch">2025: the first loss outside the pandemic year.</h2>
  {svg_theme(fig_hdmc, False)}
  <div class="spacer"></div>
  <p class="wide" style="font-size:25px;margin:0">Q4 2025 HDMC gross margin: <strong>(8.0%)</strong>. For one quarter the company sold motorcycles for less than they cost to build.</p>''',
      tag="07 / 09", sid="s1-8", foot_l="Source: HOG 10-K FY2025 · segment note · Q4 2025 release"))
    P.append(slide('''
  <div class="kick">Two qualifications, before anyone else makes them</div>
  <ul style="font-size:27px">
    <li><strong>H1 2026 consolidated operating income was $99.5M</strong>, so the full-year guide implies a second-half loss. Q4 is seasonally weak (HDMC lost $260M in Q4 2025), and management has beaten its own ranges twice this year. The guidance may be conservative.</li>
    <li><strong>The sum is checked.</strong> Segments add to the consolidated line in 2025 and 2024 to the decimal. No corporate eliminations sit between them.</li>
  </ul>
  <div class="spacer"></div>
  <p class="wide" style="font-size:27px;margin:0">It is still the number they chose to publish.</p>''',
      dark=True, tag="08 / 09", sid="s1-9", foot_l="HOG 10-Q Q2 2026 · 10-K FY2025"))
    P.append(closer("Part 2: where the 2025 profit actually came from, and why it does not happen twice.", "s1-10", "09 / 09"))
    S.append(("Part 1 · The Arithmetic", P))

    # ═══════════ PART 2 — THE SALE ═══════════
    P = []
    P.append(cover(2, "The sale", "THE<br>SALE.", "In 2025 the motor company lost money and the subsidiary lost more. The year was profitable because the finance company sold its loan book.", "s2-1"))
    P.append(route_card(1, "s2-card"))
    fig_seg = waterfall([("HDMC", -28.7, MAG), ("LiveWire", -75.0, MAG), ("HDFS", 490.4, CYAN), ("Consolidated", None, "var(--ink)")],
                        ymin=-130, ymax=520, ticks=[-100, 0, 100, 200, 300, 400, 500], val_fmt="{:+,.1f}", width=900, height=440, pad_l=90)
    P.append(slide(f'''
  <div class="kick">2025 operating income by segment · $ millions</div>
  <h2 style="font-size:58px">Two segments lost money. The third was sold.</h2>
  {svg_theme(fig_seg, False)}
  <div class="spacer"></div>
  <p class="wide" style="font-size:25px;margin:0">HDFS: "record-high earnings, driven by the HDFS transaction." The motorcycle company and its subsidiary lost $103.7M together; the finance company covered it four times over, once.</p>''',
      tag="01 / 07", sid="s2-2", foot_l="Source: HOG 10-K FY2025 · segment note"))
    P.append(slide('''
  <div class="kick">What was sold · KKR / PIMCO · announced 30 July 2025</div>
  <ul style="font-size:28px">
    <li>About <strong>$6 billion</strong> of existing retail loan receivables, at a premium to par.</li>
    <li><strong>9.8% of HDFS</strong>: 4.9% each to KKR and PIMCO, at an agreed $1.8B valuation.</li>
    <li>A five-year forward-flow agreement: <strong>two-thirds of future originations</strong>, sold.</li>
    <li>A <strong>$1.0 billion dividend</strong> from HDFS up to the parent in Q4 2025.</li>
    <li>Credit-loss provision swung from a $247M expense to a <strong>$191M credit</strong> as reserves on the sold loans were released.</li>
  </ul>
  <div class="spacer"></div>
  <p class="wide" style="font-size:25px;margin:0;color:var(--dink3)">Announced by the departing CEO, three months before he left.</p>''',
      dark=True, tag="02 / 07", sid="s2-3", foot_l="Source: H-D releases 30 Jul, 25 Aug 2025 · Q4 2025 call"))
    fig_hdfs = bars([234.7, 248.4, 490.4, 62.5, 137.5], ["2023", "2024", "2025", "2026 guide", "2029 target"],
                    colors=[CYAN, CYAN, CYAN, MAG, INK3], opacities=[.7, .85, None, None, .7], ymax=520,
                    ticks=[0, 100, 200, 300, 400, 500], tick_fmt=lambda v: f"${v:,.0f}M", val_fmt=lambda v: f"{v:,.0f}", width=900, height=420, pad_l=90)
    P.append(slide(f'''
  <div class="kick">HDFS operating income · $ millions · 2026 and 2029 at range midpoints</div>
  <h2 style="font-size:58px">The steadiest earner, converted to cash.</h2>
  {svg_theme(fig_hdfs, False)}
  <div class="spacer"></div>
  <p class="wide" style="font-size:25px;margin:0">HDFS was <strong>60%</strong> of consolidated operating income in 2024. It is guided to $55–70M for 2026.</p>''',
      tag="03 / 07", sid="s2-4", foot_l="Source: HOG 10-K FY2025 · Q1, Q2 2026 calls"))
    P.append(slide('''
  <div class="kick">The trade</div>
  <div class="big mag" style="font-size:120px">$180M<br>a year</div>
  <div class="sub" style="font-size:20px">FOREGONE, AT THE 2024 RUN RATE</div>
  <div class="big" style="font-size:120px;margin-top:40px">$1.25B</div>
  <div class="sub" style="font-size:20px">"DISCRETIONARY CASH," ONCE</div>
  <div class="spacer"></div>
  <p class="wide" style="font-size:27px;margin:0">Seven years of HDFS earnings, paid up front. Not a bad trade if the cash earns more than HDFS did. So far: a $200M buyback at ~$26.50, and $1.9B sitting on a balance sheet guided to breakeven.</p>''',
      dark=True, tag="04 / 07", sid="s2-5", foot_l="Calculated · HOG 10-K FY2025 · Q4 2025 call"))
    P.append(slide(f'''
  <div class="kick">What H-D got · what H-D gave</div>
  {tbl(["Got", "Gave"], [
      ["~$1.25B of discretionary cash; $450M to debt, ~$500M earmarked for shareholders", "~$180M a year of operating income, rebuilding to perhaps half by 2029"],
      ["$1.0B dividend from HDFS", "9.8% of HDFS, with a right to buy back a third a year"],
      ["Debt $6.96B → $2.97B; cash $1.59B → $3.09B", "Two-thirds of future loans, forward-sold for five years"],
      ["A capital-light HDFS with &ldquo;significantly higher ROE&rdquo;", "The captive that floored dealers and financed riders when banks would not"]])}
  <div class="spacer"></div>
  <p class="wide" style="font-size:24px;margin:0;color:var(--ink3)">The last row is industry context, not a filing. A forward-flow partner has a contract; a captive had a reason.</p>''',
      tag="05 / 07", sid="s2-6", foot_l="Source: H-D releases · 10-K FY2025 · industry context"))
    P.append(slide('''
  <div class="spacer"></div>
  <h2 style="font-size:60px;max-width:16ch">This is why 2025 EPS was $2.78 and not something near zero.</h2>
  <p class="wide" style="font-size:28px;margin-top:30px">And why the 2026 guidance looks like a cliff. It is not a cliff. <strong>It is the ground.</strong> The $350M HDMC EBITDA target now has to carry the enterprise in a way it never had to before the sale.</p>
  <div class="spacer"></div>''',
      dark=True, tag="06 / 07", sid="s2-7", foot_l="Ground Truth No. 02 · Part 2"))
    P.append(closer("Part 3: what LiveWire costs the parent, and the date it stops being a line item and becomes a decision.", "s2-8", "07 / 07"))
    S.append(("Part 2 · The Sale", P))

    # ═══════════ PART 3 — THE SUBSIDIARY ═══════════
    P = []
    P.append(cover(3, "The subsidiary", "THE<br>SUBSIDIARY.", "$422 million of LiveWire losses consolidated into Harley-Davidson since 2022. Cash to May 2027. A note due in December.", "s3-1"))
    P.append(route_card(2, "s3-card"))
    fig_lw = bars([15.0, 26.3, 19.4, 33.8], ["2023", "2024", "2025", "TTM Jun 2026"], colors=[MAG]*4, opacities=[.55, .75, .85, None],
                  ymax=40, ticks=[0, 10, 20, 30, 40], tick_fmt="{:.0f}%", val_fmt="{:.1f}%", width=900, height=420, pad_l=80)
    P.append(slide(f'''
  <div class="kick">LiveWire operating loss as a share of H-D consolidated operating income</div>
  <h2 style="font-size:58px">0.6% of revenue. A third of the drag.</h2>
  {svg_theme(fig_lw, True)}
  <div class="spacer"></div>
  <p class="wide" style="font-size:25px;margin:0">Every dollar LiveWire loses lands in Harley-Davidson's operating income. Only the ~11% belonging to the public minority comes back out, below the line. <strong>H-D shareholders bear ~89%.</strong></p>''',
      dark=True, tag="01 / 08", sid="s3-2", foot_l="Calculated · HOG 10-K FY2025 · 10-Q Q2 2026"))
    P.append(slide(f'''
  <div class="kick">LiveWire, in the parent's numbers · 2025</div>
  <div class="row" style="margin-top:20px">
    {stat("Cumulative losses consolidated · 2022–Jun 2026", "$422M", "$337M from Jan 2023 alone", size=90)}
    {stat("Share of H-D revenue", "0.6%", "$25.7M of $4,473M", mag=False, size=90)}
  </div>
  <div class="row" style="margin-top:60px">
    {stat("Share of H-D headcount", "2.7%", "~150 of ~5,500", mag=False, size=90)}
    {stat("Share of the 2025 profit drag", "19%", "34% trailing twelve months", size=90)}
  </div>
  <div class="spacer"></div>
  <p class="wide" style="font-size:25px;margin:0">Against the 2021 plan of 100,000 units and $1.8B of revenue by 2026: 923 units, $31.3M. Ground Truth No. 01 has that story.</p>''',
      tag="02 / 08", sid="s3-3", foot_l="Source: HOG 10-K FY2025 · LVWR 10-Q Q2 2026"))
    P.append(slide('''
  <div class="kick">The seat change · one instrument, rewritten</div>
  <h3 style="color:var(--dink3)">February 2024</h3>
  <p class="wide" style="font-size:27px">A <strong>$100M convertible</strong> loan. If LiveWire could not repay, Harley-Davidson would take equity. A parent's instrument. Never drawn.</p>
  <h3 style="color:var(--dmag);margin-top:30px">November 2025</h3>
  <p class="wide" style="font-size:27px">Amended and restated at <strong>$75M</strong>. Conversion feature <strong>removed</strong>. Security interest over <strong>substantially all assets</strong> added. SOFR + 4%, compounding, all due <strong>15 December 2027</strong>. First $10M of any equity raised goes to the lender. Drawn in full 15 December 2025.</p>
  <div class="spacer"></div>
  <p class="wide" style="font-size:26px;margin:0;color:var(--dink3)">A convertible says: if this fails, we own it. A secured loan says: if this fails, we get paid first.</p>''',
      dark=True, tag="03 / 08", sid="s3-4", foot_l="Source: LVWR 8-K Ex. 10.1 (Feb 2024) · LVWR 10-K FY2025"))
    P.append(slide(f'''
  <div class="kick">The clock</div>
  <div class="row" style="margin-top:10px">
    {stat("LiveWire cash · 30 Jun 2026", "$52.9M", "from $82.8M at year-end · $29.9M burned in six months", size=96)}
    {stat("Owed to Harley-Davidson · 15 Dec 2027", "$76.8M", "compounding to ~$85M · secured on everything", mag=False, size=96)}
  </div>
  <div class="spacer"></div>
  <h2 style="font-size:54px;max-width:17ch">Straight-line the burn and the cash runs out around May 2027. The note is due seven months later. The plan's only dated target is 2027.</h2>''',
      tag="04 / 08", sid="s3-5", foot_l="Source: LVWR 10-Q Q2 2026 · 10-K FY2025 · calculated"))
    P.append(slide(f'''
  <div class="kick">The options, as they stand on the filings · an enumeration, not a prediction</div>
  {tbl(["Option", "Cost to H-D", "Effect on H-D's P&L"], [
      ["Fund again", "Reverses the stated position", "None; already consolidated"],
      ["Buy the minority", "~$28M at $1.20. Severance plan already carves out an H-D acquisition", "None; already consolidated"],
      ["Third-party raise", "Dilution to ~70%; new money sits behind H-D's lien", "Still consolidated"],
      ["Foreclose / wind down", "Write-down of the $75M note against collateral", "Losses stop"],
      ["Sell or merge", "Depends on buyer; H-D keeps the contracts", "Deconsolidation"]])}
  <div class="spacer"></div>
  <p class="wide" style="font-size:25px;margin:0">H-D has stated no intention to fund, acquire, divest or wind down LiveWire. None is asserted here.</p>''',
      dark=True, tag="05 / 08", sid="s3-6", foot_l="Source: LVWR 10-Q Q2 2026 · HOG 10-K FY2025"))
    P.append(slide('''
  <div class="spacer"></div>
  <h2 style="font-size:58px;max-width:16ch;color:var(--mag)">Because LiveWire is already consolidated, no ownership change short of deconsolidation improves Harley-Davidson's reported operating income.</h2>
  <p class="wide" style="font-size:27px;margin-top:30px">Buying the minority for $28M would be the cheapest corporate action in the company's recent history. It would change the operating line by exactly nothing. Back to the Bricks handles this by scoring HDMC alone.</p>
  <div class="spacer"></div>''',
      tag="06 / 08", sid="s3-7", foot_l="Calculated · Ground Truth No. 02 §07"))
    P.append(slide('''
  <div class="kick">What the parent has said in 2026</div>
  <div class="quote" style="font-size:34px;max-width:24ch">"LiveWire is now working diligently to attract its own sources of capital to continue to finance its operations and future plans."</div>
  <div class="src">Artie Starrs · Q4 2025 call · 10 Feb 2026</div>
  <div class="spacer"></div>
  <p class="wide" style="font-size:26px;margin:0">No 2026 statement from Starrs or CFO Root uses "strategic alternatives," "divestiture" or "wind-down." Back to the Bricks does not mention LiveWire outside its forward-looking factors. LiveWire's 10-Q says it will pursue financing "during the third quarter of 2026." That quarter ends in three weeks.</p>''',
      dark=True, tag="07 / 08", sid="s3-8", foot_l="Source: Q4 2025 call · Back to the Bricks release · LVWR 10-Q"))
    P.append(closer("Part 4: what Back to the Bricks actually commits to, what Hardwire delivered, and the one motorcycle carrying the growth target.", "s3-9", "08 / 08"))
    S.append(("Part 3 · The Subsidiary", P))

    # ═══════════ PART 4 — THE BRICKS ═══════════
    P = []
    P.append(cover(4, "The bricks", "THE<br>BRICKS.", "Five pillars, six targets, one dated number, and a 2027 that lands everything at once: the EBITDA target, the Sportster, and the LiveWire note.", "s4-1"))
    P.append(route_card(3, "s4-card", heading="The plan, the bet,<br>the final word", dek="Parts IV, V and VI of the brief, in one carousel."))
    P.append(slide('''
  <div class="kick">Back to the Bricks · 5 May 2026 · the five pillars, as written</div>
  <ol class="pillars">
    <li><b>1</b><span>Deep appreciation of competitive advantages and legacy<small>"iconic brand, diversified and powerful revenue channels, and best-in-class dealer network"</small></span></li>
    <li><b>2</b><span>Renewed commitment to the exclusive dealer network<small>"enable dealers to double profitability in 2026 and then double it again by 2029"</small></span></li>
    <li><b>3</b><span>Recapture share where H-D has "right to win"<small>"new motorcycles, used motorcycles, Parts &amp; Accessories, and Apparel &amp; Licensing"</small></span></li>
    <li><b>4</b><span>Strong financial position<small>"a path to stronger free cash flow and EBITDA margin over time"</small></span></li>
    <li><b>5</b><span>Bolstered management team<small>"a number of leadership appointments"</small></span></li>
  </ol>
  <div class="spacer"></div>
  <p class="wide" style="font-size:24px;margin:0;color:var(--ink3)">The word "electric" does not appear. LiveWire is in the forward-looking factors only.</p>''',
      tag="01 / 09", sid="s4-2", foot_l="Source: Back to the Bricks release · 5 May 2026"))
    P.append(slide(f'''
  <div class="kick">The targets, against the record</div>
  {tbl(["Target", "Stated", "Record"], [
      ["HDMC EBITDA", "<strong>&gt;$350M in 2027</strong>", "≈ $190M operating income, ~5% margin. 2019: $290M. 2023: $661M."],
      ["Retail growth", "Mid-single-digit CAGR", "≈ 6,600 units/yr. 2019–25 CAGR: <span class='hi'>−8%</span>"],
      ["Gross margin", "25–30%", "2025: 24.2%. 2024: 28.0%."],
      ["Opex", "&lt;20% of sales", "2025: 25.0%"],
      ["EBITDA margin", "10–12%", "Hardwire promised 15% op margin by 2025. Got <span class='hi'>(0.8%)</span>."],
      ["Fixed cost", "−$150M by 2027", "&ldquo;Not including LiveWire.&rdquo;"]])}
  <div class="spacer"></div>
  <p class="wide" style="font-size:24px;margin:0;color:var(--dink3)">Not in it: a revenue figure, EPS, free cash flow, Sportster volume, a capital-return commitment, or any LiveWire target.</p>''',
      dark=True, tag="02 / 09", sid="s4-3", foot_l="Source: Back to the Bricks release · Q1, Q2 2026 calls · 10-K FY2025"))
    P.append(slide('''
  <div class="kick">The only dated number, translated</div>
  <div class="big" style="font-size:150px">$350M</div>
  <div class="sub" style="font-size:20px">HDMC EBITDA · 2027</div>
  <div class="big mag" style="font-size:150px;margin-top:36px">≈ 5%</div>
  <div class="sub" style="font-size:20px">OPERATING MARGIN · DERIVED (D&amp;A ~$170M/YR FROM Q2 2026 ADJ. EBITDA LESS OPERATING INCOME)</div>
  <div class="spacer"></div>
  <p class="wide" style="font-size:27px;margin:0">HDMC ran a 6.3% margin in 2019, the year Hardwire was written to fix. <strong>The new plan's target is below where the company stood before the old plan.</strong></p>''',
      tag="03 / 09", sid="s4-4", foot_l="Calculated · confirm HDMC D&A from the 10-K (open item 2)"))
    P.append(slide(f'''
  <div class="kick">Hardwire, 2021–2025 · promised vs delivered</div>
  {tbl(["Commitment", "Target", "FY2025"], [
      ["HDMC revenue", "+5–7% CAGR → ~$5.5–5.9B", "<span class='hi'>$3,578M</span> · −21% vs 2021"],
      ["HDMC op margin", "<strong>15% by 2025</strong>", "<span class='hi'>(0.8%)</span>"],
      ["EPS", "Low-double-digit growth", "$4.19 → $2.78"],
      ["HDFS", "Double-digit growth", "$490M via a one-time sale"],
      ["Cost", "$400M productivity", "New plan needs $150M more"],
      ["<strong>Lead in Electric</strong>", "100,000 LiveWires/yr from 2026", "<span class='hi'>923. $422M of losses.</span>"]])}
  <div class="spacer"></div>
  <p class="wide" style="font-size:25px;margin:0">Every quantified target missed. Shareholders withheld <strong>over 48%</strong> from the CEO in May 2025; he and two directors were gone within a year.</p>''',
      dark=True, tag="04 / 09", sid="s4-5", foot_l="Source: Hardwire release 2 Feb 2021 · Stage II 10 May 2022 · 10-K FY2025"))
    fig_buy = bars([38.6, 34.3, 36.0, 26.5, 20.0, 28.30], ["2022", "2023", "2024", "2025", "H1 2026", "HOG today"],
                   colors=[INK3, INK3, INK3, INK3, INK3, MAG], opacities=[.7, .7, .7, .7, .7, None], ymax=44, ticks=[0, 10, 20, 30, 40],
                   tick_fmt="${:.0f}", val_fmt="${:.2f}", width=900, height=400, pad_l=80)
    P.append(slide(f'''
  <div class="kick">Capital returned · average repurchase price by year vs the share price, 4 Sep 2026</div>
  <h2 style="font-size:56px">$1.63 billion of buybacks. 52.1M shares. $31.30 average.</h2>
  {svg_theme(fig_buy, False)}
  <div class="spacer"></div>
  <p class="wide" style="font-size:25px;margin:0">Those shares are worth about $1.47B at $28.30. HOG was $30.47 the day Zeitz took the job in February 2020. Market cap today: ~$2.9B, with $1.9B of cash on the balance sheet.</p>''',
      tag="05 / 09", sid="s4-6", foot_l="Source: HOG results releases 2022–Q2 2026 · calculated"))
    fig_sport = hbars([("Plan: +5% a year", 6600, CYAN, None, "motorcycles"), ("Sportster, low", 35000, MAG, .8, ""), ("Sportster, high", 40000, MAG, None, "")],
                      xmax=44000, width=900, row_h=64, pad_l=250, pad_r=140)
    P.append(slide(f'''
  <div class="kick">The bet · what the growth target needs vs what the Sportster used to sell · units a year</div>
  <h2 style="font-size:56px">One motorcycle carries the growth target.</h2>
  {svg_theme(fig_sport, True)}
  <p class="wide" style="font-size:25px;margin-top:20px">Starrs: the Sportster market "as recently as five, six years ago… was 35,000–40,000+ on a global basis." Recover a third of that and the 883 alone delivers two years of the plan's growth.</p>
  <div class="spacer"></div>
  <p class="wide" style="font-size:24px;margin:0;color:var(--dink3)">Raymond James, same call: "there's a reason why Sportster was discontinued, right? It was hard to make money." Starrs: the cost is now "extremely comfortable against the expected MSRP."</p>''',
      dark=True, tag="06 / 09", sid="s4-7", foot_l="Source: Q1 2026 call · calculated"))
    P.append(slide(f'''
  <div class="kick">2027, if every target lands on time</div>
  {tbl(["", "Plan delivered"], [
      ["Worldwide retail", "~143,000 · <strong>66% of 2019</strong>"],
      ["HDMC operating income", "~$190M · <strong>~5% margin</strong>"],
      ["HDFS operating income", "~$80–100M · a third of 2024"],
      ["LiveWire", "Unaddressed · cash out mid-2027 · $85M due December"],
      ["Consolidated operating income", "<strong>~$210M</strong> with LiveWire · <strong>~$280M</strong> without"],
      ["Dealers", "~1,150, twice as profitable as 2025"]])}
  <div class="spacer"></div>
  <p class="wide" style="font-size:26px;margin:0">A quarter of 2023's earnings. Two-thirds of 2019's motorcycles. Three-quarters of the dealers. <strong>That is the plan, working.</strong></p>''',
      tag="07 / 09", sid="s4-8", foot_l="Calculated from the company's own targets · Ground Truth No. 02 §12"))
    P.append(slide('''
  <div class="kick">Three things that are true at once</div>
  <ul style="font-size:27px">
    <li><strong>LiveWire did not break Harley-Davidson.</strong> A $75M loss does not take a company from $779M to zero. Touring, tariffs, a 12% retail decline and the HDFS sale did that. The electric bet is the flattering villain.</li>
    <li><strong>LiveWire is exactly what the new Harley cannot afford.</strong> When the motor company is guided to make $10–50M, a $70–80M loss is the difference between a profit and a loss. The plan solves this by not counting it.</li>
    <li><strong>The decision has a date.</strong> Cash to May 2027. Note due December 2027. EBITDA target: 2027. Nobody has said what the decision is.</li>
  </ul>
  <div class="spacer"></div>''',
      dark=True, tag="08 / 09", sid="s4-9", foot_l="Ground Truth No. 02 · §13 · Analysis, not reporting"))
    P.append(slide(f'''
  <div class="spacer"></div>
  <h2 style="font-size:66px;max-width:14ch;color:var(--dmag)">Which brick is LiveWire under?</h2>
  <p class="wide" style="font-size:27px;margin-top:26px">Back to the Bricks has five pillars, six targets and a two-year clock. It is scored on the motor company. Harley-Davidson, Inc. is not the motor company. It is HDMC, plus a finance company sold forward, minus a subsidiary guided to lose more than HDMC makes, with a note due in the plan's own target year.</p>
  <div class="spacer"></div>
  <p class="wide" style="font-size:26px;color:var(--dcyan)">Full brief: 16 sections in six parts, every source linked, open items and corrections published.<br>{URL}</p>''',
      dark=True, tag="09 / 09", sid="s4-10", foot_l="Former H-D product manager · Independent analyst", foot_r="No position held"))
    S.append(("Part 4 · The Bricks", P))
    # stand-alone route card (no part highlighted)
    S.append(("The route", [route_card(-1, "route-card", heading="Six parts,<br>one thesis", dek="Harley-Davidson's own filings, added up: the arithmetic, the sale, the subsidiary, the plan, the bet, and the final word.")]))

    # ═══════════ PAGE ═══════════
    parts_html = []
    for name, slides in S:
        label = f'<div class="parthead">{name} · {len(slides)-1} slides</div>\n' if len(slides) > 1 else ""
        parts_html.append(label + "\n".join(slides))
    total = sum(len(p) - 1 for _, p in S if len(p) > 1)
    html = f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{TITLE} · Carousels</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@600;700;800&family=IBM+Plex+Mono:wght@400;500;600&family=Public+Sans:ital,wght@0,300;0,400;0,500;0,600&display=swap">
<style>{CSS}
{EXTRA_CSS}
body.web .slide.card{{display:none}}
</style></head><body>
<div class="webhdr">
  <h4>Harley-Davidson: Back to<br>the Bricks, Down to Breakeven</h4>
  <p>What LiveWire costs the parent, and what the plan leaves out. Ground Truth No. 02, the LinkedIn series in full: four parts, {total} slides. The full brief, with every figure linked to its filing, is <a href="../">here</a>.</p>
  <p style="font-family:var(--mono);font-size:12px;letter-spacing:.12em;text-transform:uppercase;margin-top:18px">Contact Patch Advisory &middot; William Weppner &middot; September 2026</p>
</div>
<div class="wrapper">
{chr(10).join(parts_html)}
</div>
<script>document.body.classList.add("web");</script>
</body></html>'''
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write(html)
    print(OUT, len(html), "bytes;", total, "slides +", len(S), "cards")

if __name__ == "__main__":
    build()
