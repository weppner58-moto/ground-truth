#!/usr/bin/env python3
"""
Contact Patch Advisory — static site build.

  python3 build.py

Reads:  site.tpl.html (home page), site/css/site.css, posts/*.py
Writes: site/index.html, site/news/index.html, site/news/<slug>/index.html,
        site/sitemap.xml, site/feed.xml, and the single-file contact-patch.html
"""
import base64, glob, html, importlib.util, json, os, re

SITE = "https://contactpatchadvisory.com"
OUT  = "site"
IMGS = {'__IMG_HERO__':'img/hero.jpg', '__IMG_SX__':'img/band-sx.jpg',
        '__IMG_NIGHT__':'img/band-night.jpg', '__IMG_PORTRAIT__':'img/portrait.jpg'}

# ---------------------------------------------------------------- posts
def load_posts():
    posts = []
    for f in sorted(glob.glob("posts/*.py")):
        spec = importlib.util.spec_from_file_location("p", f)
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        posts.append(mod.POST)
    return sorted(posts, key=lambda p: p["date"], reverse=True)

# ---------------------------------------------------------------- chrome
def topbar(prefix, active):
    def a(href, label, key):
        cls = ' class="now"' if key == active else ''
        return f'<a href="{href}"{cls}>{label}</a>'
    return f'''<header class="topbar">
  <div class="wrap">
    <a class="mark" href="{prefix}index.html">Contact Patch<span>&nbsp;/</span>&nbsp;Advisory</a>
    <nav class="navbtns">
      {a(prefix+"index.html#who","Who","who")}
      {a(prefix+"index.html#services","Services","services")}
      {a(prefix+"index.html#experience","Experience","experience")}
      {a(prefix+"news/index.html" if prefix=="" else "../index.html","News","news")}
      {a(prefix+"groundtruth/","Ground Truth","groundtruth")}
      {a(prefix+"index.html#contact","Contact","contact")}
    </nav>
  </div>
</header>'''

FOOTER = '''<footer class="footer">
  <div class="wrap">
    <p>
      Contact Patch Advisory &mdash; William Weppner. Nothing on this page is legal advice or an
      opinion on any matter. An inquiry does not create an expert engagement or any duty of
      confidentiality until a conflict check is completed and an engagement letter is executed.
      <br><br><span class="credit">Photography by Anthony.</span>
    </p>
    <p class="reg mono" aria-hidden="true">
      <i style="background:var(--cyan)"></i><i style="background:var(--magenta)"></i><i style="background:var(--ink-3)"></i>
      Reg. 2026
    </p>
  </div>
</footer>'''

def page(title, desc, canonical, css_href, body, head_extra=""):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<link rel="canonical" href="{canonical}">
<meta name="description" content="{desc}">
<meta name="author" content="William Weppner">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<link rel="alternate" type="application/rss+xml" title="Contact Patch Advisory" href="{SITE}/feed.xml">
{head_extra}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&family=Public+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap">
<link rel="stylesheet" href="{css_href}">
</head>
<body>
{body}
</body>
</html>
'''

def og(title, desc, url, img=f"{SITE}/img/og.jpg", typ="website"):
    return f'''<meta property="og:type" content="{typ}">
<meta property="og:site_name" content="Contact Patch Advisory">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{img}">'''

# ---------------------------------------------------------------- css
def build_css():
    """Stylesheet is generated from the template so image paths resolve.
    Missing this substitution silently blanks the hero and both photo bands."""
    tpl = open("site.tpl.html").read()
    css = tpl.split("<style>", 1)[1].split("</style>")[0].strip()
    css += "\n" + open("css-extra.css").read()
    for k, v in IMGS.items():
        css = css.replace(k, "../" + v)          # stylesheet lives in /css/
    os.makedirs(f"{OUT}/css", exist_ok=True)
    open(f"{OUT}/css/site.css", "w").write(css)
    assert "__IMG_" not in css, "unsubstituted image placeholder in stylesheet"

