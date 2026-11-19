Sampati by VayuX: The Master Product Document (the Sampati Granth)
=================================================================

*Product name: Sampati, branded "Sampati by VayuX" (confirmed; trademark
and domain clearance still open, see sections 5.6 and 13). In this
document the product, an open-source compliance automation platform, is
called "the Platform" or "Sampati".*

**Prepared by:** PragneshKumar S. Singh, Co-Founder & CTO, VayuX Systems
LLP

**Version:** 0.3 (build granth for Claude Code) · **Date:** 16 November
2026 · **Status:** internal planning document

Start here: Sampati explained simply
------------------------------------

This page is written so that anyone, even a ten-year-old, can understand
the whole project. The rest of the document goes deeper and deeper, so
you can stop reading at any point and still have the right picture.

### The one-minute story

Imagine a school. The school has rules: wear your uniform, finish your
homework, don't run in the corridors. Once in a while an inspector
visits and asks, "Can you prove you follow your rules?" If nobody wrote
anything down, the school panics.

Companies have rules too. Some come from the law (India's privacy law is
called DPDP). Some come from famous rule books (ISO 27001 and SOC 2).
Some come from customers ("show us that you keep our data safe"). Today
most companies prove it with messy spreadsheets and screenshots, and
they redo it all every year.

**Sampati is a smart rule-keeper for companies.** It knows the rules,
checks by itself whether the company follows them, keeps the proof safe,
reminds people when something is missing, and shows the inspector
everything neatly. It is free to use, and anyone can read how it works
(that is what "open source" means).

**What makes it special:** most tools like this are made for America and
know American rules best. Sampati is made for India first. You add a
"country pack" and it already knows that country's rules, deadlines and
forms. Other people can build packs for their own countries.

**Why now:** most of India's DPDP privacy duties start on 13 May 2027,
and many companies have no system at all.

**The name:** Sampati is a vulture in the Ramayana who could see Lanka
from far across the sea. A far-seeing watcher is exactly what a
compliance tool should be. The full name is always "Sampati by VayuX".

### The tiny dictionary (school edition)

  Real word            Think of it as                                                                  Example
  -------------------- ------------------------------------------------------------------------------- ---------------------------------------------------------------
  Framework            The school's rule book                                                          ISO 27001, SOC 2, the DPDP law
  Control              One rule from the book                                                          "Everyone logs in with a second password step"
  Evidence             Proof that you followed the rule                                                A photo of your finished homework
  Control test         A robot that checks one rule again and again                                    Every night it checks that the second password step is on
  Connector            A helper that visits another app and brings back proof                          A helper that asks the company's email system about passwords
  Plugin               An add-on that gives Sampati a new power                                        A new connector, a new country pack
  SDK                  A toolkit for building add-ons                                                  Instructions, blocks and a test kit
  Country pack         One country's rule book, checking robots, forms and deadlines in a single box   The India pack
  Ledger               A notebook with glued pages: if anyone changes a page, you can tell             Where evidence is stored safely
  Policy               A written promise that everyone reads and signs                                 "We keep customer data private"
  Risk                 Something that could go wrong                                                   A stolen laptop
  Audit and auditor    An inspection and the inspector                                                 A visit from an outside checker
  Trust centre         A shop window that shows customers you are safe                                 A public page with live status
  Organisation         One whole school using Sampati                                                  A company
  Community Edition    The free home version                                                           Everything most companies need
  Enterprise Edition   The company version with extra, paid features                                   Single sign-on, extra-safe audit tools
  Open source          A recipe published for everyone to read and improve                             The Sampati code
  Claude Code          The robot programmer that will build most of Sampati                            The tool that reads this document

### The three boxes (repositories)

-   **Box 1, the SDK (free, MIT licence):** the toolkit and rules for
    building add-ons.

-   **Box 2, the Community Edition (free, Apache 2.0 licence):** Sampati
    itself: the website, the engine, the helpers, the India pack.

-   **Box 3, the Enterprise Edition (paid, private, PCL licence):**
    extra features for big companies, built on top of Box 2.

Box 3 uses Box 2, and Box 2 uses Box 1. Never the other way round.

### How we build it, in five steps

1.  **Lay the foundation:** the toolkit rules, the login system, the
    rule books and the proof notebook.

2.  **Teach it to collect proof:** helpers that visit other apps, and
    robots that check rules.

3.  **Teach it India's rules:** the DPDP and CERT-In packs, an Indian ID
    scanner, and a breach alarm with the right countdown clocks.

4.  **Make it safe and ready for customers:** the inspector's view, the
    public trust page, security testing, and the paid enterprise
    features.

5.  **Grow:** a shop for add-ons, more helpers from the community, and
    rule packs for other countries.

### Map of this document

  Sections                        What you will find
  ------------------------------- -------------------------------------------------------------------------
  This page and sections 1 to 5   The story, the market, the competitors and what makes Sampati different
  Sections 6 and 7                The tools we build with, and how the project earns money
  Section 8                       Every feature explained: why it matters and how it works
  Sections 9 to 14                The plan, the risks, the success measures and the sources
  Sections 15 and 16              The three repositories, the licences and the build roadmap
  Section 17                      Every decision made so far, with its status
  Section 18                      The rules Claude Code must follow while building
  Sections 19 and 20              Technical blueprints and quality targets
  Section 21                      The feature-by-feature checklist with "done when" tests
  Section 22                      The starter content for the India packs
  Section 23                      The first tasks, in order
  Section 24                      When Claude Code must stop and ask a human
  Section 25                      An extra plain-language dictionary
  Section 26                      Document history and how to keep it up to date

### How to use this document with Claude Code

1.  Download this document as Markdown and keep it in the repository
    (for example as docs/SAMPATI-GRANTH.md).

2.  Create the agent rules file (AGENTS.md) in each repository from
    section 18.2.

3.  Tell Claude Code to read this whole document, then start at task
    T001 in section 23.

4.  As each feature is finished, tick its boxes in section 21.

5.  A human reviews every pull request. For security-critical code the
    review is mandatory and detailed.

How to read this document
-------------------------

Sections 1 to 5 are strategy: what we are building, who it is for, who
else is in the space, and why we win. Sections 6 and 7 cover how we
build it (tech stack) and how it earns money. Section 8 is the
feature-by-feature specification: what each must-have feature is and how
it is intended to work. Sections 9 to 13 cover the phased development
runway, risks, success metrics, open decisions and a glossary.

Two cautions apply throughout. First, competitor facts come from public
web sources checked in November 2026; anything marked "claim" is the
vendor's own statement and has not been independently verified. Second,
every regulatory statement is a planning note, not legal advice, and
must be reviewed by a qualified lawyer before it appears in product
content or marketing.

1. Product description
----------------------

### 1.1 One-line description

An open-source compliance automation platform, in the same category as
Vanta and Drata, that ships with country-specific compliance packs
(India first) and a plugin system that connects to the software a
company already uses, so that evidence is collected and controls are
monitored automatically instead of by hand.

### 1.2 The problem we solve

-   **Compliance is still manual.** Most companies prove compliance with
    spreadsheets, screenshots and consultant calls, repeated every audit
    cycle. Evidence goes stale the day after it is collected.

-   **Commercial automation tools are closed, USD-priced and
    US-shaped.** Vanta, Drata and similar platforms are built around US
    frameworks such as SOC 2. One open-source competitor's marketing
    claims legacy platforms cost USD 22,000 to 80,000 a year before
    audit fees (vendor claim).

-   **Open-source alternatives are either broad but light on automation,
    or automation-focused but SOC 2-centred.** None of the six
    open-source projects we studied is built around a non-US country's
    regulators.

-   **India has a stack of overlapping obligations.** The Digital
    Personal Data Protection (DPDP) Act 2023 with the DPDP Rules
    notified on 14 November 2025 (most obligations apply from 13 May
    2027, with penalties up to ₹250 crore), CERT-In directions (6-hour
    incident reporting, 180-day log retention), sector regulators (RBI,
    SEBI CSCRF, IRDAI) and customer-driven ISO 27001 and SOC 2. Existing
    tools treat Indian rules as "custom framework" add-ons, or are
    closed products.

### 1.3 Who it is for

  Segment                                     Who they are                                       Why they care                                                                                How they use the Platform
  ------------------------------------------- -------------------------------------------------- -------------------------------------------------------------------------------------------- -----------------------------------------------------------------------------------------------------
  Startups and SaaS companies                 Indian software firms selling to enterprises       Customers demand SOC 2 / ISO 27001 and now DPDP proof                                        Self-host free or use managed cloud; connect cloud, code and identity tools; reach audit-ready fast
  Regulated entities (BFSI)                   Banks, NBFCs, fintechs, brokers, insurers          RBI, SEBI and IRDAI rules; strict data residency; auditors and regulators ask for evidence   Self-hosted enterprise install inside their own environment; multi-regulator reporting
  SMEs and mid-size enterprises               Non-tech Indian companies handling personal data   Must meet DPDP by May 2027 with small teams                                                  Guided DPDP programme: data inventory, consent, rights requests, breach workflow
  Consultants, CA/CS firms, auditors, MSSPs   Advisors serving many clients                      Need one tool to run many client programmes                                                  Partner (multi-client) mode with per-client workspaces and white-label reports
  Global open-source community                Developers and compliance engineers                Want an open tool for their own country                                                      Use the core; write and publish packs and plugins for their country

### 1.4 What the Platform is, and what it is not

**It is:** a system of record for controls, policies, risks, evidence,
assets and vendors; an automation engine that tests controls
continuously; a library of country packs; a plugin ecosystem; and
portals for auditors and customers.

**It is not:** a certification body (auditors issue SOC 2 reports and
certification bodies issue ISO certificates, not us); a law firm; a SIEM
or security monitoring product; or a substitute for actually operating
security controls. It tracks and proves controls; it does not replace
them.

### 1.5 Product principles

1.  **Open by default.** The core, the plugin SDK and the country packs
    are open. We charge for operating things for people, not for the
    basics.

2.  **Country-native, not translated.** A country pack carries the
    regulator's own structure, deadlines and vocabulary.

3.  **Automation first, humans accountable.** Every automated result is
    explainable, overridable and attributable to a named owner.

4.  **Evidence stays with the customer.** Self-hosting, India data
    residency and a metadata-first design (the Platform stores proof of
    a check, not the sensitive data itself, wherever possible).

5.  **Plugins over monoliths.** Anything that touches an outside system
    is a plugin with a defined permission scope.

6.  **Explainable and auditable.** Every pass or fail traces to a
    source, a timestamp and a rule.

7.  **Secure by design.** The Platform holds credentials and sensitive
    evidence, so it must be harder to breach than the companies it
    serves.

2. Market context and timing
----------------------------

-   **DPDP is the near-term forcing function.** The Act received assent
    in August 2023, the Rules were notified on 14 November 2025, and
    most obligations apply from 13 May 2027, roughly six months after
    the date of this document. Penalties can reach ₹250 crore. A vendor
    guide estimates typical DPDP platform spend at ₹25 to 50 lakh a year
    (vendor claim), which leaves a clear gap for a free, self-hostable
    option.

-   **CERT-In rules create operational evidence needs.** Six-hour
    incident reporting, 180-day log retention and time synchronisation
    to an Indian source are all things a tool can check and prove.

-   **Sector regulators add layers.** RBI, SEBI CSCRF and IRDAI each
    require their own controls, testing and reporting. Regulated
    entities often insist on on-premise deployment for data residency.

-   **The vendor field is split.** Indian vendors that are native to
    these rules (ComplyDP, Niyam, Gordon and others) appear to be
    closed-source. Open-source tools (CISO Assistant, Eramba, Comp AI,
    Openlane, Probo, Unicis) are Western-built. The intersection, open
    source and Indian-native, looks empty (to be verified before we
    claim it, see section 5.4).

-   **Why open source works here.** Security buyers trust what they can
    inspect; there is no vendor lock-in; the community can scale
    connectors and country packs far beyond what one company can
    maintain; and CA/CS firms and auditors become a distribution
    channel.

3. Competitive landscape
------------------------

### 3.1 The six open-source tools at a glance

  Tool                 Origin                Licence                                             Core focus                                                     Automation depth                                             Commercial model
  -------------------- --------------------- --------------------------------------------------- -------------------------------------------------------------- ------------------------------------------------------------ --------------------------------------------------
  CISO Assistant       France (intuitem)     AGPLv3 community; enterprise folder is commercial   Broad GRC: risk, compliance, audit, vendors, privacy           Light in Community (API, n8n, MCP, Kafka hooks)              Free; Pro SaaS and on-prem; enterprise
  Eramba               UK/EU (Eramba LTD)    Free community edition; enterprise is paid          GRC suite: risk, compliance, policies, audits                  Low; some features paywalled                                 Flat annual fee, unlimited users
  Comp AI              USA (San Francisco)   AGPLv3 for about 99%; small commercial slice        SOC 2-first automation, plus ISO 27001, HIPAA, GDPR and more   High (claims 580+ integrations, device agent)                Free self-host; managed and bundled audit offers
  Openlane             USA                   Apache 2.0                                          Compliance programmes, evidence, workflows                     Medium, growing (Google Drive, GitHub, Entra ID, AWS, GCP)   Commercial cloud on open code
  Probo                USA/France (YC X25)   MIT                                                 Startup SOC 2 / ISO 27001 with hands-on service                Medium                                                       Service-led, plus platform
  Unicis Platform CE   Estonia               Apache 2.0 (feature-limited edition)                Privacy-led GRC for startups and SMEs                          Low to medium                                                Open core; paid SaaS edition

### 3.2 Detailed profiles

**CISO Assistant (intuitem, France)**

-   *What it does:* a GRC platform covering risk management, compliance
    and audit, third-party risk, business impact analysis, privacy and
    reporting. Frameworks are stored as data, and compliance is
    deliberately decoupled from security-operations implementation.
    Integration options include an API, n8n, MCP and Kafka.

-   *Licence and pricing:* AGPLv3 for the community edition; files in an
    enterprise directory use a commercial licence. A third-party listing
    shows Pro SaaS at about €39 per contributor per month and Pro
    on-premise at about €2,400 per instance per year.

-   *Strengths:* 200+ frameworks, a large and active community,
    self-host or SaaS, 26+ languages, a trust-centre portal and audit
    campaigns.

-   *Gaps:* strongest as a GRC record-keeper; an independent review says
    not to expect connector-led SOC 2 evidence automation from the
    Community edition; the multi-service deployment needs ops skill; no
    verified India-specific pack.

-   *Threat to us:* **high.** Frameworks-as-data means intuitem could
    add Indian packs quickly.

**Eramba (Eramba LTD)**

-   *What it does:* a GRC suite that has existed since 2015 covering
    risk, compliance, audits, policies and security programmes.

-   *Licence and pricing:* free community edition with no user or data
    limits; enterprise from €2,500 a year on-premise or €5,000 a year
    SaaS (third-party listing), flat fee, unlimited users.

-   *Strengths:* mature, predictable flat pricing, a large practitioner
    base.

-   *Gaps:* user reports say APIs, compliance-package mapping and email
    notifications are enterprise-only; teams without dedicated GRC staff
    may find setup and administration heavy; not focused on cloud
    evidence automation.

-   *Threat to us:* **medium.** Its paywall choices are the resentment
    we position against.

**Comp AI (USA)**

-   *What it does:* a SOC 2-first automation platform with policies,
    controls, tasks, a device agent that checks endpoints, a trust
    portal, security-questionnaire automation and an API. It claims 580+
    integrations and supports SOC 2, ISO 27001, HIPAA and GDPR, with
    more frameworks listed by third parties. It also sells a bundled
    audit and penetration-test offer.

-   *Licence and pricing:* AGPLv3 for about 99% of the code; the
    remaining slice is commercial. Pricing is quote-based and
    third-party estimates vary widely.

-   *Strengths:* the closest open-source match to Vanta and Drata in
    automation breadth; developer friendly.

-   *Gaps:* US and SOC 2 centred; a commercial slice exists; it does not
    itself issue the SOC 2 report; no non-US country packs; Indian
    regulators and data residency are not a focus.

-   *Threat to us:* **high** on the global automation story, **low** in
    India for now.

**Openlane (USA, Go)**

-   *What it does:* programmes with pre-built templates for SOC 2, ISO
    27001 and NIST 800-53; controls, risks, evidence, policies, tasks,
    questionnaires and vendor assessments; automation through
    integrations (Google Drive, GitHub, Entra ID, AWS, GCP) and
    configurable workflows; a GraphQL API.

-   *Licence:* Apache 2.0 for the open code; its hosted cloud is a
    commercial product.

-   *Strengths:* clean modern architecture, permissive licence,
    API-first.

-   *Gaps:* still pre-1.0, a smaller framework set, a trust centre only
    planned, no country packs.

-   *Threat to us:* **medium.** The best architectural reference to
    learn from.

**Probo (YC X25)**

-   *What it does:* a compliance platform for startups paired with a
    service model in which the team scopes the audit, writes policies,
    configures controls and collects evidence. The platform covers
    risks, vendors, evidence, policies and trust sharing.

-   *Licence and pricing:* MIT. A third-party tracker lists pricing from
    about USD 667 a month.

-   *Strengths:* permissive licence and hands-on guidance; proves that
    "open source plus services" sells.

-   *Gaps:* service-heavy (hard to scale as software), core frameworks
    are SOC 2 and ISO 27001, US startup focus.

-   *Threat to us:* **low to medium.**

**Unicis Platform Community Edition (Unicis.Tech OÜ, Estonia)**

-   *What it does:* an open-core trust-management platform for startups
    and SMEs. It began from GDPR work (records of processing, transfer
    impact assessments) and now lists ISO 27001, SOC 2, GDPR, NIS2 and
    NIST among 18+ frameworks (vendor claim). It also ships Atlassian
    Marketplace apps.

