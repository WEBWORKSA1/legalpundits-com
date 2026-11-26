#!/usr/bin/env python3
"""LegalPundits.com static site generator (Python 3 standard library only).

Usage:  python build.py
Writes HTML into the repository root so GitHub Pages can serve the main branch.
"""
import datetime
import hashlib
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from siteconfig import SITE, NAV, FOOTER_COLUMNS  # noqa: E402
from data import AREAS, STATES, CONTRIBUTORY_STATES, TOOLS, CHANNELS, MORE_CHANNELS, GLOBAL_DESK, FEEDS  # noqa: E402
from content.guides_a import GUIDES_A  # noqa: E402
from content.guides_b import GUIDES_B  # noqa: E402
from content.extras import GLOSSARY, QUIZ  # noqa: E402
from content import legal_pages as LP  # noqa: E402

GUIDES = GUIDES_A + GUIDES_B
AREA_BY_SLUG = {a["slug"]: a for a in AREAS}
TOOL_BY_SLUG = {t["slug"]: t for t in TOOLS}
GUIDE_BY_SLUG = {g["slug"]: g for g in GUIDES}
esc = html.escape
PAGES = []  # registry for sitemap + search index


def load_json(rel, default):
    p = ROOT / rel
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return default
    return default


NEWS = load_json("data/news.json", {"updated": "", "items": []})
VIDEOS = load_json("data/videos.json", {"updated": "", "items": []})


def asset_version():
    h = hashlib.md5()
    for rel in ("assets/css/style.css", "assets/js/app.js", "assets/js/tools.js"):
        p = ROOT / rel
        if p.exists():
            h.update(p.read_bytes())
    return h.hexdigest()[:10]


VER = asset_version()

# ---------------------------------------------------------------- helpers

def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def inline_md(text):
    text = esc(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)

    def link(m):
        label, url = m.group(1), m.group(2)
        if url.startswith("/"):
            return '<a href="%ROOT%' + url.lstrip("/") + '">' + label + "</a>"
        return '<a href="' + url + '" target="_blank" rel="noopener">' + label + "</a>"

    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, text)


def md(src):
    """Tiny markdown subset: ## h2, ### h3, - lists, 1. lists, > callout, paragraphs."""
    out, toc, buf, list_type = [], [], [], None

    def flush_para():
        if buf:
            out.append("<p>" + inline_md(" ".join(buf)) + "</p>")
            buf.clear()

    def close_list():
        nonlocal list_type
        if list_type:
            out.append("</%s>" % list_type)
            list_type = None

    for raw in src.strip().splitlines():
        line = raw.rstrip()
        if not line.strip():
            flush_para(); close_list(); continue
        if line.startswith("## "):
            flush_para(); close_list()
            t = line[3:].strip(); i = slugify(t)
            toc.append((i, t))
            out.append('<h2 id="%s">%s</h2>' % (i, inline_md(t)))
        elif line.startswith("### "):
            flush_para(); close_list()
            out.append("<h3>%s</h3>" % inline_md(line[4:].strip()))
        elif line.startswith("> "):
            flush_para(); close_list()
            out.append('<div class="callout">%s</div>' % inline_md(line[2:]))
        elif re.match(r"^- ", line):
            flush_para()
            if list_type != "ul":
                close_list(); out.append("<ul>"); list_type = "ul"
            out.append("<li>%s</li>" % inline_md(line[2:]))
        elif re.match(r"^\d+\. ", line):
            flush_para()
            if list_type != "ol":
                close_list(); out.append("<ol>"); list_type = "ol"
            out.append("<li>%s</li>" % inline_md(re.sub(r"^\d+\. ", "", line)))
        else:
            close_list(); buf.append(line.strip())
    flush_para(); close_list()
    return "\n".join(out), toc


def ad(name):
    slot = SITE["ad_slots"].get(name, "")
    if not slot:
        return ""
    return ('<div class="ad-wrap" aria-label="Advertisement"><span class="ad-label">Advertisement</span>'
            '<ins class="adsbygoogle" style="display:block" data-ad-client="%s" data-ad-slot="%s" '
            'data-ad-format="auto" data-full-width-responsive="true"></ins></div>') % (SITE["adsense_client"], slot)


LOGO_SVG = ('<svg class="logo-mark" viewBox="0 0 48 48" aria-hidden="true"><defs><linearGradient id="lpg" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#f2b53a"/><stop offset="1" stop-color="#c9821a"/></linearGradient></defs>'
            '<path d="M6 10a6 6 0 0 1 6-6h24a6 6 0 0 1 6 6v18a6 6 0 0 1-6 6H22l-9 8v-8h-1a6 6 0 0 1-6-6z" fill="url(#lpg)"/>'
            '<path d="M24 11v17M17 14h14M17 14l-4 8h8zM31 14l-4 8h8zM19 28h10" stroke="#0f1b2d" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def breadcrumbs_html(crumbs):
    if not crumbs:
        return ""
    parts = ['<a href="%ROOT%">Home</a>']
    for label, url in crumbs:
        parts.append('<a href="%ROOT%' + url + '">' + esc(label) + "</a>" if url else "<span>" + esc(label) + "</span>")
    return '<nav class="breadcrumbs" aria-label="Breadcrumb">' + ' <span aria-hidden="true">›</span> '.join(parts) + "</nav>"


def breadcrumbs_ld(crumbs, path):
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE["url"] + "/"}]
    for i, (label, url) in enumerate(crumbs, start=2):
        items.append({"@type": "ListItem", "position": i, "name": label,
                      "item": SITE["url"] + "/" + (url if url else path)})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


def header_html():
    links = "".join('<li%s><a href="%%ROOT%%%s" data-nav="%s">%s</a></li>' % (' class="nav-dup"' if u == "case-review/" else "", u, u, esc(t)) for t, u in NAV)
    return f'''<header class="site-header">
  <div class="container nav-wrap">
    <a class="brand" href="%ROOT%" aria-label="LegalPundits home">{LOGO_SVG}<span class="brand-text">Legal<span>Pundits</span></span></a>
    <nav class="main-nav" id="main-nav" aria-label="Main"><ul>{links}</ul></nav>
    <div class="header-actions">
      <button class="icon-btn" type="button" data-open-search aria-label="Search">
        <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg></button>
      <button class="icon-btn" type="button" data-theme-toggle aria-label="Toggle dark mode">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg></button>
      <a class="btn btn-gold btn-sm hide-sm" href="%ROOT%case-review/">Free Case Review</a>
      <button class="icon-btn menu-toggle" type="button" aria-controls="main-nav" aria-expanded="false" aria-label="Menu">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
    </div>
  </div>
</header>'''


def footer_html():
    cols = ""
    for title, links in FOOTER_COLUMNS:
        lis = "".join('<li><a href="%%ROOT%%%s">%s</a></li>' % (u, esc(t)) for t, u in links)
        cols += '<div><h3>%s</h3><ul>%s</ul></div>' % (esc(title), lis)
    return f'''<footer class="site-footer">
  <div class="container">
    <div class="footer-top">
      <div class="footer-brand">
        <a class="brand" href="%ROOT%">{LOGO_SVG}<span class="brand-text">Legal<span>Pundits</span></span></a>
        <p>{esc(SITE["tagline"])} Free legal guides, calculators and a free case review.</p>
        <form class="newsletter mini" data-lp-form="newsletter" novalidate>
          <label for="nl-foot" class="sr-only">Email address</label>
          <input id="nl-foot" type="email" name="Email" placeholder="Your email for the weekly legal brief" required>
          <input type="hidden" name="Form" value="Newsletter (footer)">
          <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">
          <button class="btn btn-gold btn-sm" type="submit">Subscribe</button>
          <p class="form-status" role="status"></p>
        </form>
      </div>
      <div class="footer-grid">{cols}</div>
    </div>
    <div class="footer-legal">
      <p><strong>Not a law firm. Not legal advice.</strong> LegalPundits.com provides general legal information only. Using this site or submitting a form does not create an attorney-client relationship. Attorney listings and sponsored placements are paid advertising. In some states this service may be considered a lawyer referral service. See our <a href="%ROOT%disclaimer/">Disclaimer</a>.</p>
      <p>© {SITE["year"]} LegalPundits.com · Independent publication, not affiliated with any business using a similar name. <a href="%ROOT%trademark/">Trademark &amp; Copyright Disclosure</a> · <a href="%ROOT%privacy/">Privacy</a> · <a href="%ROOT%terms/">Terms</a> · <a href="%ROOT%privacy/#cookies" data-cookie-settings>Cookie settings</a></p>
    </div>
  </div>
</footer>'''


SEARCH_OVERLAY = '''<div class="search-overlay" id="search-overlay" hidden>
  <div class="search-box" role="dialog" aria-modal="true" aria-label="Search LegalPundits">
    <div class="search-row">
      <input id="site-search" type="search" placeholder="Search guides, tools and legal terms…" autocomplete="off" aria-label="Search">
      <button class="icon-btn" type="button" data-close-search aria-label="Close search"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg></button>
    </div>
    <ul class="search-results" id="search-results"></ul>
    <p class="search-hint">Try “car accident”, “overtime”, “custody”, “deadline” or “demand letter”.</p>
  </div>
</div>'''

COOKIE = '''<div class="cookie" id="cookie" hidden>
  <p>We use cookies to run this site, remember preferences and show ads (including Google AdSense). See our <a href="%ROOT%privacy/">Privacy Policy</a>.</p>
  <div><button class="btn btn-ghost btn-sm" type="button" data-cookie="essential">Essential only</button>
  <button class="btn btn-gold btn-sm" type="button" data-cookie="all">Accept</button></div>
</div>'''


def layout(path, title, description, body, crumbs=None, jsonld=None, og_type="website", body_class="", scripts=""):
    depth = path.count("/")
    R = "../" * depth
    full_title = title if title.endswith("LegalPundits") or path == "" else title + " | LegalPundits"
    canonical = SITE["url"] + "/" + path
    lds = list(jsonld or [])
    if crumbs:
        lds.append(breadcrumbs_ld(crumbs, path))
    ld_html = "".join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in lds)
    doc = f'''<!DOCTYPE html>
<html lang="en" data-root="%ROOT%">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:site_name" content="LegalPundits">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE["url"]}/assets/img/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0f1b2d">
<meta name="google-adsense-account" content="{SITE["adsense_client"]}">
<link rel="icon" href="%ROOT%assets/img/favicon.svg" type="image/svg+xml">
<link rel="alternate" type="application/rss+xml" title="LegalPundits guides" href="%ROOT%feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="%ROOT%assets/css/style.css?v={VER}">
<script>try{{if(localStorage.getItem('lp-theme')==='dark')document.documentElement.classList.add('dark');if(localStorage.getItem('lp-cookie')==='essential'){{(window.adsbygoogle=window.adsbygoogle||[]).requestNonPersonalizedAds=1}}}}catch(e){{}}</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6620975821265271" crossorigin="anonymous"></script>
{ld_html}
</head>
<body class="{body_class}">
<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><a href="{SITE["owner_contact_url"]}" target="_blank" rel="noopener">{esc(SITE["banner_text"])}</a></div>
{header_html()}
<main id="main">
{breadcrumbs_html(crumbs) if crumbs else ""}
{body}
</main>
{footer_html()}
<div class="mobile-cta"><a class="btn btn-gold" href="%ROOT%case-review/">Free Case Review</a><a class="btn btn-ghost-light" href="%ROOT%tools/">Free Tools</a></div>
{SEARCH_OVERLAY}
{COOKIE}
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script src="%ROOT%assets/js/app.js?v={VER}" defer></script>
{scripts}
</body>
</html>'''
    doc = doc.replace("%ROOT%", R)
    out = ROOT / path / "index.html" if path else ROOT / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    return out


def register(path, title, description, kind="page", priority="0.6"):
    PAGES.append({"path": path, "title": title, "description": description, "kind": kind, "priority": priority})


def page(path, title, description, body, kind="page", priority="0.6", **kw):
    register(path, title, description, kind, priority)
    return layout(path, title, description, body, **kw)


# ---------------------------------------------------------------- shared blocks

def card(href, title, text, tag="", icon=""):
    t = '<span class="tag">%s</span>' % esc(tag) if tag else ""
    i = '<span class="card-icon" aria-hidden="true">%s</span>' % icon if icon else ""
    return f'<a class="card" href="%ROOT%{href}">{i}{t}<h3>{esc(title)}</h3><p>{esc(text)}</p><span class="card-link">Read more →</span></a>'


def tool_card(t):
    return f'<a class="card tool-card" href="%ROOT%tools/{t["slug"]}/"><span class="card-icon" aria-hidden="true">{t["icon"]}</span><h3>{esc(t["name"])}</h3><p>{esc(t["blurb"])}</p><span class="card-link">Use free tool →</span></a>'


