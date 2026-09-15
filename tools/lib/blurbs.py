"""One line under each picture. Keyed by file name; applied after the images are placed, so a
picture carries the same line wherever it appears. Product photos included.

  from blurbs import apply; html = apply(html)
"""
import base64, hashlib, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

BLURBS = {
    # No. 01
    "gt01-01-juneau.jpg": "Juneau Avenue. The parent, the landlord, the supplier and, since November 2025, the secured lender.",
    "gt01-02-form.jpg": "The financing the 10-Q says is being pursued this quarter. This box gets the clip the day it lands.",
    "gt01-03-floor.jpg": "A $15,499 roadster and a $4,999 minimoto on the same floor. Nobody has published this photo yet.",
    "gt01-04-tape.jpg": "LVWR under a dollar and over three within a week. The float is 22%; Harley owns the rest.",
    "gt01-05-team.jpg": "The people who cut cost per motorcycle 47% in two years while launching two platforms. They did the work.",
    "gt01-06-stacyc.jpg": "A $799 balance bike. Harley hopes the kid becomes a rider some day; the parent is the customer today.",
    "gt01-07-floor2019.jpg": "2019. The $29,799 bike the 100,000-unit plan was sold on, hemmed in by the big twins that pay the rent.",
    "gt01-08-stripped.jpg": "Cast frame, battery case, motor. Every one built for LiveWire is bought from Harley at cost plus a mark-up.",
    "gt01-09-redshift.jpg": "Alta Motors, Brisbane, California. Harley took a stake in March 2018; Alta was gone by October.",
    "gt01-10-bench.jpg": "The precedent: a small electric company that built real motorcycles and ran out of money anyway.",
    "gt01-11-kymco.jpg": "KYMCO, Taiwan. The second contract, signed the same day as the first. Minimum volumes from 2027.",
    "gt01-12-honcho-grass.jpg": "The S4 Honcho. The volume bike, priced $1,400 above the bike that already owns the segment.",
    "gt01-13-honcho-stand.jpg": "Honcho on the stand. The reveal was the easy part.",
    "gt01-14-groms.jpg": "Two Groms, downtown, $3,599 each. This is the customer the Honcho has to win.",
    "gt01-15-dust.jpg": "Dust. Real bike, real riders, small category. Bought in May 2026 for up to $14.75M.",
    "gt01-16-parts.jpg": "Bikes on a bench waiting on parts Harley already bought to build motorcycles LiveWire did not take.",
    "gt01-17-chair.jpg": "Same building, different chair. Harley did not leave; it moved from owner to creditor.",
    "gt01-18-line.jpg": "Small electric frames on a contract line. Product built here carries a take-or-pay minimum.",
    "gt01-19-quarter.jpg": "267 motorcycles in a quarter. A strong Harley dealer sells that many in a month.",
    "gt01-20-crates.jpg": "Take-or-pay. Miss the minimum and the deficit fee is owed on motorcycles that were never built.",
    "gt01-21-loan.jpg": "The loan that settled it, eight months before the quarter everyone is arguing about.",
    "gt01-22-lien.jpg": "Built it, badged it, sold it, lent against it. A lien on substantially all of LiveWire's assets.",
    "gt01-23-grom-kerb.jpg": "The category leader, and very nearly the category. About 10,000 a year, by my estimate.",
    "gt01-24-denominator.jpg": "Three bikes on an empty floor. 386% growth is measured against 55 motorcycles.",
    "gt01-one.jpg": "LiveWire ONE. $29,799 in 2019 as a Harley-Davidson, $21,999 in 2021 as a LiveWire, $16,499 today.",
    # No. 02
    "gt02-01-juneau.jpg": "Juneau Avenue, reopened for return-to-office in March 2026. Every decision in this brief was signed here.",
    "gt02-02-hdfs-desk.jpg": "The finance desk. Two-thirds of the loans written here for the next five years are already sold.",
    "gt02-03-delmar-floor.jpg": "One electric on a Harley floor. The dealer did not ask for it and does not get paid much to sell it.",
    "gt02-04-keynote.jpg": "5 May 2026. Five pillars, six targets, no subsidiary.",
    "gt02-05-883.jpg": "The 883. Discontinued in 2022 because it did not make money; back in 2027 as the plan's one volume lever.",
    "gt02-06-bricks.jpg": "The bricks. The plan is named after the building.",
    "gt02-07-dealer-closed.jpg": "Half the motorcycles of 2014, three-quarters of the dealers. The other quarter looked like this.",
    "gt02-08-loan-files.jpg": "About $6 billion of receivables, sold. $180 million a year of earnings went out with the boxes.",
    "gt02-09-handshake.jpg": "February 2024, a convertible loan. November 2025, a secured one. Same counterparty, different seat.",
    "gt02-10-clock.jpg": "Cash runs out around May 2027. The note is due in December. The plan is scored on 2027.",
    "gt02-11-banner.jpg": "Hardwire promised 15% by 2025 and delivered 0.8%. The banners are still up.",
    "gt02-12-investor-room.jpg": "$1.63 billion of buybacks at an average of $31, for a stock at $28.",
    "gt02-13-york-line.jpg": "York, 2027, if every target lands: 143,000 motorcycles, two-thirds of 2019.",
    "gt02-14-call.jpg": "The call that replaced the five-year strategy. Fourteen words on LiveWire.",
    # No. 03
    "gt03-01-varese.jpg": "Varese, 1961. The first Sprint was an Aermacchi. Harley bought half the company and sold it back in 1978.",
    "gt03-02-easttroy.jpg": "East Troy, October 2009. The last Buell. Production ended at the end of the month, employment on December 18.",
    "gt03-03-redshift-floor.jpg": "Brisbane, 2018. An Alta on a Harley floor, one of 44 dealers that carried it. Six months later the building was empty.",
    "gt03-04-bawal.jpg": "Bawal, Haryana. Harley's own Indian plant, opened 2011, closed September 2020. Hero signed one month later.",
    "neemrana.jpg": "Neemrana, Rajasthan. Hero's line, Hero's engine, Harley's badge. The Sprint's powertrain starts here.",
    "gt03-06-juneau-dusk.jpg": "Juneau Avenue at dusk. The building has room for one brand.",
    "gt03-07-museum.jpg": "Sixteen outside moves in sixty-six years. Every brand Harley bought is in a museum or a footnote.",
    "gt03-08-mv.jpg": "MV Agusta. $105 million in, $268 million out, sold back to the seller for a euro.",
    "gt03-09-stacyc-race.jpg": "Twenty-one thousand StaCycs a year. Harley hopes they become riders some day.",
    "gt03-10-engine.jpg": "The Milwaukee-Eight. Built in-house, kept, and still paying for everything else.",
    "gt03-11-x440.jpg": "Hero's X440, about $2,760 in India. The Sprint's engine, and the test of the rule.",
    "gt03-12-883.jpg": "The other half of the test. If the 883 makes money at $10,000 in York, it is the first small Harley that ever has.",
    "gt03-13-frames.jpg": "Each CEO's purchases are the next CEO's focus story. Same sentence, three times.",
    # product photos
    "one.jpg": "LiveWire ONE. $29,799 in 2019, $21,999 in 2021, $16,499 today. Same motorcycle.",
    "s2.jpg": "S2 Del Mar. $15,499, built by Harley-Davidson at cost plus a mark-up. The bike behind the 386%.",
    "honcho.jpg": "S4 Honcho. $4,999, built by KYMCO under a take-or-pay contract. The volume bike.",
    "lineup.jpg": "The lineup, $799 to $16,499. One segment in it makes money, and it is the one without a motor.",
    "stacyc.jpg": "StaCyc. Bought for $14.9 million in 2019. Outsells LiveWire motorcycles thirty-three to one.",
}

