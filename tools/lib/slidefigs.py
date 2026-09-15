#!/usr/bin/env python3
"""
A figure on every carousel slide that carries only text. Drawn from the slide's own numbers with
tools/lib/figs.py and inserted at the top of the slide (after the header) or the end (before the foot).
Idempotent; run after place.py and before fit.py.

  python3 tools/lib/slidefigs.py 02
"""
import re, sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "lib"))
import figs as F  # noqa: E402


def pos(d, a, b):
    return (d - a).days / (b - a).days


D = date
FIGS = {
    "02": {
        # Part 1 · The Arithmetic
        "s1-3": ("end", F.hbars([
            ("HDMC · the motor company", (10, 50), "$10–50M", "cy"),
            ("HDFS · the finance company", (55, 70), "$55–70M", "cy"),
            ("LiveWire · the subsidiary", (-80, -70), "$(70–80)M", "mg"),
        ], cap="2026 operating income guidance, $ millions · 23 Jul 2026")),
        "s1-4": ("end", F.numberline(-100, 100, [
            ("range", -15, 50, "2026, implied: $(15)M to $50M", "cy"),
        ], offscale="2023: $779M, off this chart", cap="Consolidated operating income, $ millions")),
        "s1-5": ("end", F.proportion([
            ("LiveWire's share of H-D revenue", 0.6, "0.6%", "mg"),
            ("LiveWire's share of H-D headcount", 2.7, "2.7%", "mg"),
            ("LiveWire's loss against HDMC's guided profit", 140, ">100%", "mg"),
        ], cap="$70–80M of loss against $10–50M of profit, at every point in both ranges")),
        "s1-9": ("end", F.hbars([
            ("H1 2026 · reported", 99.5, "$99.5M", "cy"),
            ("Full year · guided", (-15, 50), "$(15)–50M", "cy"),
            ("H2 2026 · implied", (-114.5, -49.5), "$(50–115)M", "mg"),
        ], cap="Consolidated operating income, $ millions · Q4 2025 alone lost $260M at HDMC")),
        "s1-10": ("top", F.route([(1, "The Arithmetic"), (2, "The Sale"), (3, "The Subsidiary"), (4, "The Bricks")], 1)),
        # Part 2 · The Sale
        "s2-5": ("end", F.hbars([
            ("HDFS operating income foregone · $180M a year, seven years", [180] * 7, "$1.26B", "mg"),
            ("Discretionary cash from the sale · once", 1250, "$1.25B", "cy"),
        ], cap="$ millions · the two sides of the trade, at the 2024 run rate")),
        "s2-7": ("end", F.hbars([
            ("HDFS · the finance company", 490.4, "$490.4M", "cy"),
            ("HDMC · the motor company", -28.7, "$(28.7)M", "mg"),
            ("LiveWire · the subsidiary", -75.0, "$(75.0)M", "mg"),
            ("Harley-Davidson, Inc. · consolidated", 386.6, "$386.6M", "cy"),
        ], cap="2025 operating income by segment, $ millions · 10-K FY2025")),
        "s2-8": ("top", F.route([(1, "The Arithmetic"), (2, "The Sale"), (3, "The Subsidiary"), (4, "The Bricks")], 2)),
        # Part 3 · The Subsidiary
        "s3-7": ("end", F.hbars([
            ("H-D operating income · with the minority outstanding, as today", 100, "same", "cy"),
            ("H-D operating income · after buying the minority for ~$28M", 100, "same", "cy"),
        ], cap="Already consolidated · the whole loss is on the line either way; $28M moves nothing above minority interest")),
        "s3-8": ("end", F.span("Q3 2026 · the quarter LiveWire said it would pursue financing", [
            (0.0, 0.25, "cy", ""),
            (0.77, 1.0, "hatch", "three weeks left"),
        ], [
            (pos(D(2026, 7, 23), D(2026, 7, 1), D(2026, 9, 30)), "23 Jul · Q2 results", "inkline"),
            (pos(D(2026, 8, 5), D(2026, 7, 1), D(2026, 9, 30)), "5 Aug · 10-Q: financing “this quarter”", "inkline"),
            (1.0, "30 Sep · quarter ends", "mgline"),
        ], note="No financing announced as of this writing")),
        "s3-9": ("top", F.route([(1, "The Arithmetic"), (2, "The Sale"), (3, "The Subsidiary"), (4, "The Bricks")], 3)),
        # Part 4 · The Bricks
        "s4-2": ("end", F.doc("Back to the Bricks · release, 5 May 2026 · find: \u201celectric\u201d", [
            "Five pillars", "", "", "", "Six targets", "", "", "Forward-looking factors: LiveWire",
        ], 7, stamp="0 MATCHES", cap="The word \u201celectric\u201d does not appear · LiveWire is in the forward-looking factors only")),
        "s4-4": ("end", F.hbars([
            ("2019 · HDMC operating margin, the year Hardwire was written to fix", 6.3, "6.3%", "cy"),
            ("2027 · Back to the Bricks target, derived from $350M EBITDA", 5.0, "≈5%", "cy"),
            ("2025 · HDMC operating margin, delivered", -0.8, "(0.8%)", "mg"),
        ], cap="HDMC operating margin · the new target sits below the year the old plan set out to fix")),
        "s4-9": ("end", F.timeline([
            (pos(D(2026, 5, 5), D(2026, 1, 1), D(2028, 1, 1)), "5 May 2026", "Back to the Bricks announced", "ink"),
            (pos(D(2026, 9, 30), D(2026, 1, 1), D(2028, 1, 1)), "Q3 2026", "10-Q: financing “during the third quarter”", "ink"),
            (pos(D(2027, 5, 15), D(2026, 1, 1), D(2028, 1, 1)), "May 2027", "LiveWire cash reaches zero at the H1 burn", "mg"),
            (pos(D(2027, 12, 15), D(2026, 1, 1), D(2028, 1, 1)), "Dec 2027", "$75M note due to Harley; FY2027 is the EBITDA target year", "mg"),
        ], start="2026", end="2028", cap="The decision has a date. Three of them.")),
        "s4-10": ("end", F.bricks(["Competitive advantages and legacy", "The exclusive dealer network", "Share where H-D has a right to win",
                                   "Strong financial position", "Bolstered management team"],
                                  under=("LIVEWIRE", "not in the wall · $(70–80)M"),
                                  cap="Scored on the motor company · the subsidiary sits under the footing")),
    },
    "03": {
        # Part 1 · The Record
        "s1-2": ("end", F.chain([
            ("Hero MotoCorp", "Neemrana, Rajasthan"),
            ("440cc single", "the X440's engine, ₹2.29 lakh / $2,760 bike"),
            ("The Sprint", "Harley badge, “existing platforms”"),
            ("The dealer floor", "the space below the big twin"),
        ], cap="The first new motorcycle under the plan, and where its engine comes from")),
        "s1-5": ("end", F.chips(
            ("Carried its own brand", "sold or shut, every one", "mg", ["Aermacchi", "Holiday Rambler", "Buell", "MV Agusta"]),
            ("Carried no badge into a Harley segment", "kept, every one", "cy", ["Eaglemark", "StaCyc", "Hero's engine", "Qianjiang's twin", "KYMCO's line", "KKR's capital"]),
            cap="Sixteen moves, sorted by the one thing that decided them")),
        "s1-9": ("end", F.threshold("full brand · full price", [
            ("Milwaukee-Eight", "built", "cy"), ("Rev Max", "built", "cy"),
        ], [
            ("440 single", "Hero", "mg"), ("Balance bike", "StaCyc", "mg"), ("Battery", "Alta, then own lab", "mg"), ("Loan book", "Eaglemark, sold on", "mg"),
        ], cap="What Harley builds, and what it buys")),
        "s1-10": ("top", F.route([(1, "The Record"), (2, "Same Sentence"), (3, "Too Small to Say"), (4, "The Sprint")], 1)),
        # Part 2 · Same Sentence
        "s2-2": ("end", F.timeline([
            (pos(D(1993, 6, 1), D(1993, 1, 1), D(2010, 1, 1)), "1993", "49% stake, about $500K", "cy"),
            (pos(D(2008, 6, 1), D(1993, 1, 1), D(2010, 1, 1)), "2008", "13,119 shipped · $123.1M revenue", "ink"),
            (pos(D(2009, 10, 15), D(1993, 1, 1), D(2010, 1, 1)), "15 Oct 2009", "Shut · ~$125M exit cost · ~180 jobs", "mg"),
        ], start="1993", end="2010", cap="Buell, sixteen years · the exit cost 250 times the entry")),
        "s2-3": ("end", F.span("Keith Wandell's first year as CEO · 1 May 2009 to 30 Apr 2010", [
            (0.0, pos(D(2009, 10, 15), D(2009, 5, 1), D(2010, 4, 30)), "cy", "five months"),
        ], [
            (0.0, "1 May 2009 · takes the job", "inkline"),
            (pos(D(2009, 10, 15), D(2009, 5, 1), D(2010, 4, 30)), "15 Oct 2009 · Buell shut", "mgline"),
        ], note="MV Agusta followed on 6 August 2010, fifteen months in")),
        "s2-6": ("end", F.hbars([
            ("The receivable Harley had lent MV Agusta", 103.8, "€103.8M", "cy"),
            ("Cash left inside, in escrow", 20.0, "€20.0M", "cy"),
            ("Price for the shares, the LLC and the receivable", 0.000003, "€1 + $1 + €1", "mg"),
        ], cap="The sale, 6 Aug 2010 · € millions · “nominal consideration”, itemised")),
        "s2-8": ("end", F.stamps([
            ("1996", "“the core motorcycle business” · Holiday Rambler sold", "cy"),
            ("2009", "“investment on the Harley-Davidson brand” · Buell shut", "mg"),
            ("2010", "“investment on the Harley-Davidson brand” · MV Agusta sold", "mg"),
        ], cap="The same sentence, three exits")),
        "s2-9": ("end", F.hbars([
            ("Paid for MV Agusta · 2008", 105.1, "$105.1M", "cy"),
            ("Lost on MV Agusta · 24 months", 268.4, "$268.4M", "mg"),
            ("Received on the way out · 2010", 0.000001, "€1", "mg"),
        ], cap="$ millions · 2.55 times the purchase price, and the factory back to the family it came from")),
        "s2-10": ("top", F.route([(1, "The Record"), (2, "Same Sentence"), (3, "Too Small to Say"), (4, "The Sprint")], 2)),
        # Part 3 · Too Small to Say
        "s3-2": ("end", F.doc("Harley-Davidson, Inc. · 8-K Ex. 99.1 · Q1 2018 results · 24 Apr 2018", [
            "First quarter highlights", "", "", "Invested in a collaborative agreement with Alta Motors", "", "", "",
        ], 3, cap="The only Harley-Davidson SEC filing that has ever contained the word “Alta” · one sentence, no number")),
        "s3-5": ("end", F.span("2018 · Harley and Alta, on the calendar", [
            (pos(D(2018, 3, 1), D(2018, 1, 1), D(2019, 1, 1)), pos(D(2018, 8, 29), D(2018, 1, 1), D(2019, 1, 1)), "cy", "six months"),
        ], [
            (pos(D(2018, 2, 2), D(2018, 1, 1), D(2019, 1, 1)), "2 Feb · Alta's round closes, $20.8M", "inkline"),
            (pos(D(2018, 3, 1), D(2018, 1, 1), D(2019, 1, 1)), "1 Mar · Harley in", "cyline"),
            (pos(D(2018, 8, 29), D(2018, 1, 1), D(2019, 1, 1)), "29 Aug · Harley out, sourced", "mgline"),
            (pos(D(2018, 10, 17), D(2018, 1, 1), D(2019, 1, 1)), "17 Oct · Alta ceases operations", "inkline"),
        ], note="5 Sep: Harley announces its own EV lab, a week after the split leaked")),
        "s3-6": ("end", F.hbars([
            ("Alta's round, closed 2 Feb 2018", 20.84, "$20.84M", "cy"),
            ("Growth in the round after July 2017 · where Harley's check sits, if it is there", 5.65, "≤ $5.65M", "mg"),
            ("What Harley disclosed", 0.0, "$0", "mg"),
        ], cap="$ millions · Form D, Faster Faster, Inc. · the check is bounded, never stated")),
        "s3-11": ("top", F.route([(1, "The Record"), (2, "Same Sentence"), (3, "Too Small to Say"), (4, "The Sprint")], 3)),
        # Part 4 · The Sprint and the Final Word
        "s4-3": ("end", F.chain([
            ("Street 500/750", "own platform, 2013"),
            ("Bawal, India", "own plant, opened 2011"),
            ("Lost money", "plant closed Sep 2020"),
            ("Hero licence", "Oct 2020 · the 440 for ₹2.29 lakh"),
        ], cap="The one time Harley built its own small bike in its own plants", cls="mg")),
        "s4-6": ("end", F.fork("Where does the Sprint ship from?", [
            ("Neemrana, Rajasthan", "The rule held. An “existing platform” that belongs to a licensee.", "cy"),
            ("York, Pennsylvania", "Not a $6,000 motorcycle at a York cost base. The Street's history says what comes next.", "mg"),
        ], cap="Plant and price, both undecided · both are the test")),
        "s4-9": ("end", F.hbars([
            ("StaCyc balance bikes · 2025", 21633, "21,633", "cy"),
            ("LiveWire motorcycles · 2025", 653, "653", "mg"),
        ], cap="Units · 33 to 1 · the two pieces with a future were never electric motorcycles")),
        "s4-10": ("end", F.hub(("THE DEALER", "FLOOR"), [
            ("Milwaukee-Eight", "built, $25,000 bikes", "cy"),
            ("StaCyc", "bought 2019, kept", "cy"),
            ("Hero 440 single", "licensed 2020", "cy"),
            ("KYMCO line", "contracted 2026", "cy"),
            ("Buell", "shut 2009", "mg"),
            ("MV Agusta", "sold 2010", "mg"),
            ("Alta", "dropped 2018", "mg"),
            ("LiveWire", "2027?", "mg"),
        ], cap="Kept when it feeds the dealer · dropped when it competes with the badge")),
        "s4-11": ("end", F.chips(
            ("Fills the floor", "kept", "cy", ["StaCyc", "Hero's engine", "KYMCO's line", "Eaglemark"]),
            ("Competes with the badge", "sold or shut", "mg", ["Buell", "MV Agusta", "Aermacchi", "Alta"]),
            centre=("THE SPRINT", "?"),
            cap="Which of those is the Sprint?")),
    },
}