-   *Licence and pricing:* Apache 2.0 for the Community Edition, which
    is deliberately feature-limited; a managed Business Edition adds
    features. Premium plans start from about USD 19 a month (vendor
    claim).

-   *Strengths:* light installation (a database plus the app), privacy
    modules, low price.

-   *Gaps:* the Community Edition is intentionally limited; a European
    privacy lens; not India-aware.

-   *Threat to us:* **low.**

### 3.3 Indian closed-source players

  Vendor                                What they offer                                                                                                                                                                                           Notes
  ------------------------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -------------------------------------------------------------------------------------------------------------------
  ComplyDP (Bengaluru, Nihonium Labs)   DPDP-first platform for banks and NBFCs; one breach workflow covering DPDP, CERT-In, RBI and SEBI deadlines; data discovery and records of processing                                                     Claims zero PII ingestion through connectors
  Niyam (FlickerBytes)                  DPDP, RBI, SEBI, CERT-In plus ISO and SOC 2 packs; Indian PII scanner (Aadhaar, PAN, Voter ID, IFSC, UPI); connectors for Zoho, Razorpay, Darwinbox, Tally, DigiLocker; INR pricing from ₹4,999 a month   Some modules marked coming soon; sells DPO-as-a-service
  Gordon (Alphawave Technologies)       Pre-mapped RBI CSCRF, SEBI, DPDP, IRDAI and CERT-In frameworks with SOC and incident response                                                                                                             From about USD 1,787 a month for two frameworks (listing)
  Jupitice DPDP OS                      17-module DPDP operating system with a zero-data-exposure design                                                                                                                                          Launched via press coverage
  Cross Identity VISHWAAS AI            DPDP consent with cryptographically verifiable consent records                                                                                                                                            Offered at no cost per a press release
  IDfy (Privy)                          Privacy and data-governance platform                                                                                                                                                                      IDfy has said it plans to open-source parts of its stack for SMEs; a watch item for any "first open-source" claim
  Sprinto, Scrut                        Indian-founded SOC 2 / ISO automation vendors                                                                                                                                                             Closed SaaS; included from general market knowledge, verify before citing

### 3.4 Global closed incumbents

Vanta, Drata and Secureframe lead the market. A third-party comparison
credits market leaders with roughly 30 to 35+ frameworks and 300 to 400+
integrations each. They are USD-priced, closed-source SaaS, hosted
outside India, and treat non-US regulation as a customisation. Sprinto
and Scrut compete on lower price and India presence, but remain SOC 2 /
ISO-first.

### 3.5 What the landscape tells us

1.  **No open-source project is built around a non-US regulatory
    system.** That is our opening.

2.  **Open-core gating is a real pain point.** Paywalled APIs,
    notifications and mapping (Eramba), a limited community edition
    (Unicis) and commercial slices (Comp AI, CISO Assistant) all
    frustrate users.

3.  **There is a breadth-versus-automation split.** GRC tools are broad
    but light on evidence automation; automation tools are SOC
    2-centred. Nobody combines both with country depth.

4.  **Indian specialists are closed and often service-heavy.** Their
    pricing and lock-in leave room for an open alternative.

5.  **Integration counts are marketing; auditor acceptance is the real
    test.** Quality of evidence beats number of logos.

4. How we are different and what we do better
---------------------------------------------

### 4.1 Differences at a glance

  Dimension            Typical competitor                                                   Our approach
  -------------------- -------------------------------------------------------------------- -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Regulatory focus     US and EU frameworks first; other countries as "custom frameworks"   Country packs are first-class, versioned and community-maintained plugins; India ships first
  Automation           Either GRC record-keeping or SOC 2 evidence collection               Both: a GRC system of record plus connector-driven continuous control tests
  Plugin model         Vendor-built integrations inside the main repo                       Open plugin SDK with manifest, permission scopes, signed registry and sandboxed runtime; community can add connectors, packs, scanners and report templates
  Local ecosystem      Absent                                                               Connectors for Zoho, Razorpay, Tally, DigiLocker, Darwinbox and Indian cloud providers; scanners aware of Aadhaar, PAN, UPI and similar identifiers
  Data residency       SaaS in the US or EU; self-hosting is operationally heavy            One-command self-host and an India-region managed cloud; metadata-first evidence
  Open-core line       Paywalls on APIs, notifications, mapping and sometimes more          Basics are never gated: APIs, notifications, mapping, OIDC login, policies and evidence are free. Paid: SAML/SCIM, HA, advanced audit controls, SLAs, hosting, services
  Pricing              Per seat, in USD                                                     Per framework or entity, in INR; free self-host
  Regulatory change    Manual updates                                                       Regulatory change feed and versioned packs
  Incident deadlines   Generic incident log                                                 One breach workflow that tracks DPDP, CERT-In, RBI and SEBI clocks together
  Distribution         Direct sales                                                         Partner mode for CA/CS firms, auditors and MSSPs, plus community

### 4.2 Against each competitor: where we win and where they still lead

-   **vs CISO Assistant:** we win on evidence automation, Indian
    regulators and connectors for local software. They lead on framework
    count, community size and maturity. *Our answer:* do not race on 200
    frameworks; go deep on India, and make our framework format
    importable so users can bring their own.

-   **vs Eramba:** we win on modern UX and automation, and on a cleaner
    free tier. They lead on years in the field and flat-fee simplicity.
    *Our answer:* match flat, predictable pricing for enterprise.

-   **vs Comp AI:** we win on country packs, local data residency and a
    fully open plugin model. They lead on integration breadth, audit
    bundling and US startup traction. *Our answer:* do not chase SOC 2
    breadth first; ship SOC 2 and ISO 27001 as well-tested packs and
    partner with auditors.

-   **vs Openlane:** we win on country depth and a ready product for
    compliance teams. They lead on API-first architecture and Go
    engineering. *Our answer:* borrow the good ideas (typed API,
    workflow engine) and differentiate on packs and ecosystem.

-   **vs Probo:** we win on software scalability and community. They
    lead on a hands-on service wrapper and YC network. *Our answer:*
    offer partner-delivered services rather than staffing them all
    ourselves.

-   **vs Unicis CE:** we win on a fuller free edition and automation.
    They lead on a very light install and privacy modules. *Our answer:*
    keep our minimum install light (single-node, small footprint).

-   **vs Indian closed vendors (ComplyDP, Niyam, Gordon and others):**
    we win on openness, no lock-in, self-hosting and price (free core).
    They lead on being live today, on regulated-sector references and on
    services. *Our answer:* move fast on DPDP, win auditors and
    consultants as partners, and use open source as the trust advantage
    regulated buyers cannot get from them.

5. Unique selling proposition (USP)
-----------------------------------

### 5.1 The USP in one sentence

**The open-source compliance platform that speaks your country's
regulations: install a country pack and your controls, automated checks,
deadlines and reports already match what your regulator and auditor
expect.**

### 5.2 Five pillars

1.  **Country packs as code.** A pack is a versioned bundle of the
    regulation's controls, automated tests, evidence collectors,
    deadline workflows and report templates. Anyone can write one
    against a public specification. India ships first (DPDP, CERT-In,
    RBI, SEBI CSCRF, IRDAI), then others.

2.  **A real plugin ecosystem.** Connectors, packs, scanners and report
    templates all use the same SDK, so the community can extend the
    Platform without touching the core.

3.  **Implement once, comply many.** One control maps to many frameworks
    through a crosswalk, so a single piece of evidence can satisfy DPDP,
    CERT-In, ISO 27001 and SOC 2 at the same time.

4.  **Sovereign by design.** Self-host in minutes, or use the
    India-region cloud; sensitive data is scanned where it lives and
    only metadata is stored.

5.  **Honest open source.** No paywalls on basics. We earn from running,
    supporting and certifying, not from holding features hostage.

### 5.3 Positioning statement

For Indian companies that must prove compliance to regulators, auditors
and customers, the Platform is an open-source compliance automation
platform that turns Indian regulations into automated, auditable checks.
Unlike closed vendors, it can be inspected, self-hosted and extended by
anyone; unlike Western open-source tools, it is built around Indian
rules and software from day one.

### 5.4 About the claim "India's first open-source compliance automation tool"

Do not use this wording until it has been verified. Indian closed-source
vendors already market "India-first" positioning, one of them has said
it may open-source parts of its stack, and my research was not
exhaustive. A safer, defensible line is: **"The open-source compliance
automation platform built for India's regulators."** Before any "first"
claim: (1) search GitHub and GitLab for DPDP, CERT-In, CSCRF and
compliance-automation repositories; (2) check what IDfy and the other
Indian vendors have actually released; (3) get marketing and legal
review; (4) date-stamp the claim ("as of" a month and year).

### 5.5 What is hard to copy (our moat)

-   **Depth of the India pack** and the speed at which it tracks
    regulatory change.

-   **Community maintainers** for packs and connectors, which compound
    over time.

-   **Partner network** of CA/CS firms, auditors and MSSPs who deliver
    and refer.

-   **Local connector coverage** for Indian SaaS, payments and
    government services.

-   **Trust of regulated buyers** earned through open code, self-hosting
    and published security practices.

### 5.6 Name and brand: Sampati by VayuX

The product name is final: **Sampati**, always shown as "Sampati by
VayuX".

**Why this name.** In the Ramayana, Sampati is Jatayu's elder brother,
the vulture who could see Lanka across the sea. That far sight stands
for continuous oversight of an organisation's compliance posture, and it
keeps the VayuX sky theme (the VayuX logo carries an eagle head).

**Naming convention for all VayuX tools.** Every tool takes the name of
a character from Hindu mythology (Ramayana, Mahabharata and other texts)
and is branded "\[Name\] by VayuX". The endorsed format keeps the VayuX
search terms working. Prefer characters over deities, and keep any
imagery respectful.

**Known overlaps** (web check on 17 November 2026 from search results;
not a legal clearance, verify each before relying on it):