CSS = """
/* blurbs.py */
.blurb{font-family:var(--f-mono,var(--mono));font-size:11.5px;letter-spacing:.02em;line-height:1.45;color:var(--ink-3,var(--ink3));padding:8px 2px 0;max-width:none}
.dk .blurb{color:var(--dink3,#9AA0A6)}
.band .blurb{padding:8px 12px 9px;border-top:1px solid var(--rule)}
.dk .band .blurb{border-color:var(--drule)}
.band:has(> .blurb) > .c,.cell:has(> .blurb) > .c{position:static;background:none;color:var(--ink,#15171A);padding:8px 12px 0}
.dk .band:has(> .blurb) > .c,.dk .cell:has(> .blurb) > .c{color:#E7E9EB}
.cell.white:has(> .blurb) > .c{color:#4A4E54;border-top:1px solid #E3E0D8}
.cell.white .blurb{color:#4A4E54;border-color:#E3E0D8}
.part-img:has(> .blurb) > .c{position:static;background:none;color:var(--ink);padding:8px 12px 0}
.part-img .blurb{border-top:0;padding-top:4px}
.gt-fig .blurb,.part-img .blurb{background:var(--ground-2,#fff)}
/* /blurbs.py */"""


def _keys():
    m = {}
    for f in list((ROOT / "tools").glob("gt0*/img/*.jpg")) + list((ROOT / "tools" / "lib" / "products").glob("*.jpg")):
        b = base64.b64encode(f.read_bytes()).decode()
        m[hashlib.md5(b[:20000].encode()).hexdigest()[:8]] = f.name
    return m


def apply(html):
    """Under every band, cell or part-img whose picture has a blurb, add the line (idempotent)."""
    keys = _keys()
    html = re.sub(r"\n?/\* blurbs\.py \*/.*?/\* /blurbs\.py \*/", "", html, count=1, flags=re.S)
    html = html.replace("</style>", CSS + "\n</style>", 1)
    html = re.sub(r'\s*<div class="blurb">[^<]*</div>', "", html)
    n = 0

    def box(m):
        nonlocal n
        blk = m.group(0)
        im = re.search(r'<img[^>]*?src=["\']data:image/\w+;base64,([^"\']+)', blk)
        if not im:
            return blk
        name = keys.get(hashlib.md5(im.group(1)[:20000].encode()).hexdigest()[:8])
        if not name or name not in BLURBS:
            return blk
        n += 1
        return blk[:-6] + f'<div class="blurb">{BLURBS[name]}</div></div>'

    # a box is a .cell, or a .band / .part-img that holds one img and an optional .c, closed by </div>
    html = re.sub(r'<div class=["\'](?:cell|cell white)["\']>\s*<img[^>]*>(?:\s*<div class=["\']c["\']>.*?</div>)?\s*</div>', box, html, flags=re.S)
    html = re.sub(r'<div class=["\'](?:band|part-img)(?![^"\']*duo)[^"\']*["\'][^>]*>\s*<img[^>]*>(?:\s*<div class=["\']c["\']>.*?</div>)?\s*</div>', box, html, flags=re.S)
    return html, n
