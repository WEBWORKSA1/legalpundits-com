"""Structured data: practice areas, states, statutes of limitations, tools, feeds, channels."""

AREAS = [
    {"slug": "personal-injury", "name": "Personal Injury & Accidents", "icon": "🚗",
     "blurb": "Car crashes, slip-and-falls, insurance claims, settlements and deadlines."},
    {"slug": "employment", "name": "Employment & Workplace", "icon": "💼",
     "blurb": "Firing, discrimination, unpaid wages, overtime and workers' comp."},
    {"slug": "family", "name": "Divorce & Family", "icon": "👪",
     "blurb": "Divorce steps, custody, child support and co-parenting."},
    {"slug": "criminal", "name": "Criminal Defense & DUI", "icon": "⚖️",
     "blurb": "Arrests, your rights, DUI charges and clearing your record."},
    {"slug": "immigration", "name": "Immigration", "icon": "🌎",
     "blurb": "Green cards, visas, finding real immigration help and avoiding scams."},
    {"slug": "estate-planning", "name": "Wills, Trusts & Estates", "icon": "📜",
     "blurb": "Wills, living trusts, probate and powers of attorney."},
    {"slug": "housing", "name": "Landlord & Tenant", "icon": "🏠",
     "blurb": "Security deposits, repairs, leases and the eviction process."},
    {"slug": "consumer-debt", "name": "Debt, Bankruptcy & Consumer", "icon": "💳",
     "blurb": "Debt collectors, bankruptcy options and consumer rights."},
    {"slug": "business-ip", "name": "Business & Trademarks", "icon": "🏢",
     "blurb": "Choosing a business entity and protecting your brand."},
    {"slug": "lawyers-courts", "name": "Lawyers & Courts", "icon": "🏛️",
     "blurb": "Hiring a lawyer, fees, small claims court and court deadlines."},
]

# Personal-injury (general negligence) statute of limitations in years.
# Educational summary only; exceptions (minors, discovery rule, government
# claims, medical malpractice, wrongful death) frequently change the deadline.
STATES = [
    ("AL", "Alabama", 2, ""), ("AK", "Alaska", 2, ""), ("AZ", "Arizona", 2, ""),
    ("AR", "Arkansas", 3, ""), ("CA", "California", 2, ""),
    ("CO", "Colorado", 2, "3 years for motor-vehicle accident injuries."),
    ("CT", "Connecticut", 2, ""), ("DE", "Delaware", 2, ""),
    ("DC", "District of Columbia", 3, ""),
    ("FL", "Florida", 2, "2 years for negligence causes of action accruing after March 24, 2023 (previously 4)."),
    ("GA", "Georgia", 2, ""), ("HI", "Hawaii", 2, ""), ("ID", "Idaho", 2, ""),
    ("IL", "Illinois", 2, ""), ("IN", "Indiana", 2, ""), ("IA", "Iowa", 2, ""),
    ("KS", "Kansas", 2, ""),
    ("KY", "Kentucky", 1, "Generally 2 years for motor-vehicle injuries under the no-fault law."),
    ("LA", "Louisiana", 2, "2 years for injuries on or after July 1, 2024 (previously 1 year)."),
    ("ME", "Maine", 6, ""), ("MD", "Maryland", 3, ""), ("MA", "Massachusetts", 3, ""),
    ("MI", "Michigan", 3, ""),
    ("MN", "Minnesota", 6, "Shorter periods apply to some claims, including intentional torts."),
    ("MS", "Mississippi", 3, ""), ("MO", "Missouri", 5, ""), ("MT", "Montana", 3, ""),
    ("NE", "Nebraska", 4, ""), ("NV", "Nevada", 2, ""), ("NH", "New Hampshire", 3, ""),
    ("NJ", "New Jersey", 2, ""), ("NM", "New Mexico", 3, ""), ("NY", "New York", 3, ""),
    ("NC", "North Carolina", 3, ""), ("ND", "North Dakota", 6, ""), ("OH", "Ohio", 2, ""),
    ("OK", "Oklahoma", 2, ""), ("OR", "Oregon", 2, ""), ("PA", "Pennsylvania", 2, ""),
    ("RI", "Rhode Island", 3, ""), ("SC", "South Carolina", 3, ""),
    ("SD", "South Dakota", 3, ""), ("TN", "Tennessee", 1, ""), ("TX", "Texas", 2, ""),
    ("UT", "Utah", 4, ""), ("VT", "Vermont", 3, ""), ("VA", "Virginia", 2, ""),
    ("WA", "Washington", 3, ""), ("WV", "West Virginia", 2, ""), ("WI", "Wisconsin", 3, ""),
    ("WY", "Wyoming", 4, ""),
]