-   The Government of India runs a system called [SAMPATI (System for
    Asset Monitoring, Presentation and
    Tracking)](https://sampati.cga.gov.in), reported live from
    October 2024.

-   [Sampat](https://village.ai/company/sampat-software) is an Indian
    software company offering asset management and IT ticketing.

-   [Sammati](https://yourstory.com/companies/sammati) is a DPDP-native
    consent and privacy platform, one letter away in the same niche.

-   [Sampati Securities
    Limited](https://www.paperli.ai/company/sampati-securities-limited-U67120GJ1995PLC024926)
    is a finance company in Ahmedabad, and the Hindi word *sampatti*
    (property, wealth) sounds close.

**Mitigations.** Always use the full "Sampati by VayuX" form with the
descriptor "open-source compliance automation"; publish a pronunciation
guide (sum-PAH-tee); complete IP India and WIPO clearance in classes 9
and 42 before launch; use a distinct bird-based logo; and avoid
describing the product as asset management.

6. Architecture and tech stack
------------------------------

### 6.1 Architecture in plain words

The Platform has five layers:

1.  **Experience layer:** the web app for compliance teams, the auditor
    portal, the public trust centre, a command-line tool and the API.

2.  **Core services:** authentication and access control, the framework
    and control engine, the evidence service, the automated test (rules)
    engine, workflows and notifications, and the policy, risk, vendor,
    asset and privacy (DPDP) modules.

3.  **Plugin runtime:** connectors, country packs, scanners and report
    templates, each a package that runs outside the core under a
    declared permission scope.

4.  **Data layer:** a relational database, encrypted object storage for
    evidence files, a job queue and search.

5.  **Edge components:** a device agent for laptops and servers, and an
    optional collector that runs inside the customer's own network and
    sends back only metadata.

**How data flows, end to end:**

1.  A connector pulls information from an outside system using a
    read-only credential (for example, "is multi-factor authentication
    enforced for all users?" from the identity provider).

2.  The result is normalised into an **evidence record**: what was
    checked, where, when, the result, and a cryptographic hash.

3.  The rules engine evaluates **control tests** against the new
    evidence (for example, "MFA enforced for 100% of active users").

4.  The control's status updates (passing, failing, or needs review),
    and the Platform raises a task or alert for the control owner if
    something fails.

5.  Auditors and customers see the same status, with the evidence trail,
    through the auditor portal and the trust centre.

### 6.2 Recommended tech stack

  Layer                                   Choice                                                                                                                                                                                                                                                                 Why                                                                                                            Alternative considered
  --------------------------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -------------------------------------------------------------------------------------------------------------- ----------------------------------------------------------------------------
  Backend                                 Python 3.12 with FastAPI and typed models                                                                                                                                                                                                                              The best cloud and SaaS SDKs are in Python; large contributor pool in India; fastest way to write connectors   Go (strong performance, smaller plugin-author pool); revisit for hot paths
  Frontend                                TypeScript, React (Next.js), Tailwind CSS, accessible component library                                                                                                                                                                                                Mainstream skills, fast to build, good accessibility                                                           Other frameworks add no clear benefit
  API                                     REST with an OpenAPI specification as the main contract; webhooks                                                                                                                                                                                                      Easiest for integrators; self-documenting                                                                      GraphQL can be added later
  Database                                PostgreSQL with row-level security for tenant isolation and JSONB for flexible evidence metadata                                                                                                                                                                       One reliable store; strong isolation features                                                                  Separate database per tenant for the largest customers
  Jobs and workflows                      Redis-backed job queue for the MVP; a durable workflow engine from Phase 3                                                                                                                                                                                             Keeps the MVP simple; long-running workflows (audits, breach clocks) need durability later                     Run a workflow engine from day one (more moving parts)
  File storage                            Any S3-compatible object store, encrypted at rest with per-tenant keys                                                                                                                                                                                                 Works on cloud and on-premise                                                                                  Local disk for tiny installs
  Search                                  PostgreSQL full-text search first                                                                                                                                                                                                                                      No extra service to run                                                                                        Dedicated search service only if needed
  Authentication                          Built-in OIDC login (Google, Microsoft), MFA (TOTP and WebAuthn), scoped API tokens; SAML and SCIM in the enterprise tier                                                                                                                                              Covers most users for free                                                                                     Delegating to an external identity server for enterprise installs
  Rules engine                            Declarative YAML control tests with CEL expressions, evaluated in a sandbox                                                                                                                                                                                            Readable by compliance staff, safe to run, easy for the community to write                                     Rego policies as an advanced option later
  Plugin runtime                          Out-of-process plugins talking to the core over gRPC or HTTP; signed manifest; permission scopes; containerised with network allow-lists; Python SDK first, TypeScript second, any language via the protocol                                                           A broken or hostile plugin cannot take down or read the core                                                   In-process plugins (simpler, but unsafe)
  Device agent and on-premise collector   Go, single static binary for Windows, macOS and Linux, osquery-compatible checks                                                                                                                                                                                       Easy install, small footprint, no runtime needed                                                               Scripts (harder to ship and secure)
  Evidence integrity                      SHA-256 hash chain over an append-only evidence ledger, with optional trusted timestamping                                                                                                                                                                             Lets an auditor verify that evidence was not altered                                                           Database audit tables only
  Indian PII scanner                      Runs in the customer environment; pattern matching plus checksum validators (for example the Aadhaar check-digit scheme and PAN structure) and an optional classifier                                                                                                  Few false positives; raw data never leaves the customer                                                        Cloud-side scanning (rejected for privacy)
  AI layer                                Provider-agnostic interface using the common OpenAI-compatible API protocol, so hosted or self-hosted models can be used; retrieval over the customer's own policies and the pack's source text; human approval required; disabled by default in air-gapped installs   Keeps data local when needed; no lock-in to one model vendor                                                   Hard-wiring one provider (rejected)
  Deployment                              Docker Compose (single node), Helm chart (Kubernetes), air-gapped bundle                                                                                                                                                                                               Minutes to first run; fits banks                                                                               Managed-only (rejected)
  Observability                           OpenTelemetry, Prometheus-compatible metrics, structured logs                                                                                                                                                                                                          Standard and vendor-neutral                                                                                    
  CI/CD and supply chain                  GitHub Actions; signed releases and container images; software bill of materials for every release; dependency scanning; mandatory review                                                                                                                              Credibility with security buyers                                                                               
  Hosting (managed cloud)                 India-region infrastructure from a major or domestic provider (to be chosen)                                                                                                                                                                                           Data residency                                                                                                 
  Billing                                 Razorpay with GST-compliant invoicing                                                                                                                                                                                                                                  Native to the Indian market                                                                                    

### 6.3 Securing the Platform itself

Because the Platform holds credentials and sensitive evidence, security
is a feature, not a task:

-   Connectors default to **read-only, least-privilege** scopes and show
    the exact permissions they request.

-   Credentials live in an encrypted secrets vault; each tenant has its
    own encryption keys.

-   The design is **metadata-first**: store the result of a check and a
    hash, not the personal data that was inspected.

-   Plugins are signed, sandboxed and permission-scoped; unsigned
    plugins need an explicit admin opt-in.

-   Every administrator action is written to a tamper-evident audit log.

-   A written threat model is kept current, and an independent
    penetration test is completed before general availability.

-   A public security policy and responsible-disclosure process are
    published at launch.

-   We **use the Platform to achieve our own SOC 2 and ISO 27001** and
    show it publicly: the best proof is a compliance tool that is itself
    compliant.

### 6.4 Licensing approach (decision needed)

  Option                                                                                                                                                          Pros                                                                                 Cons
  --------------------------------------------------------------------------------------------------------------------------------------------------------------- ------------------------------------------------------------------------------------ --------------------------------------------------------------------------------
  Core under AGPLv3, enterprise folder under a commercial licence (CISO Assistant and Comp AI pattern)                                                            Deters closed-source cloud clones; self-hosting stays free                           Some enterprises avoid AGPL; needs clear line between free and commercial code
  Everything permissive (Apache 2.0 or MIT) with proprietary cloud and enterprise modules (Openlane, Unicis, Probo pattern)                                       Maximum adoption and contribution                                                    Anyone, including large vendors, can host it commercially
  Split licensing: Apache 2.0 for the plugin SDK, interfaces and country packs; AGPLv3 for the core server and UI; commercial licence for the enterprise folder   Encourages packs and plugins (including commercial ones) while protecting the core   More complex to explain and administer

**Decision:** Apache 2.0 for the Community Edition core, MIT for the
plugin SDK and a proprietary commercial licence (PCL) for the Enterprise
Edition, kept in three separate repositories (see section 15).
Regardless of the choice, we also need a trademark policy for the name
and logo, a contributor process (a Developer Certificate of Origin is
lighter than a contributor licence agreement), and legal review of the
framework text we may or may not redistribute (many standards, such as
ISO texts, are copyrighted; packs should ship our own control wording
and mappings, with references to official clause numbers).

7. Revenue model
----------------

### 7.1 Model in one paragraph

Open core, with a managed India-region cloud and partner-delivered
services. The core Platform and country packs are free. Customers pay
for being operated for (managed hosting), for enterprise needs (single
sign-on, high availability, advanced audit controls, SLAs), for
expertise (implementation and advisory) and, later, for ecosystem
services (marketplace and certification). Services fund the early period
while the software matures; the mix shifts toward software over time.

### 7.2 Revenue streams

All prices are **indicative placeholders** to be tested with customers
before launch. Anchors from the market: Niyam lists ₹4,999 a month;
Gordon lists about USD 1,787 a month for two frameworks; a vendor guide
says DPDP platforms commonly cost ₹25 to 50 lakh a year; Eramba
enterprise starts at about €2,500 a year and CISO Assistant Pro
on-premise at about €2,400 a year.

  Stream                           What we sell                                                                                        Who pays                                         Indicative pricing                                                                                                                                                                                                                                    Starts
  -------------------------------- --------------------------------------------------------------------------------------------------- ------------------------------------------------ ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -------------------------------
  Implementation and advisory      DPDP readiness, gap assessment, audit preparation, pack customisation                               Companies preparing for DPDP, ISO 27001, SOC 2   Fixed-fee packages, roughly ₹1.5 to 6 lakh by company size                                                                                                                                                                                            Phase 1
  Managed Cloud, India region      Hosted, backed-up, upgraded Platform                                                                SMEs, startups, mid-size firms                   Starter about ₹7,999/month (1 pack plus 1 global framework, up to 50 staff); Growth about ₹24,999/month (up to 3 frameworks, 250 staff, trust centre, auditor portal); Business from about ₹75,000/month (multi-entity, SAML SSO, priority support)   Phase 2 beta, Phase 3 general
  Enterprise self-hosted licence   Commercial features and support for on-premise installs                                             Banks, NBFCs, large enterprises                  Flat annual fee per instance, roughly ₹3 to 10 lakh by size and support tier, unlimited users                                                                                                                                                         Phase 3
  Regulatory update subscription   Fast, reviewed updates when RBI, SEBI, CERT-In or DPDP guidance changes                             Regulated entities and consultants               Add-on of about 10 to 15% of the platform fee                                                                                                                                                                                                         Phase 3
  Partner programme                Multi-client console, white-label reports, discounted bundles for CA/CS firms, auditors and MSSPs   Advisory firms                                   Volume discount of about 20 to 30% plus referral share                                                                                                                                                                                                Phase 3
  Marketplace and certification    Paid third-party plugins (revenue share), certified-implementer training and exams                  Plugin authors, partners                         Revenue share of about 15 to 30%; exam and training fees                                                                                                                                                                                              Phase 4
  Sponsorship and grants           Open-source sponsorships, grants, programmes                                                        Foundations, companies                           Variable                                                                                                                                                                                                                                              Any time

### 7.3 What is free forever and what is paid

  Always free (self-host)                                                         Paid
  ------------------------------------------------------------------------------- -----------------------------------------------------------------------------
  All core modules: controls, evidence, policies, risks, vendors, assets, tasks   Managed hosting, backups, monitored upgrades
  API, webhooks, notifications and framework mapping                              SAML single sign-on and SCIM user provisioning
  Country packs and the plugin SDK                                                High availability and multi-region setups
  OIDC login, MFA, unlimited users                                                Advanced audit controls (legal hold, dual approval, certified export packs)
  Auditor portal and basic trust centre                                           SLAs, priority and 24x7 support
  Community connectors                                                            Regulatory change feed, partner console, white-label

The rule: **never put an API, notification or mapping feature behind a
paywall.** That is exactly what frustrates users of the current
open-source tools.

### 7.4 Illustrative first-year view

This is a planning illustration built on stated assumptions, **not a
forecast**. It covers the first 12 months of selling and excludes costs
(team, infrastructure, legal, security testing).

  Stream                Assumption                                                             Illustrative revenue
  --------------------- ---------------------------------------------------------------------- ----------------------
  Services              10 engagements at about ₹3 lakh                                        ₹30 lakh
  Managed Cloud         15 paying accounts on average across the year at about ₹15,000/month   ₹27 lakh
  Enterprise licences   4 licences at about ₹5 lakh                                            ₹20 lakh
  Partner and other     Referrals, sponsorships                                                ₹5 lakh
  **Total**                                                                                    **about ₹82 lakh**

Services dominate the first year by design. The goal is to grow the
software streams (cloud, licences, subscriptions) until they are the
majority of revenue by year three.

### 7.5 Pricing principles

-   Priced in rupees, with GST invoices, and **per framework or legal
    entity rather than per employee**, so costs are predictable.

-   Public price list (among the tools compared, only one openly
    publishes prices), which builds trust.

-   Annual discounts; free or discounted plans for students, non-profits
    and open-source projects to build community.

-   Enterprise pricing is flat, not metered, so large teams are not
    punished for adding users.

### 7.6 How we will validate the model

1.  Interview at least 10 target buyers (startups, a bank or NBFC, two
    CA/CS firms) about willingness to pay for hosting versus
    self-hosting.

2.  Run 3 design-partner pilots, with a written price discussion at the
    end of each.

3.  Track the conversion from free self-host users to paid cloud or
    support; adjust the line between free and paid if the free tier
    cannibalises revenue or the paid tier feels artificial.

4.  Revisit pricing at the end of each phase.

8. Feature specification: every must-have feature and how it works
------------------------------------------------------------------

Each feature below has a **phase tag** (the phase in which it first
ships; see section 9), a short statement of why it matters, and a
plain-language description of how it is intended to work. Features are
grouped into seven areas.

### Area A: Foundation

**F1. Workspaces, organisations and entities** (Phase 1)

*Why:* companies have subsidiaries, business units and clients;
consultants manage many companies. *How it works:* an **organisation**
is the top-level tenant. Inside it, **entities** (legal entities or
business units) each have their own scope, owners and framework
selections, while sharing common policies and controls where wanted.
Every record carries its tenant and entity, and the database enforces
isolation with row-level security so one tenant can never read another's
data.

**F2. Users, roles and sign-in** (Phase 1; SAML and SCIM in Phase 3)

*Why:* compliance data is sensitive and auditors need narrow access.
*How it works:* users sign in with OIDC (Google or Microsoft) or email,
with multi-factor authentication. Built-in roles (admin, compliance
manager, control owner, contributor, read-only executive, auditor) can
be refined into custom roles. Auditor access is time-boxed and
read-only, scoped to one audit. API tokens have scopes and expiry.
Enterprise installs add SAML and automated user provisioning (SCIM).

**F3. Platform audit log** (Phase 1)

*Why:* the tool must be able to prove who changed what. *How it works:*
every create, change, approval, login and permission change is written
to an append-only log with actor, time, object and before/after values.
Logs can be exported or streamed to the customer's own log system, and
in the enterprise tier are protected against deletion.

### Area B: Compliance engine

**F4. Framework and control library (frameworks as data)** (Phase 1)

*Why:* adding a framework should be data work, not programming. *How it
works:* a framework is a structured file (sections, requirement IDs, our
own plain-language descriptions, references to official clause numbers)
loaded into the library. Frameworks are versioned, so an organisation
can stay on one version and upgrade when ready. We ship our own wording
rather than copying copyrighted standards text. Day-one frameworks: SOC
2, ISO 27001:2022, and the India pack (F6). An importer lets users bring
their own framework from a spreadsheet or file.

**F5. Unified control set and crosswalk ("implement once, comply
many")** (Phase 1 basic, Phase 2 full)

*Why:* the same real-world control (for example "multi-factor
authentication for all staff") satisfies many frameworks. *How it
works:* the Platform keeps one list of **controls** and a **mapping
table** that links each control to requirements in every framework. A
company implements the control and attaches evidence once; every linked
framework's progress updates. Mappings are community-reviewed, versioned
and shown with a confidence note so users can see where a mapping is
partial.

**F6. Country packs (regulation-as-code)** (Phase 2 for DPDP and
CERT-In; Phase 3 for RBI, SEBI CSCRF and IRDAI)

*Why:* this is our core differentiator. *How it works:* a pack is an
installable bundle containing (1) the regulation as a framework, (2) the
controls and mappings, (3) automated control tests and the connectors
they need, (4) deadline workflows (for example a breach clock), (5)
policy and notice templates in the right language, and (6) report
templates that match what the regulator or auditor expects. Installing
the India pack for an entity switches on all of this together. Packs
have owners, a changelog and a version, and are written against a public
pack specification so others can build packs for other countries.

**F7. Gap assessment and readiness score** (Phase 1)

*Why:* the first question every customer asks is "where do we stand?".
*How it works:* the user chooses frameworks and answers a short, guided
scoping questionnaire (company size, data types, sector, cloud usage).
The Platform generates the applicable control list, marks each control
as not started, in progress, implemented or not applicable (with a
reason), and calculates a readiness score per framework with a
prioritised list of gaps and suggested next steps.

**F8. Regulatory change feed and pack versioning** (Phase 3)

*Why:* rules change; stale compliance is a risk. *How it works:*
maintainers publish reviewed pack updates when a regulator issues new
rules or guidance. Customers see a "what changed" diff showing new,
changed and removed requirements and which of their controls are
affected, with tasks created for each. The free edition receives pack
releases on the normal release schedule; the paid feed is faster and
reviewed by legal advisers.

### Area C: Automation

**F9. Plugin framework and SDK** (Phase 1 internal alpha; Phase 2
public)

*Why:* a plugin ecosystem is what lets the community scale us. *How it
works:* a plugin is a package with a **manifest** declaring its type
(connector, pack, scanner, report template), the permissions it needs,
its configuration fields and the evidence it produces. It runs outside
the core, in a container with a network allow-list, and talks to the
core over a defined protocol. Admins see and approve permissions at
install time. Plugins are signed, and a registry lists verified ones.
The SDK gives authors helpers for authentication, pagination, rate
limiting, testing against recorded responses and publishing.

**F10. Connectors (initial set)** (Phase 2 first ten; more in Phase 3
and 4)

*Why:* automation only works if the tools a company already uses can be
read. *How it works:* each connector authenticates with a read-only
credential, fetches defined data on a schedule (or on a webhook), and
converts it to evidence records. Planned order: cloud (AWS, Google
Cloud, Microsoft Azure), code (GitHub, GitLab), identity (Google
Workspace, Microsoft Entra ID), tickets and chat (Jira, Slack), HR
(Darwinbox or a similar Indian HR system), and the device agent.
India-specific connectors come next: Zoho suite, Razorpay, Tally,
DigiLocker and Indian cloud providers. Each connector page lists exactly
what it reads and the controls it supports.

**F11. Evidence collection and ledger** (Phase 1)

*Why:* evidence is the product auditors actually look at. *How it
works:* evidence arrives three ways: automatically from connectors, from
the device agent, or manually (file upload, link or written statement).
Each record stores the source, collection time, who or what collected
it, a validity period, the result, and a SHA-256 hash; a hash chain
links records so tampering is detectable. Evidence has an expiry (for
example 90 days) after which the control shows as "stale" and a refresh
task is raised. Large files go to encrypted object storage; the database
keeps metadata.

**F12. Automated control tests (continuous monitoring)** (Phase 2)

*Why:* point-in-time checks go stale; continuous checks catch drift.
*How it works:* a control test is a short declarative definition: which
evidence to read, a condition (for example "all active users have MFA
enabled"), a schedule, a severity and exception handling. The rules
engine evaluates tests whenever new evidence arrives. Results are pass,
fail or error, with the exact data that caused the result. A failing
test marks the control as failing, opens a task for the owner with
remediation guidance, and notifies them. Owners can record a
time-limited exception with a reason and approver.

**F13. Device agent** (Phase 2)

*Why:* many controls concern laptops and servers (disk encryption,
patching, screen lock, antivirus). *How it works:* a small agent
installed on staff devices runs read-only checks on a schedule (hourly
by default) and reports pass/fail results, not file contents. It
supports Windows, macOS and Linux, can be deployed by existing
device-management tools, and is open source so customers can audit it.
Reports map to personnel and asset records.

**F14. Evidence requests and manual evidence** (Phase 1)

*Why:* not everything can be automated (for example a signed board
resolution). *How it works:* a compliance manager creates a request
(what, who, due date) that appears in the owner's task list and email or
chat. The owner uploads the evidence or records a statement, and a
reviewer approves or rejects it with comments. Approved items become
evidence records like any other.

### Area D: Programme management

**F15. Policy management and attestations** (Phase 1)

*Why:* every framework requires written policies that staff have read.
*How it works:* a template library (in English, with Hindi for key
staff-facing policies in Phase 2) gives editable starting policies.
Policies have owners, versions, review dates and an approval workflow.
Once approved, the Platform distributes them to staff and tracks
acknowledgements, chasing anyone overdue. Each policy links to the
controls and requirements it supports.

**F16. Risk register and assessment** (Phase 2)

*Why:* ISO 27001, SOC 2 and the Indian sector rules all expect
documented risk management. *How it works:* users record risks (or pick
from a starter catalogue, including India-sector scenarios), score
likelihood and impact on a configurable scale, and assign owners. Each
risk is linked to controls that reduce it, with a treatment plan
(mitigate, accept, transfer, avoid), residual risk and review date. A
heat map and a list of risks above the appetite threshold feed the
dashboards.

**F17. Vendor (third-party) risk management** (Phase 2)

*Why:* regulators and customers expect control over suppliers and data
processors. *How it works:* a vendor register stores each vendor, what
data they handle, criticality and the contract and data processing
agreement dates. Vendors are tiered by risk; higher tiers receive a
security questionnaire sent by link and can upload their own
certificates and reports. Renewal and review reminders are automatic,
and cross-border transfers are flagged for the privacy module.

**F18. Asset inventory** (Phase 2)

*Why:* you cannot protect what you have not listed. *How it works:*
assets (cloud resources, code repositories, devices, applications, data
stores) are imported by connectors and the agent, then enriched by
owners with classification, business purpose and data types. Gaps (for
example assets without an owner) become tasks.

**F19. People compliance** (Phase 2)

*Why:* auditors check that staff are trained and that joiners and
leavers are handled. *How it works:* the HR connector (or a CSV import)
provides the staff list. Onboarding and offboarding checklists are
generated automatically (for example, access removed within an agreed
number of days). Security and privacy awareness training is assigned and
tracked, with completion evidence stored. Training content can be linked
or uploaded.

**F20. Tasks, workflows, notifications and SLAs** (Phase 1)

*Why:* compliance runs on small recurring actions that get forgotten.
*How it works:* every failing control, expiring evidence, overdue policy
or incoming request becomes a task with an owner, due date and priority.
Simple configurable workflows add approvals and escalation (for example,
remind after 3 days, escalate to the manager after 7). Notifications go
by email, Slack and Microsoft Teams in Phase 1 to 2, with WhatsApp
Business as a plugin later. A weekly digest summarises what is due.

### Area E: India privacy and incident management

**F21. DPDP privacy module** (Phase 2)

*Why:* most DPDP obligations apply from 13 May 2027 and many Indian
companies have no process at all. *How it works (to be validated by
legal counsel):* the module provides (1) a **data inventory** (what
personal data, why, where, which processors, how long kept); (2) a
**notice and consent register** that stores versions of notices and
records consent events with timestamps, and can link to a Consent
Manager where one is used; (3) a **data principal rights workflow** for
access, correction, erasure and grievance requests, with identity
checks, deadline tracking and a response log; (4) a **grievance officer
and DPO page** with published contact details; (5) **processor
tracking** with data processing agreements; (6) flags for **children's
data** and for **cross-border transfers**; and (7) for significant data
fiduciaries, templates and tasks for data protection impact assessments
and periodic audits.

**F22. Indian PII scanner and data discovery** (Phase 2)

*Why:* companies cannot protect or report on personal data they have not
found. *How it works:* a scanner runs inside the customer's environment
against databases, file stores, cloud buckets and code repositories. It
looks for Indian identifiers (Aadhaar, PAN, voter ID, IFSC, UPI IDs,
GSTIN, phone numbers, email addresses) and uses structure and checksum
validation (for example the Aadhaar check-digit scheme and PAN format)
to cut false positives. Only **metadata** leaves the environment: where
something was found, what type, how many, and a masked sample or hash,
never the raw value. Findings feed the data inventory and create tasks
(for example, "Aadhaar stored unencrypted in this table"). The scanner
is itself a plugin, so more patterns can be added.

**F23. Incident and breach management with regulator clocks** (Phase 2)

*Why:* a breach triggers several deadlines at once and teams lose
precious hours working out who must be told. *How it works:* when an
incident is created, the user answers a few questions (what was
affected, whether personal data is involved, which regulators apply).
The Platform starts a **clock for each applicable obligation**, such as
the CERT-In six-hour reporting window, DPDP notification to the Data
Protection Board and affected individuals, and RBI or SEBI reporting for
regulated entities, with the exact deadlines set by the installed pack.
It assigns tasks, supplies notification templates, records every action
with a timestamp, and produces a post-incident report. Deadlines are
configurable and always shown with the pack version they came from.

### Area F: Assurance and sharing

**F24. Audit management and auditor portal** (Phase 2 export; Phase 3
full portal)

*Why:* the audit is where all the work pays off. *How it works:* an
**audit project** has a scope, period and auditor team. The auditor
receives a read-only, time-limited portal login, sees the controls in
scope with their evidence trail, uses sampling tools, requests more
evidence (the traditional "prepared by client" list), and records
findings and exceptions. At the end, the Platform exports an **audit
pack** (controls, evidence index, test results, exceptions) in a
standard format. Audit comments never alter the underlying evidence.

**F25. Trust centre** (Phase 3)

*Why:* customers ask security questions constantly; a public page
answers many of them. *How it works:* a branded page shows chosen
controls, certifications and policies, and the live status of key
controls. Sensitive documents sit behind a request-and-approve flow with
a click-through NDA. The page is generated from live data, so it never
drifts from reality, and it can run on the company's own domain.

**F26. Reporting and dashboards** (Phase 2 basic; Phase 3 board reports)

*Why:* leaders need a one-page answer. *How it works:* dashboards show
readiness per framework, failing controls, overdue tasks, expiring
evidence, risk heat map and vendor status. One-click reports (PDF and
spreadsheet) include a board summary, a gap report and regulator-style
templates provided by each pack.

**F27. Security questionnaire automation** (Phase 3)

*Why:* sales teams lose days answering customer security questionnaires.
*How it works:* the user uploads a questionnaire. The Platform matches
each question to approved answers in an **answer library** built from
controls, policies and previous responses, proposes answers with a link
to the source, and flags questions with no good match for human answer.
Approved answers are saved back to the library. Nothing is sent without
human approval.

### Area G: Platform and operations

**F28. API, webhooks, command line and MCP server** (Phase 1 API and
webhooks; Phase 3 MCP)

*Why:* integrators and automation teams must be able to drive the
Platform. *How it works:* every feature available in the interface is
available through a documented REST API described by an OpenAPI file.
Webhooks announce events such as a control failing or evidence expiring.
A command-line tool supports scripting and compliance-as-code workflows
(for example, run checks in a CI pipeline). In Phase 3 an MCP server
lets AI agents query and update the Platform with the same permission
checks as a human user.

**F29. AI assistant (assistive only)** (Phase 3 first features; Phase 4
broader)

*Why:* writing policies, mapping controls and answering questions are
slow. *How it works:* the assistant can draft a policy from a template
and company context, suggest which controls a piece of evidence
supports, explain a regulation clause in plain language with a link to
the source text, and propose questionnaire answers. Hard rules: every
suggestion is labelled as AI-generated, cites its source, and needs
human approval before it changes any record; customer data is not used
to train anything; it can run against self-hosted models; and it is off
by default in air-gapped installs.

**F30. Deployment, backup, upgrade and air-gapped install** (Phase 1)

*Why:* regulated buyers need to run it themselves, safely. *How it
works:* a single Docker Compose file starts a working instance in
minutes; a Helm chart supports Kubernetes. Built-in commands handle
encrypted backup, restore and one-step upgrades with automatic database
migrations. An air-gapped bundle includes all images and packs for
networks without internet. Configuration lets the operator pin data to a
specific region and choose their own storage, database and keys.

**F31. Localisation and Indian formats** (Phase 2)

*Why:* "made for India" includes language and formats. *How it works:*
the interface is in English and Hindi at first (with a framework for
community translations); dates, currency (INR, lakh and crore grouping),
time zone (IST) and GST invoice details follow Indian conventions.
Policy and notice templates exist in Hindi where staff-facing.

**F32. Partner (multi-client) console** (Phase 3)

*Why:* CA/CS firms, auditors and MSSPs run many clients and are a key
distribution channel. *How it works:* a partner account sees a roll-up
of all its client workspaces (readiness, overdue items, upcoming
audits), can switch between them with a clear audit trail, can apply its
own branding to reports, and can reuse its own policy templates and
answer libraries across clients.

**F33. Billing and licensing for the managed cloud and enterprise tier**
(Phase 3)

*Why:* we need to be able to charge. *How it works:* plans, usage limits
and invoices (with GST) are handled through Razorpay; licence keys
unlock the enterprise folder for self-hosted customers; free-tier limits
never block core features.

**F34. Plugin registry and marketplace** (Phase 2 basic registry; Phase
4 marketplace)

*Why:* discoverability and trust for community work. *How it works:* the
registry lists plugins with their author, permissions, version,
signature, download count and compatibility. A verification process
(code review plus automated checks) earns a "verified" badge. In Phase
4, authors can list paid plugins and receive revenue share.

9. Phased development runway
----------------------------

### 9.1 Overview

The plan is anchored to one hard date: **13 May 2027**, when most DPDP
obligations begin to apply. The Indian pack and its supporting features
must be in public beta before then, which makes Phase 2 the critical
phase. Dates assume work starts on 16 November 2026 and are **targets,
not promises**; they depend on team size (see 9.4).

  Phase   Target dates                 Name                              One-line goal
  ------- ---------------------------- --------------------------------- ----------------------------------------------------------------------------------------------------------------
  0       16 Nov to 13 Dec 2026        Foundations                       Settle the key decisions, sign design partners, set up the project
  1       14 Dec 2026 to 28 Feb 2027   Foundation MVP (internal alpha)   A working core that one design partner can use end to end
  2       1 Mar to 30 Apr 2027         India Beta                        Public open-source release with DPDP and CERT-In packs, ten connectors and a private cloud beta, before 13 May
  3       May to Aug 2027              v1.0 and revenue                  General availability, RBI/SEBI/IRDAI packs, auditor portal, trust centre, managed cloud and enterprise licence
  4       Sep to Dec 2027              Ecosystem                         Marketplace, certification programme, more connectors, first non-Indian country pack
  5       2028 onward                  Scale and global                  More countries, deeper continuous monitoring, enterprise scale, community governance

### 9.2 Phase details

**Phase 0: Foundations (4 weeks)**

-   *Scope:* run trademark and domain clearance for the Sampati name;
    finalise the licence texts and contributor process with counsel
    (section 15); engage legal counsel for DPDP content review and
    framework-text licensing; recruit **three design partners** (ideally
    a startup, a regulated entity and a CA/CS or auditor firm); create
    the repository, contribution guide, code of conduct and security
    policy; write architecture decision records and the first threat
    model; verify the "first open-source" claim research (section 5.4);
    set up continuous integration, signed builds and a baseline security
    pipeline.

-   *Exit criteria:* every item in section 13 marked "needed in Phase 0"
    is decided; three design partners have agreed to participate; the
    repository builds and deploys a "hello world" instance.

**Phase 1: Foundation MVP (about 11 weeks)**

-   *Scope:* F1 (workspaces), F2 (sign-in and roles, basic), F3 (audit
    log), F4 (framework library), F5 (crosswalk, basic), F7 (gap
    assessment), F9 (plugin framework, internal alpha), F11 (evidence
    ledger), F14 (manual evidence), F15 (policies), F20 (tasks and
    notifications), F28 (API and webhooks), F30 (deployment). Two
    proof-of-concept connectors (for example GitHub and Google
    Workspace) to prove the plugin design. SOC 2 and ISO 27001 loaded as
    frameworks.

-   *Exit criteria:* a clean install takes under 15 minutes; one design
    partner completes a gap assessment, assigns controls, attaches
    manual and automated evidence and generates a readiness report;
    documentation covers install, concepts and writing a first plugin.

**Phase 2: India Beta (about 8 weeks, the critical phase)**

-   *Scope:* F6 (India pack: DPDP and CERT-In), F10 (first ten
    connectors), F12 (automated control tests), F13 (device agent), F16
    (risks), F17 (vendors), F18 (assets), F19 (people), F21 (DPDP
    module), F22 (Indian PII scanner), F23 (incident and breach clocks),
    F24 (audit export), F26 (basic dashboards), F31 (English and Hindi),
    F34 (basic plugin registry). **Public open-source release (v0.x)**
    and a **private beta of the India-region managed cloud**.

-   *Exit criteria:* released before 13 May 2027; at least three design
    partners run real programmes on it; the DPDP and CERT-In packs have
    passed legal review; a plugin written by someone outside the core
    team has been published.

**Phase 3: v1.0 and revenue (about 16 weeks)**

-   *Scope:* F2 (SAML and SCIM), F6 (RBI, SEBI CSCRF and IRDAI packs),
    F8 (regulatory change feed), F24 (full auditor portal), F25 (trust
    centre), F26 (board reports), F27 (security questionnaires), F28
    (MCP server), F29 (first AI features), F32 (partner console), F33
    (billing and licensing). Managed cloud general availability,
    enterprise licence, an independent penetration test, and the
    Platform's own SOC 2 and ISO 27001 readiness.

-   *Exit criteria:* v1.0 released; independent penetration test
    completed with no open critical findings; first paying cloud and
    enterprise customers; at least two auditor or CA/CS partners
    onboarded.

**Phase 4: Ecosystem (about 16 weeks)**

-   *Scope:* paid-plugin marketplace and revenue share (F34),
    implementer certification programme, 25 or more connectors (many
    from the community), first non-Indian country pack (chosen by demand
    and contributor interest), broader AI assistance (F29), partner
    programme at scale.

-   *Exit criteria:* at least 25 connectors; a community-maintained pack
    exists; software revenue is more than half of total revenue.

**Phase 5: Scale and global (2028 onward)**

-   *Scope:* more country packs; deeper continuous monitoring and
    remediation guidance; high availability across regions; additional
    cloud regions; formal community governance (for example a steering
    group or foundation) if the project grows into one.

### 9.3 Dependencies (what blocks what)

1.  The **plugin framework (F9)** blocks every connector, scanner and
    pack.

2.  The **framework engine (F4)** and **crosswalk (F5)** block country
    packs (F6).

3.  The **evidence ledger (F11)** blocks control tests (F12), audits
    (F24) and the trust centre (F25).

4.  The **legal review of DPDP content** blocks the public release of
    the DPDP pack in Phase 2; start it in Phase 0.

5.  The **device agent (F13)** and **PII scanner (F22)** need the
    on-premise collector design to be agreed early, because both run in
    the customer's network.

### 9.4 Team and scope assumptions

The team size is **not yet confirmed**. The plan assumes a core of four
to six people: a backend lead, two backend or connector engineers, a
frontend engineer, a DevOps and security engineer (part-time is
acceptable at first), and a part-time compliance and legal content lead,
supported by design partners and early community contributors. If the
team is smaller, cut in this order and protect the rest:

1.  Defer F27 (questionnaires), F29 (AI assistant), F32 (partner
    console) and F34 (marketplace).

2.  Reduce F18 (assets) and F19 (people) to imports only.

3.  Reduce F16 (risks) and F17 (vendors) to simple registers.

4.  **Do not cut:** the plugin framework (F9), evidence ledger (F11),
    control tests (F12), the DPDP, scanner and incident features (F21 to
    F23), and deployment (F30), because they carry the USP and the
    deadline.

### 9.5 Governance and community

From day one: a public roadmap, a contribution guide, a code of conduct,
labelled "good first issue" tasks, a published security policy, regular
release notes, and named **pack maintainers** for each country pack.
Pack and connector maintainers are the scaling mechanism of the project
and should be recognised publicly. Partner firms (CA/CS, auditors) are
invited to review packs for accuracy.

10. Risks and mitigations
-------------------------

  Risk                                                Why it matters                                                            Mitigation
  --------------------------------------------------- ------------------------------------------------------------------------- -----------------------------------------------------------------------------------------------------------------------------------------
  An established open-source tool adds Indian packs   CISO Assistant's framework-as-data design makes this feasible             Go deeper than a framework file: tests, collectors, deadlines and Indian connectors; build an India community and partner network early
  Missing the DPDP window                             Demand peaks before 13 May 2027 and vendors are moving                    Protect the Phase 2 scope; use cut lines (9.4); start legal review in Phase 0
  Incorrect regulatory content                        A wrong deadline or obligation damages trust and could create liability   Counsel review before release, "not legal advice" notices, versioned packs, a public change log and a fast correction process
  Framework text licensing                            Standards such as ISO are copyrighted                                     Ship our own wording and mappings; reference official clause numbers; get legal advice before redistributing any official text
  The Platform is breached                            It holds credentials and sensitive evidence                               Read-only scopes, metadata-first design, sandboxed signed plugins, penetration test, public disclosure process (section 6.3)
  Auditors do not accept the evidence                 Without acceptance the product has no value                               Co-design with auditor partners; tamper-evident evidence ledger; standard export formats
  Connector maintenance burden                        Third-party APIs change constantly                                        Recorded-response tests, connector health dashboard, community maintainers, deprecation policy
  Free tier cannibalises revenue                      Many users self-host forever                                              Charge for operations, enterprise needs and expertise; test the line during pilots (section 7.6)
  Services crowd out product                          Early revenue from services can absorb the team                           Cap services hours; use partners for delivery; review the ratio every quarter
  Over-claiming "first"                               A false claim hurts credibility                                           Use the safer wording and verify before any claim (section 5.4)
  Regulatory timelines shift                          Phase dates in the DPDP Rules could change                                Track official notices; keep packs configurable; do not hard-code dates
  Team capacity                                       The plan is ambitious for a small team                                    Phase gates, cut lines, and community contribution from Phase 2

11. Success metrics
-------------------

Targets are **proposals** to be adjusted once the real team and market
feedback are known.

  Phase   Product                                                                            Community                                                                  Business
  ------- ---------------------------------------------------------------------------------- -------------------------------------------------------------------------- ------------------------------------------------------------------
  1       Install in under 15 minutes; one end-to-end gap assessment with a design partner   Internal alpha; docs for first plugin                                      Three design partners signed; 10 or more buyer interviews done
  2       DPDP and CERT-In packs legally reviewed; 10 connectors; plugin SDK published       300 or more repository stars; 10 contributors; 3 or more outside plugins   5 paying pilots; first revenue
  3       v1.0 shipped; clean penetration test; auditor portal and trust centre live         1,000 or more stars; 25 contributors                                       15 paying cloud accounts; 4 enterprise licences; 2 partner firms
  4       25 or more connectors; one non-Indian pack                                         2,000 or more stars; 50 contributors; community pack maintainers           Software revenue above 50% of total

Product health measures to track throughout: time from install to first
automated control test, percentage of controls with automated evidence,
evidence freshness, plugin install success rate, and auditor-reported
evidence acceptance.

12. Glossary
------------

-   **GRC:** governance, risk and compliance; the discipline and
    software category for managing them.

-   **SOC 2:** a report, issued by an independent audit firm, on a
    company's controls for security and related criteria. Popular with
    software companies selling to enterprises.

-   **ISO 27001:** an international standard for an information security
    management system; certification is awarded by accredited
    certification bodies.

-   **DPDP Act:** India's Digital Personal Data Protection Act, 2023,
    supported by the DPDP Rules, 2025.

-   **Data Fiduciary / Data Principal:** under the DPDP Act, the
    organisation that decides how personal data is processed, and the
    individual the data is about. A **Significant Data Fiduciary** has
    extra obligations.

-   **DPO:** data protection officer.

-   **CERT-In:** India's national computer emergency response team,
    whose directions include incident reporting and log retention
    requirements.

-   **RBI, SEBI, IRDAI:** the banking, securities and insurance
    regulators. **CSCRF** is SEBI's cybersecurity and cyber resilience
    framework.

-   **Control:** a safeguard or practice (for example, multi-factor
    authentication) that a company puts in place.

-   **Evidence:** proof that a control is in place and working (a
    setting export, a log, a signed document).

-   **Control test:** an automated check that evaluates evidence against
    a rule.

-   **Crosswalk:** a mapping showing which controls satisfy which
    requirements across frameworks.

-   **Country pack:** an installable bundle of one country's
    regulations, controls, tests, workflows and templates.

-   **Connector / plugin:** a package that reads data from another
    system (or adds a feature) through the Platform's plugin framework.

-   **SSO, OIDC, SAML, SCIM:** ways to sign in with an existing account
    (OIDC, SAML) and to create and remove users automatically (SCIM).

-   **RBAC:** role-based access control.

-   **TPRM:** third-party (vendor) risk management.

-   **Trust centre:** a public page showing a company's security and
    compliance posture.

-   **PBC list:** the "prepared by client" list of items an auditor asks
    a company to provide.

-   **MCP:** a protocol that lets AI agents use tools and data sources
    in a controlled way.

-   **SBOM:** software bill of materials, a list of the components
    inside a software release.

13. Open decisions
------------------

  Decision                             Options or notes                                                                                                                                                                 Needed by
  ------------------------------------ -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ----------------------
  Sampati brand clearance              Name is final. Run IP India and WIPO clearance in classes 9 and 42, resolve the overlaps listed in section 5.6, and secure the domain, GitHub organisation, PyPI and npm names   End of Phase 0
  Licence model                        Decided: Apache 2.0 core, MIT SDK, PCL enterprise. Counsel to draft the PCL and review the cloud-clone risk (section 15.5)                                                       End of Phase 0
  Legal counsel                        Retain a data-protection lawyer for DPDP pack review and framework-text advice                                                                                                   Phase 0
  Design partners                      Three: a startup, a regulated entity, a CA/CS or auditor firm                                                                                                                    End of Phase 0
  Team plan                            Confirm size and roles; hire or contract the compliance and legal content lead                                                                                                   Phase 0
  First ten connectors                 Confirm the list with design-partner input (section F10)                                                                                                                         Start of Phase 2
  India-region hosting provider        Major provider region or domestic provider; consider data-residency commitments                                                                                                  Phase 2
  Pricing                              Validate the indicative tiers through interviews and pilots (section 7.6)                                                                                                        End of Phase 2
  Auditor and CA/CS partner approach   Referral, co-delivery or white-label                                                                                                                                             Phase 2
  Community governance                 Company-led for now; decide when to form a steering group or foundation                                                                                                          Phase 3
  AI policy                            Which AI features ship, data handling rules, default-off settings                                                                                                                Phase 3
  Public claim wording                 Final text for any "first" positioning after verification (section 5.4)                                                                                                          Before public launch

14. Sources and caveats
-----------------------

Competitor information was gathered from public sources in November
2026, including the projects' own repositories and websites (CISO
Assistant and intuitem, Eramba, Comp AI, Openlane, Probo, Unicis),
technology press coverage (for example Help Net Security on Comp AI),
independent comparison and listing sites (including soc2auditors.org,
europeanpurpose.com and fitgap), Indian press and vendor pages for the
DPDP landscape (including coverage of ComplyDP, Niyam by FlickerBytes,
Gordon, Jupitice, Cross Identity and IDfy), and Indian vendor and
consultancy guides on DPDP and CERT-In requirements.

-   Vendor claims (integration counts, customer counts, framework
    counts, price points) are marked as claims and may be out of date.
    Re-verify any figure before it is used publicly.

-   Pricing and revenue figures in this document are **planning
    placeholders**, not quotes or forecasts.

-   Regulatory descriptions are summaries for planning. DPDP, CERT-In,
    RBI, SEBI and IRDAI requirements must be confirmed by counsel
    against the official texts and current notifications.

-   Sprinto and Scrut were included from general market knowledge and
    were not part of the detailed research; verify before citing.

15. Repository structure and licensing
--------------------------------------

Sampati is built as three repositories with a strict one-way dependency:
the SDK is the base, the Community Edition builds on it, and the
Enterprise Edition extends the Community Edition. Names below are
working names and follow the final GitHub organisation name.

### 15.1 The three repositories

  Repository                                Visibility   Licence                                                                   What it contains                                                                                                                                                         Depends on
  ----------------------------------------- ------------ ------------------------------------------------------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ --------------------------------------------------------
  sampati-sdk                               Public       MIT                                                                       The plugin protocol, manifest and pack schemas, Python and TypeScript SDKs, the plugin command-line tool, conformance tests, examples                                    Nothing
  sampati (Community Edition)               Public       Apache 2.0                                                                The platform core: API, web app, workers, device agent, on-premise collector, first-party connectors, global and India packs, deployment files, docs                     The SDK, as a published package
  sampati-enterprise (Enterprise Edition)   Private      PCL (proprietary commercial licence, assumed meaning; counsel to draft)   Enterprise extensions: SAML and SCIM, high availability, advanced audit controls, regulatory feed client, partner console, white-label, licensing, hardened deployment   The Community Edition at a pinned version, and the SDK

**Dependency rules.** SDK, then Community Edition, then Enterprise
Edition; never the reverse. The Community Edition must run fully on its
own. The Enterprise Edition never forks the Community Edition: it
attaches through published packages and defined extension points. The
Community Edition contains no licence checks beyond an empty interface.

### 15.2 Repository 1: sampati-sdk (MIT)

Why it is separate: it is the stable public contract. Third parties
depend on it without taking the platform, and it can be versioned and
released on its own schedule.

sampati-sdk/\
├── LICENSE \# MIT\
├── README.md\
├── spec/\
│ ├── plugin-protocol/ \# gRPC and HTTP contract (versioned, v1)\
│ ├── manifest.schema.json \# plugin manifest: type, permissions,
config, evidence produced\
│ ├── pack.schema.json \# country-pack manifest\
│ ├── framework.schema.json \# framework and control data format\
│ ├── evidence.schema.json \# evidence record format\
│ └── control-test.schema.json \# control test format (YAML with CEL
expressions)\
├── python/ \# sampati-sdk on PyPI (first SDK)\
│ ├── src/sampati\_sdk/ \# auth, pagination, rate limits, evidence
helpers, testing, runtime\
│ └── tests/\
├── typescript/ \# \@sampati/sdk on npm (second SDK)\
├── cli/ \# sampati-plugin: scaffold, test, validate, sign, publish\
├── conformance/ \# tests every connector, scanner and pack must pass\
├── examples/ \# hello-connector, sample-pack, sample-scanner\
├── docs/ \# plugin author guide, pack authoring guide, RFC process\
└── .github/ \# CI, release automation, issue templates

Rules: semantic versioning; the protocol carries its own version number;
spec changes go through a short public RFC; breaking changes only in a
new protocol version.

### 15.3 Repository 2: sampati, the Community Edition (Apache 2.0)

A monorepo, so connectors and packs share one CI pipeline and one
release train.

sampati/\
├── LICENSE \# Apache-2.0\
├── NOTICE CONTRIBUTING.md CODE\_OF\_CONDUCT.md SECURITY.md\
├── GOVERNANCE.md TRADEMARKS.md AGENTS.md \# AGENTS.md = rules for AI
coding agents\
├── apps/\
│ ├── api/ \# FastAPI service: auth, tenancy, controls, evidence,
policies, risks, vendors, tasks\
│ ├── worker/ \# scheduled jobs, control-test runs, notifications\
│ ├── web/ \# Next.js web app (compliance teams, auditors)\
│ └── trust-center/ \# public trust page (Phase 3)\
├── packages/\
│ ├── core-domain/ \# shared models, framework and control engine,
crosswalk\
│ ├── rules-engine/ \# YAML and CEL control tests, sandboxed\
│ ├── ledger/ \# evidence hash chain\
│ ├── plugin-host/ \# runs plugins out of process: sandbox, permission
scopes, signing checks\
│ ├── extension-points/ \# interfaces the Enterprise Edition implements
(SSO, SCIM, audit export, licence check)\
│ └── ui-kit/\
├── agent/ \# Go device agent (Windows, macOS, Linux)\
├── collector/ \# Go on-premise collector and PII scanner runtime\
├── plugins/ \# first-party plugins, built with the SDK\
│ ├── connectors/ \# aws, gcp, azure, github, gitlab, google-workspace,
entra-id, jira, slack, hr \...\
│ ├── scanners/ \# india-pii\
│ └── notifiers/ \# email, slack, teams\
├── packs/\
│ ├── global/ \# soc2, iso27001\
│ └── india/ \# dpdp, cert-in (Phase 2); rbi, sebi-cscrf, irdai (Phase
3)\
├── frameworks/ \# framework data files and crosswalk mappings\
├── db/migrations/\
├── deploy/ \# docker-compose, helm, air-gapped bundle\
├── docs/ \# user, admin, developer and pack-authoring docs\
├── e2e/ \# end-to-end tests\
├── tools/ \# scripts and code generation\
└── .github/ \# CI: tests, lint, static analysis, secret and dependency
scans, SBOM, signed releases

Third parties publish their own plugins and packs from their own
repositories using the SDK; the plugin registry lists them.

### 15.4 Repository 3: sampati-enterprise (PCL, private)

sampati-enterprise/\
├── LICENSE-PCL EULA.md\
├── ee-api/ \# extensions registered through Community Edition extension
points\
│ ├── sso-saml/\
│ ├── scim/\
│ ├── audit-advanced/ \# legal hold, dual approval, certified export
packs\
│ ├── ha/ \# multi-node and multi-region support\
│ ├── reg-feed-client/ \# fetches reviewed pack updates from the
VayuX-operated feed\
│ ├── partner-console/ \# multi-client console\
│ ├── white-label/\
│ └── licensing/ \# licence-key validation and plan limits\
├── ee-web/ \# interface extensions\
├── billing-service/ \# managed cloud only: Razorpay and GST invoicing\
├── deploy-enterprise/ \# hardened images, high-availability Helm
charts, upgrade runbooks\
├── docs-enterprise/\
└── .github/ \# builds against a pinned Community Edition version;
publishes to a private registry

The infrastructure code and runbooks for the India-region managed cloud
belong in a separate private operations repository later; they are not
part of the product repositories.

### 15.5 Licence notes and cautions

-   **Apache 2.0 (Community Edition core).** Permissive, with an
    explicit patent grant. It also lets anyone, including a large
    vendor, host the Community Edition as a competing paid service. This
    replaces the earlier AGPL-core lean, so it is a conscious trade for
    adoption. Protect the business with a trademark policy (the name and
    logo are not licensed), keeping paid differentiators in the
    Enterprise repository, and competing on operations: India-region
    hosting, the regulatory update feed, support and the partner
    network. Note that the Ankush project uses AGPLv3 with a CLA, so the
    two products now follow different licence strategies.

-   **MIT (SDK).** Maximum freedom for plugin authors, including
    commercial ones. MIT has no explicit patent grant; Apache 2.0 would
    add one, and the two are compatible. Keep MIT if simplicity matters
    more than the patent grant.

-   **PCL (Enterprise Edition).** Counsel should draft it. Typical
    scope: internal use only, no redistribution or reverse engineering,
    licence keys, term and renewal, audit rights, support terms,
    termination. It must also carry the required notices for the Apache
    and MIT components it bundles.

-   **Dependencies.** Because the core is permissive, block copyleft
    licences (GPL, AGPL) among dependencies with an automated licence
    scan in CI, and keep a software bill of materials for every release.

-   **Contributions.** A Developer Certificate of Origin sign-off is
    enough for the Community Edition and SDK, because contributions stay
    Apache 2.0 or MIT. A contributor licence agreement is only needed if
    you ever want to relicense contributions.

### 15.6 Versioning and releases

-   **SDK:** semantic versioning; the plugin protocol has its own
    version (v1).

-   **Community Edition:** semantic versioning with a monthly minor
    release; security fixes for the latest two minor versions.

-   **Enterprise Edition:** released after each Community Edition minor
    with a matching version number (for example Community 1.4 pairs with
    Enterprise 1.4.x); built against the exact pinned Community version.

-   **All releases:** signed container images, a software bill of
    materials, and a public changelog.

16. Build roadmap: from the base to the complete build
------------------------------------------------------

**The base:** the SDK contract plus the Community Edition core (tenancy,
access control, the framework and control engine, and the evidence
ledger). Everything else depends on these, so they come first.

**The direction:** build inside-out. Contracts first, then the domain
core, then evidence and automation, then country depth, then operability
and assurance, then enterprise layers, then the ecosystem, then other
countries. The Community Edition ships extension points from the start,
so the Enterprise Edition can attach later without rewrites.

### 16.1 Stages

Dates are targets and match the phases in section 9.

  Stage                                Target window                Repositories        What gets built                                                                                                                                                                                                                                                                                                                  Exit gate
  ------------------------------------ ---------------------------- ------------------- -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------------------------------------------------------------------------------
  0\. Foundation                       16 Nov to 13 Dec 2026        All three created   Repositories, licence files, contribution and AI-agent rules, CI skeleton with security scans, decision records, threat model, design partners, trademark and domain clearance                                                                                                                                                   CI is green; a hello-world instance deploys; licence texts reviewed
  1\. Contracts and core skeleton      14 Dec 2026 to 31 Jan 2027   SDK, Community      SDK specs v0 (manifest, evidence, framework, control test, plugin protocol) and a Python SDK alpha. In the Community Edition: API skeleton, sign-in and roles, tenancy with row-level security, audit log, migrations, web shell, framework library with SOC 2 and ISO 27001, controls and a basic crosswalk, extension points   A user can create an organisation, load a framework and assign controls end to end; specs frozen as v0
  2\. Evidence and first automation    1 Feb to 28 Feb 2027         SDK, Community      Evidence ledger, manual evidence and requests, policies and attestations, tasks and notifications, plugin host with two proof-of-concept connectors (GitHub, Google Workspace), control-test engine v0, API and webhooks, Docker Compose deployment                                                                              A design partner completes a gap assessment with manual and automated evidence (Phase 1 exit)
  3\. India depth                      1 Mar to 30 Apr 2027         SDK, Community      DPDP and CERT-In packs; DPDP module (data inventory, notice and consent register, rights requests); Indian PII scanner and collector; breach and incident clocks; device agent; ten connectors; risks, vendors, assets, people; English and Hindi; plugin registry; SDK 0.x published; public Community release                  Released before 13 May 2027; packs legally reviewed; an outside-written plugin published (Phase 2 exit)
  4\. Assurance and v1.0               May to Aug 2027              All three           Community: auditor portal, trust centre, reporting, questionnaires, MCP server, first AI assistance, RBI, SEBI and IRDAI packs, Helm chart, penetration test, Community 1.0 and SDK 1.0. Enterprise: SAML, SCIM, licensing, advanced audit controls, partner console. Managed cloud and billing                                  v1.0 released; clean penetration test; first paying customers (Phase 3 exit)
  5\. Enterprise depth and ecosystem   Sep to Dec 2027              All three           High availability and multi-region, white-label, live regulatory feed, SLAs, partner programme; plugin marketplace and certification; 25 or more connectors; first non-Indian pack                                                                                                                                               Software revenue above half of total; a community-maintained pack exists (Phase 4 exit)
  6\. Complete build and global        2028 onward                  All three           More country packs maintained by community maintainers, deeper continuous monitoring and remediation guidance, more cloud regions, formal community governance                                                                                                                                                                   See the definition below

### 16.2 Definition of the complete build

The build is complete when all of the following are true:

-   All 34 must-have features (F1 to F34 in section 8) are in
    production.

-   SDK 1.x is stable and documented, with at least 25 connectors
    available.

-   Packs exist for SOC 2, ISO 27001, DPDP, CERT-In, RBI, SEBI and
    IRDAI, plus at least one non-Indian country.

-   The Enterprise Edition ships every item on the paid list in section
    7.3.

-   The managed cloud is generally available with billing, and an
    independent penetration test is repeated every year.

-   Community governance is formal, with named pack maintainers and a
    public roadmap.

### 16.3 Build rules that apply at every stage

1.  Every feature lands as a small pull request with tests; nothing
    merges without green CI and a human review.

2.  Extension points are designed in the Community Edition before the
    Enterprise feature that needs them.

3.  Security-critical code (authentication, tenant isolation, secrets,
    the plugin sandbox, the evidence ledger) is reviewed by an expert
    even when AI wrote it.

4.  Regulatory content ships only after legal review.

5.  Never put an API, notification or mapping feature behind the
    Enterprise licence (section 7.3).

17. Decision log: everything decided so far
-------------------------------------------

**Status key.** **Final:** do not change without the owner's written
approval. **Default:** use it unless an approved architecture decision
record (ADR, see 18.11) changes it. **Proposed:** the working
assumption, not yet approved. **Open:** undecided; ask before building
anything that depends on it. The owner is PragneshKumar S. Singh,
Co-Founder & CTO of VayuX Systems LLP.

  \#   Decision                                                                                                                                                                                                                                       Status                                      Details in
  ---- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ------------------------------------------- ------------
  1    The product is an open-source compliance automation platform in the Vanta/Drata category                                                                                                                                                       Final                                       1
  2    Name: **Sampati**, always shown as "Sampati by VayuX"                                                                                                                                                                                          Final (trademark clearance still open)      5.6
  3    Every VayuX tool is named after a character from Hindu mythology (Ramayana, Mahabharata and other texts) and branded "\[Name\] by VayuX"; characters preferred over deities; imagery respectful                                                Final                                       5.6
  4    India first, global by design through country packs                                                                                                                                                                                            Final                                       1, 5
  5    The two core ideas: country packs and a plugin ecosystem                                                                                                                                                                                       Final                                       5.2
  6    Three repositories: SDK, Community Edition, Enterprise Edition; dependencies run SDK, then Community, then Enterprise                                                                                                                          Final                                       15
  7    Licences: MIT for the SDK, Apache 2.0 for the Community Edition core, PCL (proprietary commercial licence) for the Enterprise Edition                                                                                                          Final (PCL text to be drafted by counsel)   15.5
  8    Tech stack: Python 3.12 with FastAPI; TypeScript with React and Next.js; PostgreSQL with row-level security; Redis job queue; S3-compatible storage; Go for the agent and collector; YAML with CEL for control tests; out-of-process plugins   Default                                     6.2
  9    Evidence is stored metadata-first: store proof of a check and a hash, not the personal data inspected                                                                                                                                          Final                                       1.5, 6.3
  10   Never gate APIs, notifications or framework mapping behind a paid licence                                                                                                                                                                      Final                                       7.3
  11   AI features are assistive only: labelled, cited and approved by a human before anything changes                                                                                                                                                Final                                       F29
  12   Claude Code does most of the implementation; security-critical code and regulatory content always get expert human review                                                                                                                      Final                                       18
  13   Public claim wording: "The open-source compliance automation platform built for India's regulators." No "India's first" claim until verified                                                                                                   Final                                       5.4
  14   Interface languages at first: English and Hindi                                                                                                                                                                                                Final                                       F31
  15   Public content rules: keep the VayuX search terms prominent, name only PragneshKumar S. Singh as founder contact, never name VayuX's internal tools                                                                                            Final                                       18.8
  16   Revenue model: open core, managed India-region cloud, enterprise licence, services, regulatory update subscription, partner programme, later a marketplace                                                                                     Proposed (all prices are placeholders)      7
  17   Phases and dates, anchored to 13 May 2027                                                                                                                                                                                                      Proposed (targets, not promises)            9, 16
  18   Contributions use a Developer Certificate of Origin sign-off; no contributor licence agreement                                                                                                                                                 Proposed                                    15.5
  19   Governance: company-led for now; a steering group or foundation is decided later                                                                                                                                                               Proposed                                    9.5
  20   Team: four to six people plus design partners (assumption)                                                                                                                                                                                     Open                                        9.4
  21   Trademark and domain clearance for Sampati; resolve overlaps with the government SAMPATI system, Sampat and Sammati                                                                                                                            Open                                        5.6
  22   India-region hosting provider for the managed cloud                                                                                                                                                                                            Open                                        13
  23   Final prices and plan limits                                                                                                                                                                                                                   Open                                        7.6
  24   The legal text of the DPDP and CERT-In packs                                                                                                                                                                                                   Open (needs counsel)                        22

Another product, Ankush (an AI agent firewall), is a separate project
with its own licence strategy (AGPLv3 with a CLA). Nothing in this
document applies to it.

18. Rules of the road for Claude Code
-------------------------------------

### 18.1 Roles and order of authority

-   **The human owner** (PragneshKumar S. Singh) sets priorities,
    approves decisions and reviews every pull request.

-   **Claude Code** is the lead implementer: it plans, writes code,
    tests and docs, and keeps this document's checklists up to date.

-   **Order of authority when sources disagree:** (1) the latest
    explicit instruction from the owner; (2) this document; (3) existing
    code and ADRs; (4) general best practice. If this document is silent
    or contradicts itself, stop and ask (section 24). Never invent a
    requirement.

### 18.2 The AGENTS.md file to create in every repository

\# AGENTS.md: rules for AI coding agents working on Sampati\
\
Project: Sampati by VayuX, an open-source compliance automation
platform.\
Source of truth: docs/SAMPATI-GRANTH.md. Read sections 17, 18, 19, 21 and
23 before any task.\
\
\#\# Always\
- Work on one checklist item at a time. Write the plan in the PR
description.\
- Write tests from the acceptance criteria first, then the code.\
- Run lint, type checks, tests, secret scan and licence scan before
opening a PR.\
- Keep PRs small (under about 400 changed lines). One feature slice per
PR.\
- Record every real design choice as an ADR in docs/adr/.\
- Tick the feature checklist and update docs and the changelog in the
same PR.\
\
\#\# Never\
- Never commit secrets, real customer data or real personal data (use
synthetic data).\
- Never copy code, framework text or data from other projects.\
- Never add a dependency with a GPL or AGPL licence.\
- Never put Enterprise code in the Community repo or the reverse
dependency direction.\
- Never hard-code legal text, deadlines or regulator rules; they live in
pack data.\
- Never weaken tenant isolation, authentication or audit logging to make
a test pass.\
- Never name VayuX internal tools in public files.\
\
\#\# Stop and ask a human when\
- A requirement is unclear, missing or contradictory.\
- A change touches authentication, tenant isolation, secrets, the plugin
sandbox or the evidence ledger design.\
- A change alters a public API, a spec schema or a licence.\
- Anything involves legal or regulatory wording, money, or real customer
data.\
\
\#\# Style\
- Python: type hints everywhere, ruff, mypy strict, pytest. TypeScript:
strict mode, ESLint. Go: golangci-lint.\
- Every source file starts with an SPDX licence identifier for its repo.

### 18.3 Workflow for every task

1.  Pick the next unchecked item in section 23 (tasks) or section 21
    (features).

2.  Read the matching feature description in section 8 and its "done
    when" list in section 21.

3.  Write a short plan: what you will change, which files, which tests,
    what could go wrong. For anything large or risky, show the plan to
    the owner first.

4.  Turn each "done when" line into a failing test.

5.  Implement until the tests pass.

6.  Run the full local checks: lint, type check, unit tests, integration
    tests, secret scan, licence scan.

7.  Update documentation, the changelog, and the checklist boxes.

8.  Open a small pull request with the plan, test evidence and any ADR.

9.  Address review comments; do not merge your own pull request in
    security-critical areas.

### 18.4 Engineering standards

  Area                   Standard
  ---------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------
  Backend                Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2 with Alembic migrations; type hints and mypy strict; ruff for lint and format
  Frontend               TypeScript strict, React with Next.js, Tailwind CSS; ESLint and Prettier; accessibility target WCAG 2.1 AA
  Agent and collector    Go, single static binaries, golangci-lint
  Database               PostgreSQL 16 or newer; every table has organisation\_id and row-level security; migrations are forward-only and reviewed
  Tests                  pytest, Playwright for end-to-end, recorded API responses for connectors; at least 80% line coverage on core packages, 100% of acceptance criteria covered
  Identifiers and time   UUIDv7 for ids; timestamps in UTC ISO 8601; display in the user's time zone (default IST)
  API                    REST under /api/v1, JSON with snake\_case keys, OpenAPI generated from code; conventions in 19.4
  Errors                 One error shape everywhere; no stack traces to clients
  Logging                Structured JSON logs with a request id; never log secrets or personal data
  Dependencies           Permissive licences only (MIT, Apache 2.0, BSD, ISC); pin versions in lock files; automated updates reviewed weekly
  Versions               Use the latest stable release when a repository starts, then pin it. The versions named here are targets, not exact pins

### 18.5 Security rules (non-negotiable)

-   Secrets come from environment variables or the secrets vault, never
    from source code or logs.

-   **Tenant isolation:** every query is scoped to an organisation;
    row-level security is on for every tenant table; an automated test
    proves that a user in organisation A cannot read, write or even
    detect data in organisation B.

-   Passwords (if local sign-in is used) use argon2id; multi-factor
    authentication is supported; sessions are short-lived with secure
    cookies; API tokens are scoped and expire.

-   Validate all input at the edge; encode all output; protect against
    CSRF and server-side request forgery; rate-limit sensitive
    endpoints.

-   Every write action creates an audit-log entry (who, what, when,
    before and after).

-   Connector credentials are encrypted with per-tenant keys, requested
    with read-only scopes, and never shown again after entry.

-   Plugins run out of process, in containers, with a network allow-list
    and declared permissions. Unsigned plugins need an explicit admin
    opt-in.

-   Run static analysis, dependency scanning and secret scanning in CI;
    fail the build on high-severity findings.

-   Produce a software bill of materials and signed images for every
    release.

-   Keep the threat model in docs/threat-model.md up to date whenever
    the design changes.

### 18.6 Data and privacy rules

-   **Metadata first.** Store the result of a check, where it was found
    and a hash, not the sensitive data itself, wherever possible.

-   The PII scanner never sends raw values off the customer's
    environment; it sends only counts, locations, types and masked or
    hashed samples.

-   Never store raw Aadhaar numbers. Where an identifier must be shown,
    mask it.

-   Tests, fixtures and demos use synthetic data only. Never paste real
    customer data, credentials or personal data into code, tests, issues
    or prompts.

### 18.7 Licence and intellectual-property rules

-   Every source file carries an SPDX identifier: MIT in the SDK,
    Apache-2.0 in the Community Edition, and a proprietary notice in the
    Enterprise Edition.

-   **Do not copy code, framework wording or data from other projects**,
    including the open-source tools studied in section 3. Some use AGPL,
    which would contaminate a permissive core. Build independently and
    write our own control wording.

-   Do not copy the text of copyrighted standards (such as ISO). Ship
    our own wording and mappings, with references to official clause
    numbers.

-   Run a licence scan in CI and block copyleft dependencies.

-   The Enterprise Edition must keep the required notices for the Apache
    and MIT components it bundles.

### 18.8 Public content and branding rules

These apply to READMEs, docs, the website, release notes and any text a
stranger can read.

-   Always write the full brand "Sampati by VayuX", and keep the terms
    "VayuX", "VayuX Systems" and "vayux.systems" prominent for search.

-   Where a founder contact is needed, name only "PragneshKumar S.
    Singh, Co-Founder & CTO, VayuX Systems LLP". Do not name other
    company leadership.

-   Do not name VayuX's internal operational tools (its monitoring,
    automation or AI tooling) in public text.

-   Describe Sampati with the approved line in decision 13. Never claim
    "India's first" or "guaranteed compliance". Sampati helps companies
    prove compliance; auditors and certification bodies issue reports
    and certificates.

-   Every regulatory page carries a "not legal advice" notice.

-   Use mythology respectfully: no deity imagery, no jokes.

### 18.9 Git, pull requests and releases

-   Trunk-based development: short-lived branches named like
    feat/F12-control-tests or fix/tenant-scope-bug; main is always
    releasable and protected.

-   Conventional Commits for messages (feat, fix, docs, test, chore,
    refactor). Every commit is signed off (DCO).

-   Pull request template: what and why, plan, tests added, checklist
    items ticked, risks, ADR link, screenshots for interface changes.

-   Required checks: lint, types, tests, secret scan, licence scan,
    static analysis. At least one human approval; two for
    security-critical areas.

-   Releases follow section 15.6: semantic versions, signed images, a
    software bill of materials and a changelog.

### 18.10 Definition of done (applies to every feature)

-   [ ] Every "done when" line in section 21 has a passing automated
    test.

-   [ ] Lint, type checks, unit, integration and end-to-end tests are
    green in CI.

-   [ ] Tenant isolation, permissions and audit logging are covered by
    tests for the new feature.

-   [ ] The API is documented in the OpenAPI file; the interface works
    on desktop and mobile widths and is keyboard accessible.

-   [ ] No new secret, copyleft dependency or high-severity scan
    finding.

-   [ ] Documentation for users and developers is updated; the changelog
    has an entry.

-   [ ] Any design choice is recorded in an ADR.

-   [ ] The checklist box in section 21 is ticked and the owner has
    approved the pull request.

### 18.11 Architecture decision records (ADRs)

Whenever you choose between real alternatives (a library, a pattern, a
data design), add a short file in docs/adr/ named NNNN-title.md with:
context, options considered, decision, consequences. Changing a
**Default** decision in section 17 needs an ADR approved by the owner.
Never edit an old ADR; add a new one that supersedes it.

### 18.12 Dealing with uncertainty and mistakes

-   If a requirement is unclear, ask one precise question and propose a
    default; do not guess silently.

-   If you find an error in this document, say so and propose the
    correction; the owner updates section 17 first, then the rest.

-   If a test fails and you cannot fix it properly, report it; do not
    weaken or delete the test.

-   If you cause a regression or a security problem, say so immediately,
    fix it, and add a test that would have caught it.

19. Technical blueprints
------------------------

These blueprints remove guesswork. They are starting points: the final,
versioned schemas live in the SDK repository under spec/, and any change
to them follows the RFC process in 15.2.

### 19.1 Core data model

Every table below also carries id (UUIDv7), organisation\_id,
created\_at, updated\_at, created\_by and, where it makes sense,
entity\_id.

  Group             Entity                                            Key fields and notes
  ----------------- ------------------------------------------------- -----------------------------------------------------------------------------------------------------------------
  Tenancy           organisation                                      name, slug, region, settings; the top-level tenant
  Tenancy           entity                                            organisation, name, type (legal entity or business unit), parent entity
  Tenancy           user, membership                                  user identity; membership links a user to an organisation with a role
  Tenancy           api\_token, session                               hashed token, scopes, expiry; session with MFA state
  Compliance        framework, framework\_version                     code, name, version, source references, status (draft, reviewed, published)
  Compliance        requirement                                       framework\_version, reference number, our own wording, parent
  Compliance        control                                           code (for example CTRL-ACCESS-002), title, description, category, guidance
  Compliance        control\_mapping                                  control, requirement, strength (full, partial), reviewer note
  Compliance        entity\_framework                                 which frameworks and versions an entity has chosen
  Compliance        control\_implementation                           entity, control, status (not started, in progress, implemented, not applicable with reason), owner, next review
  Compliance        exception                                         control\_implementation, reason, approver, expires\_at
  Automation        plugin, plugin\_install                           plugin id and version; install per organisation with config and status
  Automation        plugin\_credential                                encrypted secret, key id, last rotated; never returned by the API
  Automation        collection\_run                                   plugin\_install, started, finished, status, counts, error
  Automation        evidence                                          record described in 19.5; append-only; hash and prev\_hash chain
  Automation        evidence\_file                                    object-store key, size, content type, scan status
  Automation        evidence\_link                                    evidence, control\_implementation
  Automation        control\_test, test\_result                       test definition (19.6) and each run's pass, fail or error with the exact data used
  Programme         policy, policy\_version, policy\_attestation      text, version, approval state, who acknowledged and when
  Programme         risk, risk\_treatment                             scores, owner, treatment, residual risk, review date
  Programme         vendor, vendor\_assessment                        tier, data handled, contract and agreement dates, questionnaire answers
  Programme         asset                                             type, source, owner, classification, data types
  Programme         person, training\_assignment                      staff record, start and end dates, training status
  Programme         task, notification                                owner, due date, priority, source object, SLA; delivery channel and state
  Privacy           data\_store, processing\_activity                 where personal data lives; purpose, data types, processors, retention
  Privacy           notice\_version, consent\_record                  notice text and version; consent event with timestamp and source
  Privacy           rights\_request                                   type, requester reference, identity check, due date, status, response log
  Incident          incident, regulator\_clock, incident\_action      incident facts; one clock per obligation with deadline; timestamped actions
  Audit             audit\_project, auditor\_access, audit\_finding   scope and period; time-boxed read-only access; findings and exceptions
  Packs             pack, pack\_version, pack\_install                installed country packs with version and review status
  Platform          audit\_log                                        actor, action, object, before, after, ip, request id; append-only
  Platform          webhook\_endpoint, webhook\_delivery              url, secret, events; delivery attempts
  Enterprise only   licence                                           key, plan, limits, expiry (held by the Enterprise Edition)

### 19.2 Multi-tenancy rules

1.  Every tenant table has organisation\_id, and PostgreSQL row-level
    security restricts reads and writes to the organisation set for the
    current request.

2.  The application sets the organisation for each request in one place
    (a request-scoped database session) and nowhere else.

3.  Background jobs carry their organisation explicitly and set it
    before touching data.

4.  An automated test suite attempts cross-tenant reads, writes,
    searches and file downloads and must find nothing.

5.  Partner (multi-client) access in the Enterprise Edition works
    through explicit, audited memberships, never by bypassing row-level
    security.

### 19.3 Roles and permissions

  Action                                   Admin   Compliance manager   Control owner   Contributor   Executive (read-only)   Auditor
  ---------------------------------------- ------- -------------------- --------------- ------------- ----------------------- ------------------
  Manage organisation settings and users   Yes     No                   No              No            No                      No
  Install and configure plugins            Yes     Yes                  No              No            No                      No
  Choose frameworks and packs              Yes     Yes                  No              No            No                      No
  Edit controls and ownership              Yes     Yes                  Own controls    No            No                      No
  Upload and request evidence              Yes     Yes                  Own controls    Assigned      No                      Request only
  Approve evidence                         Yes     Yes                  No              No            No                      No
  Edit and approve policies                Yes     Yes                  No              Draft only    No                      No
  Acknowledge policies                     Yes     Yes                  Yes             Yes           Yes                     No
  View everything in scope                 Yes     Yes                  Own area        Assigned      Yes                     Audit scope only
  Export audit pack                        Yes     Yes                  No              No            No                      Yes
  Delete data                              Yes     No                   No              No            No                      No

### 19.4 API conventions

-   Base path /api/v1. JSON with snake\_case keys. UUIDv7 ids.
    Timestamps in UTC ISO 8601.

-   Authentication by session cookie (web) or bearer token with scopes
    (API). Every endpoint declares the permission it needs.

-   Lists use cursor pagination (limit and cursor parameters,
    next\_cursor in the response), filtering and stable sort.

-   Errors always use one shape: an error object with code, message,
    details and request\_id.

-   POST requests that create things accept an Idempotency-Key header.

-   Webhooks are signed with HMAC and a timestamp; receivers must reject
    old timestamps. Failed deliveries retry with backoff.

-   Rate limits per token with clear headers. Breaking changes only in a
    new version path.

-   The OpenAPI file is generated from the code and checked into the
    repository; the client libraries are generated from it.

### 19.5 Evidence record (shown as YAML for readability; the wire format is JSON)

id: 0191f3e2-7b1a-7c3d-9e44-2a6f1b0c8d55\
organisation\_id: 0191f3e2-0000-7000-8000-000000000001\
source:\
plugin: github\
plugin\_version: 1.0.0\
collector: connector \# connector \| agent \| manual \| scanner\
check: branch\_protection\_enabled\
subject: repo:example/payments-api\
result: pass \# pass \| fail \| error \| info\
collected\_at: 2026-12-05T09:30:12Z\
valid\_until: 2027-03-05T09:30:12Z\
data: \# metadata only, never raw personal data\
default\_branch: main\
required\_reviews: 2\
hash: sha256:\<hash of this record\>\
prev\_hash: sha256:\<hash of the previous record in the chain\>\
linked\_controls: \[CTRL-CODE-001\]

### 19.6 Control test (YAML with CEL)

id: TEST-MFA-001\
control: CTRL-ACCESS-002\
title: Multi-factor authentication is enforced for all active users\
schedule: daily\
inputs:\
- evidence\_check: idp\_user\_mfa\_status \# produced by an identity
connector\
condition: \|\
evidence.filter(e, e.data.active == true).all(e, e.data.mfa\_enabled ==
true)\
severity: high\
on\_fail:\
task: Enable multi-factor authentication for the listed users\
notify: \[control\_owner\]\
exceptions:\
max\_days: 30\
requires\_approval: true

Rules: the condition is a pure expression with no network or file
access; the engine runs it in a sandbox with a time limit; the result
stores the exact evidence ids used.

### 19.7 Plugin manifest and protocol

id: github\
name: GitHub connector\
type: connector \# connector \| scanner \| notifier \| pack \|
report-template\
version: 1.0.0\
protocol: v1\
licence: Apache-2.0\
permissions:\
network\_allowlist: \[api.github.com\]\
scopes: \[read:org, read:repo\_metadata\] \# read-only scopes only\
config:\
- key: organisation\
label: GitHub organisation\
type: string\
required: true\
- key: token\
label: Read-only access token\
type: secret\
required: true\
produces:\
- check: branch\_protection\_enabled\
supports\_controls: \[CTRL-CODE-001\]\
schedule\_default: every 6 hours

**Protocol v1 (the host calls the plugin over gRPC or HTTP):**

1.  **Describe:** returns the manifest.

2.  **ValidateConfig:** checks the settings and credentials without
    collecting anything; returns clear errors.

3.  **Collect:** streams evidence records for a time window; handles
    pagination and rate limits itself.

4.  **Health:** reports status for the connector health dashboard.

5.  Scanners add **Scan** (returns findings as metadata only). Notifiers
    add **Send**.

The host enforces permissions: a plugin cannot reach a host that is not
on its allow-list, and cannot read another plugin's credentials.

### 19.8 Country pack layout and manifest

packs/india/dpdp/\
├── pack.yaml\
├── frameworks/dpdp.yaml\
├── controls/\*.yaml\
├── mappings/iso27001.yaml\
├── tests/\*.yaml\
├── workflows/breach.yaml\
├── templates/policies/\*.md\
├── templates/notices/\*.md\
├── reports/gap-report.yaml\
└── CHANGELOG.md

id: in-dpdp\
name: India DPDP pack\
version: 0.1.0\
country: IN\
regulator: Data Protection Board of India\
locale: \[en-IN, hi-IN\]\
sdk\_protocol: v1\
frameworks: \[frameworks/dpdp.yaml\]\
controls: \[controls/\*.yaml\]\
mappings: \[mappings/iso27001.yaml\]\
tests: \[tests/\*.yaml\]\
workflows:\
- id: breach-clock\
file: workflows/breach.yaml\
review:\
legal\_reviewed: false \# must be true before a public release\
reviewed\_by: null\
reviewed\_on: null

A pack with legal\_reviewed set to false can be installed only in a
clearly labelled "draft" mode.

### 19.9 Configuration (environment variables)

  Variable                                                                          Purpose                                            Default
  --------------------------------------------------------------------------------- -------------------------------------------------- ---------------------
  SAMPATI\_ENV                                                                      dev, test or prod                                  dev
  SAMPATI\_BASE\_URL                                                                Public URL of the instance                         none
  SAMPATI\_DATABASE\_URL                                                            PostgreSQL connection                              none
  SAMPATI\_REDIS\_URL                                                               Job queue connection                               none
  SAMPATI\_STORAGE\_URL, SAMPATI\_STORAGE\_BUCKET                                   S3-compatible evidence storage                     none
  SAMPATI\_KEY\_MODE                                                                local or external key management for tenant keys   local
  SAMPATI\_OIDC\_ISSUER, SAMPATI\_OIDC\_CLIENT\_ID, SAMPATI\_OIDC\_CLIENT\_SECRET   Sign-in provider                                   none
  SAMPATI\_SMTP\_URL                                                                Outgoing email                                     none
  SAMPATI\_DEFAULT\_LOCALE, SAMPATI\_TIMEZONE                                       Defaults                                           en-IN, Asia/Kolkata
  SAMPATI\_PLUGIN\_SANDBOX                                                          container or process                               container
  SAMPATI\_AI\_ENABLED, SAMPATI\_AI\_BASE\_URL                                      Optional AI assistant and its model endpoint       false, none
  SAMPATI\_LOG\_LEVEL                                                               Logging detail                                     info

20. Quality targets (non-functional requirements)
-------------------------------------------------

These are starting targets to design and test against; adjust through an
ADR when real data says otherwise.

  Area                   Target
  ---------------------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------
  Install                A new instance runs in under 15 minutes from a clean machine with one command
  Performance            95% of interface and API requests under 500 ms for an organisation with 500 users and 100,000 evidence records; background collection never slows the interface
  Scale                  One organisation up to 5,000 users and 1 million evidence records on a single recommended node size; horizontal workers for more
  Availability           Community: restart-safe, documented backup and restore. Enterprise: high-availability option with a documented recovery target
  Backup and recovery    Documented encrypted backups; restore tested in CI; recovery steps written for operators
  Security               No high-severity scan findings at release; independent penetration test before v1.0 and yearly after
  Privacy                No raw personal data in logs; scanner sends metadata only
  Accessibility          WCAG 2.1 AA for the web app and public pages
  Browsers and devices   Current and previous major versions of Chrome, Edge, Firefox and Safari; usable on a 375 px wide phone screen
  Languages              English and Hindi from Phase 2; all text externalised for translation
  Observability          Structured logs, metrics and traces; a connector health dashboard; an audit log for every write
  Upgrades               One-step upgrade with automatic, reversible-in-practice migrations; no data loss; release notes list breaking changes
  Documentation          Every feature has user docs and developer docs before its checklist box is ticked

21. Feature-by-feature checklist
--------------------------------

Each feature below shows the stage in which it is built (stages are in
section 16.1), the repository, what must exist first, what we expect to
see, and the boxes that must all be true. The longer description of how
each feature works is in section 8. A feature is finished only when
every box is ticked and the definition of done in 18.10 is met.

### Area A: Foundation

**F1. Workspaces, organisations and entities**

*Stage 1 · Community Edition · Depends on: nothing*

Expectation: a company creates an organisation with entities; one
organisation can never see another's data.

-   [ ] Create, rename and archive organisations and entities through
    the API and the web app

-   [ ] Entities can have one parent level

-   [ ] Row-level security is on for every tenant table

-   [ ] The cross-tenant test suite (read, write, search, file download)
    passes

-   [ ] Users with several memberships can switch organisation in the
    web app

**F2. Users, roles and sign-in**

*Stage 1 · Community Edition (SAML and SCIM in the Enterprise Edition,
Stage 4) · Depends on: F1*

Expectation: people sign in safely and see only what their role allows.

-   [ ] Sign in with OIDC (Google, Microsoft) or email with TOTP
    multi-factor authentication

-   [ ] Built-in roles match the matrix in 19.3; custom roles can be
    created

-   [ ] Auditor accounts are time-boxed and read-only

-   [ ] API tokens have scopes, expiry and revoke

-   [ ] Failed sign-ins are rate-limited and logged

-   [ ] Empty extension points exist for SAML and SCIM

**F3. Platform audit log**

*Stage 1 · Community Edition · Depends on: F1*

Expectation: any change can be traced to a person and a time.

-   [ ] Every write creates an entry with actor, action, object, before,
    after, time and request id

-   [ ] Entries cannot be edited or deleted through the API

-   [ ] Filter, export (CSV and JSON) and stream out by webhook

-   [ ] A test fails the build if any write endpoint lacks audit logging

### Area B: Compliance engine

**F4. Framework and control library**

*Stage 1 · Community Edition · Depends on: F1*

Expectation: adding a framework is a data task, not a coding task.

-   [ ] A framework file validates against framework.schema.json and
    imports with one command

-   [ ] Frameworks are versioned; an entity can stay on an older version

-   [ ] SOC 2 and ISO 27001:2022 load with our own wording and official
    clause references

-   [ ] A user-supplied spreadsheet can be imported as a framework

-   [ ] Draft, reviewed and published status is visible in the interface

**F5. Unified control set and crosswalk**

*Stage 1 basic, Stage 3 full · Community Edition · Depends on: F4*

Expectation: do a control once, get credit in every framework it covers.

-   [ ] One control maps to many requirements with a strength (full or
    partial) and a note

-   [ ] Implementing a control updates progress in every linked
    framework

-   [ ] Evidence linked to a control counts for all mapped frameworks

-   [ ] Mapping files are versioned data that can be reviewed in a pull
    request

-   [ ] Partial mappings are clearly shown in the interface

**F6. Country packs (regulation-as-code)**

*Stage 3 (DPDP, CERT-In) and Stage 4 (RBI, SEBI, IRDAI) · Community
Edition and SDK · Depends on: F4, F5, F9*

Expectation: installing the India pack turns on India's rules, tests,
deadlines and templates in one step.

-   [ ] A valid pack manifest installs the framework, controls, tests,
    workflows, templates and reports

-   [ ] Install, upgrade and uninstall work without data loss; an
    upgrade shows a "what changed" diff

-   [ ] A pack with legal\_reviewed set to false installs only in
    labelled draft mode

-   [ ] The DPDP and CERT-In packs install on a clean instance and pass
    their own tests

-   [ ] The pack specification and a sample pack are published in the
    SDK repository

-   [ ] An outside contributor can build and install a pack using the
    docs alone

**F7. Gap assessment and readiness score**

*Stage 1 · Community Edition · Depends on: F4, F5*

Expectation: the first screen answers "where do we stand?".

-   [ ] A guided scoping questionnaire (size, sector, data types, cloud
    use) generates the applicable controls

-   [ ] Each control can be not started, in progress, implemented, or
    not applicable with a reason

-   [ ] A readiness score per framework is calculated and explained

-   [ ] A prioritised gap list suggests next steps

-   [ ] The gap report exports as PDF

**F8. Regulatory change feed and pack versioning**

*Stage 4 basic, Stage 5 live feed · Community and Enterprise · Depends
on: F6*

Expectation: when a rule changes, customers see what is affected and get
tasks.

-   [ ] Pack versions carry a changelog and a diff

-   [ ] Customers see new, changed and removed requirements and the
    controls they affect

-   [ ] A task is created for each affected control

-   [ ] Community: updates arrive with normal releases. Enterprise:
    updates are fetched from the VayuX-operated feed

### Area C: Automation

**F9. Plugin framework and SDK**

*Stage 1 alpha, Stage 3 public · SDK and Community Edition · Depends on:
F1*

Expectation: anyone can add a connector, scanner or pack safely without
touching the core.

-   [ ] Manifest and protocol v1 are published as JSON schemas and a
    protocol file

-   [ ] The host runs plugins out of process in containers with network
    allow-lists and permission scopes

-   [ ] Admins see requested permissions at install and must approve
    them

-   [ ] Plugin signing and verification work; unsigned plugins need an
    explicit opt-in

-   [ ] The CLI can scaffold, test, validate, sign and publish a plugin

-   [ ] Conformance tests exist and a sample connector passes them

**F10. Connectors**

*Stage 2 (two), Stage 3 (ten), later 25 or more · Community Edition ·
Depends on: F9, F11*

Expectation: the tools a company already uses feed evidence
automatically.

-   [ ] Stage 2: GitHub and Google Workspace connectors

-   [ ] Stage 3: AWS, Google Cloud, Microsoft Azure, GitLab, Microsoft
    Entra ID, Jira, Slack and one Indian HR system

-   [ ] Each connector uses read-only scopes and lists exactly what it
    reads

-   [ ] Each has recorded-response tests and a health status

-   [ ] Each declares the controls it supports

-   [ ] Stages 4 and 5: Zoho, Razorpay, Tally, DigiLocker and Indian
    cloud providers

**F11. Evidence collection and ledger**

*Stage 2 · Community Edition · Depends on: F1, F3*

Expectation: every piece of proof is stored once, tamper-evident, with a
clear expiry.

-   [ ] Evidence from connectors, the agent, the scanner and manual
    upload all use the record in 19.5

-   [ ] Each record has hash and prev\_hash, and a verify command
    detects tampering

-   [ ] Records are append-only; a correction is a new record

-   [ ] A validity period and a "stale" status exist; stale evidence
    raises a refresh task

-   [ ] Files go to encrypted object storage with a scan status

-   [ ] An auditor can verify the chain from the interface

**F12. Automated control tests**

*Stage 2 v0, Stage 3 full · Community Edition · Depends on: F10, F11*

Expectation: rules are checked continuously and drift is caught fast.

-   [ ] Test YAML validates and runs in a sandbox with a time limit and
    no network or file access

-   [ ] Each result (pass, fail, error) stores the evidence ids it used

-   [ ] A failing test marks the control failing, opens a task and sends
    a notification

-   [ ] Exceptions need a reason, an approver and an expiry

-   [ ] Schedules run reliably and a test can be re-run manually

-   [ ] At least 20 starter tests ship across SOC 2, ISO 27001 and the
    India pack

**F13. Device agent**

*Stage 3 · Community Edition · Depends on: F11*

Expectation: laptops and servers report their security status without
exposing their contents.

-   [ ] Windows, macOS and Linux builds come from one codebase

-   [ ] Read-only checks cover disk encryption, OS updates, screen lock,
    endpoint protection status and firewall

-   [ ] The agent reports pass or fail only, never file contents, hourly
    by default

-   [ ] Enrolment uses a one-time token and can be revoked

-   [ ] The agent is open source with signed releases and can be
    deployed by device-management tools

-   [ ] Reports link to person and asset records

**F14. Evidence requests and manual evidence**

*Stage 2 · Community Edition · Depends on: F11, F20*

Expectation: things that cannot be automated still flow through one
clean process.

-   [ ] A request can be created with what, who and due date

-   [ ] The owner can upload a file or link or write a statement

-   [ ] A reviewer approves or rejects with comments

-   [ ] Approved items become ledger records

-   [ ] Reminders and escalation work

### Area D: Programme management

**F15. Policy management and attestations**

*Stage 2 · Community Edition · Depends on: F1, F20*

Expectation: policies are written, approved, shared and acknowledged in
one place.

-   [ ] A starter template library exists (English; Hindi for key
    staff-facing policies by Stage 3)

-   [ ] Versioning, approval workflow and review dates work

-   [ ] Policies are distributed to staff and acknowledgements are
    tracked with reminders

-   [ ] Policies link to controls and requirements

-   [ ] A policy exports as PDF

**F16. Risk register and assessment**

*Stage 3 · Community Edition · Depends on: F5*

Expectation: risks are scored, owned and tied to controls.

-   [ ] A register with a configurable likelihood and impact scale

-   [ ] A starter catalogue including India-sector scenarios

-   [ ] Treatment plans, residual risk and review dates

-   [ ] Risks link to the controls that reduce them

-   [ ] A heat map and a list of risks above appetite

**F17. Vendor risk management**

*Stage 3 · Community Edition · Depends on: F20*

Expectation: suppliers and processors are tracked and reviewed.

-   [ ] A register with tier, data handled, contract and agreement dates

-   [ ] A questionnaire sent by link, with document upload by the vendor

-   [ ] Renewal and review reminders

-   [ ] Cross-border flags feed the privacy module (F21)

**F18. Asset inventory**

*Stage 3 · Community Edition · Depends on: F10, F13*

Expectation: an up-to-date list of what the company must protect.

-   [ ] Import from connectors, the agent and CSV

-   [ ] Owner, classification and data types per asset

-   [ ] Assets without an owner create tasks

**F19. People compliance**

*Stage 3 · Community Edition · Depends on: F10, F15*

Expectation: joiners, leavers, training and acknowledgements are
provable.

-   [ ] Staff import through an HR connector or CSV

-   [ ] Onboarding and offboarding checklists are generated
    automatically

-   [ ] Training is assigned and completion evidence stored

-   [ ] Policy acknowledgement status is visible per person

**F20. Tasks, workflows, notifications and SLAs**

*Stage 2 · Community Edition · Depends on: F1*

Expectation: nothing important is forgotten.

-   [ ] Tasks are created automatically from failing controls, expiring
    evidence, overdue policies and requests

-   [ ] Owner, due date, priority, SLA and escalation rules work

-   [ ] Email, Slack and Microsoft Teams notifications and a weekly
    digest work

-   [ ] Users control their notification preferences

-   [ ] A WhatsApp notifier is planned as a later plugin

### Area E: India privacy and incident management

**F21. DPDP privacy module**

*Stage 3 · Community Edition · Depends on: F6, F17*

Expectation: an Indian company can run its DPDP programme end to end.

-   [ ] Data inventory

-   [ ] Notice and consent register with versions and timestamps

-   [ ] Rights-request workflow with identity check and deadline
    tracking

-   [ ] Grievance officer and DPO page

-   [ ] Processor tracking with agreements

-   [ ] Flags for children's data and cross-border transfers

-   [ ] Impact-assessment and audit templates for significant data
    fiduciaries

-   [ ] All legal wording comes from the pack and has been legally
    reviewed

**F22. Indian PII scanner and data discovery**

*Stage 3 · Community Edition (scanner plugin and collector) · Depends
on: F9, F21*

Expectation: find Indian personal data where it lives, without moving
it.

-   [ ] Detects Aadhaar, PAN, voter ID, IFSC, UPI ID, GSTIN, phone and
    email using structure and checksum validators

-   [ ] Scans relational databases, S3-compatible stores and Git
    repositories first

-   [ ] Runs in the customer's environment and sends metadata only

-   [ ] On synthetic test data the false-positive rate is below 5%

-   [ ] Findings create inventory entries and tasks

-   [ ] More patterns can be added as plugins

**F23. Incident and breach management with regulator clocks**

*Stage 3 · Community Edition · Depends on: F6, F20*

Expectation: when something goes wrong, every deadline starts counting
and everyone knows what to do.

-   [ ] Incident creation asks scoping questions

-   [ ] One clock per applicable obligation (the CERT-In six-hour
    window, DPDP, and RBI or SEBI where installed), with deadlines taken
    from the pack

-   [ ] Tasks, notification templates and a timestamped action log

-   [ ] A post-incident report exports

-   [ ] Clocks keep running when the page is closed and alert before
    each deadline

### Area F: Assurance and sharing

**F24. Audit management and auditor portal**

*Stage 3 export, Stage 4 portal · Community Edition · Depends on: F11,
F12*

Expectation: the audit is a smooth, read-only visit instead of a
scramble.

-   [ ] An audit project has scope, period and team

-   [ ] Auditors get time-boxed, read-only access

-   [ ] Evidence request list, sampling and findings work

-   [ ] The audit pack exports controls, evidence index, test results
    and exceptions

-   [ ] An auditor can verify the evidence chain

**F25. Trust centre**

*Stage 4 · Community Edition · Depends on: F12*

Expectation: customers can check your security posture without emailing
you.

-   [ ] A public page works on a custom domain

-   [ ] Admins choose which controls, certifications and policies appear

-   [ ] The live status of selected controls shows

-   [ ] Gated documents use request-and-approve with a click-through NDA

-   [ ] The page passes accessibility and search-engine checks

**F26. Reporting and dashboards**

*Stage 3 basic, Stage 4 board reports · Community Edition · Depends on:
F7, F12*

Expectation: leaders get a one-page answer.

-   [ ] Dashboards show readiness per framework, failing controls,
    overdue tasks, expiring evidence, risk heat map and vendor status

-   [ ] PDF and spreadsheet exports

-   [ ] A board summary and a gap report

-   [ ] Regulator-style templates supplied by packs

**F27. Security questionnaire automation**

*Stage 4 · Community Edition · Depends on: F15, F29*

Expectation: customer questionnaires are answered in hours, with a human
approving every answer.

-   [ ] A spreadsheet or document questionnaire can be uploaded

-   [ ] Suggested answers come from an answer library, with source links

-   [ ] Unmatched questions are flagged

-   [ ] A human approves before export, and approved answers are saved
    back

### Area G: Platform and operations

**F28. API, webhooks, command line and MCP server**

*Stage 1 API and webhooks, Stage 4 MCP · Community Edition · Depends on:
F2*

Expectation: anything the interface can do, automation can do.

-   [ ] Every interface feature has an API endpoint

-   [ ] The OpenAPI file is generated and client libraries are generated
    from it

-   [ ] Signed webhooks retry with backoff

-   [ ] A command-line tool supports scripts and CI checks

-   [ ] The MCP server respects the same permissions as a human user

**F29. AI assistant (assistive only)**

*Stage 4 first features, Stage 5 wider · Community Edition · Depends on:
F4, F15*

Expectation: AI speeds up writing and mapping, but a person decides.

-   [ ] Off by default; the model endpoint is configurable (hosted or
    self-hosted)

-   [ ] Drafts policies, suggests control mappings, explains clauses
    with source links and proposes questionnaire answers

-   [ ] All output is labelled AI-generated, cited, and needs human
    approval

-   [ ] No customer data is used for training and no personal data is
    sent unless an admin enables it

-   [ ] An evaluation set of at least 50 test prompts has written pass
    criteria

**F30. Deployment, backup, upgrade and air-gapped install**

*Stage 2 Compose, Stage 4 Helm, Stage 5 high availability · Community
and Enterprise · Depends on: nothing*

Expectation: easy to run, safe to keep, simple to upgrade.

-   [ ] One-command Docker Compose install

-   [ ] A Helm chart

-   [ ] Backup and restore commands and one-step upgrades with
    migrations

-   [ ] An air-gapped bundle with all images and packs

-   [ ] Region pinning and a choice of storage, database and keys

-   [ ] A CI test proves a clean install in under 15 minutes

**F31. Localisation and Indian formats**

*Stage 3 · Community Edition · Depends on: F1*

Expectation: the product feels Indian.

-   [ ] All strings are externalised

-   [ ] English and Hindi are complete for the web app

-   [ ] Dates, INR with lakh and crore grouping, and IST as default

-   [ ] Hindi templates for staff-facing policies and notices

-   [ ] A community translation process is documented

**F32. Partner (multi-client) console**

*Stage 4 · Enterprise Edition · Depends on: F1, F2*

Expectation: advisory firms run many clients from one place.

-   [ ] A roll-up across client organisations

-   [ ] Switching between clients leaves an audit trail

-   [ ] White-label report branding

-   [ ] Templates and answer libraries are reusable across clients

-   [ ] Row-level security is never bypassed

**F33. Billing and licensing**

*Stage 4 · Enterprise Edition · Depends on: nothing*

Expectation: we can charge, and customers are never surprised.

-   [ ] Plans and limits, Razorpay payments and GST invoices

-   [ ] Licence keys unlock Enterprise features offline

-   [ ] Free-tier limits never block core features

-   [ ] A failed renewal degrades gracefully and data stays accessible

**F34. Plugin registry and marketplace**

*Stage 3 basic registry, Stage 5 marketplace · Community Edition and SDK
· Depends on: F9*

Expectation: people can find and trust community plugins.

-   [ ] The registry lists author, permissions, version, signature and
    compatibility

-   [ ] A verification process earns a "verified" badge

-   [ ] Search and install work from inside the app

-   [ ] Stage 5: paid plugins and revenue share

### Release gates

**Public beta gate (before 13 May 2027)**

-   [ ] F1 to F7, F9 to F15, F20 to F23 and F31 are complete

-   [ ] The DPDP and CERT-In packs are legally reviewed

-   [ ] Ten connectors work and the plugin SDK is published

-   [ ] The threat model is current and a penetration test is scheduled

-   [ ] Install, upgrade and quick-start docs are complete

**Version 1.0 gate**

-   [ ] Every Stage 4 feature is complete

-   [ ] The independent penetration test has no open critical findings

-   [ ] SDK 1.0 and Community Edition 1.0 are tagged, with signed images
    and a software bill of materials

-   [ ] The Enterprise Edition passes its own test suite against
    Community 1.0

22. Starter content for the India packs
---------------------------------------

### 22.1 Rules for all pack content

-   Everything below is a **draft starting hypothesis** drawn from
    public summaries. It must be checked against the official texts and
    signed off by a lawyer before any pack is marked legal\_reviewed.

-   Never hard-code legal text, deadlines or thresholds in application
    code. They live in pack data, each with a reference to the official
    source (the Act, Rule or notification) and an effective date.

-   Every requirement in a pack carries our own plain-language wording
    plus the official reference.

-   Where a date or duration is uncertain, store a clearly marked
    placeholder and ask the owner.

### 22.2 DPDP pack: draft control groups

  Group                               What the pack should cover (draft)                                                                                                  Evidence or automated test idea
  ----------------------------------- ----------------------------------------------------------------------------------------------------------------------------------- -----------------------------------------------------------------------------------------------------------------
  Notice and consent                  A clear notice at the time of consent; consent that can be recorded and withdrawn as easily as it was given; notice versions kept   Every active processing activity points to a published notice version; consent events have timestamp and source
  Purpose and minimisation            Each processing activity has a stated purpose and only the data it needs                                                            Activity records are complete; fields without a purpose are flagged
  Data inventory                      Where personal data lives, who processes it, how long it is kept                                                                    Scanner findings compared with the inventory; unknown stores raise tasks
  Data principal rights               A process to receive, verify and answer access, correction, erasure and grievance requests within the times set in the pack         No open request is past its deadline
  Grievance redressal                 A published contact point and a response process                                                                                    The DPO or grievance page is public and complete
  Security safeguards                 Encryption, access control, multi-factor authentication, logging and backups appropriate to the data                                Connector tests: encryption at rest on, MFA enforced, logs retained
  Breach response                     Detection, assessment, and notification to the regulator and affected people on the timelines in the pack                           Incident clocks exist; a drill is recorded each year
  Retention and erasure               A retention period for each data type and deletion when the purpose is served                                                       Data stores without a retention rule are flagged
  Processors and transfers            Contracts with processors; checks on transfers outside India                                                                        Vendor register complete; agreements current; transfers flagged
  Children's data                     A verifiable parental-consent process where children's data is processed                                                            Activities flagged as children's data have a documented process
  Significant data fiduciary extras   If designated: an India-based DPO, an independent audit and impact assessments                                                      A checklist with owners and dates
  Governance                          An accountable owner, staff training, policies                                                                                      Policy acknowledgement and training completion rates

### 22.3 CERT-In pack: draft control groups

Based on public summaries of the CERT-In directions issued on 28 April
2022. Verify every item.

  Group                  What the pack should cover (draft)                                          Evidence or automated test idea
  ---------------------- --------------------------------------------------------------------------- --------------------------------------------------------------------------------------
  Incident reporting     Report listed incident types to CERT-In within six hours of noticing them   An incident workflow with a six-hour clock and a report template
  Log retention          Keep system logs for 180 days, stored within India                          Cloud and log connectors confirm retention of at least 180 days and an Indian region
  Time synchronisation   System clocks synchronised to the Indian government time sources            Agent and cloud configuration checks
  Point of contact       A named point of contact for CERT-In, kept current                          A contact record with a review date
  Incident catalogue     The list of reportable incident types, kept as pack data                    The catalogue version is shown in each incident

### 22.4 Later packs

RBI, SEBI CSCRF and IRDAI packs start with desk research and a
conversation with a regulated design partner. Claude Code should not
draft them from memory; it should ask the owner for the source documents
first.

### 22.5 How a pack becomes release-ready

1.  Claude Code drafts the pack with a source reference for every
    requirement.

2.  A human compliance reviewer checks the wording and mappings.

3.  A lawyer signs off.

4.  Set legal\_reviewed to true, record the reviewer and the date.

5.  Publish with a changelog, and schedule the next review.

23. The first tasks, in order
-----------------------------

Tick each box when the task is done and merged. Feature references point
to section 21. "SDK", "CE" and "EE" mean the three repositories.

**Stage 0: Foundation**

-   [ ] **T001** Create the three repositories (SDK, CE, EE) with the
    correct licence files, SPDX headers, README, and the standard
    project files listed in section 15.

-   [ ] **T002** Set up the GitHub organisation, branch protection,
    required checks and the DCO check.

-   [ ] **T003** Add AGENTS.md (from 18.2) and a copy of this document
    to each repository.

-   [ ] **T004** Build the CI skeleton: lint, type check, tests, secret
    scan, dependency and licence scan, static analysis, software bill of
    materials.

-   [ ] **T005** Create the local development environment: PostgreSQL,
    Redis, an S3-compatible store and a mail catcher, started with one
    command.

-   [ ] **T006** Write the first threat model and the first ADRs (plugin
    runtime, tenancy, evidence ledger).

**Stage 1: Contracts and core skeleton**

-   [ ] **T007** SDK: write the v0 JSON schemas for manifest, evidence,
    framework, control test and pack (F4, F9, F11, F12).

-   [ ] **T008** SDK: write the plugin protocol v1 definition (F9).

-   [ ] **T009** SDK: build the Python SDK skeleton with runtime helpers
    and testing helpers (F9).

-   [ ] **T010** SDK: build the conformance test harness v0 and the CLI
    scaffold command (F9).

-   [ ] **T011** CE: create the API application with health endpoints,
    configuration, structured logging and the standard error shape
    (F28).

-   [ ] **T012** CE: set up migrations and the base tables:
    organisation, entity, user, membership (F1).

-   [ ] **T013** CE: add row-level security and the cross-tenant test
    suite (F1).

-   [ ] **T014** CE: sign-in with OIDC, sessions and TOTP multi-factor
    authentication (F2).

-   [ ] **T015** CE: roles and permissions matching 19.3, and API tokens
    (F2).

-   [ ] **T016** CE: the audit log and the test that every write is
    logged (F3).

-   [ ] **T017** CE: the web shell with sign-in, layout, organisation
    switcher and translation scaffolding (F1, F31).

-   [ ] **T018** CE: the framework importer and loader (F4).

-   [ ] **T019** CE: draft SOC 2 and ISO 27001 framework files in our
    own wording with official references, for human review (F4).

-   [ ] **T020** CE: the control library, crosswalk tables and API (F5).

-   [ ] **T021** CE: web screens for choosing frameworks, the scoping
    questionnaire and the control list (F7).

-   [ ] **T022** CE: the readiness score and the gap report (F7).

-   [ ] **T023** CE: the extension-points package with empty interfaces
    for SAML, SCIM, audit export and licence checks (F2, F32, F33).

**Stage 2: Evidence and first automation**

-   [x] **T024** CE: tasks and notifications (F20).

-   [x] **T025** CE: policies, approvals and attestations (F15).

-   [x] **T026** CE: the evidence ledger with hash chain and verify
    command (F11).

-   [x] **T027** CE: manual evidence and evidence requests (F14).

-   [x] **T028** CE: the plugin host with sandbox, permissions and
    signing checks (F9).

-   [x] **T029** CE: GitHub and Google Workspace connectors as proof of
    the plugin design (F10).

-   [x] **T030** CE: the control-test engine v0 with ten starter tests
    (F12).

-   [x] **T031** CE: the Docker Compose deployment and the quick-start
    guide (F30).

-   [x] **T032** CE: an end-to-end test of the full gap-assessment flow
    with synthetic data (F1 to F15).

-   [x] **T033** Write the design-partner demo script and the first user
    guide.

-   [x] **T034** Hold the Stage 2 review with the owner; update this
    document and plan Stage 3.

Stages 3 to 6 follow the checklist in section 21 and the roadmap in
section 16.1. At the end of each stage, Claude Code proposes the next
task list in the same style and waits for the owner's approval.

24. When Claude Code must stop and ask a human
----------------------------------------------

Stop and ask, with a short question, the options, your recommendation
and the impact of each option, in any of these cases:

-   A requirement is unclear, missing or contradicts this document.

-   A change touches authentication, tenant isolation, secrets, the
    plugin sandbox or the evidence ledger design.

-   A change alters a public API, a spec schema, a licence or the
    repository boundaries.

-   A dependency has an unusual or unclear licence, or looks abandoned.

-   Anything involves legal or regulatory wording, deadlines or
    thresholds.

-   Anything involves real customer data, real credentials or real
    personal data.

-   Something would cost money (a paid service, a paid scan, a new
    account).

-   A decision marked Open in section 17 blocks the work.

-   A decision changes naming, branding or public wording.

-   You are about to delete data, rewrite history or weaken a test.

-   A test cannot be made to pass in a sound way.

-   You find that a feature is much larger or riskier than this document
    assumes.

25. Plain-language dictionary (extra words)
-------------------------------------------

  Word                  What it means, simply
  --------------------- ----------------------------------------------------------------------------------------------------
  API                   A menu of things one program can ask another program to do
  Webhook               A doorbell: Sampati rings another program when something happens
  SSO, OIDC, SAML       Ways to sign in with an account you already have, so you do not need a new password
  MFA                   A second step when you sign in, like a code on your phone
  RBAC, role            Different people get different keys: a guest cannot open the principal's office
  Tenant                One customer's private room inside the shared building
  Row-level security    A rule inside the database that hides other customers' rows, like a lock on every drawer
  Hash                  A fingerprint of some data: change one letter and the fingerprint changes
  Hash chain            Each page's fingerprint includes the previous page's fingerprint, so tearing out a page is obvious
  Metadata              Information about a thing, not the thing itself: "a file exists and is encrypted", not the file
  PII, personal data    Facts that point to a real person, like a name, phone number or ID number
  Schema                A form with rules about what may be written in each box
  YAML, JSON            Two simple ways to write structured information as text
  CEL                   A tiny, safe language for writing yes-or-no conditions
  Container             A sealed lunchbox that holds a program and everything it needs
  Sandbox               A play area with walls, so a program cannot wander off and break things
  Out of process        Running as a separate helper, so if it breaks the main program is fine
  Repository (repo)     A project folder that remembers every change ever made
  Pull request          A proposal to change the code that others look at before it is accepted
  CI                    A robot that tests every proposal automatically
  SBOM                  An ingredients list for software
  SPDX identifier       A short label at the top of a file that says which licence applies
  DCO sign-off          A promise by the author that they have the right to share the code
  ADR                   A short note explaining why we made a design choice
  Semantic versioning   Version numbers that tell you how big a change is: 2.0.0 is bigger than 1.4.1
  Open core             The main product is free and open; some extras are paid
  Self-hosting          Running the software on your own computers instead of someone else's
  Data residency        Keeping data inside a particular country
  Managed cloud         We run Sampati for you and you pay a monthly fee
  DPDP, CERT-In         India's personal-data law and India's national cyber-incident team
  DPO                   The person responsible for protecting people's data in a company
  Penetration test      Hiring friendly experts to try to break in so we can fix the weak spots
  Legal review          A lawyer checks that our wording matches the law

26. Document history and how to keep it up to date
--------------------------------------------------

### 26.1 History

  Version   Date               What changed
  --------- ------------------ ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  0.1       16 November 2026   First full draft: strategy, competitors, USP, stack, revenue, features, roadmap, risks
  0.2       17 November 2026   Name confirmed as Sampati by VayuX; naming convention; three repositories and licences; build roadmap
  0.3       19 November 2026   Build granth for Claude Code: plain-language start page, decision log, agent rules, technical blueprints, feature checklist, India pack starter, first tasks, stop-and-ask rules, dictionary

### 26.2 Keeping the document true

1.  When a decision changes, update section 17 first, then every section
    that depends on it.

2.  Tick the checklist boxes in sections 21 and 23 in the same pull
    request that finishes the work.

3.  Bump the version and add a line to the history table whenever
    something material changes.

4.  If the document and the code disagree, fix one of them the same day
    and tell the owner.

5.  The owner approves every change to sections 17, 18 and 22.

6.  At the end of each stage, review the whole document together and
    update the next stage's plan.

### 26.3 How Claude Code reports back

-   After every task: a short summary of what changed, which tests prove
    it, any risks or open questions, and the next task.

-   Every week: a one-page status listing finished items, blocked items,
    decisions needed and the plan for next week.

-   Raise blockers and doubts early and plainly. A short, honest
    question is always better than a quiet guess.

### 26.4 What success looks like

-   By the public beta: an Indian company can install Sampati in
    minutes, load the DPDP and CERT-In packs, connect its tools, see
    automated checks, run a breach clock and show an auditor the
    evidence.

-   By version 1.0: the same, plus auditor and trust-centre views, the
    Enterprise features, a clean security test and paying customers.

-   Always: a codebase that a stranger can read, test and extend, and a
    product that never claims more than it can prove.
