"""Site-wide configuration for LegalPundits.com."""

SITE = {
    "name": "LegalPundits",
    "domain": "LegalPundits.com",
    # Canonical production URL (used for canonical tags, sitemap, Open Graph).
    "url": "https://legalpundits.com",
    "tagline": "Plain-English law. Free tools. Real help.",
    "description": (
        "LegalPundits explains the law in plain English, with free legal calculators, "
        "deadline finders, letter generators, legal news and a free case review."
    ),
    "adsense_client": "ca-pub-6620975821265271",
    # Optional manual ad units. Leave empty to rely on AdSense Auto ads.
    # Add slot IDs from your AdSense account to switch manual units on.
    "ad_slots": {
        "top": "",
        "in_article": "",
        "sidebar": "",
        "footer": "",
    },
    "owner_contact_url": "https://web.works/contact",
    "banner_text": (
        "Contact, if you are interested in this website/domain name/"
        "Sponsorship/Advertisement/Partnership"
    ),
    "year": 2026,
    "reviewed": "November 2026",
}

NAV = [
    ("Guides", "guides/"),
    ("Tools", "tools/"),
    ("Free Case Review", "case-review/"),
    ("News", "news/"),
    ("Videos", "videos/"),
    ("Glossary", "glossary/"),
    ("Contests", "contests/"),
    ("Support", "support/"),
]

FOOTER_COLUMNS = [
    ("Get help", [
        ("Free Case Review", "case-review/"),
        ("Ask the Pundits", "ask/"),
        ("Free Legal Aid", "legal-aid/"),
        ("Do I Need a Lawyer?", "tools/do-i-need-a-lawyer/"),
        ("Global Law Desk", "global/"),
    ]),
    ("Learn", [
        ("All Guides", "guides/"),
        ("Practice Areas", "topics/"),
        ("Legal Glossary", "glossary/"),
        ("Legal IQ Quiz", "quiz/"),
        ("Legal News", "news/"),
        ("Video Library", "videos/"),
    ]),
    ("Community", [
        ("Pundit Challenge Contests", "contests/"),
        ("Support Us / Donate", "support/"),
        ("Careers & Write for Us", "careers/"),
        ("For Attorneys", "attorneys/"),
        ("Advertise & Sponsor", "advertise/"),
    ]),
    ("Company", [
        ("About", "about/"),
        ("Editorial Policy", "editorial-policy/"),
        ("Contact", "contact/"),
        ("Disclaimer", "disclaimer/"),
        ("Privacy Policy", "privacy/"),
        ("Terms of Use", "terms/"),
        ("Trademark & Copyright", "trademark/"),
        ("Site Map", "sitemap/"),
    ]),
]