# States that still apply contributory negligence (any plaintiff fault can bar recovery).
CONTRIBUTORY_STATES = ["AL", "DC", "MD", "NC", "VA"]

TOOLS = [
    {"slug": "settlement-estimator", "name": "Injury Settlement Estimator", "icon": "🧮",
     "area": "personal-injury",
     "blurb": "Estimate a personal injury claim range using the multiplier method, fault share and policy limits."},
    {"slug": "deadline-finder", "name": "Statute of Limitations Deadline Finder", "icon": "⏳",
     "area": "personal-injury",
     "blurb": "Pick your state and injury date to see the general filing deadline and days remaining."},
    {"slug": "contingency-fee-calculator", "name": "Contingency Fee & Net Recovery Calculator", "icon": "💵",
     "area": "lawyers-courts",
     "blurb": "See what you actually take home after the lawyer's percentage, case costs and medical liens."},
    {"slug": "court-days-calculator", "name": "Court Deadline Days Calculator", "icon": "📅",
     "area": "lawyers-courts",
     "blurb": "Count calendar or business days from any date, skipping weekends and US federal holidays."},
    {"slug": "demand-letter-generator", "name": "Demand Letter Generator", "icon": "✉️",
     "area": "lawyers-courts",
     "blurb": "Create a firm, professional demand letter for money owed, a deposit, damage or a refund."},
    {"slug": "do-i-need-a-lawyer", "name": "Do I Need a Lawyer? Quiz", "icon": "🧭",
     "area": "lawyers-courts",
     "blurb": "Answer six questions to see how urgently you should talk to an attorney."},
]

# RSS/Atom feeds pulled by scripts/update_feeds.py (verified publishers).
FEEDS = [
    {"name": "SCOTUSblog", "url": "https://www.scotusblog.com/feed/", "topic": "Supreme Court"},
    {"name": "JURIST", "url": "https://www.jurist.org/news/feed/", "topic": "World legal news"},
    {"name": "ABA Journal", "url": "https://feeds.feedburner.com/abajournal/dailynews", "topic": "Legal profession"},
    {"name": "Above the Law", "url": "https://abovethelaw.com/feed/", "topic": "Legal industry"},
    {"name": "Artificial Lawyer", "url": "https://www.artificiallawyer.com/feed/", "topic": "Legal tech & AI"},
    {"name": "LawNext", "url": "https://www.lawnext.com/feed/", "topic": "Legal tech"},
    {"name": "Election Law Blog", "url": "https://electionlawblog.org/?feed=rss2", "topic": "Election law"},
    {"name": "Patently-O", "url": "https://patentlyo.com/feed", "topic": "Patents & IP"},
    {"name": "Technology & Marketing Law Blog", "url": "https://blog.ericgoldman.org/feed", "topic": "Internet law"},
]