# ---------------------------------------------------------------- home
def build_home(posts):
    tpl = open("site.tpl.html").read()
    head, rest = tpl.split("<style>", 1)
    _css, body = rest.split("</style>", 1)
    body = body.strip()

    # swap in the shared topbar (adds the News button)
    body = re.sub(r"<header class=\"topbar\">.*?</header>", topbar("", None), body, flags=re.S)

    # latest-news strip before the contact section
    if posts:
        p = posts[0]
        strip = f'''  <section id="news-teaser">
    <div class="wrap">
      <div class="exh mono"><b>04</b> <span>News &amp; Analysis</span> <i></i></div>
      <h2 class="disp">Latest.</h2>
      <div class="post-list">
        <div class="post-item">
          <div><div class="post-date">{p["datehuman"]}</div><span class="post-tag">{p["tag"]}</span></div>
          <div>
            <h3><a href="news/{p["slug"]}/">{p["title"]}</a></h3>
            <p>{p["standfirst"]}</p>
            <a class="readmore" href="news/{p["slug"]}/">Read &rarr;</a>
          </div>
        </div>
      </div>
      <div class="btn-row"><a class="btn" href="news/">All news &amp; analysis <span class="ar">&rarr;</span></a></div>
    </div>
  </section>

'''
        body = body.replace('  <!-- ============ SECTION 5 — CONTACT', strip + '  <!-- ============ SECTION 5 — CONTACT')
        if strip not in body:  # anchor differs, fall back to the contact section tag
            body = body.replace('  <section id="contact"', strip + '  <section id="contact"', 1)
        # renumber contact so exhibits stay sequential
        body = body.replace('<b>04</b> <span>Contact</span>', '<b>05</b> <span>Contact</span>')

    body = re.sub(r"<footer class=\"footer\">.*?</footer>", FOOTER, body, flags=re.S)
    for k, v in IMGS.items():
        body = body.replace(k, v)

    # keep the structured-data + og block already authored in the template head
    extra = head.split("<link rel=\"preconnect\"")[0]
    extra = extra.split("</title>",1)[1] if "</title>" in extra else extra
    extra = extra.replace('<link rel="canonical" href="https://contactpatchadvisory.com/">','')
    extra = re.sub(r'<meta name="description"[^>]*>','',extra)
    extra = re.sub(r'<meta name="author"[^>]*>','',extra)
    extra = re.sub(r'<meta name="robots"[^>]*>','',extra)

    title = "Motorcycle &amp; Powersports Expert Witness | William Weppner &mdash; Contact Patch Advisory"
    desc  = ("William Weppner — motorcycle, ATV/UTV, and e-bike expert witness for product liability and "
             "mechanical failure analysis. Twenty years of OEM product development at Harley-Davidson, "
             "Honda, and Super73. Retained by plaintiff and defense counsel. California, Nevada, Utah.")
    open(f"{OUT}/index.html","w").write(page(title, desc, f"{SITE}/", "css/site.css", body, extra.strip()))

    # single-file build for sharing offline
    sf = tpl
    for k, v in IMGS.items():
        sf = sf.replace(k, "data:image/jpeg;base64," + base64.b64encode(open(f"{OUT}/{v}","rb").read()).decode())
    open("contact-patch.html","w").write(sf)

# ---------------------------------------------------------------- news
def build_news(posts):
    items = ""
    for p in posts:
        items += f'''        <div class="post-item">
          <div><div class="post-date">{p["datehuman"]}</div><span class="post-tag">{p["tag"]}</span></div>
          <div>
            <h3><a href="{p["slug"]}/">{p["title"]}</a></h3>
            <p>{p["standfirst"]}</p>
            <a class="readmore" href="{p["slug"]}/">Read &rarr;</a>
          </div>
        </div>
'''
    body = f'''{topbar("../", "news")}
<main>
  <section>
    <div class="wrap">
      <div class="exh mono"><b>News</b> <span>&amp; Analysis</span> <i></i></div>
      <h2 class="disp">What's moving,<br>and what it means.</h2>
      <p class="lede">Regulation, litigation, and electric two&#8209;wheel product analysis &mdash;
         written from inside the product organization rather than from the outside looking in.</p>
      <div class="post-list">
{items}      </div>
      <div class="btn-row">
        <a class="btn" href="../index.html#contact">Discuss an engagement <span class="ar">&rarr;</span></a>
      </div>
    </div>
  </section>
</main>
{FOOTER}'''
    os.makedirs(f"{OUT}/news", exist_ok=True)
    open(f"{OUT}/news/index.html","w").write(page(
        "News &amp; Analysis | Contact Patch Advisory",
        "Powersports regulation, product liability, and electric motorcycle analysis from William Weppner.",
        f"{SITE}/news/", "../css/site.css", body,
        og("News &amp; Analysis | Contact Patch Advisory",
           "Powersports regulation, product liability, and electric motorcycle analysis.",
           f"{SITE}/news/")))

