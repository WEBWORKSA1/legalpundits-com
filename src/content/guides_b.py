"""Original LegalPundits guides — part B (immigration, estates, housing, debt, business, courts)."""

GUIDES_B = [
{
"slug": "green-card-paths-explained",
"title": "Green Card Paths Explained: Family, Employment, Lottery and Humanitarian",
"area": "immigration", "issue": "immigration",
"description": "The main routes to US lawful permanent residence, how waiting lines work and the difference between adjustment of status and consular processing.",
"takeaways": [
 "Most green cards come through family, employment, the diversity lottery or humanitarian protection.",
 "Immediate relatives of US citizens are not subject to annual caps; other categories can wait years.",
 "Adjustment of status happens inside the US; consular processing happens at a US embassy abroad.",
 "Always download forms from uscis.gov; the forms themselves are free.",
],
"body": """
## What a green card is

A green card (Permanent Resident Card) lets you live and work permanently in the United States. After a qualifying period, usually five years, or three if married to and living with a US citizen, permanent residents can generally apply to naturalise.

## 1. Family-based

- **Immediate relatives of US citizens**: spouses, unmarried children under 21 and parents of citizens who are at least 21. There is no annual numerical cap, so the wait is mostly processing time.
- **Family preference categories**: unmarried adult children of citizens, spouses and children of permanent residents, married children of citizens, and siblings of adult citizens. These are capped each year, so applicants wait for their **priority date** to become current in the State Department's monthly Visa Bulletin. Waits range from a couple of years to well over a decade depending on category and country.

The process usually begins with a family petition (Form I-130) filed by the US citizen or permanent resident relative.

## 2. Employment-based

Five preference categories (EB-1 to EB-5) cover people with extraordinary ability, outstanding researchers, multinational executives, advanced-degree professionals, skilled and other workers, special immigrants and investors. Many require an employer sponsor and a labor certification showing no qualified US workers are available. Some, such as EB-1 extraordinary ability and the national interest waiver, allow self-petitioning.

## 3. Diversity Visa lottery

Each year the State Department makes up to 55,000 diversity visas available to people from countries with historically low immigration to the US. Registration is free and online during a short window, usually in the autumn. Beware of websites charging to "enter" you.

## 4. Humanitarian routes

Refugees and people granted asylum can generally apply for a green card after one year. Other humanitarian categories include certain victims of crimes and trafficking and some abused spouses and children.

## Adjustment vs consular processing

If you're already in the US and eligible, you may **adjust status** (Form I-485) without leaving. Otherwise, you complete **consular processing** and an interview at a US embassy or consulate abroad. Past immigration violations, such as unlawful presence, can affect which route is available and may trigger bars to re-entry, which is why individual legal advice matters.
""",
"faqs": [
 ("How long does it take to get a green card through marriage?", "It varies by whether your spouse is a citizen or permanent resident, where you file and current processing times, commonly from about a year to a few years."),
 ("Can I work while my green card application is pending?", "Many adjustment applicants can request an employment authorization document while the application is pending."),
 ("Do I need a lawyer for a green card?", "Simple, clean cases are sometimes handled without one, but any prior visa overstay, removal proceeding, arrest or complex employment case calls for a licensed immigration attorney."),
],
"lawyer": "Speak with a licensed immigration attorney or a DOJ-accredited representative if you've ever overstayed, entered without inspection, been arrested, received a notice to appear, or had a prior application denied.",
"sources": [("USCIS — green card", "https://www.uscis.gov/green-card"), ("US Department of State — Visa Bulletin", "https://travel.state.gov/content/travel/en/legal/visa-law0/visa-bulletin.html")],
"tools": ["do-i-need-a-lawyer"],
},
{
"slug": "immigration-help-avoid-notario-fraud",
"title": "Finding Real Immigration Help and Avoiding Notario Fraud",
"area": "immigration", "issue": "immigration",
"description": "Who is legally allowed to give immigration advice, the warning signs of scams, and where to find free or low-cost help.",
"takeaways": [
 "Only licensed attorneys and DOJ-accredited representatives of recognized organizations may give immigration legal advice.",
 "In the US, a notary public is not a lawyer, even though 'notario público' means a lawyer in many countries.",
 "Never sign blank forms or forms containing false information, and keep copies of everything you submit.",
],
"body": """
## Who can legally help you

- **Licensed attorneys** in good standing with any US state bar. Immigration is federal law, so a lawyer licensed in any state can help with your case. Check their licence on the state bar website.
- **DOJ-accredited representatives** working for recognized non-profit organizations under the Justice Department's Recognition and Accreditation program. Many offer free or low-cost help.

Anyone else, including notaries, "immigration consultants", travel agents and tax preparers, may only fill in forms at your direction and charge a small fee for typing. They cannot advise you which forms to file or how to answer questions.

## Why "notario" fraud is so common

In much of Latin America and Europe, a *notario público* is a highly trained lawyer. In the United States, a notary public only witnesses signatures. Scammers exploit the confusion by advertising as "notarios" and charging thousands of dollars for bad advice, false applications and missed deadlines. The consequences can include denied applications, lost fees and even deportation proceedings.

## Warning signs

- Promises of a guaranteed green card, work permit or "special relationship" with immigration officials.
- Requests to sign blank forms or to lie on an application.
- Charging for government forms, which are free on uscis.gov.
- Refusing to give you copies of what was filed or receipts for payments.
- Pressure to pay large amounts in cash immediately.

## Where to find legitimate help

- Your state bar's lawyer referral service.
- Non-profit legal service providers recognized by the Justice Department.
- Law school immigration clinics.
- Pro bono programs run by bar associations.

## If you've been scammed

Request your file and copies of everything submitted, consult a legitimate attorney immediately about any deadlines, and report the scam to the Federal Trade Commission and your state attorney general. Victims may also file a complaint with the state bar if the person claimed to be a lawyer.
""",
"faqs": [
 ("Can a notary help with my immigration forms?", "A notary can type information you provide and notarize signatures, but cannot give legal advice or choose forms for you."),
 ("How do I check if an immigration lawyer is real?", "Search the lawyer's name on the state bar website where they claim to be licensed, and check for disciplinary history."),
 ("Are USCIS forms free?", "Yes. Forms are free to download from uscis.gov; only the filing fees go to the government."),
],
"lawyer": "Always use a licensed immigration attorney or accredited representative for anything beyond the simplest filing, and immediately if you have a deadline, a court date or a prior denial.",
"sources": [("USCIS — avoid scams", "https://www.uscis.gov/scams-fraud-and-misconduct/avoid-scams"), ("FTC — immigration scams", "https://consumer.ftc.gov/")],
"tools": ["do-i-need-a-lawyer"],
},
{
"slug": "will-vs-living-trust",
"title": "Will vs Living Trust: Which Do You Need?",
"area": "estate-planning", "issue": "estate",
"description": "How wills and revocable living trusts differ on probate, privacy, cost and incapacity planning, and how to choose.",
"takeaways": [
 "A will is simpler and cheaper but usually goes through probate.",
 "A funded revocable living trust can avoid probate and keep your plan private.",
 "Only a will can name a guardian for minor children, so trust users still need a 'pour-over' will.",
 "Beneficiary designations on retirement accounts and life insurance override both.",
],
"body": """
## What a will does

A will states who receives your property, names an executor to settle your estate and, crucially, can nominate a guardian for minor children. Most states require the will to be signed in front of two witnesses; some accept handwritten (holographic) wills. A will takes effect only at death and is administered through **probate**, the court-supervised process for paying debts and distributing property.

## What a living trust does

A **revocable living trust** is a legal arrangement in which you (as trustee) hold assets for your own benefit during life, with a successor trustee taking over at incapacity or death. Because the trust, not you personally, owns the assets, they pass to beneficiaries without probate. The trust only controls assets actually transferred into it, a step called **funding**.

## Side-by-side

- **Cost to create:** wills are cheaper; trusts cost more upfront and need funding work.
- **Probate:** wills generally go through it; funded trusts generally avoid it.
- **Privacy:** probated wills become public records; trusts usually stay private.
- **Incapacity:** a trust lets your successor trustee manage assets if you become incapacitated; with only a will, your family may need a power of attorney or a court guardianship.
- **Out-of-state property:** a trust can avoid separate probate proceedings in each state where you own real estate.
- **Guardianship of children:** only a will can nominate guardians.

## Who benefits most from a trust

People with real estate in more than one state, those in states with expensive or slow probate, blended families, people who value privacy, and anyone wanting detailed control over how and when heirs receive money.

## Don't forget non-probate transfers

Retirement accounts, life insurance, payable-on-death bank accounts, transfer-on-death securities and, in many states, transfer-on-death deeds pass directly to named beneficiaries, outside both the will and the trust. Keep those designations up to date; they override your will.
""",
"faqs": [
 ("Does a living trust protect assets from creditors?", "A revocable trust generally does not protect your assets from your own creditors during your lifetime, because you keep control."),
 ("Do I still need a will if I have a trust?", "Yes. A pour-over will catches assets left outside the trust and nominates guardians for minor children."),
 ("Can I write my own will?", "Many people do, using state-compliant forms. Mistakes in signing or witnessing can invalidate a will, so a review is wise for larger or complex estates."),
],
"lawyer": "Use an estate planning attorney if you have minor children, a blended family, a business, property in several states, a beneficiary with special needs, or an estate large enough to raise tax questions.",
"sources": [("Cornell LII — will", "https://www.law.cornell.edu/wex/will"), ("Cornell LII — living trust", "https://www.law.cornell.edu/wex/living_trust")],
"tools": ["do-i-need-a-lawyer"],
},
{
"slug": "probate-explained",
"title": "Probate Explained: What Happens After Someone Dies",
"area": "estate-planning", "issue": "estate",
"description": "The probate process step by step, executor duties, how long it takes, and how small estates can skip most of it.",
"takeaways": [
 "Probate validates the will, pays debts and taxes, and transfers what's left to heirs.",
 "Many states offer simplified procedures or affidavits for small estates.",
 "Typical probate takes several months to more than a year.",
 "Executors owe legal duties to beneficiaries and can be personally liable for mistakes.",
],
"body": """
## When probate is needed

Probate is required for assets owned solely in the deceased person's name without a beneficiary designation or co-owner, such as a house titled only to them or a bank account without a payable-on-death beneficiary. Assets in a living trust, joint accounts with survivorship and accounts with named beneficiaries usually pass outside probate.

## The process step by step

1. **File the petition.** The named executor (or a family member if there's no will) files with the probate court in the county where the person lived, along with the original will and death certificate.
2. **Appointment.** The court appoints the personal representative and issues letters testamentary (with a will) or letters of administration (without one).
3. **Notify heirs and creditors.** This usually includes mailed notice to known creditors and published notice. Creditors then have a limited window, often a few months, to file claims.
4. **Inventory and appraise** the estate's assets.
5. **Pay valid debts, expenses and taxes**, including any final income tax returns.
6. **Distribute the remaining property** according to the will, or under state intestacy law if there's no will.
7. **Close the estate** with a final accounting and court approval.

## How long and how much

Simple estates may finish in six to nine months; contested or complex estates can take years. Costs include court fees, appraisals, bond premiums and attorney and executor fees, which some states set as a percentage of the estate.

## Small estate shortcuts

Most states let heirs collect property from small estates by signing an affidavit or using a summary procedure, without full probate. Value limits vary widely by state.

## Dying without a will

If there's no will, state **intestacy** laws decide who inherits, usually the spouse and children first, then parents, siblings and more distant relatives. The court appoints an administrator.

## Executor duties

Executors must act in the estate's best interest: secure property, keep estate money separate, keep records, pay creditors in the legally required order and avoid self-dealing.
""",
"faqs": [
 ("Can you avoid probate?", "Often, with a funded living trust, beneficiary designations, joint ownership with survivorship and transfer-on-death deeds where available."),
 ("Does the executor get paid?", "Usually yes, either a fee set by state law or a reasonable fee approved by the court, unless the executor waives it."),
 ("What if someone contests the will?", "Will contests are based on grounds such as lack of capacity, undue influence, fraud or improper signing. They can significantly delay distribution."),
],
"lawyer": "Hire a probate attorney if the estate includes real estate or a business, heirs are in conflict, the estate may not cover its debts, or someone is contesting the will.",
"sources": [("Cornell LII — probate", "https://www.law.cornell.edu/wex/probate")],
"tools": ["court-days-calculator"],
},
{
"slug": "power-of-attorney-and-advance-directives",
"title": "Power of Attorney and Advance Directives: Planning for Incapacity",
"area": "estate-planning", "issue": "estate",
"description": "Durable financial powers of attorney, health care proxies and living wills: what each does and why to sign them now.",
"takeaways": [
 "A durable power of attorney lets someone handle your finances if you can't.",
 "A health care proxy names someone to make medical decisions; a living will records your treatment wishes.",
 "You must sign these while you still have capacity; afterwards your family may need a court guardianship.",
],
"body": """
## Financial power of attorney

A power of attorney (POA) appoints an **agent** to act for you in financial and legal matters: paying bills, managing bank accounts, filing taxes, dealing with insurance or selling property. Key choices:

- **Durable vs non-durable.** A durable POA stays in effect if you become incapacitated, which is the whole point for incapacity planning. Many states now make POAs durable by default.
- **Immediate vs springing.** An immediate POA works as soon as it's signed. A springing POA takes effect only upon a certified incapacity, which can delay things when time matters.
- **Scope.** General POAs cover most matters; limited POAs cover a specific task, such as closing a single real estate sale.

## Health care decisions

- **Health care power of attorney (health care proxy)** names someone to make medical decisions when you can't.
- **Living will** records your wishes about life-sustaining treatment, such as ventilators and tube feeding, in end-of-life situations.
- Many states combine these into a single **advance directive** form.
- A **HIPAA authorization** lets named people receive your medical information.

## Why it matters

Without these documents, your family may need to petition a court for guardianship or conservatorship, which is slower, costs more, is public and may result in someone you wouldn't have chosen being in charge.

## Signing requirements

States differ: some require notarization, others witnesses, some both. Financial institutions may ask for specific wording, and a POA used for real estate often must be notarized and recorded. Give copies to your agent, doctors and close family.

## Choosing your agent

Pick someone trustworthy, organised and willing. Name a backup. Agents owe you fiduciary duties: they must act in your best interest, keep your money separate and keep records.
""",
"faqs": [
 ("Does a power of attorney end at death?", "Yes. At death, authority passes to the executor named in the will or the trustee of a trust."),
 ("Can I revoke a power of attorney?", "Yes, while you have capacity, by signing a written revocation and notifying the agent and any institutions relying on it."),
 ("Is a POA from another state valid?", "Most states honour POAs validly executed elsewhere, but institutions sometimes resist; a lawyer can help."),
],
"lawyer": "An estate planning lawyer is worth consulting if you have significant assets, a business, a family member who may object, or concerns about capacity that should be documented.",
"sources": [("Cornell LII — power of attorney", "https://www.law.cornell.edu/wex/power_of_attorney"), ("National Institute on Aging — advance care planning", "https://www.nia.nih.gov/")],
"tools": ["do-i-need-a-lawyer"],
},
{
"slug": "security-deposit-and-tenant-rights",
"title": "Security Deposits and Repairs: Core Tenant Rights",
"area": "housing", "issue": "housing",
"description": "Deposit limits and return deadlines, what landlords can deduct, the right to a habitable home, and protection from retaliation.",
"takeaways": [
 "Many states cap deposits and set strict deadlines, commonly 14 to 45 days, to return them with an itemized list.",
 "Landlords can't deduct for normal wear and tear.",
 "Most states recognise a right to a habitable home: heat, water, safe wiring, no pest infestations.",
 "Retaliating against tenants for requesting repairs is illegal in most states.",
],
"body": """
## Security deposits

- **Limits.** Many states cap deposits, often at one or two months' rent; some have no cap.
- **Return deadline.** After you move out, landlords typically must return the deposit or send an itemized statement of deductions within a set period, commonly 14 to 45 days.
- **Allowed deductions.** Unpaid rent, damage beyond normal wear and tear and, in some states, cleaning to return the unit to move-in condition.
- **Normal wear and tear** includes minor scuffs, faded paint and worn carpet from ordinary use. Holes in walls, broken fixtures and pet damage are not normal wear.
- **Penalties.** Many states let tenants recover two or three times the deposit if the landlord withholds it in bad faith.

**Protect yourself:** photograph and video the unit at move-in and move-out, use a written checklist signed by both sides, and give your forwarding address in writing.

## The right to a habitable home

Most states recognise an implied **warranty of habitability**. Landlords must keep units safe and livable: working heat and plumbing, hot water, safe electrical systems, secure doors and windows, and freedom from serious pest infestations and hazards. Tenant remedies vary by state and can include:

- Written repair requests with a reasonable deadline (always in writing).
- Reporting violations to local code enforcement.
- **Repair and deduct**, where allowed, within strict limits.
- **Rent withholding or rent escrow**, where allowed and usually only after following specific procedures.
- Breaking the lease in severe cases.

Using the wrong remedy can expose you to eviction for non-payment, so check your state's rules first.

## Retaliation and discrimination

Landlords generally can't raise rent, cut services or evict you because you requested repairs, complained to an inspector or joined a tenant group. The federal Fair Housing Act prohibits discrimination based on race, colour, religion, sex, national origin, familial status or disability.

Use our [demand letter generator](/tools/demand-letter-generator/) to request your deposit in writing.
""",
"faqs": [
 ("Can my landlord keep my whole deposit for cleaning?", "Only reasonable cleaning beyond normal use is usually allowed, and the landlord must itemize. Keeping the whole deposit without justification can trigger penalties."),
 ("Can my landlord enter without notice?", "Many states require reasonable notice, often 24 to 48 hours, except in emergencies."),
 ("What if my landlord won't make repairs?", "Send a dated written request, document the problem, contact local code enforcement and check which remedies your state allows."),
],
"lawyer": "Contact a tenant lawyer or legal aid if you received an eviction notice, the landlord is retaliating or discriminating, or serious health hazards aren't being fixed.",
"sources": [("Cornell LII — security deposit", "https://www.law.cornell.edu/wex/security_deposit"), ("HUD — fair housing", "https://www.hud.gov/")],
"tools": ["demand-letter-generator", "court-days-calculator"],
},
{
"slug": "eviction-process-explained",
"title": "The Eviction Process Explained: Notice, Court and Your Defenses",
"area": "housing", "issue": "housing",
"description": "How a lawful eviction works step by step, illegal 'self-help' evictions, common tenant defenses and where to get help fast.",
"takeaways": [
 "A landlord must go through court to evict; lockouts and utility shut-offs are illegal in nearly every state.",
 "Deadlines are short: answer periods can be just a few days after you're served.",
 "Showing up to the hearing is critical; most tenants who don't appear lose by default.",
 "Rental assistance, mediation and right-to-counsel programs can stop or delay many evictions.",
],
"body": """
## Step 1: Notice

Evictions start with a written notice. Common types:

- **Pay rent or quit**, typically giving 3 to 14 days to pay overdue rent.
- **Cure or quit**, to fix a lease violation.
- **Unconditional quit**, for serious violations, in limited situations.
- **No-cause termination** of a month-to-month tenancy, often 30 to 90 days, where local law allows it.

Some cities and states require "just cause" for eviction and longer notices.

## Step 2: Court filing

If you don't comply, the landlord files an eviction lawsuit (called unlawful detainer, summary possession or forcible entry and detainer). You'll be served with a summons and complaint.

## Step 3: Your answer

Deadlines can be as short as **five days**. File a written answer if your court requires one, raising every defense you have.

## Step 4: Hearing

Bring your lease, rent receipts, bank records, photos, repair requests and texts. Many courts offer same-day mediation.

## Step 5: Judgment and removal

If the landlord wins, the court issues a judgment for possession and usually a writ. Only a sheriff or marshal can physically remove you, after giving notice.

## Common defenses

- The notice was defective or the wrong length.
- Rent was paid or the landlord refused your payment.
- Retaliation for complaints or repair requests.
- Discrimination prohibited by fair housing laws.
- Serious habitability problems, in states that allow rent offsets.
- Failure to follow local just-cause or rent-stabilization rules.

## Illegal self-help evictions

Changing locks, removing doors, shutting off utilities or removing your belongings without a court order is illegal in nearly every state and may entitle you to damages.

## Getting help

Contact legal aid immediately; several cities and states guarantee lawyers to low-income tenants facing eviction. Ask about emergency rental assistance and whether your eviction record can be sealed.
""",
"faqs": [
 ("How long does an eviction take?", "From notice to removal, commonly a few weeks to a few months depending on the state, court backlog and whether the tenant contests the case."),
 ("Can I be evicted in winter?", "A few jurisdictions restrict winter evictions in limited circumstances, but most do not."),
 ("Will an eviction show on my record?", "Court filings can appear on tenant-screening reports. Some states allow sealing, especially when the tenant wins or the case is dismissed."),
],
"lawyer": "Contact legal aid or a tenant attorney the day you receive court papers; answer deadlines are short and many defenses are lost if not raised early.",
"sources": [("Cornell LII — eviction", "https://www.law.cornell.edu/wex/eviction"), ("LawHelp.org — find free legal aid", "https://www.lawhelp.org/")],
"tools": ["court-days-calculator", "do-i-need-a-lawyer"],
},
{
"slug": "debt-collector-rights-fdcpa",
"title": "Dealing With Debt Collectors: Your Rights Under the FDCPA",
"area": "consumer-debt", "issue": "debt",
"description": "What debt collectors can and can't do, how to demand validation, stop calls, handle old debts and fight back against violations.",
"takeaways": [
 "Collectors must send validation information, and you have 30 days to dispute the debt in writing.",
 "Calls before 8 a.m. or after 9 p.m., threats, lies and harassment are prohibited.",
 "You can tell a collector in writing to stop contacting you.",
 "Violations can earn you actual damages, up to $1,000 in statutory damages and attorney fees.",
],
"body": """
## Who the FDCPA covers

The Fair Debt Collection Practices Act applies mainly to third-party debt collectors and debt buyers collecting personal, family or household debts, not to most original creditors collecting their own debts. Many states have laws that extend similar rules to original creditors.

## Validation and disputes

Within five days of first contacting you, a collector must give you **validation information**: the amount owed, the creditor and your right to dispute. If you dispute the debt **in writing within 30 days**, the collector must stop collecting until it sends verification. Disputing in writing also protects you from having the debt treated as undisputed.

## What collectors cannot do

- Call before 8 a.m. or after 9 p.m. your local time, or at work if they know your employer prohibits it.
- Harass you with repeated calls; federal rules presume excessive calling if a collector calls more than seven times within seven days about a debt.
- Threaten violence, arrest or legal action they can't or don't intend to take.
- Misrepresent the amount owed or pretend to be lawyers or government officials.
- Discuss your debt with third parties such as family, neighbours or your employer, with narrow exceptions.
- Add unauthorized fees or interest.

## Stop the contact

Send a written request telling the collector to stop communicating. After that, they may contact you only to confirm they're stopping or to tell you about a specific action, such as a lawsuit. The debt doesn't disappear, so consider your strategy.

## Old (time-barred) debts

Debts have a statute of limitations for lawsuits, often three to six years. Collectors may not sue or threaten to sue on time-barred debts. In some states, a partial payment or written acknowledgment can restart the clock, so get advice before paying on an old debt.

## If you're sued

Never ignore a summons. Respond by the deadline; many collection lawsuits are won by default because consumers don't appear. Require the collector to prove ownership of the debt and the amount.

## Fighting violations

Keep call logs, letters and voicemails. You can complain to the CFPB and your state attorney general, and you can sue within one year of a violation for actual damages, up to $1,000 statutory damages and attorney fees.
""",
"faqs": [
 ("Can a debt collector garnish my wages without going to court?", "For most consumer debts, no. A creditor must sue and win a judgment first. Federal student loans and taxes are exceptions."),
 ("Should I pay a debt I don't recognise?", "No. Dispute it in writing and demand validation first."),
 ("Will paying an old debt help my credit?", "Paying may update the account status, but negative items generally stay up to seven years from the original delinquency. Get any settlement terms in writing first."),
],
"lawyer": "Consult a consumer protection attorney if you've been sued, a collector is harassing or threatening you, or you've found errors on your credit report; FDCPA lawyers often work for fees paid by the violator.",
"sources": [("CFPB — debt collection", "https://www.consumerfinance.gov/consumer-tools/debt-collection/"), ("FTC — consumer advice", "https://consumer.ftc.gov/")],
"tools": ["demand-letter-generator", "court-days-calculator"],
},
{
"slug": "chapter-7-vs-chapter-13-bankruptcy",
"title": "Chapter 7 vs Chapter 13 Bankruptcy: Which Fits?",
"area": "consumer-debt", "issue": "debt",
"description": "How the two main consumer bankruptcy chapters work, who qualifies, what debts are wiped out and the long-term credit effect.",
"takeaways": [
 "Chapter 7 wipes out most unsecured debts in a few months but may sell non-exempt property.",
 "Chapter 13 is a 3–5 year repayment plan that lets you keep property and catch up on a mortgage.",
 "Filing triggers an automatic stay that halts most collection, garnishment and foreclosure activity.",
 "Child support, most taxes, most student loans and criminal fines usually survive bankruptcy.",
],
"body": """
## Chapter 7: liquidation

- **Who qualifies:** people whose income is below their state's median, or who pass the **means test** after deducting allowed expenses.
- **How it works:** a trustee reviews your assets. Property protected by exemptions (often home equity up to a limit, a vehicle up to a limit, household goods, retirement accounts) is kept; non-exempt property can be sold to pay creditors. Most consumer Chapter 7 cases have no non-exempt assets.
- **Timeline:** discharge typically arrives around three to four months after filing.
- **Best for:** people with mostly credit card, medical and personal loan debt, limited income and few non-exempt assets.

## Chapter 13: reorganization

- **Who qualifies:** individuals with regular income and debts under the statutory limits.
- **How it works:** you propose a three- to five-year plan to repay some or all debts. You keep your property, and you can catch up on mortgage or car arrears over the life of the plan.
- **Best for:** people behind on a home or car they want to keep, those above the median income, and those with non-exempt assets to protect.

## The automatic stay

Filing either chapter immediately stops most collection calls, lawsuits, wage garnishments, repossessions and foreclosure sales. Creditors can ask the court to lift the stay in some situations.

## Debts that usually survive

Child support and alimony, most recent tax debts, most student loans (unless you prove undue hardship), criminal fines and restitution, and debts from fraud or drunk-driving injuries.

## Required steps

Complete credit counseling from an approved agency within 180 days before filing, and a debtor education course before discharge.

## Credit impact

A Chapter 7 can remain on your credit report up to 10 years and a Chapter 13 up to 7, although many filers start rebuilding credit within a year or two.
""",
"faqs": [
 ("Will I lose my house in bankruptcy?", "Not necessarily. Homestead exemptions protect some equity, and Chapter 13 can help you catch up on missed payments."),
 ("How often can I file?", "You generally must wait 8 years between Chapter 7 discharges; other combinations have different waiting periods."),
 ("Can I file without a lawyer?", "You can, but mistakes can cost assets or the discharge itself. Many bankruptcy lawyers offer free consultations and payment plans."),
],
"lawyer": "Talk to a bankruptcy attorney before you file, before transferring property or repaying relatives, and immediately if a foreclosure sale or garnishment is imminent.",
"sources": [("US Courts — bankruptcy basics", "https://www.uscourts.gov/services-forms/bankruptcy")],
"tools": ["do-i-need-a-lawyer"],
},
{
"slug": "llc-vs-corporation-vs-sole-proprietorship",
"title": "LLC vs Corporation vs Sole Proprietorship: Choosing a Business Structure",
"area": "business-ip", "issue": "business",
"description": "Liability protection, taxes, paperwork and fundraising: how the main US business structures compare and how to form one.",
"takeaways": [
 "Sole proprietorships are simplest but leave your personal assets exposed.",
 "LLCs offer liability protection with flexible, pass-through taxation by default.",
 "C corporations suit venture-funded startups; S corporations can reduce self-employment tax for profitable small businesses.",
 "Liability protection only works if you keep business and personal finances separate.",
],
"body": """
## Sole proprietorship

The default if you start doing business alone. No formation filing (beyond local licences and possibly a DBA), and profits are reported on your personal tax return. The downside: **no separation** between you and the business, so business debts and lawsuits can reach your personal savings and home.

## Limited liability company (LLC)

Formed by filing articles of organization with a state. Members are generally not personally liable for business debts. By default, a single-member LLC is taxed like a sole proprietorship and a multi-member LLC like a partnership, with profits passing through to the owners. An LLC can elect to be taxed as an S corporation. An **operating agreement** sets ownership, management and what happens if a member leaves.

## Corporation

Formed by filing articles of incorporation. Owned by shareholders, managed by a board and officers, with bylaws and formal minutes.

- **C corporation:** taxed at the corporate level (21% federal rate), with dividends taxed again to shareholders. Preferred by venture investors and for issuing stock options.
- **S corporation:** a tax election allowing pass-through taxation, limited to 100 shareholders who are generally US citizens or residents, with one class of stock. Profitable owners can pay themselves a reasonable salary and take remaining profit as distributions not subject to self-employment tax.

## Partnerships

General partnerships form automatically when two or more people do business together for profit, with each partner personally liable. Limited partnerships and LLPs offer varying protection.

## How to form an LLC or corporation

1. Choose and check name availability with your state.
2. Appoint a registered agent.
3. File formation documents and pay the state fee.
4. Get an EIN from the IRS (free).
5. Sign an operating agreement or adopt bylaws.
6. Open a separate business bank account.
7. Get required licences and calendar annual reports.

## Keeping the liability shield

Courts can "pierce the corporate veil" when owners mix personal and business funds, undercapitalise the business or ignore formalities. Keep separate accounts and records.
""",
"faqs": [
 ("Which state should I form my LLC in?", "Usually your home state, where you'll operate anyway. Delaware is popular for venture-backed corporations, but forming elsewhere often means registering in your home state too."),
 ("Does an LLC protect me from my own mistakes?", "Not from your own negligence or personal guarantees. It protects against business debts and others' acts within the business."),
 ("When should I elect S corporation status?", "Often when profits comfortably exceed a reasonable salary for your role; consult a tax professional."),
],
"lawyer": "Use a business attorney if you have co-founders, plan to raise investment, are buying a business, or need custom ownership, vesting or buy-sell terms.",
"sources": [("SBA — choose a business structure", "https://www.sba.gov/business-guide/launch-your-business/choose-business-structure"), ("IRS — limited liability company", "https://www.irs.gov/businesses/small-businesses-self-employed/limited-liability-company-llc")],
"tools": ["do-i-need-a-lawyer", "demand-letter-generator"],
},
{
"slug": "trademark-basics-protect-your-brand",
"title": "Trademark Basics: How to Protect a Brand Name",
"area": "business-ip", "issue": "business",
"description": "What makes a name protectable, how to clear it, federal registration steps, ™ vs ®, and keeping your rights alive.",
"takeaways": [
 "Distinctive names (invented or arbitrary) are strongest; descriptive names are hard to protect; generic terms can't be trademarks.",
 "Search before you invest: a conflicting earlier mark can force a costly rebrand.",
 "Use ™ any time; use ® only after federal registration issues.",
 "Registrations require ongoing use and maintenance filings.",
],
"body": """
## What a trademark protects

A trademark is a word, phrase, logo, sound or other identifier that tells customers who provides goods or services. It protects against confusingly similar uses in related markets, not ownership of a word for every purpose.

## The strength spectrum

1. **Fanciful** (invented words) — strongest.
2. **Arbitrary** (real words unrelated to the product) — very strong.
3. **Suggestive** (hint at a quality, requiring imagination) — protectable.
4. **Descriptive** (directly describe the product) — protectable only after acquiring distinctiveness through use.
5. **Generic** (the common name of the product) — never protectable.

## Clearance search

Before launching, search the USPTO trademark database, state registrations, business names, domain names, app stores and general web use. Rights in the US can come from use alone ("common law" rights), so an unregistered prior user can still cause problems.

## Federal registration

1. Identify the goods and services and their classes.
2. File based on current use in commerce or a bona fide **intent to use**.
3. A USPTO examining attorney reviews the application and may issue an office action raising issues such as likelihood of confusion or descriptiveness.
4. If approved, the mark is published for opposition.
5. Registration issues (for intent-to-use filings, after you file proof of use).

The process often takes a year or longer. Registration gives nationwide priority, a legal presumption of ownership, the right to use ®, and help with customs enforcement and online platform takedowns.

## ™ vs ®

Use ™ (or ℠ for services) for any mark you claim. Using ® before federal registration is improper and can harm your rights.

## Keeping it alive

Use the mark consistently, police infringers, and file maintenance documents: a declaration of use between the 5th and 6th years after registration and renewals every 10 years. Abandoned marks can be lost.

## Domains and trademarks

Registering a domain doesn't create trademark rights by itself, and registering a domain in bad faith to profit from someone else's mark can lead to a UDRP complaint or a cybersquatting lawsuit.
""",
"faqs": [
 ("Do I need to register a trademark?", "No, use creates some rights, but federal registration gives much stronger, nationwide protection."),
 ("How long does trademark registration take?", "Often around a year or more, longer if the examiner raises issues or someone opposes."),
 ("Can I trademark a common word?", "Yes, if it's arbitrary for your goods (like a fruit name for computers), but not if it's generic or merely descriptive."),
],
"lawyer": "Use a trademark attorney for clearance opinions, office action responses, oppositions, or if you receive a cease-and-desist letter.",
"sources": [("USPTO — trademarks", "https://www.uspto.gov/trademarks")],
"tools": ["demand-letter-generator", "do-i-need-a-lawyer"],
},
{
"slug": "how-to-hire-the-right-lawyer",
"title": "How to Find and Hire the Right Lawyer (and What It Costs)",
"area": "lawyers-courts", "issue": "other",
"description": "Where to find a lawyer, fee structures explained, the questions to ask in a consultation and red flags to avoid.",
"takeaways": [
 "Match the lawyer's practice area to your problem; general practitioners rarely beat specialists in court.",
 "Fees are usually hourly, flat, contingency or a mix; always get the agreement in writing.",
 "Verify the licence and disciplinary record on your state bar's website.",
 "Many lawyers offer free first consultations, especially in injury, employment and criminal cases.",
],
"body": """
## Where to look

- **State and local bar referral services**, which screen lawyers and often offer low-cost first consultations.
- **Personal referrals** from people who had a similar case.
- **Legal aid organizations** if your income qualifies (see our [free legal aid page](/legal-aid/)).
- **Online directories and reviews**, read critically.
- **Our [free case review](/case-review/)**, which can connect you with independent attorneys who handle your type of matter, where permitted.

## Fee structures

- **Hourly:** billed in increments, often six minutes. Rates vary hugely by market and experience.
- **Flat fee:** one price for a defined task, common for wills, uncontested divorces, simple bankruptcies and some criminal matters.
- **Contingency:** the lawyer takes a percentage of what you recover, commonly about one-third, sometimes rising to 40% if a lawsuit is filed or the case goes to trial, and nothing if you lose. Most states require these agreements in writing. Case costs (filing fees, experts, records) may be charged separately. See the [contingency fee calculator](/tools/contingency-fee-calculator/).
- **Retainer:** an upfront deposit held in a trust account and billed against.
- **Limited-scope ("unbundled") help:** paying for specific tasks, such as reviewing documents or coaching you for a hearing.

## Questions to ask in the consultation

1. How many cases like mine have you handled, and what happened?
2. Who will actually work on my case day to day?
3. How will you communicate with me, and how fast do you respond?
4. What are the possible outcomes, and what's a realistic timeline?
5. How will I be billed, what costs should I expect, and who pays costs if we lose?
6. What do you need from me?

## Red flags

- Guaranteed results.
- Pressure to sign immediately.
- No written fee agreement.
- Unreturned calls before you've even hired them.
- Disciplinary history for client-money or honesty issues.

## Check the licence

Every state bar has a public lookup showing whether a lawyer is licensed and in good standing, and often their discipline history.
""",
"faqs": [
 ("Is a free consultation really free?", "Usually yes for the first meeting, especially for injury, employment, bankruptcy and criminal lawyers. Confirm before the meeting."),
 ("Can I negotiate a lawyer's fee?", "Often. Contingency percentages, hourly rates and payment plans can sometimes be negotiated, especially for strong cases."),
 ("Can I fire my lawyer?", "Yes, at any time, though you may owe for work done, and on contingency cases the first lawyer may claim part of the final fee."),
],
"lawyer": "If you're unsure whether you need a lawyer at all, take our two-minute quiz or request a free case review.",
"sources": [("American Bar Association — find legal help", "https://www.americanbar.org/groups/legal_services/flh-home/")],
"tools": ["contingency-fee-calculator", "do-i-need-a-lawyer"],
},
{
"slug": "small-claims-court-guide",
"title": "Small Claims Court: How to Sue (or Defend) Without a Lawyer",
"area": "lawyers-courts", "issue": "other",
"description": "Dollar limits, filing and serving a claim, preparing evidence, presenting your case and collecting the judgment.",
"takeaways": [
 "Small claims limits range from a few thousand dollars to about $25,000 depending on the state.",
 "Send a written demand letter first; many disputes settle and courts like to see you tried.",
 "Organise evidence in date order and bring copies for the judge and the other side.",
 "Winning is only half the job; you may need to use collection tools to get paid.",
],
"body": """
## Is small claims right for you?

Small claims courts handle money disputes up to a state-set limit, from around $2,500 in some states to $25,000 in others. Typical cases include unpaid loans or invoices, security deposits, property damage, faulty repairs and minor car accidents. Procedures are simplified, fees are low and in some states lawyers aren't allowed to represent parties at the hearing.

## Step 1: Send a demand letter

Explain what happened, the amount owed, how you calculated it and a deadline to pay, often 10 to 14 days. Our [demand letter generator](/tools/demand-letter-generator/) makes this fast. Keep proof of delivery.

## Step 2: File the claim

File in the right court, usually where the defendant lives or does business, or where the dispute happened. Use the defendant's exact legal name; for businesses, check the state business registry. Pay the filing fee or request a waiver.

## Step 3: Serve the defendant

Service rules vary: certified mail, sheriff, process server or another adult. The court won't hear the case until service is proven.

## Step 4: Prepare your evidence

- Contracts, invoices, receipts and estimates.
- Photos and videos, dated.
- Texts, emails and letters, printed.
- Witnesses, or signed statements if your court allows them.
- A one-page timeline and a calculation of the amount claimed.

Bring three copies of everything: for you, the judge and the other side.

## Step 5: The hearing

Arrive early, be respectful, and present your case in two or three minutes: what the agreement was, what went wrong, what it cost you, and what you want. Answer questions directly. Let the evidence do the work.

## Step 6: Collect

If the defendant doesn't pay voluntarily, courts offer tools such as wage garnishment, bank levies and property liens. Judgments are often valid for many years and can be renewed.

## If you're the defendant

Respond on time, gather your evidence, consider a counterclaim, and explore settlement or mediation before the hearing.
""",
"faqs": [
 ("Can I bring a lawyer to small claims court?", "Some states prohibit lawyers at small claims hearings, others allow them. Check your court's rules."),
 ("Can I appeal a small claims decision?", "Rules vary. In some states only the defendant can appeal, and appeals may result in a new trial in a higher court."),
 ("What if the other side doesn't show up?", "You can usually ask for a default judgment, provided you prove proper service."),
],
"lawyer": "Consider a lawyer if your claim exceeds the small claims limit, involves complex contracts or injuries, or the other side has a lawyer and the stakes are high.",
"sources": [("Cornell LII — small claims court", "https://www.law.cornell.edu/wex/small_claims_court")],
"tools": ["demand-letter-generator", "court-days-calculator"],
},
]