# YouTube channels (channel IDs). Uploads playlist = "UU" + id[2:].
CHANNELS = [
    {"name": "LegalEagle", "id": "UCpa-Zb0ZcQjTCPP1Dx_1M8Q",
     "about": "A practicing attorney breaks down headline cases and legal myths."},
    {"name": "Law Talk With Mike", "id": "UCYWtiAEcmR-Fb7fGF0hQfog",
     "about": "Practical explainers on everyday legal questions."},
    {"name": "America's Estate Planning Lawyers", "id": "UCkYr5Sh_MHVzpx28Hq00nyw",
     "about": "Wills, trusts, probate and long-term planning, explained."},
    {"name": "The Law Simplified", "id": "UCCyS1rOQP8eLHHkUDe6HjmA",
     "about": "Legal concepts reduced to the essentials."},
    {"name": "Steve Vondran", "id": "UCegzdaulNeA87a9J38-VRzQ",
     "about": "Copyright, trademarks and online business law."},
    {"name": "Rohit Pradhan – Attorney at Law", "id": "UCEjxHflLV45OCilSxlFgaBg",
     "about": "Attorney explainers on practical legal issues."},
    {"name": "Aradhya Gupta – Lawvita", "id": "UCnmYgMicZDTVh1p1_k9xHog",
     "about": "Indian law explained for everyday situations."},
]

# More creators (linked, not embedded).
MORE_CHANNELS = [
    ("Steve Lehto", "https://www.youtube.com/@stevelehto/", "Consumer protection and lemon law."),
    ("Emily D. Baker", "https://www.youtube.com/@TheEmilyDBaker/", "Former prosecutor covering trials."),
    ("The Lead Attorney", "https://www.youtube.com/@TheLeadAttorney/", "Family-law explainers."),
    ("Lawful Masses with Leonard French", "https://www.youtube.com/@lawfulmasses/", "Copyright and internet law."),
    ("The Real Estate Lawyer", "https://www.youtube.com/@TheRealEstateLawyer/", "Property and real estate law."),
    ("Angela Vorpahl", "https://www.youtube.com/@AngelaVorpahl/", "Injury attorney on accident claims."),
]

GLOBAL_DESK = [
    {"country": "United States", "flag": "🇺🇸", "links": [
        ("LawHelp.org — free legal aid by state", "https://www.lawhelp.org/"),
        ("USA.gov — find legal aid", "https://www.usa.gov/legal-aid"),
        ("ABA Free Legal Answers", "https://abafreelegalanswers.org/"),
        ("Legal Services Corporation", "https://www.lsc.gov/"),
        ("Cornell LII — free US law", "https://www.law.cornell.edu/"),
    ], "note": "Laws differ by state. Start with your state court's self-help center and your state bar's lawyer referral service."},
    {"country": "Canada", "flag": "🇨🇦", "links": [
        ("CanLII — free Canadian case law & legislation", "https://www.canlii.org/"),
        ("Department of Justice Canada", "https://www.justice.gc.ca/"),
        ("Steps to Justice (Ontario)", "https://stepstojustice.ca/"),
        ("Éducaloi (Québec)", "https://educaloi.qc.ca/"),
    ], "note": "Family, property and employment law are mostly provincial; criminal law is federal."},
    {"country": "United Kingdom", "flag": "🇬🇧", "links": [
        ("Citizens Advice", "https://www.citizensadvice.org.uk/"),
        ("GOV.UK — check if you can get legal aid", "https://www.gov.uk/check-legal-aid"),
        ("Law Society — find a solicitor", "https://solicitors.lawsociety.org.uk/"),
        ("legislation.gov.uk", "https://www.legislation.gov.uk/"),
    ], "note": "England & Wales, Scotland and Northern Ireland have separate legal systems."},
    {"country": "India", "flag": "🇮🇳", "links": [
        ("NALSA — free legal services", "https://nalsa.gov.in/"),
        ("India Code — central acts", "https://www.indiacode.nic.in/"),
        ("eCourts Services", "https://ecourts.gov.in/"),
        ("Supreme Court of India", "https://www.sci.gov.in/"),
    ], "note": "Free legal aid is available to eligible people through Legal Services Authorities at national, state and district level."},
    {"country": "Australia", "flag": "🇦🇺", "links": [
        ("National Legal Aid", "https://www.nationallegalaid.org/"),
        ("AustLII — free Australian law", "https://www.austlii.edu.au/"),
        ("Federal Register of Legislation", "https://www.legislation.gov.au/"),
    ], "note": "Each state and territory has its own legal aid commission and court system."},
]
