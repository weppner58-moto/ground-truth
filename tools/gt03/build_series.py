#!/usr/bin/env python3
"""Build groundtruth/03/series/index.html — the four-part LinkedIn series for Ground Truth No. 03.

Run from the repo root:  python3 tools/gt03/build_series.py
Then:                    python3 tools/lib/render_slides.py groundtruth/03/series/index.html 03 \
                           "1:The-Record" "2:Same-Sentence" "3:Too-Small-to-Say" "4:The-Sprint-and-Final-Word"
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "lib"))
from charts import bars, hbars, sbars, svg_theme, MAG, CYAN, INK3  # noqa: E402

LIB = ROOT / "tools" / "lib"
OUT = ROOT / "groundtruth" / "03" / "series" / "index.html"
URL = "weppner58-moto.github.io/ground-truth/groundtruth/03/"
CREDIT = "Contact Patch Advisory"
ISSUE = "Ground Truth No. 03"

EXTRA_CSS = """
.tbl{width:100%;border-collapse:collapse;font-size:24px;margin:10px 0 20px}
.tbl th{font-family:var(--mono);font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink3);text-align:left;padding:0 10px 10px 0;border-bottom:2px solid var(--rule2);font-weight:500}
.dk .tbl th{color:var(--dink3);border-color:#343A40}
.tbl td{padding:12px 10px 12px 0;border-bottom:1px solid var(--rule);vertical-align:top;line-height:1.35}
.dk .tbl td{border-color:var(--drule)}
.tbl td.num{text-align:right;font-family:var(--mono);font-size:22px;white-space:nowrap}
.tbl .hi{color:var(--mag);font-weight:600} .dk .tbl .hi{color:var(--dmag)}
ol.pillars{margin:0;padding:0;list-style:none;counter-reset:p}
ol.pillars li{counter-increment:p;display:grid;grid-template-columns:70px 1fr;gap:18px;padding:18px 0;border-top:1px solid var(--rule);font-size:27px;line-height:1.4;max-width:none}
ol.pillars li::before{content:counter(p,decimal-leading-zero);font-family:var(--disp);font-weight:800;font-size:44px;line-height:1;color:var(--mag)}
.dk ol.pillars li{border-color:var(--drule)} .dk ol.pillars li::before{color:var(--dmag)}
ol.pillars li b{font-weight:600}
.slide.card h1{font-size:80px}
.rgrid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:30px}
.rgrid .c{border:1px solid var(--rule);padding:16px;position:relative}
.dk .rgrid .c{border-color:var(--drule)}
.rgrid .c.on{border-color:var(--mag)} .dk .rgrid .c.on{border-color:var(--dmag)}
.rgrid .n{font-family:var(--mono);font-size:13px;letter-spacing:.18em;text-transform:uppercase;color:var(--mag)}
.dk .rgrid .n{color:var(--dmag)}
.rgrid .t{font-family:var(--disp);font-weight:800;text-transform:uppercase;font-size:38px;line-height:.95;margin:8px 0 10px}
.rgrid .d{font-size:21px;line-height:1.4;color:var(--ink2)}
.dk .rgrid .d{color:var(--dink3)}
.verdict{font-family:var(--disp);font-weight:800;text-transform:uppercase;font-size:58px;line-height:.95;border-top:4px solid var(--mag);padding-top:22px;margin-top:10px}
.dk .verdict{border-color:var(--dmag)}
.verdict i{font-style:normal;color:var(--mag)} .dk .verdict i{color:var(--dmag)}
.tl{list-style:none;margin:0;padding:0}
.tl li{display:grid;grid-template-columns:190px 1fr;gap:20px;padding:14px 0;border-top:1px solid var(--rule);font-size:25px;line-height:1.4;max-width:none}
.dk .tl li{border-color:var(--drule)}
.tl li b{font-family:var(--mono);font-size:15px;letter-spacing:.14em;text-transform:uppercase;color:var(--mag);font-weight:600;padding-top:6px}
.dk .tl li b{color:var(--dmag)}
.tl li.h b{color:var(--cyan)} .dk .tl li.h b{color:var(--dcyan)}
body.web .slide.card{display:none}
"""

PARTS = [("The Record", "Sixteen moves in one table. Brands go. Channels stay."),
         ("Same Sentence", "Buell, MV Agusta, and the words used both times."),
         ("Too Small to Say", "Alta, never disclosed. StaCyc, $14.9M, 33 to 1."),
         ("The Sprint & the Final Word", "1960: an Aermacchi. 2026: a Hero. What it was for.")]


def slide(sid, body, dark=False, tag="", cls=""):
    hdr = f"<div class='tophdr'><div class='mark'>CONTACT&nbsp;<i>PATCH</i></div><div class='tag'>{tag}</div></div>"
    return f"<div class='slide{' dk' if dark else ''}{(' ' + cls) if cls else ''}' id='{sid}'>{hdr}{body}</div>\n"


def foot(left, right=CREDIT):
    return f"<div class='foot'><span>{left}</span><span>{right}</span></div>"


def stat(k, v, sub="", mag=False, size=None):
    st = f" style='font-size:{size}px'" if size else ""
    return f"<div class='col stat{' m' if mag else ''}'><div class='k'>{k}</div><div class='v{' m' if mag else ''}'{st}>{v}</div>{('<div class=' + chr(39) + 'sub' + chr(39) + '>' + sub + '</div>') if sub else ''}</div>"


def tbl(head, rows):
    th = "".join(f"<th>{h}</th>" for h in head)
    trs = []
    for r in rows:
        tds = []
        for c in r:
            cls = ""
            if isinstance(c, tuple):
                c, cls = c
            tds.append(f"<td class='{cls}'>{c}</td>" if cls else f"<td>{c}</td>")
        trs.append("<tr>" + "".join(tds) + "</tr>")
    return "<table class='tbl'><thead><tr>" + th + "</tr></thead><tbody>" + "".join(trs) + "</tbody></table>"


def route_card(sid, n_on, dark=True):
    cells = "".join(f"<div class='c{' on' if i == n_on else ''}'><div class='n'>Part {i+1} of 4{' · this post' if i == n_on else ''}</div><div class='t'>{t}</div><div class='d'>{d}</div></div>" for i, (t, d) in enumerate(PARTS))
    body = f"""
  <div class='kick'>Harley-Davidson: Outside In · The route</div>
  <h1>Four parts.<br>One thesis.</h1>
  <p class='wide' style='font-size:26px;margin-top:22px;color:{'var(--dink3)' if dark else 'var(--ink2)'}'>Sixty-six years of buying what it could build, from the filings. Every figure links to its document in the full brief.</p>
  <div class='rgrid'>{cells}</div>
  <div class='spacer'></div>
  {foot(URL, ISSUE)}"""
    return slide(sid, body, dark=dark, tag="Route card", cls="card")


def build():
    css = (LIB / "series.css").read_text() + EXTRA_CSS
    S = []
    S.append(f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Harley-Davidson: Outside In, the series</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@600;700;800&family=IBM+Plex+Mono:wght@400;500;600&family=Public+Sans:ital,wght@0,300;0,400;0,500;0,600&display=swap">
<style>{css}</style>
</head><body class="web">
<div class="webhdr">
  <h4>Harley-Davidson:<br>Outside In</h4>
  <p>Sixty-six years of buying what it could build. Ground Truth No. 03, the LinkedIn series in full: four parts, in the order the brief reads, the record, the same sentence, too small to say, the Sprint and the final word. Every figure is drawn from an SEC filing, a company release or a full call transcript, except where marked. The complete brief, with each source linked to the document, is <a href="../">here</a>.</p>
  <p style="font-family:var(--mono);font-size:12px;letter-spacing:.12em;text-transform:uppercase;margin-top:18px">Contact Patch Advisory &middot; William Weppner &middot; September 2026</p>
</div>
<div class="wrapper">
""")

    # ═══════════ PART 1 — THE RECORD (10 slides) ═══════════
    P = 1
    N = 9
    S.append("<div class='parthead'>Part 1 · The Record · 10 slides</div>\n")
    S.append(slide("s1-1", f"""
  <div class='spacer'></div>
  <div class='kick'>Harley-Davidson: Outside In · Part 1 of 4</div>
  <h1 style='font-size:118px'>OUTSIDE<br>IN.</h1>
  <p class='wide' style='margin-top:36px;color:var(--dink3);font-size:30px'>Sixty-six years of Harley-Davidson buying what it could build. Aermacchi, Buell, MV Agusta, Alta, StaCyc, Hero, KYMCO, Dust. What it paid, what it got, what it was for.</p>
  <div class='spacer'></div>
  {foot('Harley-Davidson, Inc. · NYSE: HOG', 'September 2026')}""", dark=True, tag=ISSUE))
    S.append(route_card("s1-card", 0))
    S.append(slide("s1-2", f"""
  <div class='kick'>What they said · 5 May 2026 · the new plan</div>
  <div class='quote'>“By using and leveraging existing powertrain, existing platforms, we can have a much broader assortment of motorcycles to present.”</div>
  <div class='src'>Artie Starrs, CEO · Q1 2026 earnings call</div>
  <div class='spacer'></div>
  <p class='wide' style='font-size:30px'>The first new motorcycle under that plan is the Sprint. Its engine is a <strong>440cc single Hero MotoCorp builds in Rajasthan</strong> for a ₹2.29 lakh motorcycle.</p>
  <p class='wide' style='font-size:30px'>Same call: <strong>“we’re finalizing the specific production plans.”</strong></p>
  {foot('Source: Q1 2026 call transcript')}""", dark=True, tag=f"01 / {N:02d}"))
    S.append(slide("s1-3", f"""
  <h2 style='font-size:66px'>A company leaning on the platforms it already has is opening the plan with one it does not own.</h2>
  <p class='wide' style='font-size:30px;margin-top:20px'>That is not new. It is the sixty-sixth year of it.</p>
  <p class='wide' style='font-size:30px'>So I went back through the record, the filed one rather than the press one, for every time Harley-Davidson went outside for a product. What did it pay? What did it get? How did it end?</p>
  <div class='spacer'></div>
  {foot(ISSUE)}""", tag=f"02 / {N:02d}"))
    rows = [("1960", "Aermacchi", ("~$250K", "num"), "Sold 1978"), ("1986", "Holiday Rambler", ("~$155M", "num"), "Sold 1996"),
            ("1993", "Eaglemark → HDFS", ("$55M", "num"), ("Kept", "hi")), ("1993", "Buell", ("~$500K", "num"), "Shut 2009 · ~$125M"),
            ("2008", "MV Agusta", ("$105.1M", "num"), "Sold for €1 · $268M lost"), ("2018", "Alta Motors", ("n/d", "num"), "Gone in 6 months"),
            ("2019", "StaCyc", ("$14.9M", "num"), ("Kept · 21,633 units", "hi")), ("2019–20", "Qianjiang · Hero (licences)", ("n/d", "num"), ("Kept", "hi")),
            ("2021", "LiveWire SPAC", ("$100M", "num"), "2027?"), ("2026", "Dust · KYMCO Honcho", ("$375K cash", "num"), "Via LiveWire")]
    S.append(slide("s1-4", f"""
  <div class='kick'>Sixteen moves, 1960–2026 · the ones that fit on a slide</div>
  {tbl(['Year', 'Bought / licensed', 'Cost, as filed', 'How it ended'], rows)}
  <div class='spacer'></div>
  <p class='wide' style='font-size:24px;margin:0'>Full table, with the in-house programs and every source linked, in §01 of the brief.</p>
  {foot('Source: HOG 10-Ks and 8-Ks 1994–2026')}""", dark=True, tag=f"03 / {N:02d}"))
    S.append(slide("s1-5", f"""
  <h2>Two patterns fall out before any analysis</h2>
  <ol class='pillars'>
    <li><span><b>Every purchase that carried its own brand was sold or shut.</b> Holiday Rambler, Buell, MV Agusta, Aermacchi. Three of the four within two years of a CEO change. Same sentence every time.</span></li>
    <li><span><b>Every purchase that carried no badge into a Harley segment was kept.</b> Eaglemark’s balance sheet. StaCyc’s balance bikes. Hero’s engine. Qianjiang’s twin. KYMCO’s line. KKR’s capital.</span></li>
  </ol>
  <div class='spacer'></div>
  {foot(ISSUE)}""", tag=f"04 / {N:02d}"))
    lost = hbars([268.4, 125, 75, 422], ["MV Agusta", "Buell", "India / Street", "LiveWire"], fills=[MAG, MAG, INK3, MAG], fmt=lambda v: f"${v:,.0f}M",
                 sublabels=["filed", "estimate", "estimate", "consolidated"], vb=(900, None), row_h=70, left=250, scale=2.0,
                 label="Cost to unwind: MV Agusta $268M; Buell $125M; India $75M; LiveWire $422M.")
    S.append(slide("s1-6", f"""
  <h2 style='font-size:62px'>What the outside moves cost to unwind</h2>
  {svg_theme(lost, True)}
  <p class='wide' style='font-size:26px;margin-top:30px;color:var(--dink3)'>$ millions. MV Agusta is the filed net loss from discontinued operations. Buell and India are the company’s own estimates, never reconciled. LiveWire is the consolidated loss since the spin.</p>
  <p class='wide' style='font-size:26px;color:var(--dink3)'>Alta is missing because there is no number to put on it.</p>
  <div class='spacer'></div>
  {foot('Source: HOG 10-K FY2010; 10-Q Q3 2009; 8-K 24 Sep 2020; GT No. 02')}""", dark=True, tag=f"05 / {N:02d}"))
    S.append(slide("s1-7", f"""
  <div class='kick'>Same sentence · three CEOs</div>
  <div class='quote' style='font-size:31px'>“…in order to concentrate on its core motorcycle business.”</div>
  <div class='src'>10-K FY1996 · Holiday Rambler sold</div>
  <div class='quote' style='font-size:31px;margin-top:34px'>“We must focus both our effort and our investment on the Harley-Davidson brand.”</div>
  <div class='src'>Keith Wandell · 15 Oct 2009 · Buell shut, MV for sale</div>
  <div class='quote' style='font-size:31px;margin-top:34px'>“Over the last several years, we leaned heavily into Touring and Electric.”</div>
  <div class='src'>Artie Starrs · 5 May 2026</div>
  <div class='spacer'></div>
  {foot(ISSUE)}""", tag=f"06 / {N:02d}"))
    S.append(slide("s1-8", f"""
  <div class='kick'>The number that frames everything</div>
  <div class='row' style='margin-top:30px'>
    {stat('StaCyc · bought 2019', '$14.9M', 'Q1 2019 10-Q', size=84)}
    {stat('LiveWire · SPAC 2021', '$1.77B', 'pro-forma enterprise value', mag=True, size=84)}
  </div>
  <div class='row' style='margin-top:50px'>
    {stat('StaCyc units · 2025', '21,633', size=84)}
    {stat('LiveWire motorcycles · 2025', '653', mag=True, size=84)}
  </div>
  <div class='spacer'></div>
  <p class='wide' style='font-size:34px'><strong>The $14.9M acquisition outsells the $1.77B one thirty-three to one.</strong></p>
  {foot('Source: HOG 10-Q Q1 2019 · LVWR FY2025 results')}""", dark=True, tag=f"07 / {N:02d}"))
    S.append(slide("s1-9", f"""
  <div class='kick'>The thesis</div>
  <div class='verdict'>Harley doesn’t want electric. <i>It wants floor traffic.</i></div>
  <p class='wide' style='font-size:29px;margin-top:34px'>Harley builds when the product carries the full brand at the full price. Everything below the big twin (a small bike, a balance bike, a battery, a loan book) gets bought, licensed or partnered. Kept when it feeds the dealer. Dropped when it competes with the badge.</p>
  <div class='spacer'></div>
  <p class='wide' style='font-size:26px;color:var(--ink3);margin:0'>Read the whole record with that sentence in hand and it stops looking like a series of mistakes.</p>
  {foot(ISSUE)}""", tag=f"08 / {N:02d}"))
    S.append(slide("s1-10", f"""
  <div class='spacer'></div>
  <div class='kick'>Next · Part 2 of 4</div>
  <h1 style='font-size:100px'>SAME<br>SENTENCE.</h1>
  <p class='wide' style='margin-top:30px;color:var(--dink3);font-size:30px'>Buell and MV Agusta. $125 million and $268 million. What the two biggest purchases cost, from the 10-Ks and the sale agreement, and the words used both times.</p>
  <div class='spacer'></div>
  <p style='font-family:var(--mono);font-size:17px;letter-spacing:.12em;text-transform:uppercase;color:var(--dink3);margin:0'>Full brief, every source linked:<br>{URL}</p>
  {foot(ISSUE, 'William Weppner')}""", dark=True, tag=f"09 / {N:02d}"))

    # ═══════════ PART 2 — SAME SENTENCE (10 slides) ═══════════
    N = 9
    S.append("<div class='parthead'>Part 2 · Same Sentence · 10 slides</div>\n")
    S.append(slide("s2-1", f"""
  <div class='spacer'></div>
  <div class='kick'>Harley-Davidson: Outside In · Part 2 of 4</div>
  <h1 style='font-size:110px'>SAME<br>SENTENCE.</h1>
  <p class='wide' style='margin-top:36px;color:var(--dink3);font-size:30px'>Buell and MV Agusta. What the two biggest outside purchases cost, from the filings, and the words used to end both.</p>
  <div class='spacer'></div>
  {foot('Harley-Davidson, Inc. · NYSE: HOG', 'September 2026')}""", dark=True, tag=ISSUE))
    S.append(route_card("s2-card", 1))
    S.append(slide("s2-2", f"""
  <div class='kick'>Buell · 1993–2009</div>
  <div class='row' style='margin-top:20px'>
    {stat('1993 · 49% stake', '~$500K', 'secondary source', size=80)}
    {stat('2008 · units shipped', '13,119', '$123.1M revenue', size=80)}
  </div>
  <div class='row' style='margin-top:50px'>
    {stat('14 Oct 2009 · exit cost', '~$125M', 'Q3 2009 10-Q, Note 19', mag=True, size=80)}
    {stat('Jobs', '~180', '80 hourly, 100 salaried', mag=True, size=80)}
  </div>
  <div class='spacer'></div>
  <p class='wide' style='font-size:27px'>~$70M incentives, inventory and operating costs. ~$14M fixed assets. ~$9M severance. ~$32M contracts. <strong>The realized total was never reported on its own.</strong></p>
  {foot('Source: HOG 10-Q Q3 2009 · 8-K 15 Oct 2009')}""", tag=f"01 / {N:02d}"))
    S.append(slide("s2-3", f"""
  <div class='kick'>Keith Wandell · five months into the job · 15 October 2009</div>
  <div class='quote'>“The fact is we must focus both our effort and our investment on the Harley-Davidson brand, as we believe this provides an optimal path to sustained, meaningful, long-term growth.”</div>
  <div class='src'>8-K Ex. 99.1 · filed with the SEC</div>
  <div class='spacer'></div>
  <p class='wide' style='font-size:30px'>Erik Buell, eighteen months later: <strong>“They didn’t shut down Buell because they were mean.”</strong> He was right. They shut it because it was a second brand in a building with room for one.</p>
  {foot('Source: 8-K 15 Oct 2009 · Powersports Business 14 Mar 2011')}""", dark=True, tag=f"02 / {N:02d}"))
    S.append(slide("s2-4", f"""
  <div class='kick'>MV Agusta · bought 8 August 2008</div>
  <div class='row' style='margin-top:20px'>
    {stat('Total consideration', '€68.3M', '$105.1M · incl. €47.5M of bank debt', size=84)}
    {stat('Goodwill booked', '$85.8M', 'FY2009 10-K, final allocation', size=84)}
  </div>
  <div class='row' style='margin-top:50px'>
    {stat('IPR&D written off on arrival', '$20.1M', 'a fifth of the price, day one', mag=True, size=84)}
    {stat('Months owned', '24', '8 Aug 2008 – 6 Aug 2010', mag=True, size=84)}
  </div>
  <div class='spacer'></div>
  <p class='wide' style='font-size:28px'>Jim Ziemer, announcing it: <strong>“Motorcycles are the heart, soul and passion of Harley-Davidson, Buell and MV Agusta.”</strong> He retired nine months later.</p>
  {foot('Source: HOG 8-K 11 Jul 2008 · 10-K FY2009')}""", tag=f"03 / {N:02d}"))
    mv = hbars([105.1, 20.1, 115.4, 111.8, 268.4], ["Consideration", "IPR&D write-off", "2009 impairment", "2010 impairment", "Net loss 2008–10"],
               fills=[INK3, MAG, MAG, MAG, MAG], fmt=lambda v: f"${v:,.1f}M", vb=(900, None), row_h=64, left=260, scale=2.0,
               label="MV Agusta: $105.1M in; $20.1M IPR&D, $115.4M and $111.8M impairments; $268.4M net loss.")
    S.append(slide("s2-5", f"""
  <h2 style='font-size:62px'>$105 million in. $268 million out.</h2>
  {svg_theme(mv, True)}
  <p class='wide' style='font-size:26px;margin-top:26px;color:var(--dink3)'>Loss from discontinued operations, net of tax: $29.5M (2008) + $125.8M (2009) + $113.1M (2010). <strong style='color:var(--dink)'>2.55 times the purchase price, or $11.2M for every month Harley owned it.</strong> A $51.0M tax reversal in 2011 nets it to $217.4M.</p>
  <div class='spacer'></div>
  {foot('Source: HOG 10-K FY2009, FY2010, FY2011')}""", dark=True, tag=f"04 / {N:02d}"))
    S.append(slide("s2-6", f"""
  <div class='kick'>The sale · 6 August 2010 · the 10-K says “nominal consideration”</div>
  <h2 style='font-size:60px'>The agreement says what nominal means.</h2>
  <ul class='tl'>
    <li><b>The shares</b><span>All 120,000 shares of MV Agusta Motor S.p.A., “for a consideration of Euro 1 (one).”</span></li>
    <li><b>The U.S. company</b><span>MV Agusta USA LLC, for US$1.</span></li>
    <li><b>The receivable</b><span>€103,789,617.60 Harley had lent its own subsidiary. Sold for €1.</span></li>
    <li><b>Cash left inside</b><span>A capital increase of €20,000,000, paid into escrow.</span></li>
    <li><b>The earn-out</b><span>Castiglioni’s 2016 payment “finally and irrevocably waived.”</span></li>
  </ul>
  <div class='spacer'></div>
  {foot('Source: Ex. 2.1 to 8-K, 9 Aug 2010 · §2.1.1, §7.1.1, §7.2.2')}""", tag=f"05 / {N:02d}"))
    S.append(slide("s2-7", f"""
  <div class='kick'>€1, €2 or €3? All three are right.</div>
  <div class='row' style='margin-top:40px'>
    {stat('The shares', '€1', size=120)}
    {stat('The U.S. LLC', '$1', size=120)}
    {stat('The receivable', '€1', size=120)}
  </div>
  <div class='spacer'></div>
  <p class='wide' style='font-size:30px'>“€1” is the share price. “€3” is the press adding three nominal payments. “€2” counts only the euros.</p>
  <p class='wide' style='font-size:30px'>The 10-K reports <strong>“an immaterial loss on the date of sale.”</strong> Also true. By August 2010 there was nothing left to lose.</p>
  {foot('Source: HOG 10-K FY2010 · 8-K 9 Aug 2010')}""", dark=True, tag=f"06 / {N:02d}"))
    S.append(slide("s2-8", f"""
  <div class='kick'>Keith Wandell · 6 August 2010</div>
  <div class='quote'>“Our decision to divest MV Agusta reflects our strategy to focus our efforts and our investment on the Harley-Davidson brand.”</div>
  <div class='src'>H-D release · MV Agusta sale</div>
  <div class='spacer'></div>
  <h3 style='margin-bottom:14px'>1996: “core motorcycle business.”<br>2009, 2010: “the Harley-Davidson brand.”</h3>
  <p class='wide' style='font-size:29px;margin:0'>The words repeat because the decision does. A second brand that competes with Harley-Davidson for engineering dollars does not survive the next CEO.</p>
  {foot(ISSUE)}""", tag=f"07 / {N:02d}"))
    S.append(slide("s2-9", f"""
  <h2 style='font-size:64px'>MV is the one time Harley bought big.</h2>
  <p class='wide' style='font-size:31px'>It lost 2.55 times the purchase price in twenty-four months and handed the factory back to the family it bought it from. The same Castiglionis took Aermacchi off Harley’s hands in 1978.</p>
  <p class='wide' style='font-size:31px'><strong>The company learned the lesson. Every outside move since has been sized to be forgettable.</strong></p>
  <div class='spacer'></div>
  <p class='wide' style='font-size:26px;color:var(--dink3);margin:0'>Next: the two that were too small to disclose.</p>
  {foot(ISSUE)}""", dark=True, tag=f"08 / {N:02d}"))
    S.append(slide("s2-10", f"""
  <div class='spacer'></div>
  <div class='kick'>Next · Part 3 of 4</div>
  <h1 style='font-size:96px'>TOO SMALL<br>TO SAY.</h1>
  <p class='wide' style='margin-top:30px;color:var(--ink2);font-size:30px'>Alta Motors: one sentence, no number, bounded by Alta’s own Form D. StaCyc: $14.9 million, and it outsells LiveWire 33 to 1.</p>
  <div class='spacer'></div>
  <p style='font-family:var(--mono);font-size:17px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink3);margin:0'>Full brief, every source linked:<br>{URL}</p>
  {foot(ISSUE, 'William Weppner')}""", tag=f"09 / {N:02d}"))

    # ═══════════ PART 3 — TOO SMALL TO SAY (11 slides) ═══════════
    N = 10
    S.append("<div class='parthead'>Part 3 · Too Small to Say · 11 slides</div>\n")
    S.append(slide("s3-1", f"""
  <div class='spacer'></div>
  <div class='kick'>Harley-Davidson: Outside In · Part 3 of 4</div>
  <h1 style='font-size:104px'>TOO SMALL<br>TO SAY.</h1>
  <p class='wide' style='margin-top:36px;color:var(--dink3);font-size:30px'>Alta Motors, which Harley never put a number on. StaCyc, the one purchase that hit every target it was given. Together, what Harley actually wanted from electric.</p>
  <div class='spacer'></div>
  {foot('Harley-Davidson, Inc. · NYSE: HOG', 'September 2026')}""", dark=True, tag=ISSUE))
    S.append(route_card("s3-card", 2))
    S.append(slide("s3-2", f"""
  <div class='kick'>1 March 2018</div>
  <div class='quote'>“Alta has demonstrated innovation and expertise in EV and their objectives align closely with ours.”</div>
  <div class='src'>Matt Levatich, CEO · H-D release</div>
  <div class='spacer'></div>
  <p class='wide' style='font-size:30px'>No amount. No percentage. The Q1 2018 earnings release is the <strong>only Harley-Davidson SEC filing that has ever contained the word “Alta.”</strong> One sentence: “Invested in a collaborative agreement with Alta Motors.”</p>
  {foot('Source: H-D release 1 Mar 2018 · 8-K 24 Apr 2018')}""", tag=f"01 / {N:02d}"))
    inv = sbars([1.083, -1.106, -1.679], ["Q3 2017", "Q3 2018", "Q4 2018"], fills=[CYAN, MAG, MAG], fmt=lambda v: ("+" if v > 0 else "−") + f"${abs(v):.1f}M",
                vb=(900, 380), scale=1.8, left=110, label="Investment income: +$1.1M Q3 2017; −$1.1M Q3 2018; −$1.7M Q4 2018.")
    S.append(slide("s3-3", f"""
  <h2 style='font-size:60px'>Search every 10-Q and 10-K, 2018–19. No equity investment. No write-off. One footprint.</h2>
  {svg_theme(inv, True)}
  <p class='wide' style='font-size:25px;margin-top:24px;color:var(--dink3)'>“Investment (loss) income” ran at about +$1M a quarter and went negative the two quarters after Alta. No filing attributes the swing. <em>Inferred, not documented.</em></p>
  <div class='spacer'></div>
  {foot('Source: HOG 10-Q Q3 2018 · Q4 2018 release')}""", dark=True, tag=f"02 / {N:02d}"))
    fd = [("7 Mar 2016", "$7.0M convertible notes", ("$1.77M", "num"), ("18", "num")), ("2 Jun 2017", "$26.1M equity", ("$12.4M", "num"), ("42", "num")),
          ("3 Jul 2017", "$20.3M equity + debt", ("$15.2M", "num"), ("24", "num")), ("<b>5 Feb 2018</b>", "Same round, <span class='hi'>closed</span>", ("<span class='hi'>$20.84M</span>", "num"), ("<span class='hi'>30</span>", "num")),
          ("<b>13 Aug 2018</b>", "<span class='hi'>$5.0M bridge note</span>", ("<span class='hi'>$2.45M</span>", "num"), ("<span class='hi'>4</span>", "num"))]
    S.append(slide("s3-4", f"""
  <div class='kick'>Alta’s own paperwork bounds it · Faster Faster, Inc. · CIK 1620298</div>
  {tbl(['Filed', 'Offering', 'Sold', 'Investors'], fd)}
  <p class='wide' style='font-size:26px;margin-top:10px'>The round Harley joined closed by amendment on <strong>2 February 2018</strong>, four weeks before the announcement. Since July it had grown by <strong>$5.65M and six investors</strong>. No Form D reports an equity sale after that.</p>
  <div class='spacer'></div>
  <p class='wide' style='font-size:26px;margin:0'><strong>If Harley’s money is in that round, the check was inside $5.65M.</strong> Inferred. Harley has never said.</p>
  {foot('Source: Faster Faster, Inc. Forms D, 2016–2018 · EDGAR')}""", tag=f"03 / {N:02d}"))
    S.append(slide("s3-5", f"""
  <div class='kick'>Six months, on the calendar</div>
  <ul class='tl'>
    <li><b>2 Feb 2018</b><span>Alta closes its equity round at $20,843,998.</span></li>
    <li><b>1 Mar 2018</b><span>Harley announces the investment. “We intend to be the world leader in the electrification of motorcycles.”</span></li>
    <li><b>27 Jul 2018</b><span>Alta starts selling a $5.0M bridge note. Four investors, $2.45M.</span></li>
    <li><b>29 Aug 2018</b><span>Asphalt &amp; Rubber, sourced: Harley is out. No company statement.</span></li>
    <li class='h'><b>5 Sep 2018</b><span>Harley announces its own Silicon Valley EV R&amp;D facility: “battery, power electronics, and e-machine design.” Alta’s specialty.</span></li>
    <li><b>17 Oct 2018</b><span>Alta ceases operations.</span></li>
    <li><b>20 Feb 2019</b><span>BRP buys the IP. “No interest in restarting operations.”</span></li>
  </ul>
  <div class='spacer'></div>
  {foot('Source: EDGAR · H-D releases · BRP release · A&R · TechCrunch')}""", dark=True, tag=f"04 / {N:02d}"))
    S.append(slide("s3-6", f"""
  <h2 style='font-size:62px'>Alta is the cleanest case in the table.</h2>
  <p class='wide' style='font-size:31px'>Harley wanted the technology without the partner. It paid a sum too small to disclose to find out what it needed, opened its own lab a week after the split leaked, and built the rest in-house.</p>
  <p class='wide' style='font-size:31px'><strong>Six months. One press release. No number.</strong> That is what a cheap option looks like from the outside.</p>
  <div class='spacer'></div>
  <p class='wide' style='font-size:24px;color:var(--ink3);margin:0'>Alta’s co-founder has his own account of what Harley took with it. It is in the brief, on the record, unverified, with a disclosure.</p>
  {foot(ISSUE)}""", tag=f"05 / {N:02d}"))
    S.append(slide("s3-7", f"""
  <div class='kick'>StaCyc · 4 March 2019 · Q1 2019 10-Q</div>
  <div class='row' style='margin-top:20px'>
    {stat('Total consideration', '$14.9M', '$7.0M cash at close', size=84)}
    {stat('Goodwill · intangibles', '$9.5M · $5.3M', 'goodwill tax-deductible', size=66)}
  </div>
  <div class='row' style='margin-top:50px'>
    {stat('Earn-out, max', '$6.54M', 'three volume milestones', size=84)}
    {stat('Earn-out, paid', '$6.54M', '$2.18M × 2020, 2021, 2022', size=84)}
  </div>
  <div class='spacer'></div>
  <p class='wide' style='font-size:28px'>Harley’s filing never explains the other $7.9M. LiveWire’s carve-out statements do. <strong>StaCyc hit every volume target it was given.</strong></p>
  {foot('Source: HOG 10-Q Q1 2019 · LVWR 8-K 30 Sep 2022, 10-K FY2022')}""", dark=True, tag=f"06 / {N:02d}"))
    S.append(slide("s3-8", f"""
  <div class='kick'>What it was bought for · their words</div>
  <div class='quote' style='font-size:33px'>“The StaCyc team shares the same vision we have for building the next generation of riders globally.”</div>
  <div class='src'>Heather Malenshek, SVP Marketing and Brand · 5 Mar 2019</div>
  <div class='quote' style='font-size:33px;margin-top:36px'>“Kids who are enjoying two-wheeled freedom with their families, connecting through Harley-Davidson dealerships and events. Starting at $649.”</div>
  <div class='src'>Matt Levatich · Q1 2019 call</div>
  <div class='spacer'></div>
  <p class='wide' style='font-size:28px;margin:0'>Not electrification. <strong>The next customer.</strong></p>
  {foot('Source: H-D release 5 Mar 2019 · Q1 2019 call transcript')}""", tag=f"07 / {N:02d}"))
    units = bars([653, 21633], ["LiveWire motorcycles", "StaCyc"], fills=[MAG, CYAN], fmt=lambda v: f"{v:,.0f}", vb=(900, 400), ymax=25000, ticks=5, scale=1.8, left=120,
                 label="2025: 653 LiveWire motorcycles; 21,633 StaCyc.")
    S.append(slide("s3-9", f"""
  <h2 style='font-size:62px'>2025: thirty-three StaCycs for every LiveWire motorcycle</h2>
  {svg_theme(units, True)}
  <p class='wide' style='font-size:26px;margin-top:24px;color:var(--dink3)'>Revenue: $6.1M motorcycles, <strong style='color:var(--dink)'>$19.6M StaCyc, 76% of LiveWire’s product revenue</strong>, from a $14.9M purchase of a company that makes $649 balance bikes for three-year-olds.</p>
  <div class='spacer'></div>
  {foot('Source: LVWR FY2025 results, 10 Feb 2026')}""", dark=True, tag=f"08 / {N:02d}"))
    S.append(slide("s3-10", f"""
  <div class='kick'>The older precedent · Eaglemark, 1993–1995</div>
  <div class='row' style='margin-top:30px'>
    {stat('Jan 1993 · 49%', '$10M', '10-K FY1994', size=96)}
    {stat('Nov 1995 · the rest', '~$45M', '10-K FY1996', size=96)}
  </div>
  <div class='spacer'></div>
  <p class='wide' style='font-size:31px'>$55M for the business that became HDFS, made <strong>$248M</strong> in 2024, and that KKR and PIMCO paid 1.75× book for a tenth of in 2025.</p>
  <p class='wide' style='font-size:31px'><strong>The two outside purchases that were kept and made money are the two that make money on somebody else’s product on a Harley dealer’s floor.</strong> Neither has ever been asked to build a motorcycle.</p>
  {foot('Source: HOG 10-K FY1994, FY1996, FY2025')}""", tag=f"09 / {N:02d}"))
    S.append(slide("s3-11", f"""
  <div class='spacer'></div>
  <div class='kick'>Next · Part 4 of 4</div>
  <h1 style='font-size:92px'>THE SPRINT,<br>AND THE<br>FINAL WORD.</h1>
  <p class='wide' style='margin-top:30px;color:var(--dink3);font-size:30px'>1960: an Aermacchi. 2026: a Hero. The same hole below the big twin, and somebody else’s engine in it both times. Seven CEOs, one cycle, and what every purchase was for.</p>
  <div class='spacer'></div>
  <p style='font-family:var(--mono);font-size:17px;letter-spacing:.12em;text-transform:uppercase;color:var(--dink3);margin:0'>Full brief, every source linked:<br>{URL}</p>
  {foot(ISSUE, 'William Weppner')}""", dark=True, tag=f"10 / {N:02d}"))

    # ═══════════ PART 4 — THE SPRINT AND THE FINAL WORD (11 slides) ═══════════
    N = 10
    S.append("<div class='parthead'>Part 4 · The Sprint and the Final Word · 11 slides</div>\n")
    S.append(slide("s4-1", f"""
  <div class='spacer'></div>
  <div class='kick'>Harley-Davidson: Outside In · Part 4 of 4</div>
  <h1 style='font-size:92px'>THE SPRINT,<br>AND THE<br>FINAL WORD.</h1>
  <p class='wide' style='margin-top:36px;color:var(--dink3);font-size:30px'>What Harley builds, what it buys, and the rule that falls out. Then the two motorcycles that will test it, and the one thing every purchase was for.</p>
  <div class='spacer'></div>
  {foot('Harley-Davidson, Inc. · NYSE: HOG', 'September 2026')}""", dark=True, tag=ISSUE))
    S.append(route_card("s4-card", 3))
    S.append(slide("s4-2", f"""
  <div class='kick'>Built in-house · three programs, two outcomes</div>
  <ol class='pillars'>
    <li><span><b>Street 500/750, 2013.</b> “The first all-new platform in 13 years.” Built in Kansas City and Bawal, India. India exited September 2020, ~$75M. The CFO, 2021: “the unprofitable Street.”</span></li>
    <li><span><b>Milwaukee-Eight, 2016.</b> “The ninth Big Twin in its history.” Still the engine of every Touring bike.</span></li>
    <li><span><b>Revolution Max, 2021.</b> “A clean-sheet, advanced-design effort.” Pan America, Sportster S, Nightster. A $20,000 motorcycle.</span></li>
  </ol>
  <div class='spacer'></div>
  {foot('Source: H-D releases · 8-K 24 Sep 2020 · Q3 2021 call')}""", tag=f"01 / {N:02d}"))
    S.append(slide("s4-3", f"""
  <div class='kick'>The rule</div>
  <div class='verdict' style='font-size:54px'>Harley develops from within when the product carries the full brand at the full price, <i>and reaches outside for everything below it.</i></div>
  <div class='spacer'></div>
  <p class='wide' style='font-size:29px;margin:0'>The one time it built its own small bike in its own plants, it lost money, closed the plant, and licensed the segment to the partner who could build the engine for ₹2.29 lakh.</p>
  {foot(ISSUE)}""", dark=True, tag=f"02 / {N:02d}"))
    S.append(slide("s4-4", f"""
  <h2 style='font-size:62px'>The first Harley-Davidson Sprint was an Aermacchi.</h2>
  <p class='wide' style='font-size:29px'>1960: Harley bought half of the Varese motorcycle division, for about a quarter of a million dollars by the accounts that survive, because the 125cc Hummer left a gap between it and the big twins that Japan was about to fill.</p>
  <p class='wide' style='font-size:29px'>It sold the Sprint for fourteen years, won three 250cc world titles with Walter Villa, and in 1978 sold the factory to the Castiglionis. <strong>The same family it bought MV Agusta from thirty years later, and sold it back to for a euro.</strong></p>
  <div class='spacer'></div>
  {foot('Aermacchi dates and prices: secondary sources · see open items')}""", tag=f"03 / {N:02d}"))
    S.append(slide("s4-5", f"""
  <div class='kick'>Sixty-six years on · the Sprint returns · on a Hero engine</div>
  <ul class='tl'>
    <li><b>Jul 2023</b><span>Hero launches the X440. Engine “co-developed by Hero MotoCorp and Harley-Davidson,” built at Neemrana. ₹2,29,000, about $2,760.</span></li>
    <li><b>Jul 2025</b><span>Zeitz: the Sprint has “been in development since 2021,” “targeting an entry price below $6,000,” and will be “profitable.”</span></li>
    <li><b>May 2026</b><span>Starrs: “we’re finalizing the specific production plans.” Trade reporting: target now “less than $10,000,” plant undecided.</span></li>
    <li><b>Jun 2026</b><span>Hero’s CEO: “it can take it from Hero to sell elsewhere; that decision rests with Harley.”</span></li>
    <li><b>Jul 2026</b><span>Starrs: “we expect to ship Sprint end of this year.” No price. No plant. No mention of Hero.</span></li>
  </ul>
  <div class='spacer'></div>
  {foot('Source: Hero release Jul 2023 · H-D calls 2025–26')}""", dark=True, tag=f"04 / {N:02d}"))
    S.append(slide("s4-6", f"""
  <h2 style='font-size:64px'>Plant and price. Both undecided. Both are the test.</h2>
  <div class='row' style='margin-top:30px'>
    <div class='col stat'><div class='k'>If the Sprint ships from Neemrana</div><p style='font-size:27px;margin-top:10px'>The rule held. The plan’s “existing platforms” include one that belongs to a licensee in Rajasthan.</p></div>
    <div class='col stat m'><div class='k'>If it ships from York</div><p style='font-size:27px;margin-top:10px'>It is not a $6,000 motorcycle at a York cost base, and the Street’s history says what happens next.</p></div>
  </div>
  <div class='spacer'></div>
  <p class='wide' style='font-size:28px;margin:0'>The company has been trying to fill the space below the big twin with somebody else’s motorcycle since Eisenhower. <strong>It has never once filled it with its own.</strong></p>
  {foot(ISSUE)}""", tag=f"05 / {N:02d}"))
    S.append(slide("s4-7", f"""
  <div class='kick'>The other half of the test · Sportster 883 · 2027</div>
  <div class='quote' style='font-size:33px'>“This has been the most requested motorcycle from both our riders and our dealers … we have the cost at a place where we are comfortable against the expected MSRP.”</div>
  <div class='src'>Artie Starrs · Q1 2026 call</div>
  <div class='spacer'></div>
  <p class='wide' style='font-size:29px'>Air-cooled, ~$10,000, York, per trade reporting. The first air-cooled twin program since the Evolution. <strong>A Sportster built in York that makes money at $10,000 would be the first time since 1960 that Harley filled the hole with its own motorcycle.</strong></p>
  {foot('Source: Q1 2026 call · Motorcycle.com 5 May 2026 (unverified)')}""", dark=True, tag=f"06 / {N:02d}"))
    ceo = [("Bleustein", "1997–2005", "Buell to ~100%", "none"), ("Ziemer", "2005–09", "MV Agusta", "none"), ("Wandell", "2009–15", "none", ("Buell · MV Agusta", "hi")),
           ("Levatich", "2015–20", "Alta · StaCyc · QJ · Thailand", "Alta"), ("Zeitz", "2020–25", "Hero · LiveWire SPAC · HDFS sale", ("India · Street · Sportster", "hi")),
           ("Starrs", "2025–", "Sprint · 883 · Dust", "Rev Max home · “Electric”")]
    S.append(slide("s4-8", f"""
  <div class='kick'>The cycle · each CEO’s purchases are the next CEO’s focus story</div>
  {tbl(['CEO', 'Tenure', 'Bought or started', 'Sold, shut or reversed'], ceo)}
  <div class='spacer'></div>
  <p class='wide' style='font-size:27px;margin:0'>Buell lasted eleven months into a new CEO. MV lasted fourteen. <strong>LiveWire is eleven months into Starrs</strong>, with the sentence already said, cash to about May 2027, and $75M due to the parent that December.</p>
  {foot('Source: H-D releases and 8-Ks, 1997–2026 · GT No. 02')}""", tag=f"07 / {N:02d}"))
    S.append(slide("s4-9", f"""
  <div class='kick'>Analysis, not reporting</div>
  <h2 style='font-size:58px'>The two pieces of LiveWire with a future are the two that were never electric motorcycles.</h2>
  <p class='wide' style='font-size:28px'><strong>StaCyc</strong>: a dealer-traffic product with a margin and five years of hitting volume targets. <strong>Dust</strong>: an option on off-road electric that cost $375,000 in cash. The Alta structure, done inside a subsidiary this time.</p>
  <p class='wide' style='font-size:28px'>If LiveWire is sold, merged or wound down, watch whether those two come back into the motor company. <strong>That would be the tell.</strong></p>
  <div class='spacer'></div>
  {foot('Inferred · no filing states any such intention')}""", dark=True, tag=f"08 / {N:02d}"))
    S.append(slide("s4-10", f"""
  <div class='kick'>The final word</div>
  <div class='verdict'>Harley doesn’t want electric. <i>It wants floor traffic.</i></div>
  <p class='wide' style='font-size:28px;margin-top:30px'>The Milwaukee-Eight and the Rev Max got built because a $25,000 motorcycle pays for an engine program. A 440 single, a balance bike, a battery and a loan book do not, and every one was bought, licensed or partnered. Kept when it feeds the dealer, dropped when it competes with the badge.</p>
  <p class='wide' style='font-size:28px'>StaCyc is the one part of the electric decade Harley has never had to write down. <strong>It is the one that was never an electric motorcycle.</strong></p>
  <div class='spacer'></div>
  {foot(ISSUE)}""", tag=f"09 / {N:02d}"))
    S.append(slide("s4-11", f"""
  <div class='spacer'></div>
  <div class='kick'>Ground Truth No. 03 · the question</div>
  <h1 style='font-size:84px'>HARLEY KEEPS WHAT FILLS THE FLOOR AND SELLS WHAT COMPETES WITH THE BADGE.</h1>
  <p class='wide' style='margin-top:30px;color:var(--dmag);font-size:40px;font-family:var(--disp);font-weight:800;text-transform:uppercase;line-height:.95'>Which of those is the Sprint?</p>
  <div class='spacer'></div>
  <p style='font-family:var(--mono);font-size:17px;letter-spacing:.12em;text-transform:uppercase;color:var(--dink3);margin:0'>Full brief, every source linked, corrections log, open items:<br>{URL}</p>
  {foot(ISSUE, 'William Weppner · Contact Patch Advisory')}""", dark=True, tag=f"10 / {N:02d}"))

    # stand-alone route card
    S.append(route_card("route-card", -1))
    S.append("</div>\n</body></html>\n")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("".join(S))
    print("wrote", OUT, OUT.stat().st_size, "bytes")


if __name__ == "__main__":
    build()