def build_post(p):
    srcs = "".join(f'<li><a href="{u}" rel="nofollow noopener" target="_blank">{html.escape(t)}</a></li>\n'
                   for t, u in p["sources"])
    ld_obj = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": p["title"],
        "description": p["summary"],
        "datePublished": p["date"],
        "dateModified": p["date"],
        "author": {"@type": "Person", "name": "William Weppner", "url": f"{SITE}/"},
        "publisher": {"@type": "Organization", "name": "Contact Patch Advisory", "url": f"{SITE}/"},
        "mainEntityOfPage": f"{SITE}/news/{p['slug']}/",
        "image": f"{SITE}/img/og.jpg",
        "articleSection": p["tag"],
    }
    ld = ('<script type="application/ld+json">\n'
          + json.dumps(ld_obj, indent=2, ensure_ascii=False)
          + '\n</script>')

    body = f'''{topbar("../../", "news")}
<main>
  <article class="article">
    <div class="wrap">
      <div class="article-head">
        <div class="article-meta mono">
          <b>{p["tag"]}</b> <span>{p["datehuman"]}</span> <span>William Weppner</span>
        </div>
        <h1>{p["title"]}</h1>
        <p class="standfirst">{p["standfirst"]}</p>
      </div>

      <div class="article-body">
{p["body"].strip()}

        <div class="srcs">
          <span class="k">Sources</span>
          <ul>
{srcs}          </ul>
        </div>

        <p class="disclaim">
          Technical and product&#8209;development commentary. Not legal advice, and not an opinion on
          any matter. Regulatory status changes; verify the current docket before relying on any
          date or requirement described here.
        </p>
      </div>

      <div class="article-foot">
        <div class="btn-row" style="margin-top:0">
          <a class="btn btn-solid" href="../../index.html#contact">Discuss an engagement <span class="ar">&rarr;</span></a>
          <a class="btn" href="../">All news <span class="ar">&rarr;</span></a>
        </div>
      </div>
    </div>
  </article>
</main>
{FOOTER}'''
    d = f"{OUT}/news/{p['slug']}"
    os.makedirs(d, exist_ok=True)
    open(f"{d}/index.html","w").write(page(
        f'{p["title"]} | Contact Patch Advisory', html.escape(p["summary"], quote=True),
        f"{SITE}/news/{p['slug']}/", "../../css/site.css", body,
        og(html.escape(p["title"], quote=True), html.escape(p["summary"], quote=True),
           f"{SITE}/news/{p['slug']}/", typ="article") + "\n" + ld))

# ---------------------------------------------------------------- feeds
def build_feeds(posts):
    urls = [(f"{SITE}/", "1.0", "monthly"), (f"{SITE}/news/", "0.8", "weekly")]
    urls += [(f"{SITE}/news/{p['slug']}/", "0.7", "yearly") for p in posts]
    # Ground Truth: the series index plus every issue that exists on disk
    urls.append((f"{SITE}/groundtruth/", "0.9", "monthly"))
    for n in sorted(d for d in os.listdir(f"{OUT}/groundtruth") if re.fullmatch(r"\d\d", d)):
        urls.append((f"{SITE}/groundtruth/{n}/", "0.8", "monthly"))
        urls.append((f"{SITE}/groundtruth/{n}/series/", "0.6", "monthly"))
    last = posts[0]["date"] if posts else "2026-08-27"
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u, pr, cf in urls:
        sm += f"  <url><loc>{u}</loc><lastmod>{last}</lastmod><changefreq>{cf}</changefreq><priority>{pr}</priority></url>\n"
    sm += "</urlset>\n"
    open(f"{OUT}/sitemap.xml","w").write(sm)

    items = ""
    for p in posts:
        items += f'''    <item>
      <title>{html.escape(p["title"])}</title>
      <link>{SITE}/news/{p["slug"]}/</link>
      <guid isPermaLink="true">{SITE}/news/{p["slug"]}/</guid>
      <description>{html.escape(p["summary"])}</description>
      <pubDate>{p["datehuman"]}</pubDate>
      <category>{p["tag"]}</category>
    </item>
'''
    open(f"{OUT}/feed.xml","w").write(f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
  <title>Contact Patch Advisory — News &amp; Analysis</title>
  <link>{SITE}/news/</link>
  <description>Powersports regulation, product liability, and electric motorcycle analysis from William Weppner.</description>
  <language>en-us</language>
{items}</channel></rss>
''')
    open(f"{OUT}/robots.txt","w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")

# ---------------------------------------------------------------- run
if __name__ == "__main__":
    posts = load_posts()
    build_css()
    build_home(posts)
    build_news(posts)
    for p in posts:
        build_post(p)
    build_feeds(posts)
    print(f"built {len(posts)} post(s)")
    for root, dirs, files in os.walk(OUT):
        dirs[:] = [d for d in dirs if d != "groundtruth"]   # the series builds separately (tools/)
        for f in sorted(files):
            fp = os.path.join(root, f)
            print(f"  {fp:<58} {os.path.getsize(fp):>8,} B")
