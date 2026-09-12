"""Site navigation shared by every Ground Truth page: the practice-site links in the sticky top bar,
and a slim bar pinned to the bottom of the viewport. Absolute paths, so it works from any depth."""

LINKS = [("/", "Home"), ("/#who", "Who"), ("/#services", "Services"), ("/news/", "News"),
         ("/groundtruth/", "Ground Truth"), ("/#contact", "Contact")]

def _links(active):
    out = []
    for h, t in LINKS:
        cls = ' class="now"' if t == active else ""
        out.append('<a href="%s"%s>%s</a>' % (h, cls, t))
    return "".join(out)

def nav_html(active="Ground Truth"):
    return '<nav class="sitenav">%s</nav>' % _links(active)

def bottombar_html(left="Contact Patch Advisory", active="Ground Truth"):
    return '<div class="bottombar"><div class="wrap"><span class="bb-mark">%s</span><nav>%s</nav></div></div>' % (left, _links(active))

NAV_CSS = """
/* site navigation in the sticky top bar, and the bar pinned to the bottom */
.sitenav{display:flex;gap:6px;flex-wrap:wrap;margin-left:auto}
.sitenav a{font-family:var(--f-mono,var(--mono));font-size:10px;letter-spacing:.13em;text-transform:uppercase;padding:7px 10px;border:1px solid var(--rule);color:var(--ink-2,var(--ink2));text-decoration:none;white-space:nowrap}
.sitenav a:hover{border-color:var(--cyan);color:var(--cyan);text-decoration:none}
.sitenav a.now{border-color:var(--tape,var(--ink));background:var(--tape,var(--ink));color:var(--tape-ink,var(--ground,var(--paper)))}
.topbar{position:sticky;top:0;z-index:20;background:var(--ground,var(--paper))}
.topbar .stamp{margin-left:0}
@media (max-width:720px){.sitenav{width:100%;order:3}.sitenav a{flex:1;text-align:center;padding:7px 4px}.topbar .stamp{display:none}}
body{padding-bottom:44px}
.bottombar{position:fixed;left:0;right:0;bottom:0;z-index:50;background:var(--ground,var(--paper));border-top:1px solid var(--rule)}
.bottombar .wrap{display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:42px;padding-block:5px}
.bottombar .bb-mark{font-family:var(--f-mono,var(--mono));font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3,var(--ink3));white-space:nowrap}
.bottombar nav{display:flex;gap:4px;flex-wrap:nowrap;overflow-x:auto}
.bottombar nav a{font-family:var(--f-mono,var(--mono));font-size:10px;letter-spacing:.12em;text-transform:uppercase;padding:6px 9px;color:var(--ink-2,var(--ink2));text-decoration:none;white-space:nowrap;border:1px solid transparent}
.bottombar nav a:hover{color:var(--cyan);text-decoration:none}
.bottombar nav a.now{color:var(--magenta,var(--mag))}
@media (max-width:560px){.bottombar .bb-mark{display:none}.bottombar nav{width:100%;justify-content:space-between}}
@media print{.bottombar,.sitenav{display:none}body{padding-bottom:0}}
"""
