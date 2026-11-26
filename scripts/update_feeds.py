#!/usr/bin/env python3
"""Refresh data/news.json and data/videos.json from public RSS/Atom feeds.

Standard library only. Run by .github/workflows/auto-refresh.yml every 6 hours.
Only headlines, links, dates and video IDs are stored; no article text is copied.
"""
import datetime as dt
import email.utils
import html
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from data import FEEDS, CHANNELS  # noqa: E402

UA = "Mozilla/5.0 (compatible; LegalPunditsBot/1.0; +https://legalpundits.com/about/)"
NS = {"atom": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015",
      "media": "http://search.yahoo.com/mrss/"}
NOW = dt.datetime.now(dt.timezone.utc)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read()


def clean(text):
    text = html.unescape(re.sub(r"<[^>]+>", "", text or ""))
    return re.sub(r"\s+", " ", text).strip()


def parse_date(s):
    if not s:
        return None
    s = s.strip()
    try:
        d = email.utils.parsedate_to_datetime(s)
    except Exception:
        try:
            d = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
        except Exception:
            return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=dt.timezone.utc)
    return d.astimezone(dt.timezone.utc)


def parse_feed(raw):
    root = ET.fromstring(raw)
    items = []
    for it in root.iter("item"):  # RSS 2.0
        items.append({"title": clean(it.findtext("title")), "link": (it.findtext("link") or "").strip(),
                      "date": parse_date(it.findtext("pubDate") or it.findtext("{http://purl.org/dc/elements/1.1/}date"))})
    for en in root.iter("{http://www.w3.org/2005/Atom}entry"):  # Atom
        link = ""
        for l in en.findall("atom:link", NS):
            if l.get("rel", "alternate") == "alternate":
                link = l.get("href", ""); break
        items.append({"title": clean(en.findtext("atom:title", default="", namespaces=NS)), "link": link,
                      "date": parse_date(en.findtext("atom:published", default="", namespaces=NS) or en.findtext("atom:updated", default="", namespaces=NS)),
                      "video": en.findtext("yt:videoId", default="", namespaces=NS)})
    return [i for i in items if i["title"] and (i["link"] or i.get("video"))]


def load(rel):
    p = ROOT / rel
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {"updated": "", "items": []}


def update_news():
    old = load("data/news.json")
    old_by_src = {}
    for it in old.get("items", []):
        old_by_src.setdefault(it.get("source"), []).append(it)
    out = []
    for f in FEEDS:
        try:
            items = parse_feed(fetch(f["url"]))
            items = [i for i in items if not i["date"] or (NOW - i["date"]).days <= 30]
            items.sort(key=lambda i: i["date"] or NOW, reverse=True)
            got = [{"title": i["title"][:220], "link": i["link"], "source": f["name"], "topic": f["topic"],
                    "date": (i["date"] or NOW).isoformat()} for i in items[:15]]
            out.extend(got)
            print("ok   %-34s %d" % (f["name"], len(got)))
        except Exception as e:  # keep previous items for this source
            out.extend(old_by_src.get(f["name"], []))
            print("fail %-34s %s" % (f["name"], e))
    seen, uniq = set(), []
    for it in sorted(out, key=lambda x: x["date"], reverse=True):
        if it["link"] in seen:
            continue
        seen.add(it["link"]); uniq.append(it)
    data = {"updated": NOW.isoformat(timespec="minutes"), "items": uniq[:150]}
    if uniq:
        (ROOT / "data" / "news.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    return len(uniq)


def update_videos():
    old = load("data/videos.json")
    old_by_ch = {}
    for it in old.get("items", []):
        old_by_ch.setdefault(it.get("channel"), []).append(it)
    out = []
    for c in CHANNELS:
        try:
            items = parse_feed(fetch("https://www.youtube.com/feeds/videos.xml?channel_id=" + c["id"]))
            items = [i for i in items if i.get("video")]
            items.sort(key=lambda i: i["date"] or NOW, reverse=True)
            got = [{"id": i["video"], "title": i["title"][:200], "channel": c["name"], "date": (i["date"] or NOW).isoformat()} for i in items[:4]]
            out.extend(got)
            print("ok   %-34s %d" % (c["name"], len(got)))
        except Exception as e:
            out.extend(old_by_ch.get(c["name"], []))
            print("fail %-34s %s" % (c["name"], e))
    out.sort(key=lambda x: x["date"], reverse=True)
    if out:
        (ROOT / "data" / "videos.json").write_text(json.dumps({"updated": NOW.isoformat(timespec="minutes"), "items": out[:28]}, ensure_ascii=False, indent=1), encoding="utf-8")
    return len(out)


if __name__ == "__main__":
    (ROOT / "data").mkdir(exist_ok=True)
    n = update_news()
    v = update_videos()
    print("news items: %d, videos: %d" % (n, v))