def guide_card(g):
    a = AREA_BY_SLUG[g["area"]]
    return card("guides/%s/" % g["slug"], g["title"], g["description"], a["name"])


def cta_band(title="Not sure where you stand?", text="Tell us what happened. A free, no-obligation case review can connect you with an independent attorney who handles your type of problem.", issue=""):
    q = "?issue=" + issue if issue else ""
    return f'''<section class="cta-band"><div class="container cta-inner">
<div><h2>{esc(title)}</h2><p>{esc(text)}</p></div>
<div class="cta-actions"><a class="btn btn-gold btn-lg" href="%ROOT%case-review/{q}">Start my free case review</a>
<a class="btn btn-ghost-light" href="%ROOT%tools/do-i-need-a-lawyer/">Take the 2-minute quiz</a></div></div></section>'''


ISSUES = [
    ("injury", "Accident or injury", "🚗"), ("employment", "Job or workplace", "💼"),
    ("family", "Divorce, custody or support", "👪"), ("criminal", "Arrest, charge or DUI", "⚖️"),
    ("immigration", "Immigration or visa", "🌎"), ("estate", "Will, trust or probate", "📜"),
    ("housing", "Landlord or tenant", "🏠"), ("debt", "Debt or bankruptcy", "💳"),
    ("business", "Business or trademark", "🏢"), ("other", "Something else", "❓"),
]

STATE_OPTIONS = "".join('<option value="%s">%s</option>' % (esc(n), esc(n)) for _, n, _, _ in STATES)


def newsletter_block(context="home"):
    return f'''<section class="newsletter-block"><div class="container nl-inner">
<div><h2>The Weekly Legal Brief</h2><p>One email a week: the legal changes that matter, a new free tool, and one plain-English explainer. No spam, unsubscribe anytime.</p></div>
<form class="newsletter" data-lp-form="newsletter" novalidate>
<label class="sr-only" for="nl-{context}">Email</label>
<input id="nl-{context}" type="email" name="Email" placeholder="you@example.com" required>
<label class="sr-only" for="nl-topic-{context}">Topic</label>
<select id="nl-topic-{context}" name="Main interest"><option>Everything</option><option>Accidents & injury</option><option>Work & employment</option><option>Family & divorce</option><option>Money, debt & housing</option><option>Business & IP</option><option>Law student / legal pro</option></select>
<input type="hidden" name="Form" value="Newsletter ({context})">
<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">
<button class="btn btn-gold" type="submit">Get the brief</button>
<p class="form-status" role="status"></p>
</form></div></section>'''


def consent_block(kind="case"):
    if kind == "case":
        return '''<div class="consent">
<label class="check"><input type="checkbox" name="Consent to share" value="Yes" required> <span>I agree that LegalPundits may share my submission with one or more independent attorneys or legal service providers who may contact me about my matter. I understand LegalPundits is not a law firm, this is not legal advice, and no attorney-client relationship is formed. I agree to the <a href="%ROOT%terms/" target="_blank">Terms</a> and <a href="%ROOT%privacy/" target="_blank">Privacy Policy</a>.</span></label>
<label class="check"><input type="checkbox" name="Consent to calls and texts" value="Yes"> <span>Optional: I agree to receive calls and text messages about my request at the number provided, including by automated means. Consent is not a condition of any purchase. Message and data rates may apply; reply STOP to opt out.</span></label>
</div>'''
    return '''<div class="consent"><label class="check"><input type="checkbox" name="Consent" value="Yes" required> <span>I agree to the <a href="%ROOT%terms/" target="_blank">Terms</a> and <a href="%ROOT%privacy/" target="_blank">Privacy Policy</a> and understand this is not legal advice.</span></label></div>'''


def mini_case_form(issue, source):
    issue_label = dict((k, v) for k, v, _ in ISSUES).get(issue, "Something else")
    return f'''<section class="mini-case" id="free-review">
<h2>Get a free case review</h2>
<p>Describe your situation in a few lines. It's free and there's no obligation.</p>
<form class="lp-form" data-lp-form="case" novalidate>
<input type="hidden" name="Form" value="Case review (inline: {esc(source)})">
<input type="hidden" name="Legal issue" value="{esc(issue_label)}">
<div class="field-row">
<div class="field"><label for="mc-name-{source}">Full name</label><input id="mc-name-{source}" name="Name" required autocomplete="name"></div>
<div class="field"><label for="mc-email-{source}">Email</label><input id="mc-email-{source}" name="Email" type="email" required autocomplete="email"></div>
</div>
<div class="field-row">
<div class="field"><label for="mc-phone-{source}">Phone</label><input id="mc-phone-{source}" name="Phone" type="tel" autocomplete="tel"></div>
<div class="field"><label for="mc-state-{source}">State</label><select id="mc-state-{source}" name="State" required data-state-select><option value="">Select…</option>{STATE_OPTIONS}<option>Outside the US</option></select></div>
</div>
<div class="field"><label for="mc-desc-{source}">What happened?</label><textarea id="mc-desc-{source}" name="What happened" rows="3" minlength="20" required></textarea></div>
<p class="co-note" hidden>Colorado residents: we don't route Colorado submissions to attorneys. You'll receive free resources instead, including the Colorado Bar's lawyer referral information.</p>
{consent_block("case")}
<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">
<button class="btn btn-gold" type="submit">Request my free review</button>
<p class="form-status" role="status"></p>
</form></section>'''


# ---------------------------------------------------------------- pages

def build_home():
    tiles = "".join(f'<a class="tile" href="%ROOT%case-review/?issue={k}"><span aria-hidden="true">{ic}</span>{esc(lbl)}</a>' for k, lbl, ic in ISSUES)
    tools = "".join(tool_card(t) for t in TOOLS)
    featured = [GUIDE_BY_SLUG[s] for s in [
        "what-to-do-after-a-car-accident", "how-personal-injury-settlements-are-calculated", "wrongful-termination-is-it-illegal",
        "how-divorce-works-step-by-step", "dui-first-offense-what-happens", "debt-collector-rights-fdcpa"]]
    guides = "".join(guide_card(g) for g in featured)
    areas = "".join(f'<a class="area-chip" href="%ROOT%topics/{a["slug"]}/"><span aria-hidden="true">{a["icon"]}</span>{esc(a["name"])}</a>' for a in AREAS)
    news_items = NEWS.get("items", [])[:6]
    news_html = "".join(news_li(n) for n in news_items) or '<li class="muted">Headlines load here automatically.</li>'
    gl = json.dumps([[t, d] for t, d in GLOSSARY], ensure_ascii=False)
    body = f'''
<section class="hero"><div class="container hero-grid">
  <div class="hero-copy">
    <p class="eyebrow">Free legal answers · Free tools · Free case review</p>
    <h1>Plain-English law from the <em>pundits</em>.</h1>
    <p class="lead">Understand your rights, run the numbers on your situation, and get connected with real legal help, all in one place.</p>
    <form class="hero-search" role="search" data-hero-search>
      <label class="sr-only" for="hero-q">Search</label>
      <input id="hero-q" type="search" placeholder="What's your legal question? e.g. “fired after injury”" autocomplete="off">
      <button class="btn btn-gold" type="submit">Search</button>
    </form>
    <p class="hero-sub">Or tell us what happened: <a href="%ROOT%case-review/">start a free case review →</a></p>
  </div>
  <div class="hero-panel">
    <h2>What do you need help with?</h2>
    <div class="tiles">{tiles}</div>
    <p class="micro">Free · No obligation · Takes about 2 minutes</p>
  </div>
</div></section>

<section class="trust-strip"><div class="container trust-grid">
  <div><strong>{len(GUIDES)}</strong><span>in-depth legal guides</span></div>
  <div><strong>{len(TOOLS)}</strong><span>free legal tools</span></div>
  <div><strong>{len(GLOSSARY)}+</strong><span>legal terms decoded</span></div>
  <div><strong>4×</strong><span>daily news &amp; video refresh</span></div>
</div></section>

{ad("top")}

<section class="section"><div class="container">
  <div class="section-head"><h2>Free legal tools</h2><a class="more" href="%ROOT%tools/">All tools →</a></div>
  <div class="grid cards-3">{tools}</div>
</div></section>

<section class="section alt"><div class="container">
  <div class="section-head"><h2>Most-read guides</h2><a class="more" href="%ROOT%guides/">All {len(GUIDES)} guides →</a></div>
  <div class="grid cards-3">{guides}</div>
  <div class="area-chips">{areas}</div>
</div></section>

<section class="section"><div class="container split">
  <div>
    <div class="section-head"><h2>Legal news desk</h2><a class="more" href="%ROOT%news/">All headlines →</a></div>
    <ul class="news-list compact" data-news-widget data-limit="6">{news_html}</ul>
    <p class="muted small">Headlines link to the original publishers. Updated automatically every 6 hours.</p>
  </div>
  <aside class="stack">
    <div class="box term-box"><p class="eyebrow">Term of the day</p><h3 data-term-title>Statute of limitations</h3><p data-term-def>The deadline for filing a lawsuit or bringing criminal charges.</p><a href="%ROOT%glossary/">Browse the glossary →</a></div>
    <div class="box quiz-box"><p class="eyebrow">Legal IQ</p><h3>5 new questions every day</h3><p>Test yourself, learn something useful, and climb the monthly leaderboard.</p><a class="btn btn-teal btn-sm" href="%ROOT%quiz/">Take today's quiz</a></div>
  </aside>
</div></section>

<section class="section alt"><div class="container">
  <div class="section-head"><h2>Watch: the law, explained</h2><a class="more" href="%ROOT%videos/">Video library →</a></div>
  <p class="section-intro">Hand-picked explainer channels from practicing lawyers, refreshed automatically.</p>
  <div class="grid cards-3">{"".join(video_channel_card(c) for c in CHANNELS[:3])}</div>
</div></section>

{cta_band()}

<section class="section"><div class="container grid cards-3">
  <a class="card feature" href="%ROOT%contests/"><span class="card-icon" aria-hidden="true">🏆</span><h3>Pundit Challenge</h3><p>Monthly contests for the best plain-English legal explainer, 60-second law video and Legal IQ score. Win prizes and get featured.</p><span class="card-link">See this month's contests →</span></a>
  <a class="card feature" href="%ROOT%support/"><span class="card-icon" aria-hidden="true">🤝</span><h3>Support free legal help</h3><p>Reader support funds operations, outreach, new writers and contest prizes, keeping every guide and tool free.</p><span class="card-link">Become a supporter →</span></a>
  <a class="card feature" href="%ROOT%careers/"><span class="card-icon" aria-hidden="true">✍️</span><h3>Write, review or create</h3><p>We're hiring legal writers, attorney reviewers, researchers, video editors and campus ambassadors.</p><span class="card-link">View open roles →</span></a>
</div></section>

{newsletter_block("home")}

<section class="section"><div class="container narrow">
  <h2>About LegalPundits</h2>
  <p>LegalPundits.com is an independent legal information publication. We translate statutes, court rules and agency guidance into plain English, build free tools that answer the questions people actually ask ("How long do I have?", "What's my claim worth?", "What will I take home?"), and point you to the right kind of help, whether that's a free legal aid office or an experienced attorney. We're <a href="%ROOT%disclaimer/">not a law firm</a>, and nothing here is legal advice, but it's the fastest way to understand where you stand.</p>
  <p>Outside the US? Start with our <a href="%ROOT%global/">Global Law Desk</a> for Canada, the UK, India and Australia.</p>
</div></section>
<script type="application/json" id="glossary-data">{gl}</script>'''
    ld = [
        {"@context": "https://schema.org", "@type": "Organization", "name": "LegalPundits", "url": SITE["url"] + "/",
         "logo": SITE["url"] + "/assets/img/favicon.svg", "description": SITE["description"]},
        {"@context": "https://schema.org", "@type": "WebSite", "name": "LegalPundits", "url": SITE["url"] + "/",
         "potentialAction": {"@type": "SearchAction", "target": SITE["url"] + "/?q={search_term_string}",
                             "query-input": "required name=search_term_string"}},
    ]
    page("", "LegalPundits — Plain-English Law, Free Legal Tools & Free Case Review", SITE["description"], body,
         priority="1.0", jsonld=ld, body_class="home")


def news_li(n):
    d = n.get("date", "")[:10]
    return (f'<li class="news-item"><a href="{esc(n["link"])}" target="_blank" rel="noopener nofollow">{esc(n["title"])}</a>'
            f'<span class="meta">{esc(n.get("source", ""))}{" · " + d if d else ""}</span></li>')