def q(s):
    return r"[\"']" + s + r"[\"']"


def main(n):
    p = ROOT / "site" / "groundtruth" / n / "series" / "index.html"
    s = p.read_text()
    s = re.sub(r"\n?/\* figs\.py \*/.*?/\* /figs\.py \*/", "", s, count=1, flags=re.S)
    s = s.replace("</style>", F.FIG_CSS + "\n</style>", 1)
    s = re.sub(r'\s*<div class="fig [^"]*"><svg .*?</svg>(?:<div class="c cap-line">[^<]*</div>)?</div>', "", s, flags=re.S)
    n_set = 0
    for sid, (where, fig) in FIGS.get(n, {}).items():
        m = re.search(r"<div class=([\"'])(slide[^\"']*)\1 id=%s>(.*?)(?=\n\s*<div class=[\"']slide|\n</div>\n<script)" % q(sid), s, re.S)
        if not m:
            print(n, sid, "not found")
            continue
        blk = m.group(0)
        if where == "top":
            hdr = re.search(r"<div class=%s>.*?<div class=%s>.*?</div>\s*</div>" % (q("tophdr"), q("tag")), blk, re.S)
            at = hdr.end()
            blk = blk[:at] + "\n  " + fig + blk[at:]
        else:
            foot = blk.rfind('<div class="foot">')
            if foot < 0:
                foot = blk.rfind("<div class='foot'>")
            blk = blk[:foot] + fig + "\n  " + blk[foot:]
        s = s[:m.start()] + blk + s[m.end():]
        n_set += 1
    p.write_text(s)
    print(n, "series:", n_set, "figure(s) drawn")


if __name__ == "__main__":
    main(sys.argv[1])