def build_guides():
    # index
    sections = ""
    for a in AREAS:
        gs = [g for g in GUIDES if g["area"] == a["slug"]]
        if not gs:
            continue
        sections += f'<section class="area-section" id="{a["slug"]}"><h2><span aria-hidden="true">{a["icon"]}</span> {esc(a["name"])}</h2><div class="grid cards-3">{"".join(guide_card(g) for g in gs)}</div></section>'
    filt = "".join(f'<a href="#{a["slug"]}" class="area-chip">{a["icon"]} {esc(a["name"])}</a>' for a in AREAS)
    body = f'''<section class="page-head"><div class="container"><h1>Legal Guides</h1><p class="lead">{len(GUIDES)} in-depth, plain-English guides to the legal problems people search for most, each with official sources, FAQs and a "when to call a lawyer" checklist.</p>
<div class="area-chips">{filt}</div></div></section>
<div class="container">{sections}</div>{cta_band()}'''
    page("guides/", "Legal Guides: Plain-English Answers to Common Legal Problems",
         "In-depth plain-English legal guides on accidents, employment, divorce, criminal charges, immigration, wills, housing, debt and business.",
         body, priority="0.9", crumbs=[("Guides", "")])
    for g in GUIDES:
        build_guide(g)


def build_guide(g):
    a = AREA_BY_SLUG[g["area"]]
    body_html, toc = md(g["body"])
    words = len(re.sub(r"<[^>]+>", " ", body_html).split()) + sum(len(q.split()) + len(x.split()) for q, x in g["faqs"])
    minutes = max(3, round(words / 220))
    toc_html = "".join(f'<li><a href="#{i}">{esc(t)}</a></li>' for i, t in toc)
    takeaways = "".join(f"<li>{inline_md(t)}</li>" for t in g["takeaways"])
    faqs = "".join(f'<details><summary>{esc(q)}</summary><p>{inline_md(x)}</p></details>' for q, x in g["faqs"])
    sources = "".join(f'<li><a href="{esc(u)}" target="_blank" rel="noopener">{esc(n)}</a></li>' for n, u in g["sources"])
    tools = "".join(tool_card(TOOL_BY_SLUG[t]) for t in g["tools"] if t in TOOL_BY_SLUG)
    related = [x for x in GUIDES if x["area"] == g["area"] and x["slug"] != g["slug"]][:3]
    if len(related) < 3:
        related += [x for x in GUIDES if x["slug"] not in {g["slug"]} | {r["slug"] for r in related}][: 3 - len(related)]
    related_html = "".join(guide_card(x) for x in related)
    # split body to drop an in-article ad after the second h2
    parts = body_html.split("<h2", 3)
    if len(parts) > 3:
        body_html = parts[0] + "<h2" + parts[1] + "<h2" + parts[2] + ad("in_article") + "<h2" + parts[3]
    side_tools = "".join(f'<li><a href="%ROOT%tools/{t}/">{TOOL_BY_SLUG[t]["icon"]} {esc(TOOL_BY_SLUG[t]["name"])}</a></li>' for t in g["tools"] if t in TOOL_BY_SLUG)
    body = f'''<article class="guide container" data-issue="{g["issue"]}">
<header class="guide-head">
  <a class="tag" href="%ROOT%topics/{a["slug"]}/">{a["icon"]} {esc(a["name"])}</a>
  <h1>{esc(g["title"])}</h1>
  <p class="lead">{esc(g["description"])}</p>
  <p class="byline">By the LegalPundits Editorial Team · Last reviewed {SITE["reviewed"]} · {minutes} min read · <a href="%ROOT%editorial-policy/">How we write</a></p>
</header>
<div class="guide-layout">
<div class="guide-main">
  <div class="takeaways"><h2>Key takeaways</h2><ul>{takeaways}</ul></div>
  <nav class="toc" aria-label="On this page"><h2>On this page</h2><ol>{toc_html}<li><a href="#faq">FAQs</a></li><li><a href="#when-to-call-a-lawyer">When to call a lawyer</a></li></ol></nav>
  <div class="prose">{body_html}</div>
  <section class="faq" id="faq"><h2>Frequently asked questions</h2>{faqs}</section>
  <section class="lawyer-box" id="when-to-call-a-lawyer"><h2>When to call a lawyer</h2><p>{inline_md(g["lawyer"])}</p>
  <a class="btn btn-gold" href="%ROOT%case-review/?issue={g["issue"]}">Get a free case review</a></section>
  {mini_case_form(g["issue"], g["slug"])}
  <section class="sources"><h2>Official sources &amp; further reading</h2><ul>{sources}</ul>
  <p class="small muted">This guide is general information, not legal advice. Laws vary by state and change over time. <a href="%ROOT%contact/?reason=correction">Report an error</a>.</p></section>
  <section class="helpful" data-helpful><span>Was this guide helpful?</span> <button class="btn btn-ghost btn-sm" type="button" data-helpful-vote="yes">Yes</button> <button class="btn btn-ghost btn-sm" type="button" data-helpful-vote="no">No</button></section>
</div>
<aside class="guide-aside">
  <div class="sticky">
    <div class="box cta-box"><h3>Talk to a lawyer, free</h3><p>Free, no-obligation case review for {esc(a["name"].lower())} matters.</p><a class="btn btn-gold btn-block" href="%ROOT%case-review/?issue={g["issue"]}">Start free review</a></div>
    <div class="box"><h3>Related free tools</h3><ul class="link-list">{side_tools}</ul></div>
    {ad("sidebar")}
  </div>
</aside>
</div>
<section class="related"><h2>Related tools</h2><div class="grid cards-3">{tools}</div>
<h2>Keep reading</h2><div class="grid cards-3">{related_html}</div></section>
</article>
<div class="slidein" id="slidein" hidden><button class="slidein-close" type="button" aria-label="Dismiss">×</button><p><strong>Facing this right now?</strong> Get a free, no-obligation case review.</p><a class="btn btn-gold btn-sm" href="%ROOT%case-review/?issue={g["issue"]}">Start free review</a></div>'''
    url = SITE["url"] + "/guides/" + g["slug"] + "/"
    ld = [
        {"@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": g["description"],
         "author": {"@type": "Organization", "name": "LegalPundits Editorial Team", "url": SITE["url"] + "/editorial-policy/"},
         "publisher": {"@type": "Organization", "name": "LegalPundits", "logo": {"@type": "ImageObject", "url": SITE["url"] + "/assets/img/favicon.svg"}},
         "datePublished": "2026-11-26", "dateModified": "2026-11-26", "mainEntityOfPage": url, "articleSection": a["name"]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": x}} for q, x in g["faqs"]]},
    ]
    page("guides/%s/" % g["slug"], g["title"], g["description"], body, kind="guide", priority="0.8",
         crumbs=[("Guides", "guides/"), (a["name"], "topics/%s/" % a["slug"]), (g["title"], "")],
         jsonld=ld, og_type="article", body_class="guide-page")


def build_topics():
    cards = "".join(f'<a class="card" href="%ROOT%topics/{a["slug"]}/"><span class="card-icon" aria-hidden="true">{a["icon"]}</span><h3>{esc(a["name"])}</h3><p>{esc(a["blurb"])}</p><span class="card-link">{len([g for g in GUIDES if g["area"] == a["slug"]])} guides →</span></a>' for a in AREAS)
    body = f'''<section class="page-head"><div class="container"><h1>Practice Areas</h1><p class="lead">Browse guides, tools and help by the kind of legal problem you have.</p></div></section>
<div class="container"><div class="grid cards-3">{cards}</div></div>{cta_band()}'''
    page("topics/", "Legal Practice Areas", "Browse LegalPundits guides and tools by practice area.", body, priority="0.7", crumbs=[("Practice areas", "")])
    issue_for = {g["area"]: g["issue"] for g in GUIDES}
    for a in AREAS:
        gs = [g for g in GUIDES if g["area"] == a["slug"]]
        ts = [t for t in TOOLS if t["area"] == a["slug"]] or [t for t in TOOLS if t["area"] == "lawyers-courts"]
        issue = issue_for.get(a["slug"], "other")
        faq_items = "".join(f'<details><summary>{esc(q)}</summary><p>{inline_md(x)}</p></details>' for g in gs for q, x in g["faqs"][:1])
        body = f'''<section class="page-head"><div class="container"><p class="eyebrow">{a["icon"]} Practice area</p><h1>{esc(a["name"])}</h1><p class="lead">{esc(a["blurb"])} Start with the guides below, run the numbers with our free tools, or request a free case review.</p>
<a class="btn btn-gold" href="%ROOT%case-review/?issue={issue}">Free case review</a></div></section>
<div class="container">
<section class="section"><h2>Guides</h2><div class="grid cards-3">{"".join(guide_card(g) for g in gs)}</div></section>
<section class="section"><h2>Helpful tools</h2><div class="grid cards-3">{"".join(tool_card(t) for t in ts)}</div></section>
{ad("in_article")}
<section class="section faq"><h2>Quick answers</h2>{faq_items}</section>
</div>{cta_band(issue=issue)}'''
        page("topics/%s/" % a["slug"], a["name"] + " — Guides, Tools & Free Case Review",
             a["blurb"] + " Plain-English guides, free tools and a free case review.", body, priority="0.7",
             crumbs=[("Practice areas", "topics/"), (a["name"], "")])


# ---------------------------------------------------------------- tools

def field(label, inner, help_text=""):
    h = '<small>%s</small>' % help_text if help_text else ""
    return f'<div class="field"><label>{label}{inner}</label>{h}</div>'


def tool_page(t, panel, intro, how, faqs, extra_scripts=""):
    faq_html = "".join(f'<details><summary>{esc(q)}</summary><p>{inline_md(x)}</p></details>' for q, x in faqs)
    other = "".join(tool_card(x) for x in TOOLS if x["slug"] != t["slug"])[:]
    body = f'''<section class="page-head tool-head"><div class="container"><p class="eyebrow">{t["icon"]} Free legal tool</p><h1>{esc(t["name"])}</h1><p class="lead">{esc(intro)}</p></div></section>
<div class="container tool-layout">
  <div class="tool-panel" data-tool="{t["slug"]}">{panel}</div>
  <aside class="tool-aside"><div class="box"><h3>How it works</h3>{how}</div>
  <div class="box cta-box"><h3>Want a real opinion?</h3><p>Tools give estimates. A lawyer can look at your actual facts.</p><a class="btn btn-gold btn-block" href="%ROOT%case-review/?src={t["slug"]}">Free case review</a></div>{ad("sidebar")}</aside>
</div>
<div class="container"><section class="section faq"><h2>FAQs</h2>{faq_html}</section>
<p class="small muted">Estimates and templates only, not legal advice. Laws vary by jurisdiction and change. Verify with a licensed attorney.</p>
<section class="section"><h2>More free tools</h2><div class="grid cards-3">{other}</div></section></div>'''
    page("tools/%s/" % t["slug"], t["name"] + " (Free)", t["blurb"], body, kind="tool", priority="0.8",
         crumbs=[("Tools", "tools/"), (t["name"], "")],
         scripts='<script src="%ROOT%assets/js/tools.js?v=' + VER + '" defer></script>' + extra_scripts)


def build_tools():
    body = f'''<section class="page-head"><div class="container"><h1>Free Legal Tools</h1><p class="lead">Calculators, deadline finders and generators that answer the practical questions: How long do I have? What's it worth? What will I take home?</p></div></section>
<div class="container"><div class="grid cards-3">{"".join(tool_card(t) for t in TOOLS)}</div>
<section class="section"><div class="grid cards-3">
<a class="card" href="%ROOT%quiz/"><span class="card-icon">🧠</span><h3>Legal IQ Daily Quiz</h3><p>Five fresh questions every day with plain-English explanations.</p><span class="card-link">Play →</span></a>
<a class="card" href="%ROOT%glossary/"><span class="card-icon">📖</span><h3>Legal Glossary</h3><p>{len(GLOSSARY)}+ legal terms decoded with instant search.</p><span class="card-link">Search terms →</span></a>
<a class="card" href="%ROOT%legal-aid/"><span class="card-icon">🆓</span><h3>Free Legal Aid Finder</h3><p>Official free and low-cost legal help resources.</p><span class="card-link">Find help →</span></a>
</div></section></div>{cta_band()}'''
    page("tools/", "Free Legal Calculators & Tools", "Free legal calculators: settlement estimator, statute of limitations deadline finder, contingency fee calculator, court days counter and demand letter generator.",
         body, priority="0.9", crumbs=[("Tools", "")])

    # 1. settlement estimator
    t = TOOL_BY_SLUG["settlement-estimator"]
    panel = '''<form class="calc" data-calc="settlement" novalidate>
<div class="field-row">
<div class="field"><label for="se-med">Medical bills so far ($)</label><input id="se-med" type="number" min="0" step="100" value="12000" inputmode="decimal"></div>
<div class="field"><label for="se-fmed">Expected future medical ($)</label><input id="se-fmed" type="number" min="0" step="100" value="0" inputmode="decimal"></div>
</div>
<div class="field-row">
<div class="field"><label for="se-wages">Lost wages ($)</label><input id="se-wages" type="number" min="0" step="100" value="3000" inputmode="decimal"></div>
<div class="field"><label for="se-other">Property damage & other costs ($)</label><input id="se-other" type="number" min="0" step="100" value="0" inputmode="decimal"></div>
</div>
<div class="field"><label for="se-sev">Injury severity</label><select id="se-sev">
<option value="1.5">Minor — soft tissue, healed within weeks (×1.5)</option>
<option value="2" selected>Moderate — months of treatment (×2)</option>
<option value="3">Significant — injections, fractures (×3)</option>
<option value="4">Severe — surgery, long recovery (×4)</option>
<option value="5">Catastrophic — permanent impairment (×5)</option></select></div>
<div class="field-row">
<div class="field"><label for="se-fault">Your share of fault (%)</label><input id="se-fault" type="number" min="0" max="100" value="0"></div>
<div class="field"><label for="se-rule">Fault rule in your state</label><select id="se-rule">
<option value="pure">Pure comparative (reduce by your %)</option>
<option value="mod50">Modified — barred at 50%</option>
<option value="mod51" selected>Modified — barred at 51%</option>
<option value="contrib">Contributory (AL, DC, MD, NC, VA)</option></select></div>
</div>
<div class="field-row">
<div class="field"><label for="se-limit">At-fault policy limit ($, optional)</label><input id="se-limit" type="number" min="0" step="1000" placeholder="e.g. 50000"></div>
<div class="field"><label for="se-fee">Attorney fee (%)</label><input id="se-fee" type="number" min="0" max="50" step="0.01" value="33.33"></div>
</div>
<button class="btn btn-gold" type="submit">Estimate my claim</button>
</form>
<div class="result" data-result hidden></div>'''
    how = "<p>Economic damages (bills, wages, costs) are added to non-economic damages estimated with the multiplier method (medical costs × severity). We show a range one step either side of your multiplier, reduce it for your share of fault under your state's rule, flag any policy limit, then subtract the lawyer's fee.</p>"
    tool_page(t, panel, "A quick, transparent estimate of what an injury claim may be worth, before and after fault, policy limits and attorney fees.", how, [
        ("Is this what my case is worth?", "No calculator can value a real case. Adjusters weigh medical evidence, venue, credibility and policy limits. Use this as a starting point for a conversation with a lawyer."),
        ("What multiplier should I pick?", "Choose based on treatment length and permanence. Surgery and lasting limitations push the multiplier up; quick recoveries push it down."),
        ("Why does fault matter so much?", "Most states reduce awards by your percentage of fault, and some bar recovery entirely past 50% or 51%, or for any fault in contributory states."),
    ])

    # 2. deadline finder
    t = TOOL_BY_SLUG["deadline-finder"]
    sol = json.dumps([{"c": c, "n": n, "y": y, "note": note, "contrib": c in CONTRIBUTORY_STATES} for c, n, y, note in STATES])
    opts = "".join(f'<option value="{c}">{esc(n)}</option>' for c, n, _, _ in STATES)
    panel = f'''<form class="calc" data-calc="deadline" novalidate>
<div class="field-row">
<div class="field"><label for="dl-state">State where the injury happened</label><select id="dl-state" required><option value="">Select a state…</option>{opts}</select></div>
<div class="field"><label for="dl-date">Date of injury</label><input id="dl-date" type="date" required></div>
</div>
<div class="field"><label for="dl-type">Who may be responsible?</label><select id="dl-type">
<option value="private">A private person or business</option>
<option value="gov">A government agency, city or public employee</option>
<option value="med">A doctor or hospital (medical malpractice)</option>
<option value="minor">The injured person was under 18</option></select></div>
<button class="btn btn-gold" type="submit">Find my deadline</button>
</form>
<div class="result" data-result hidden></div>
<script type="application/json" id="sol-data">{sol}</script>'''
    rows = "".join(f'<tr><td>{esc(n)}</td><td>{y} year{"s" if y != 1 else ""}</td><td>{esc(note)}</td></tr>' for _, n, y, note in STATES)
    how = "<p>We apply the general personal-injury statute of limitations for your state to your injury date and count the days left. Government, malpractice and minor claims follow different rules, so we flag them.</p>"
    tool_page(t, panel, "See the general personal-injury filing deadline for all 50 states and DC, plus the days you have left.", how + f'<details class="sol-table"><summary>See all states</summary><table><thead><tr><th>State</th><th>Deadline</th><th>Note</th></tr></thead><tbody>{rows}</tbody></table></details>', [
        ("What if my deadline has passed?", "Talk to a lawyer anyway. Tolling rules (for minors, late discovery or a defendant's absence) sometimes extend deadlines."),
        ("Does negotiating with the insurer stop the clock?", "No. Only filing a lawsuit (or a valid tolling agreement) protects you against the statute of limitations."),
        ("Why are government claims different?", "Most states require a written notice of claim within a short period, sometimes 30 to 180 days, before you can sue a public entity."),
    ])

    # 3. contingency fee
    t = TOOL_BY_SLUG["contingency-fee-calculator"]
    panel = '''<form class="calc" data-calc="contingency" novalidate>
<div class="field"><label for="cf-amt">Settlement or award ($)</label><input id="cf-amt" type="number" min="0" step="500" value="50000" inputmode="decimal"></div>
<div class="field-row">
<div class="field"><label for="cf-stage">Case stage</label><select id="cf-stage"><option value="pre">Settled before a lawsuit</option><option value="lit">Settled after filing suit</option><option value="trial">Went to trial</option></select></div>
<div class="field"><label for="cf-pct">Fee % for that stage</label><input id="cf-pct" type="number" min="0" max="50" step="0.01" value="33.33"></div>
</div>
<div class="field-row">
<div class="field"><label for="cf-costs">Case costs advanced by lawyer ($)</label><input id="cf-costs" type="number" min="0" step="50" value="1500"></div>
<div class="field"><label for="cf-liens">Medical liens / bills to repay ($)</label><input id="cf-liens" type="number" min="0" step="50" value="8000"></div>
</div>
<fieldset class="field"><legend>Fee calculated on</legend>
<label class="radio"><input type="radio" name="cf-basis" value="gross" checked> Gross recovery (most common)</label>
<label class="radio"><input type="radio" name="cf-basis" value="net"> Recovery after costs</label></fieldset>
<button class="btn btn-gold" type="submit">Calculate my take-home</button>
</form>
<div class="result" data-result hidden></div>'''
    how = "<p>Contingency fees are a percentage of the recovery. Costs (filing fees, records, experts) and liens (health insurers, hospitals, Medicare) are usually repaid from the settlement too. Your written fee agreement controls the actual math.</p>"
    tool_page(t, panel, "See how a settlement splits between attorney fees, case costs, medical liens and you.", how, [
        ("Are contingency percentages negotiable?", "Often. Some lawyers offer sliding scales, lower percentages for quick settlements or caps for large recoveries."),
        ("Can medical liens be reduced?", "Frequently. Lawyers often negotiate liens down, which can significantly increase what you keep."),
        ("What if we lose?", "Under a typical contingency agreement you owe no fee. Check whether you'd still owe case costs."),
    ])

    # 4. court days
    t = TOOL_BY_SLUG["court-days-calculator"]
    panel = '''<form class="calc" data-calc="days" novalidate>
<div class="field-row">
<div class="field"><label for="cd-start">Start date (trigger event)</label><input id="cd-start" type="date" required></div>
<div class="field"><label for="cd-n">Number of days</label><input id="cd-n" type="number" min="1" max="3650" value="30"></div>
</div>
<div class="field-row">
<div class="field"><label for="cd-mode">Count</label><select id="cd-mode"><option value="cal">Calendar days</option><option value="bus">Business days (skip weekends & federal holidays)</option></select></div>
<div class="field"><label for="cd-dir">Direction</label><select id="cd-dir"><option value="f">Forward (deadline after)</option><option value="b">Backward (deadline before)</option></select></div>
</div>
<label class="check"><input type="checkbox" id="cd-roll" checked> <span>If the last day falls on a weekend or federal holiday, move to the next business day</span></label>
<button class="btn btn-gold" type="submit">Calculate date</button>
</form>
<div class="result" data-result hidden></div>'''
    how = "<p>We exclude the trigger day and count from the next day, the approach used by the federal civil rules. Holidays include all US federal holidays with weekend observance. Local court rules and state holidays can differ.</p>"
    tool_page(t, panel, "Count calendar or business days from any date, skipping weekends and US federal holidays.", how, [
        ("Do courts count the first day?", "Under the federal rules you exclude the day of the triggering event and include the last day, rolling forward if it lands on a weekend or legal holiday."),
        ("Are state holidays included?", "No, only US federal holidays. Check your court's local calendar for state holidays and closures."),
        ("Does mail service add days?", "Some rules add extra days after service by mail. Check the rule that applies to your deadline."),
    ])

    # 5. demand letter
    t = TOOL_BY_SLUG["demand-letter-generator"]
    panel = f'''<form class="calc" data-calc="letter" novalidate>
<div class="field"><label for="ml-type">Letter type</label><select id="ml-type">
<option value="money">Money owed (unpaid loan, invoice or wages)</option><option value="deposit">Security deposit return</option>
<option value="damage">Property damage</option><option value="refund">Refund for defective goods or services</option></select></div>
<div class="field-row">
<div class="field"><label for="ml-you">Your full name</label><input id="ml-you" autocomplete="name"></div>
<div class="field"><label for="ml-youaddr">Your address</label><input id="ml-youaddr" autocomplete="street-address"></div>
</div>
<div class="field-row">
<div class="field"><label for="ml-them">Recipient name / business</label><input id="ml-them"></div>
<div class="field"><label for="ml-themaddr">Recipient address</label><input id="ml-themaddr"></div>
</div>
<div class="field-row">
<div class="field"><label for="ml-amt">Amount demanded ($)</label><input id="ml-amt" type="number" min="0" step="0.01"></div>
<div class="field"><label for="ml-date">Date of agreement / incident</label><input id="ml-date" type="date"></div>
</div>
<div class="field"><label for="ml-facts">What happened (brief facts)</label><textarea id="ml-facts" rows="4" placeholder="e.g. I moved out on 1 October, returned the keys and left the unit clean. My $1,500 deposit has not been returned or itemized."></textarea></div>
<div class="field-row">
<div class="field"><label for="ml-days">Days to respond</label><select id="ml-days"><option>10</option><option selected>14</option><option>21</option><option>30</option></select></div>
<div class="field"><label for="ml-state">State (optional)</label><select id="ml-state"><option value="">—</option>{STATE_OPTIONS}</select></div>
</div>
<button class="btn btn-gold" type="submit">Generate my letter</button>
</form>
<div class="result letter-result" data-result hidden>
<textarea id="ml-out" rows="18" aria-label="Your demand letter"></textarea>
<div class="btn-row"><button class="btn btn-teal" type="button" data-copy="ml-out">Copy</button><button class="btn btn-ghost" type="button" data-print-letter>Print</button><button class="btn btn-ghost" type="button" data-download="ml-out">Download .txt</button></div>
</div>'''
    how = "<p>Fill in the facts and we assemble a firm, professional letter with a clear amount, deadline and next step. Edit freely before sending. Send it by a trackable method and keep a copy; courts like to see that you tried to resolve things.</p>"
    tool_page(t, panel, "Create a professional demand letter in minutes for money owed, a security deposit, property damage or a refund.", how, [
        ("Is a demand letter legally required?", "Not always, but some claims and many small claims courts expect you to request payment first, and a clear letter often resolves the dispute."),
        ("How should I send it?", "Use a trackable method such as certified mail with return receipt, plus email if you normally communicate that way."),
        ("What if they ignore it?", "Consider small claims court. See our small claims guide."),
    ])

    # 6. quiz
    t = TOOL_BY_SLUG["do-i-need-a-lawyer"]
    panel = '''<form class="calc quizform" data-calc="needlawyer" novalidate>
<fieldset class="q"><legend>1. What kind of problem is it?</legend>
<label class="radio"><input type="radio" name="q1" value="3" data-issue="criminal" required> Criminal charge, arrest or DUI</label>
<label class="radio"><input type="radio" name="q1" value="3" data-issue="injury"> Injury with medical treatment</label>
<label class="radio"><input type="radio" name="q1" value="2" data-issue="family"> Divorce, custody or support</label>
<label class="radio"><input type="radio" name="q1" value="2" data-issue="employment"> Job loss, discrimination or unpaid wages</label>
<label class="radio"><input type="radio" name="q1" value="2" data-issue="immigration"> Immigration status</label>
<label class="radio"><input type="radio" name="q1" value="1" data-issue="other"> Contract, consumer, housing or other</label></fieldset>
<fieldset class="q"><legend>2. Is there a court date, legal deadline or government notice?</legend>
<label class="radio"><input type="radio" name="q2" value="3" required> Yes, within 30 days</label>
<label class="radio"><input type="radio" name="q2" value="2"> Yes, later than 30 days</label>
<label class="radio"><input type="radio" name="q2" value="1"> Not sure</label>
<label class="radio"><input type="radio" name="q2" value="0"> No</label></fieldset>
<fieldset class="q"><legend>3. Roughly how much is at stake (money, property or benefits)?</legend>
<label class="radio"><input type="radio" name="q3" value="3" required> Over $25,000</label>
<label class="radio"><input type="radio" name="q3" value="2"> $5,000–$25,000</label>
<label class="radio"><input type="radio" name="q3" value="1"> Under $5,000</label>
<label class="radio"><input type="radio" name="q3" value="0"> Mostly non-financial</label></fieldset>
<fieldset class="q"><legend>4. Does the other side have a lawyer or insurance adjuster?</legend>
<label class="radio"><input type="radio" name="q4" value="2" required> Yes</label>
<label class="radio"><input type="radio" name="q4" value="1"> Not sure</label>
<label class="radio"><input type="radio" name="q4" value="0"> No</label></fieldset>
<fieldset class="q"><legend>5. Could you lose your freedom, children, home, job or immigration status?</legend>
<label class="radio"><input type="radio" name="q5" value="4" required> Yes</label>
<label class="radio"><input type="radio" name="q5" value="1"> Possibly</label>
<label class="radio"><input type="radio" name="q5" value="0"> No</label></fieldset>
<fieldset class="q"><legend>6. Have you been asked to sign anything (settlement, release, plea, severance)?</legend>
<label class="radio"><input type="radio" name="q6" value="2" required> Yes</label>
<label class="radio"><input type="radio" name="q6" value="0"> No</label></fieldset>
<button class="btn btn-gold" type="submit">See my result</button>
</form>
<div class="result" data-result hidden></div>'''
    how = "<p>Each answer adds points for urgency and stakes. Criminal exposure, near deadlines, high stakes, a represented opponent and documents awaiting signature all raise the score.</p>"
    tool_page(t, panel, "Six quick questions to gauge how urgently you should speak with an attorney.", how, [
        ("Is this quiz legal advice?", "No. It's a general triage tool to help you decide your next step."),
        ("What if I can't afford a lawyer?", "Check free legal aid, bar referral services with low-cost consultations, and contingency-fee lawyers for injury and some employment cases."),
        ("What's the fastest way to talk to someone?", "Submit a free case review, and if you have a court date, call your court's self-help center too."),
    ])


# ---------------------------------------------------------------- lead gen pages

def build_case_review():
    tiles = "".join(f'<label class="choice"><input type="radio" name="Legal issue" value="{esc(lbl)}" data-key="{k}" required><span><b aria-hidden="true">{ic}</b>{esc(lbl)}</span></label>' for k, lbl, ic in ISSUES)
    body = f'''<section class="page-head lead-head"><div class="container lead-grid">
<div>
<p class="eyebrow">Free · Confidential · No obligation</p>
<h1>Get a free case review</h1>
<p class="lead">Answer a few questions about what happened. Your request is reviewed and, where available and permitted, shared with independent attorneys who handle your type of matter.</p>
<ul class="checks"><li>No cost and no obligation to hire anyone</li><li>Takes about two minutes</li><li>Covers injury, employment, family, criminal, immigration, estates, housing, debt and business matters</li><li>Low-income? We'll also point you to free legal aid</li></ul>
<ol class="steps mini"><li><b>Tell us what happened</b></li><li><b>We review your request</b></li><li><b>Hear back about your options</b></li></ol>
</div>
<div class="form-card">
<form class="lp-form multistep" data-lp-form="case" data-multistep novalidate>
<input type="hidden" name="Form" value="Case review (main funnel)">
<input type="hidden" name="Source" value="" data-source-field>
<div class="progress" aria-hidden="true"><span data-progress></span></div>
<p class="step-label" data-step-label>Step 1 of 4</p>

<fieldset class="form-step" data-step="1"><legend>What do you need help with?</legend>
<div class="choice-grid">{tiles}</div></fieldset>

<fieldset class="form-step" data-step="2" hidden><legend>Where and when?</legend>
<div class="field"><label for="cr-state">State</label><select id="cr-state" name="State" required data-state-select><option value="">Select your state…</option>{STATE_OPTIONS}<option>Outside the US</option></select></div>
<p class="co-note" hidden>Colorado residents: under Colorado law we don't route or sell Colorado legal leads. Submit anyway and we'll send free resources, including the Colorado Bar's lawyer referral options.</p>
<div class="field"><label for="cr-when">When did this happen or start?</label><select id="cr-when" name="When it happened" required><option value="">Select…</option><option>Within the last 7 days</option><option>Within 30 days</option><option>1–6 months ago</option><option>6–12 months ago</option><option>1–2 years ago</option><option>More than 2 years ago</option><option>It's ongoing</option></select></div>
<div class="field"><label for="cr-deadline">Is there a court date or legal deadline?</label><select id="cr-deadline" name="Court date or deadline" required><option value="">Select…</option><option>Yes, within 30 days</option><option>Yes, more than 30 days away</option><option>No</option><option>Not sure</option></select></div>
<div class="field"><label for="cr-lawyer">Do you already have a lawyer for this?</label><select id="cr-lawyer" name="Already has lawyer" required><option value="">Select…</option><option>No</option><option>Yes, but I want a second opinion</option><option>Yes</option></select></div>
</fieldset>

<fieldset class="form-step" data-step="3" hidden><legend>Tell us what happened</legend>
<div class="field"><label for="cr-desc">Briefly describe your situation</label><textarea id="cr-desc" name="What happened" rows="5" minlength="20" required placeholder="What happened, who was involved, and what you'd like to achieve."></textarea><small>Please don't include highly sensitive details such as Social Security or account numbers.</small></div>
<div class="field-row">
<div class="field"><label for="cr-stake">Approximate amount at stake</label><select id="cr-stake" name="Amount at stake"><option>Not sure</option><option>Under $5,000</option><option>$5,000–$25,000</option><option>$25,000–$100,000</option><option>Over $100,000</option><option>Not about money</option></select></div>
<div class="field"><label for="cr-injury">Medical treatment involved?</label><select id="cr-injury" name="Medical treatment"><option>Not applicable</option><option>Yes, ongoing</option><option>Yes, completed</option><option>No</option></select></div>
</div>
<div class="field"><label for="cr-income">Household income (helps us flag free legal aid)</label><select id="cr-income" name="Income band"><option>Prefer not to say</option><option>Under $30,000</option><option>$30,000–$60,000</option><option>$60,000–$100,000</option><option>Over $100,000</option></select></div>
</fieldset>

<fieldset class="form-step" data-step="4" hidden><legend>How can we reach you?</legend>
<div class="field-row">
<div class="field"><label for="cr-name">Full name</label><input id="cr-name" name="Name" required autocomplete="name"></div>
<div class="field"><label for="cr-email">Email</label><input id="cr-email" name="Email" type="email" required autocomplete="email"></div>
</div>
<div class="field-row">
<div class="field"><label for="cr-phone">Phone</label><input id="cr-phone" name="Phone" type="tel" required autocomplete="tel"></div>
<div class="field"><label for="cr-zip">ZIP / postal code</label><input id="cr-zip" name="ZIP" autocomplete="postal-code"></div>
</div>
<div class="field-row">
<div class="field"><label for="cr-pref">Preferred contact</label><select id="cr-pref" name="Preferred contact"><option>Phone call</option><option>Text message</option><option>Email</option></select></div>
<div class="field"><label for="cr-time">Best time</label><select id="cr-time" name="Best time"><option>Any time</option><option>Morning</option><option>Afternoon</option><option>Evening</option></select></div>
</div>
{consent_block("case")}
<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">
</fieldset>

<div class="step-nav"><button class="btn btn-ghost" type="button" data-prev hidden>Back</button><button class="btn btn-gold" type="button" data-next>Continue</button><button class="btn btn-gold" type="submit" data-submit hidden>Submit my free review</button></div>
<p class="form-status" role="status"></p>
</form>
<div class="thanks" data-thanks hidden><h2>Thank you, your request is in.</h2><p>We'll review it and follow up using your preferred contact method. If you have a court date within days, also contact your court's self-help center or your state bar's lawyer referral service today.</p><p><a href="%ROOT%guides/">Read our guides</a> · <a href="%ROOT%tools/">Use free tools</a> · <a href="%ROOT%legal-aid/">Free legal aid</a></p></div>
<p class="micro">🔒 Your information is sent securely and used only as described in our <a href="%ROOT%privacy/">Privacy Policy</a>.</p>
</div>
</div></section>
<div class="container">
<section class="section"><div class="grid cards-3">
<div class="card static"><span class="card-icon">⏱️</span><h3>Deadlines are real</h3><p>Most legal claims have strict deadlines. Use our <a href="%ROOT%tools/deadline-finder/">deadline finder</a> and don't wait.</p></div>
<div class="card static"><span class="card-icon">💵</span><h3>Many lawyers work on contingency</h3><p>Injury and some employment lawyers are paid only if you win. See the <a href="%ROOT%tools/contingency-fee-calculator/">fee calculator</a>.</p></div>
<div class="card static"><span class="card-icon">🆓</span><h3>Free legal aid exists</h3><p>If your income is limited, <a href="%ROOT%legal-aid/">free legal aid</a> may handle your case at no cost.</p></div>
</div></section>
<section class="section faq narrow"><h2>Questions about the free case review</h2>
<details><summary>Is it really free?</summary><p>Yes. There's no charge to submit a request and no obligation to hire anyone.</p></details>
<details><summary>Is LegalPundits a law firm?</summary><p>No. We're an independent legal information publication. We don't give legal advice. Attorneys who contact you are independent; any agreement is between you and them.</p></details>
<details><summary>Who sees my information?</summary><p>Our intake team and, with your consent, one or more independent attorneys or legal service providers who handle your type of matter. See our Privacy Policy.</p></details>
<details><summary>What if I'm in Colorado?</summary><p>Colorado law restricts legal lead generation, so we don't route or sell Colorado requests. We'll reply with free resources instead.</p></details>
<details><summary>How fast will I hear back?</summary><p>We aim to respond within one business day. If you face a deadline within days, also contact your court's self-help center or your state bar's lawyer referral service immediately.</p></details>
</section></div>'''
    page("case-review/", "Free Case Review — Talk to a Lawyer About Your Legal Problem",
         "Free, no-obligation case review for accidents, employment, divorce, criminal, immigration, estate, housing, debt and business problems.",
         body, priority="0.95", crumbs=[("Free case review", "")], body_class="lead-page")


def simple_form_page(path, title, desc, intro_html, form_inner, form_name, submit_label, crumbs, after_html="", priority="0.6"):
    body = f'''<section class="page-head"><div class="container"><h1>{esc(title)}</h1>{intro_html}</div></section>
<div class="container form-layout">
<div class="form-card">
<form class="lp-form" data-lp-form="{form_name}" novalidate>
{form_inner}
<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">
<button class="btn btn-gold" type="submit">{esc(submit_label)}</button>
<p class="form-status" role="status"></p>
</form>
</div>
<div class="form-side">{after_html}</div>
</div>'''
    page(path, title, desc, body, priority=priority, crumbs=crumbs)


def build_ask():
    areas = "".join(f'<option>{esc(a["name"])}</option>' for a in AREAS)
    inner = f'''<input type="hidden" name="Form" value="Ask the Pundits">
<div class="field-row"><div class="field"><label for="ak-topic">Topic</label><select id="ak-topic" name="Topic" required><option value="">Select…</option>{areas}</select></div>
<div class="field"><label for="ak-state">State / country</label><select id="ak-state" name="State" data-state-select><option value="">Select…</option>{STATE_OPTIONS}<option>Outside the US</option></select></div></div>
<div class="field"><label for="ak-q">Your question</label><textarea id="ak-q" name="Question" rows="6" minlength="20" required placeholder="Keep it general: no names, account numbers or confidential details."></textarea></div>
<div class="field-row"><div class="field"><label for="ak-name">First name</label><input id="ak-name" name="Name" required></div>
<div class="field"><label for="ak-email">Email</label><input id="ak-email" name="Email" type="email" required></div></div>
<label class="check"><input type="checkbox" name="OK to publish anonymized" value="Yes"> <span>You may publish an anonymized version of my question with a general answer.</span></label>
<label class="check"><input type="checkbox" name="Wants attorney contact" value="Yes"> <span>I'd also like a free case review from an independent attorney.</span></label>
{consent_block("general")}'''
    side = '''<div class="box"><h3>How Ask the Pundits works</h3><ol><li>Send a general legal question.</li><li>We answer the most common questions in new guides and FAQs.</li><li>Need help with your specific facts? Tick the case review box.</li></ol></div>
<div class="box"><h3>Urgent?</h3><p>If you have a court date or deadline within days, use the <a href="%ROOT%case-review/">free case review</a> and contact your court's self-help center.</p></div>'''
    simple_form_page("ask/", "Ask the Pundits", "Send a general legal question to LegalPundits. We answer common questions in plain English.",
                     '<p class="lead">Have a general legal question? Ask it here. We turn the most common questions into free plain-English answers.</p>',
                     inner, "ask", "Send my question", [("Ask the Pundits", "")], side)


def build_attorneys():
    areas = "".join(f'<label class="check"><input type="checkbox" name="Practice areas" value="{esc(a["name"])}"> <span>{esc(a["name"])}</span></label>' for a in AREAS if a["slug"] != "lawyers-courts")
    inner = f'''<input type="hidden" name="Form" value="Attorney network application">
<div class="field-row"><div class="field"><label for="at-name">Attorney name</label><input id="at-name" name="Attorney name" required></div>
<div class="field"><label for="at-firm">Firm</label><input id="at-firm" name="Firm" required></div></div>
<div class="field-row"><div class="field"><label for="at-bar">Bar state(s) &amp; number</label><input id="at-bar" name="Bar admission" required></div>
<div class="field"><label for="at-web">Firm website</label><input id="at-web" name="Website" type="url" placeholder="https://"></div></div>
<div class="field-row"><div class="field"><label for="at-email">Email</label><input id="at-email" name="Email" type="email" required></div>
<div class="field"><label for="at-phone">Phone</label><input id="at-phone" name="Phone" type="tel"></div></div>
<fieldset class="field"><legend>Practice areas</legend><div class="check-grid">{areas}</div></fieldset>
<div class="field"><label for="at-geo">Cities / counties served</label><input id="at-geo" name="Service area" required></div>
<div class="field-row"><div class="field"><label for="at-int">Interested in</label><select id="at-int" name="Interest"><option>Case review referrals</option><option>Featured (sponsored) listing</option><option>Sponsored guide or tool</option><option>Expert contributor / reviewer</option><option>All of the above</option></select></div>
<div class="field"><label for="at-cap">Monthly new-case capacity</label><select id="at-cap" name="Capacity"><option>1–5</option><option>6–20</option><option>21–50</option><option>50+</option></select></div></div>
{consent_block("general")}'''
    side = '''<div class="box"><h3>Why join</h3><ul class="checks"><li>Consumers arrive pre-educated by our guides and tools</li><li>Intake captures issue, state, timing, stakes and deadlines</li><li>Filter by practice area and geography</li><li>Featured listings, sponsored tools and contributor bylines available</li></ul></div>
<div class="box"><h3>Compliance first</h3><p>Programs are structured to respect state advertising and referral rules. We do not route or sell Colorado leads. Sponsored placements are labelled as advertising.</p></div>'''
    simple_form_page("attorneys/", "For Attorneys: Join the LegalPundits Network",
                     "Attorneys and law firms: receive case review referrals, featured listings and contributor opportunities from LegalPundits.",
                     '<p class="lead">Reach people researching their legal problem at the moment they need help. Apply for case review referrals, featured listings and contributor opportunities.</p>',
                     inner, "attorney", "Apply to the network", [("For attorneys", "")], side, priority="0.7")


def build_advertise():
    packages = [
        ("Sponsored practice-area hub", "Exclusive sponsor badge and placement across one practice area's guides and tools."),
        ("Sponsored free tool", "Your brand on a calculator or generator, with a labelled call to action."),
        ("Weekly Legal Brief sponsor", "Top placement in our weekly newsletter."),
        ("Video & contest sponsorship", "Fund monthly Pundit Challenge prizes with branded recognition."),
        ("Featured attorney listings", "Labelled featured placement for law firms by city and practice area."),
        ("Domain, website or partnership", "Interested in LegalPundits.com itself, a joint venture or a strategic partnership."),
    ]
    cards = "".join(f'<div class="card static"><h3>{esc(a)}</h3><p>{esc(b)}</p></div>' for a, b in packages)
    inner = '''<input type="hidden" name="Form" value="Advertising / sponsorship enquiry">
<div class="field-row"><div class="field"><label for="ad-name">Name</label><input id="ad-name" name="Name" required></div>
<div class="field"><label for="ad-co">Company</label><input id="ad-co" name="Company"></div></div>
<div class="field-row"><div class="field"><label for="ad-email">Email</label><input id="ad-email" name="Email" type="email" required></div>
<div class="field"><label for="ad-int">Interest</label><select id="ad-int" name="Interest"><option>Sponsorship</option><option>Advertising</option><option>Featured attorney listing</option><option>Partnership</option><option>Website / domain acquisition</option><option>Other</option></select></div></div>
<div class="field-row"><div class="field"><label for="ad-bud">Monthly budget</label><select id="ad-bud" name="Budget"><option>Not sure</option><option>Under $500</option><option>$500–$2,000</option><option>$2,000–$10,000</option><option>$10,000+</option></select></div>
<div class="field"><label for="ad-start">Desired start</label><input id="ad-start" name="Start" placeholder="e.g. January 2027"></div></div>
<div class="field"><label for="ad-msg">Message</label><textarea id="ad-msg" name="Message" rows="4" required></textarea></div>'''
    body = f'''<section class="page-head"><div class="container"><h1>Advertise, Sponsor or Partner</h1><p class="lead">LegalPundits reaches people actively researching legal problems: accident victims, employees, families, small businesses and law students. All sponsored placements are clearly labelled.</p></div></section>
<div class="container"><div class="grid cards-3">{cards}</div></div>
<div class="container form-layout section"><div class="form-card">
<form class="lp-form" data-lp-form="advertise" novalidate>{inner}
<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">
<button class="btn btn-gold" type="submit">Send enquiry</button><p class="form-status" role="status"></p></form></div>
<div class="form-side"><div class="box"><h3>Interested in the domain or the whole website?</h3><p>For domain, website, sponsorship, advertising or partnership discussions, you can also <a href="{SITE["owner_contact_url"]}" target="_blank" rel="noopener">contact the owner directly</a>.</p></div>
<div class="box"><h3>Our standards</h3><p>We don't accept ads that mislead consumers, impersonate law firms or promise outcomes. Editorial content is never for sale.</p></div></div></div>'''
    page("advertise/", "Advertise, Sponsor or Partner with LegalPundits", "Sponsorship, advertising, featured listings and partnership opportunities on LegalPundits.com.",
         body, crumbs=[("Advertise", "")])


def build_support():
    tiers = [
        ("Supporter", "$5/mo", "Keeps a guide reviewed and current.", "5 monthly"),
        ("Advocate", "$25/mo", "Funds a new free tool feature each quarter.", "25 monthly"),
        ("Pundit Patron", "$100/mo", "Sponsors a monthly contest prize.", "100 monthly"),
        ("Founding Sponsor", "$1,000+", "Named recognition on our supporters page (optional).", "1000 one-time"),
    ]
    tier_html = "".join(f'<button class="tier" type="button" data-tier="{v}"><span class="tier-name">{n}</span><span class="tier-price">{p}</span><span class="tier-desc">{d}</span></button>' for n, p, d, v in tiers)
    uses = [("Operations", 35, "Hosting, research tools, legal review and keeping every guide current."),
            ("Promotions & marketing", 25, "Reaching people who need legal information at the moment they need it."),
            ("Hiring talent", 25, "Paying writers, attorney reviewers, researchers and video editors."),
            ("Contests & prizes", 15, "Monthly Pundit Challenge prizes for students and creators.")]
    bars = "".join(f'<div class="use"><div class="use-head"><strong>{esc(n)}</strong><span>{p}%</span></div><div class="bar"><span style="width:{p}%"></span></div><p>{esc(d)}</p></div>' for n, p, d in uses)
    inner = '''<input type="hidden" name="Form" value="Support pledge">
<div class="field-row"><div class="field"><label for="sp-amt">Amount (USD)</label><input id="sp-amt" name="Amount" type="number" min="1" step="1" required placeholder="25"></div>
<div class="field"><label for="sp-freq">Frequency</label><select id="sp-freq" name="Frequency"><option>Monthly</option><option>One-time</option><option>Yearly</option></select></div></div>
<div class="field"><label for="sp-use">Direct my support to</label><select id="sp-use" name="Allocation"><option>Where it's needed most</option><option>Operations</option><option>Promotions &amp; marketing</option><option>Hiring talent</option><option>Contests &amp; prizes</option></select></div>
<div class="field-row"><div class="field"><label for="sp-name">Name</label><input id="sp-name" name="Name" required></div>
<div class="field"><label for="sp-email">Email</label><input id="sp-email" name="Email" type="email" required></div></div>
<div class="field"><label for="sp-msg">Message (optional)</label><textarea id="sp-msg" name="Message" rows="3"></textarea></div>
<label class="check"><input type="checkbox" name="Public recognition" value="Yes"> <span>You may list my name as a supporter.</span></label>
<label class="check"><input type="checkbox" name="Business sponsor" value="Yes"> <span>I'm supporting on behalf of a business and would like sponsor recognition.</span></label>'''
    body = f'''<section class="page-head"><div class="container"><h1>Support Free Legal Help</h1><p class="lead">Every guide, calculator and contest on LegalPundits is free. Reader and sponsor support keeps it that way and funds what's next.</p></div></section>
<div class="container">
<section class="section"><h2>Choose a level</h2><div class="tier-grid">{tier_html}</div></section>
<section class="section split">
<div><h2>Where your support goes</h2><div class="uses">{bars}</div></div>
<div class="form-card"><h2>Make a pledge</h2><p class="small">Submit your pledge and we'll email you a secure payment link with a receipt. Contributions are not tax-deductible.</p>
<form class="lp-form" data-lp-form="support" novalidate>{inner}
<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">
<button class="btn btn-gold" type="submit">Pledge my support</button><p class="form-status" role="status"></p></form></div>
</section>
<section class="section grid cards-3">
<div class="card static"><span class="card-icon">📣</span><h3>Promotions</h3><p>Support helps us reach people searching for legal answers after accidents, layoffs and evictions.</p></div>
<div class="card static"><span class="card-icon">🧑‍💼</span><h3>Hiring</h3><p>We pay legal writers, attorney reviewers and student researchers. See <a href="%ROOT%careers/">open roles</a>.</p></div>
<div class="card static"><span class="card-icon">🏆</span><h3>Contests</h3><p>Prizes reward the best plain-English explainers. See the <a href="%ROOT%contests/">Pundit Challenge</a>.</p></div>
</section></div>'''
    page("support/", "Support LegalPundits — Donate to Keep Legal Help Free",
         "Support LegalPundits with a monthly or one-time contribution that funds operations, promotion, hiring talent and contest prizes.",
         body, priority="0.7", crumbs=[("Support", "")])


CONTESTS = [
    ("Explain It Like a Pundit", "✍️", "Write a 500–800 word plain-English explainer on any consumer legal topic. Judged on accuracy, clarity and usefulness.", "$250 + featured publication", "Essay"),
    ("60-Second Law", "🎬", "Create a video of 60 seconds or less explaining one legal right or myth. Upload to YouTube or Drive and share the link.", "$250 + featured on our video page", "Video"),
    ("Legal IQ Leaderboard", "🧠", "Play the daily Legal IQ quiz, then submit your best streak and score for the month.", "$100 gift card", "Quiz"),
]


def build_contests():
    cards = "".join(f'<div class="contest-card"><span class="card-icon" aria-hidden="true">{ic}</span><h3>{esc(n)}</h3><p>{esc(d)}</p><p class="prize">🏅 Prize: {esc(p)}</p><p class="countdown" data-countdown>Closes at the end of this month</p><a class="btn btn-gold btn-sm" href="#enter" data-contest="{esc(n)}">Enter now</a></div>' for n, ic, d, p, _ in CONTESTS)
    opts = "".join(f"<option>{esc(n)}</option>" for n, *_ in CONTESTS)
    inner = f'''<input type="hidden" name="Form" value="Contest entry">
<div class="field"><label for="ct-c">Contest</label><select id="ct-c" name="Contest" required>{opts}</select></div>
<div class="field-row"><div class="field"><label for="ct-name">Full name</label><input id="ct-name" name="Name" required></div>
<div class="field"><label for="ct-email">Email</label><input id="ct-email" name="Email" type="email" required></div></div>
<div class="field-row"><div class="field"><label for="ct-loc">Country & state/province</label><input id="ct-loc" name="Location" required></div>
<div class="field"><label for="ct-school">School / organisation (optional)</label><input id="ct-school" name="School or organisation"></div></div>
<div class="field"><label for="ct-link">Link to your entry (Google Doc, Drive, YouTube) or quiz score</label><input id="ct-link" name="Entry link or score" required></div>
<div class="field"><label for="ct-title">Entry title</label><input id="ct-title" name="Entry title" required></div>
<label class="check"><input type="checkbox" name="Age 18+" value="Yes" required> <span>I am 18 or older (or the age of majority where I live).</span></label>
<label class="check"><input type="checkbox" name="Original work" value="Yes" required> <span>My entry is my own original work and I accept the official rules.</span></label>'''
    body = f'''<section class="page-head"><div class="container"><p class="eyebrow">Monthly · Free to enter · Skill-based</p><h1>The Pundit Challenge</h1><p class="lead">Can you explain the law better than the pros? Enter our monthly contests, win prizes and get featured to thousands of readers.</p></div></section>
<div class="container"><div class="contest-grid">{cards}</div>
<section class="section form-layout" id="enter"><div class="form-card"><h2>Enter this month's challenge</h2>
<form class="lp-form" data-lp-form="contest" novalidate>{inner}
<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">
<button class="btn btn-gold" type="submit">Submit my entry</button><p class="form-status" role="status"></p></form></div>
<div class="form-side"><div class="box"><h3>Want to sponsor a prize?</h3><p>Law firms, legal-tech companies and schools can fund prizes with branded recognition. <a href="%ROOT%advertise/">Sponsor a contest →</a></p></div>
<div class="box"><h3>Practice for the leaderboard</h3><p><a class="btn btn-teal btn-sm" href="%ROOT%quiz/">Play today's Legal IQ quiz</a></p></div></div></section>
<section class="section rules narrow"><h2>Official rules (summary)</h2>
<ol>
<li><strong>No purchase necessary.</strong> Entry is free. Void where prohibited or restricted by law. Residents of Quebec are not eligible.</li>
<li><strong>Eligibility.</strong> Open to individuals 18+ (or the age of majority in their jurisdiction). Employees of LegalPundits and their immediate families are not eligible.</li>
<li><strong>Entry period.</strong> Each contest runs from the 1st to the last day of the calendar month (11:59 p.m. US Eastern). One entry per person per contest per month.</li>
<li><strong>Judging.</strong> These are skill-based contests. Entries are judged by the LegalPundits editorial team on accuracy (40%), clarity (30%), usefulness (20%) and originality (10%). Quiz leaderboard prizes go to the highest verified score; ties are broken by earliest submission.</li>
<li><strong>Prizes.</strong> Prizes are as listed for the month. Winners are notified by email within 15 days after the month ends and must respond within 14 days. Prizes may be substituted with equal or greater value. Winners are responsible for applicable taxes.</li>
<li><strong>Content.</strong> Entries must be original, accurate and must not contain confidential client information or legal advice to a specific person. By entering, you grant LegalPundits a non-exclusive licence to publish and promote your entry with credit.</li>
<li><strong>Privacy.</strong> Entry information is used as described in our <a href="%ROOT%privacy/">Privacy Policy</a>.</li>
</ol></section></div>'''
    page("contests/", "Pundit Challenge — Monthly Legal Explainer Contests & Prizes",
         "Free monthly contests for the best plain-English legal explainer, 60-second law video and Legal IQ quiz score.",
         body, priority="0.7", crumbs=[("Contests", "")])


def build_careers():
    roles = [
        ("Legal Content Writer (freelance, remote)", "Write plain-English guides on consumer legal topics from primary sources. Paralegal, JD or legal journalism background preferred."),
        ("Attorney Reviewer (per-review, remote)", "Licensed attorneys review guides in their practice area for accuracy and sign off on review dates."),
        ("Legal Research Assistant", "Track statute changes, deadlines and dollar limits by state; ideal for law students."),
        ("Video Editor / Short-form Creator", "Turn guides into short explainer videos for YouTube and social."),
        ("Campus Ambassador", "Represent LegalPundits at your law school, promote contests and recruit contributors."),
        ("Partnerships & Sales Associate", "Grow sponsorships, featured listings and attorney partnerships (commission-based)."),
    ]
    role_html = "".join(f'<div class="card static"><h3>{esc(r)}</h3><p>{esc(d)}</p><a class="card-link" href="#apply" data-role="{esc(r)}">Apply →</a></div>' for r, d in roles)
    opts = "".join(f"<option>{esc(r)}</option>" for r, _ in roles)
    inner = f'''<input type="hidden" name="Form" value="Job application">
<div class="field"><label for="jb-role">Role</label><select id="jb-role" name="Role" required>{opts}<option>Student contributor program</option><option>Other</option></select></div>
<div class="field-row"><div class="field"><label for="jb-name">Full name</label><input id="jb-name" name="Name" required></div>
<div class="field"><label for="jb-email">Email</label><input id="jb-email" name="Email" type="email" required></div></div>
<div class="field-row"><div class="field"><label for="jb-loc">Location / time zone</label><input id="jb-loc" name="Location"></div>
<div class="field"><label for="jb-link">Portfolio or LinkedIn URL</label><input id="jb-link" name="Portfolio" type="url" placeholder="https://"></div></div>
<div class="field-row"><div class="field"><label for="jb-bar">Bar admission (attorneys)</label><input id="jb-bar" name="Bar admission"></div>
<div class="field"><label for="jb-hours">Availability</label><select id="jb-hours" name="Availability"><option>A few hours a week</option><option>10–20 hours a week</option><option>Part-time</option><option>Full-time</option></select></div></div>
<div class="field"><label for="jb-note">Why you? (short note)</label><textarea id="jb-note" name="Cover note" rows="4" required></textarea></div>
{consent_block("general")}'''
    body = f'''<section class="page-head"><div class="container"><h1>Careers &amp; Write for Us</h1><p class="lead">Help millions of people understand the law. We're building a remote team of writers, reviewers, researchers and creators.</p></div></section>
<div class="container"><div class="grid cards-3">{role_html}</div>
<section class="section form-layout" id="apply"><div class="form-card"><h2>Apply</h2>
<form class="lp-form" data-lp-form="careers" novalidate>{inner}
<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">
<button class="btn btn-gold" type="submit">Send application</button><p class="form-status" role="status"></p></form></div>
<div class="form-side"><div class="box"><h3>Student Contributor Program</h3><p>Law students can publish bylined explainers reviewed by our editors, a strong addition to any résumé.</p></div>
<div class="box"><h3>How we work</h3><ul class="checks"><li>Remote and flexible</li><li>Paid per piece or per review</li><li>Clear style guide and editorial support</li></ul></div></div></section></div>'''
    page("careers/", "Careers & Write for LegalPundits", "Remote roles for legal writers, attorney reviewers, research assistants, video creators and campus ambassadors.",
         body, priority="0.6", crumbs=[("Careers", "")])


def build_contact():
    inner = '''<input type="hidden" name="Form" value="Contact form">
<div class="field"><label for="co-reason">Reason</label><select id="co-reason" name="Reason" required data-reason-select>
<option value="General question">General question</option><option value="Correction">Report an error / correction</option>
<option value="Advertising or partnership">Advertising, sponsorship or partnership</option><option value="Press">Press</option>
<option value="Privacy request">Privacy request</option><option value="Copyright or trademark">Copyright or trademark concern</option><option value="Other">Other</option></select></div>
<div class="field-row"><div class="field"><label for="co-name">Name</label><input id="co-name" name="Name" required autocomplete="name"></div>
<div class="field"><label for="co-email">Email</label><input id="co-email" name="Email" type="email" required autocomplete="email"></div></div>
<div class="field"><label for="co-url">Page URL (if relevant)</label><input id="co-url" name="Page" type="url" placeholder="https://"></div>
<div class="field"><label for="co-msg">Message</label><textarea id="co-msg" name="Message" rows="6" required></textarea></div>
<p class="small muted">Need help with your own legal problem? Use the <a href="%ROOT%case-review/">free case review</a>, since we can't give legal advice by message.</p>'''
    side = f'''<div class="box"><h3>Domain, website, sponsorship or partnership?</h3><p>If you're interested in this website, the LegalPundits.com domain name, sponsorship, advertising or a partnership, <a href="{SITE["owner_contact_url"]}" target="_blank" rel="noopener">contact the owner here</a>.</p></div>
<div class="box"><h3>Corrections</h3><p>We review every correction request against primary sources and update the page's review date when we change it.</p></div>'''
    simple_form_page("contact/", "Contact LegalPundits", "Contact LegalPundits with questions, corrections, partnership or press enquiries.",
                     '<p class="lead">Questions, corrections, partnerships or press: send us a message and we\'ll get back to you.</p>',
                     inner, "contact", "Send message", [("Contact", "")], side, priority="0.5")


# ---------------------------------------------------------------- resources

def build_news():
    items = NEWS.get("items", [])
    sources = sorted({n.get("source", "") for n in items if n.get("source")})
    chips = '<button class="chip active" type="button" data-filter="all">All</button>' + "".join(f'<button class="chip" type="button" data-filter="{esc(s)}">{esc(s)}</button>' for s in sources)
    lis = "".join(news_li(n) for n in items[:80]) or '<li class="muted">Headlines will appear after the next automatic refresh.</li>'
    feeds = "".join(f'<li>{esc(f["name"])} <span class="muted">— {esc(f["topic"])}</span></li>' for f in FEEDS)
    upd = NEWS.get("updated", "")
    body = f'''<section class="page-head"><div class="container"><h1>Legal News Desk</h1><p class="lead">Headlines from leading legal publishers, from Supreme Court coverage to legal tech, refreshed automatically every six hours. Every headline links to the original source.</p>
<p class="small muted">Last refreshed: <span data-news-updated>{esc(upd[:16].replace("T", " ")) + " UTC" if upd else "pending"}</span></p></div></section>
<div class="container split wide-left">
<div><div class="chips" data-news-filters>{chips}</div>
<ul class="news-list" data-news-widget data-limit="80">{lis}</ul></div>
<aside class="stack"><div class="box"><h3>Our sources</h3><ul class="link-list plain">{feeds}</ul><p class="small muted">We publish headlines and links only. Read full stories on each publisher's site.</p></div>
<div class="box cta-box"><h3>Does the news affect you?</h3><p>Get a free, no-obligation case review.</p><a class="btn btn-gold btn-block" href="%ROOT%case-review/">Free case review</a></div>{ad("sidebar")}</aside>
</div>'''
    page("news/", "Legal News Today — Headlines from Leading Legal Publishers",
         "Auto-updated legal news headlines: Supreme Court, courts, legal profession, legal tech and more, linked to the original publishers.",
         body, priority="0.7", crumbs=[("News", "")])


def video_channel_card(c):
    pl = "UU" + c["id"][2:]
    return (f'<div class="card video-card static"><div class="video-facade" data-playlist="{pl}" role="button" tabindex="0" aria-label="Play latest uploads from {esc(c["name"])}">'
            f'<span class="play" aria-hidden="true">▶</span><span class="vf-label">Latest uploads · {esc(c["name"])}</span></div>'
            f'<h3>{esc(c["name"])}</h3><p>{esc(c["about"])}</p><a class="card-link" href="https://www.youtube.com/channel/{c["id"]}" target="_blank" rel="noopener">Visit channel →</a></div>')


def build_videos():
    latest = VIDEOS.get("items", [])[:12]
    latest_html = ""
    if latest:
        cards = "".join(f'<div class="card video-card static"><div class="video-facade thumb" data-video="{esc(v["id"])}" role="button" tabindex="0" aria-label="Play {esc(v["title"])}" style="background-image:url(https://i.ytimg.com/vi/{esc(v["id"])}/hqdefault.jpg)"><span class="play" aria-hidden="true">▶</span></div><h3>{esc(v["title"])}</h3><p class="muted small">{esc(v.get("channel", ""))} · {esc(v.get("date", "")[:10])}</p></div>' for v in latest)
        latest_html = f'<section class="section"><h2>Latest explainers</h2><div class="grid cards-3">{cards}</div></section>'
    more = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{esc(n)}</a> <span class="muted">— {esc(d)}</span></li>' for n, u, d in MORE_CHANNELS)
    body = f'''<section class="page-head"><div class="container"><h1>Video Library: The Law, Explained</h1><p class="lead">Explainer videos from practicing lawyers and legal educators. New uploads appear automatically. Videos play from YouTube and remain the property of their creators.</p></div></section>
<div class="container">{latest_html}
<section class="section"><h2>Featured channels</h2><div class="grid cards-3">{"".join(video_channel_card(c) for c in CHANNELS)}</div></section>
{ad("in_article")}
<section class="section"><h2>More legal creators worth following</h2><ul class="link-list plain">{more}</ul></section>
<section class="section narrow"><div class="box"><h3>Make a video, win a prize</h3><p>Enter the monthly <a href="%ROOT%contests/">60-Second Law</a> challenge.</p></div>
<p class="small muted">Videos are general information, not legal advice. Inclusion doesn't imply endorsement by or of any creator.</p></section></div>'''
    page("videos/", "Legal Video Library — Lawyers Explain the Law",
         "Watch legal explainer videos from practicing lawyers and legal educators, refreshed automatically.",
         body, priority="0.6", crumbs=[("Videos", "")])


def build_glossary():
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    nav = "".join(f'<a href="#letter-{l}">{l}</a>' for l in letters)
    groups = ""
    for l in letters:
        items = "".join(f'<div class="term" id="{slugify(t)}" data-term="{esc(t.lower())}"><dt>{esc(t)}</dt><dd>{esc(d)}</dd></div>' for t, d in GLOSSARY if t[0].upper() == l)
        groups += f'<section class="letter-group" id="letter-{l}"><h2>{l}</h2><dl>{items}</dl></section>'
    gl = json.dumps([[t, d] for t, d in GLOSSARY], ensure_ascii=False)
    body = f'''<section class="page-head"><div class="container"><h1>Legal Glossary</h1><p class="lead">{len(GLOSSARY)} legal terms explained in plain English.</p>
<div class="box term-box inline"><p class="eyebrow">Term of the day</p><h3 data-term-title>…</h3><p data-term-def></p></div>
<label class="sr-only" for="gl-search">Filter terms</label><input id="gl-search" class="big-search" type="search" placeholder="Filter terms… e.g. tort, lien, probate" data-glossary-filter></div></section>
<div class="container"><nav class="az" aria-label="Jump to letter">{nav}</nav>{groups}{ad("footer")}</div>
<script type="application/json" id="glossary-data">{gl}</script>'''
    ld = [{"@context": "https://schema.org", "@type": "DefinedTermSet", "name": "LegalPundits Legal Glossary",
           "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in GLOSSARY]}]
    page("glossary/", "Legal Glossary — Legal Terms in Plain English", "Plain-English definitions of legal terms, from acquittal to wrongful termination.",
         body, priority="0.7", crumbs=[("Glossary", "")], jsonld=ld)


def build_quiz():
    data = json.dumps(QUIZ, ensure_ascii=False)
    body = f'''<section class="page-head"><div class="container"><p class="eyebrow">New questions every day</p><h1>Legal IQ Daily Quiz</h1><p class="lead">Five questions, plain-English explanations, and a fresh set tomorrow. Post your best monthly score to the <a href="%ROOT%contests/">leaderboard contest</a>.</p></div></section>
<div class="container narrow"><div class="quiz" data-daily-quiz><p class="muted">Loading today's questions…</p></div>
<p class="small muted">Questions describe general US law and are for education only.</p></div>
<script type="application/json" id="quiz-data">{data}</script>'''
    page("quiz/", "Legal IQ Daily Quiz — Test Your Legal Knowledge", "A free daily five-question legal quiz with plain-English explanations.",
         body, priority="0.6", crumbs=[("Legal IQ quiz", "")])


def build_global():
    def country_links(c):
        return "".join('<li><a href="%s" target="_blank" rel="noopener">%s</a></li>' % (u, esc(n)) for n, u in c["links"])
    blocks = "".join(f'<section class="country"><h2>{c["flag"]} {esc(c["country"])}</h2><p>{esc(c["note"])}</p><ul class="link-list plain">{country_links(c)}</ul></section>' for c in GLOBAL_DESK)
    body = f'''<section class="page-head"><div class="container"><h1>Global Law Desk</h1><p class="lead">LegalPundits focuses on US law, but legal questions are global. Start with these official and non-profit resources in your country.</p></div></section>
<div class="container"><div class="country-grid">{blocks}</div>
<p class="small muted">Links go to official government, court, bar or non-profit sources. LegalPundits is not affiliated with these organisations.</p></div>{cta_band(title="In the US and need help?")}'''
    page("global/", "Global Law Desk — Free Legal Help in the US, Canada, UK, India & Australia",
         "Official free legal help and legal information resources for the United States, Canada, the United Kingdom, India and Australia.",
         body, priority="0.6", crumbs=[("Global Law Desk", "")])


def build_legal_aid():
    body = f'''<section class="page-head"><div class="container"><h1>Free Legal Aid Finder</h1><p class="lead">If money is tight, free or low-cost legal help may be available. Here's where to look, in order.</p></div></section>
<div class="container narrow prose">
<h2>1. Your state's legal aid network</h2><p><a href="https://www.lawhelp.org/" target="_blank" rel="noopener">LawHelp.org</a> connects you to free legal aid programs and self-help resources by state. The <a href="https://www.lsc.gov/" target="_blank" rel="noopener">Legal Services Corporation</a> funds legal aid organisations nationwide.</p>
<h2>2. Free online advice</h2><p><a href="https://abafreelegalanswers.org/" target="_blank" rel="noopener">ABA Free Legal Answers</a> lets income-eligible users post civil legal questions to volunteer lawyers in their state. Criminal matters aren't covered.</p>
<h2>3. Court self-help centers</h2><p>Most state court systems run self-help centers with forms and instructions for common cases such as small claims, eviction, divorce and protective orders.</p>
<h2>4. Bar referral services</h2><p>State and local bar associations run lawyer referral services, often with a low-cost first consultation. See the <a href="https://www.americanbar.org/groups/legal_services/flh-home/" target="_blank" rel="noopener">ABA's find legal help</a> directory.</p>
<h2>5. Law school clinics</h2><p>Many law schools run supervised clinics that help with housing, immigration, family, consumer and criminal matters.</p>
<h2>6. Government help</h2><p>See <a href="https://www.usa.gov/legal-aid" target="_blank" rel="noopener">USA.gov's legal aid page</a> for programs for seniors, veterans, people with disabilities and more.</p>
<div class="callout">Criminal charge with possible jail time? You have a constitutional right to a court-appointed lawyer if you can't afford one. Ask at your first court appearance.</div>
</div>{cta_band(title="Not eligible for legal aid?", text="Many attorneys offer free consultations, and injury lawyers usually work on contingency. Request a free case review.")}'''
    page("legal-aid/", "Free Legal Aid Finder — Where to Get Free Legal Help",
         "Where to find free and low-cost legal help: legal aid, ABA Free Legal Answers, court self-help centers, bar referral services and law school clinics.",
         body, priority="0.7", crumbs=[("Free legal aid", "")])


def build_static_pages():
    for path, title, desc, content, crumb in [
        ("about/", "About LegalPundits", "About LegalPundits.com, an independent plain-English legal information publication.", LP.ABOUT, "About"),
        ("editorial-policy/", "Editorial Policy", "How LegalPundits researches, writes, reviews and corrects legal content.", LP.EDITORIAL, "Editorial policy"),
        ("disclaimer/", "Legal Disclaimer & Advertising Disclosure", "LegalPundits is not a law firm and does not provide legal advice.", LP.DISCLAIMER, "Disclaimer"),
        ("privacy/", "Privacy Policy", "How LegalPundits collects, uses and protects information, including cookies and Google AdSense.", LP.PRIVACY.replace("<h2>Information collected automatically</h2>", '<h2 id="cookies">Information collected automatically</h2>'), "Privacy"),
        ("terms/", "Terms of Use", "Terms governing use of LegalPundits.com.", LP.TERMS, "Terms"),
        ("trademark/", "Trademark & Copyright Disclosure", "How the LegalPundits name is used, no-affiliation statement, and third-party trademark and copyright policy.", LP.TRADEMARK, "Trademark & copyright"),
    ]:
        body = f'<section class="page-head"><div class="container"><h1>{esc(title)}</h1></div></section><div class="container narrow prose">{content}</div>'
        page(path, title, desc, body, priority="0.4", crumbs=[(crumb, "")])


def build_sitemap_html():
    groups = {}
    for p in PAGES:
        groups.setdefault(p["kind"], []).append(p)
    names = {"page": "Pages", "guide": "Guides", "tool": "Tools"}
    out = ""
    for k in ("guide", "tool", "page"):
        lis = "".join(f'<li><a href="%ROOT%{p["path"]}">{esc(p["title"])}</a></li>' for p in sorted(groups.get(k, []), key=lambda x: x["title"]))
        out += f"<section><h2>{names[k]}</h2><ul class='link-list plain cols'>{lis}</ul></section>"
    body = f'<section class="page-head"><div class="container"><h1>Site Map</h1></div></section><div class="container">{out}</div>'
    layout("sitemap/", "Site Map", "Every page on LegalPundits.com.", body, crumbs=[("Site map", "")])
    register("sitemap/", "Site Map", "Every page on LegalPundits.com.", "page", "0.3")


def build_404():
    body = '''<section class="page-head center"><div class="container narrow"><h1>Page not found</h1><p class="lead">That page doesn't exist, but your answer probably does.</p>
<p><a class="btn btn-gold" href="%ROOT%guides/">Browse guides</a> <a class="btn btn-ghost" href="%ROOT%tools/">Free tools</a> <a class="btn btn-ghost" href="%ROOT%case-review/">Free case review</a></p></div></section>'''
    # GitHub Pages serves 404.html at any URL depth, so links are made relative to a
    # <base> chosen at runtime: the repo sub-path on github.io, or "/" on the custom domain.
    out = layout("404/", "Page not found", "Page not found.", body)
    doc = out.read_text(encoding="utf-8")
    doc = doc.replace('href="../', 'href="').replace('src="../', 'src="').replace('data-root="../"', 'data-root=""')
    base = ("<script>(function(){var b=location.hostname.endsWith('github.io')?'/'+location.pathname.split('/')[1]+'/':'/';"
            "document.write('<base href=\"'+b+'\">');document.documentElement.setAttribute('data-root',b);})();</script>")
    doc = doc.replace("<head>\n", "<head>\n" + base + "\n", 1)
    doc = doc.replace("<head>\n", "<head>\n<meta name=\"robots\" content=\"noindex\">\n", 1)
    (ROOT / "404.html").write_text(doc, encoding="utf-8")
    out.unlink()
    out.parent.rmdir()


def build_meta_files():
    today = datetime.date.today().isoformat()
    urls = "".join(f'<url><loc>{SITE["url"]}/{p["path"]}</loc><lastmod>{today}</lastmod><priority>{p["priority"]}</priority></url>' for p in PAGES)
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + urls + "</urlset>\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE['url']}/sitemap.xml\n", encoding="utf-8")
    (ROOT / "ads.txt").write_text("google.com, pub-6620975821265271, DIRECT, f08c47fec0942fa0\n", encoding="utf-8")
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")
    # search index
    idx = [{"t": p["title"], "d": p["description"], "u": p["path"], "k": p["kind"]} for p in PAGES if p["path"] not in ("sitemap/",)]
    idx += [{"t": t, "d": d, "u": "glossary/#" + slugify(t), "k": "term"} for t, d in GLOSSARY]
    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "data" / "search-index.json").write_text(json.dumps(idx, ensure_ascii=False), encoding="utf-8")
    # RSS feed of guides
    items = "".join(f"<item><title>{esc(g['title'])}</title><link>{SITE['url']}/guides/{g['slug']}/</link><guid>{SITE['url']}/guides/{g['slug']}/</guid><description>{esc(g['description'])}</description></item>" for g in GUIDES)
    (ROOT / "feed.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>LegalPundits Guides</title><link>{SITE["url"]}/</link><description>{esc(SITE["description"])}</description>{items}</channel></rss>\n', encoding="utf-8")


def main():
    build_home(); build_guides(); build_topics(); build_tools(); build_case_review()
    build_ask(); build_attorneys(); build_advertise(); build_support(); build_contests(); build_careers(); build_contact()
    build_news(); build_videos(); build_glossary(); build_quiz(); build_global(); build_legal_aid(); build_static_pages()
    build_sitemap_html(); build_404(); build_meta_files()
    print("Built %d pages (%d guides, %d tools)." % (len(PAGES), len(GUIDES), len(TOOLS)))


if __name__ == "__main__":
    main()
