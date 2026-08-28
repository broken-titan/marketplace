# Which regime actually binds a deployment

Load this when deciding what compliance a lab-software feature is genuinely subject
to — before asserting in a design doc, PR, or customer conversation that a framework
applies.

The general frameworks in SKILL.md (Part 11, Annex 11, ALCOA++) are triggered by
*predicate rules and activity types*, not by "this is a lab." The regimes below are
what usually binds in practice, by sector.

## The trigger test

| Framework | Trigger | Not triggered by |
|---|---|---|
| 21 CFR Part 11 | A record required by an **FDA predicate rule** (§11.1(b)) — food, device, drug, biologics, tobacco | Being a laboratory; storing scientific data; wanting to look rigorous |
| EU GMP Annex 11 | Computerised systems used in **GMP-regulated activities for medicinal products** (human or veterinary) | Non-GMP lab work; food safety; general "GxP" association |
| ISO/IEC 17025 | Seeking accreditation, or a customer/regulator requiring accredited results | Doing testing generally |
| CLIA (42 CFR 493) | Testing **human specimens** for diagnosis or treatment | Animal, food, or environmental specimens |

Adopting a framework as a **design standard** without being legally bound is a
legitimate and common posture — Part 11's controls are sound engineering for any lab
record. Say which posture you are in. Claiming unearned legal applicability is itself
a finding.

## Veterinary and poultry

- **NPIP — National Poultry Improvement Plan (9 CFR parts 145, 146, 147).** The
  poultry-specific lab regime. The **mandate** that official tests be run by an
  authorized laboratory is in **9 CFR 145.14**, not 147.52; **147.52** supplies the
  criteria for *being* an authorized laboratory. It requires: the next available check
  test **for each assay performed** (147.52(a)); testing run **or overseen by** a
  technician who every four years completes Service-approved workshops (147.52(b));
  official assays performed and reported as described in the NPIP Program Standards
  (147.52(c)); and periodic review of records and protocols — an Official State Agency
  site visit and recordkeeping audit **at least once every 2 years** (147.52(d), a floor
  rather than a fixed cadence), plus a Service review every three years (147.52(e)) and
  random sample verification (147.52(g)).
  Reporting duties, and note the trigger **changed in 2025**: 147.52(f)(2) now requires
  "*Salmonella* Pullorum and Mycoplasma Plan disease **infected flocks as confirmed by
  testing in accordance with § 145.14**" to be reported to the Official State Agency
  within **48 hours** — revised by 90 FR 46741 (30 Sept 2025), effective 30 October 2025.
  The superseded text keyed the duty to **reactors**, so anything built against a CFR
  annual edition dated 2024 or earlier has the wrong trigger. 147.52(f)(1) separately
  provides for H5/H7 LPAI to be reported **directly to the Service**, under criteria set
  by a memorandum of understanding rather than by a fixed deadline in the rule.
  **Software consequences**: test records, technician-qualification evidence, and
  proficiency-test results must be retrievable for audit; reporting deadlines are
  workflow requirements, not just policy. Method specifics live in the NPIP Program
  Standards (Standard B, bacteriological examination), revised on a rolling basis —
  treat the standards version as a config value, never a hardcoded constant.
- **AAVLD accreditation.** AAVLD accredits against **its own AC1 Requirements**
  (current version 2021.01), which are *derived from and congruent with* ISO/IEC
  17025:2017 — the FDA/Vet-LIRN white paper cross-references them clause by clause.
  Word this precisely: AAVLD accreditation is **not** ISO 17025 accreditation, which is
  granted by ILAC/GAC-recognized bodies such as A2LA or ANAB. A lab may hold either or
  both.

## Food safety (US)

- **USDA-FSIS 9 CFR 417.5 (HACCP records)** — the most directly on-point regime for
  poultry processing, and close to a domain-native restatement of ALCOA: "Each entry on
  a record maintained under the HACCP plan shall be made **at the time the specific
  event occurs** and include the date and time recorded, and shall be **signed or
  initialed by the establishment employee making the entry**." Electronic records are
  acceptable "provided that appropriate controls are implemented to ensure the
  integrity of the electronic data and signatures" — a principles-based analogue of
  Part 11, not a cross-reference to it.
  Retention: one year for slaughter and refrigerated product, two years for
  frozen/preserved/shelf-stable; offsite storage permitted after six months if
  retrievable within 24 hours.
- **FSIS Accredited Laboratory Program (9 CFR parts 439 and 391)** — accredits
  non-federal labs analyzing meat, poultry, and egg products; a 2022 final rule
  (effective 24 October 2022) expanded scope from food chemistry and chemical residues
  to microbial indicator organisms and pathogen testing. Note the contrast with FDA's
  LAAF program: FSIS **declined to require** ISO/IEC 17025 accreditation for ALP — the
  final rule (87 FR 51861, 24 Aug 2022) states "Laboratories may choose whether to be
  accredited to the ISO 17025 standard; however, FSIS will not require ISO 17025
  accreditation under the ALP", while separately accepting ISO 17025-accredited
  management systems as *satisfying* ALP requirements. Word it as "not required, but the
  recognized route to satisfying ALP's management-system requirement" — "recommended" is
  an over-claim FSIS did not make.
  **9 CFR 439.20(b)** is the retention rule that governs an ALP-accredited
  **laboratory's own** records — a three-year floor, anchored per record family
  (including "three years after the last recorded entry" for prepared standards, a
  rolling anchor). This, not 417.5's establishment-facing 1–2 years, is the number a lab
  LIMS must implement.
- **FDA Egg Safety Rule, 21 CFR 118.10** — requires *Salmonella* Enteritidis testing
  records containing "the date and time of the activity that the record reflects" and
  "the signature or initials of the person performing the operation or creating the
  record," retained one year after the flock leaves production. Electronic records are
  permitted and are deemed onsite if accessible from an onsite location. This is a
  plausible **Part 11 predicate rule** hook for poultry work.
- **FSMA → LAAF rule (21 CFR part 1, subpart R, §§1.1101–1.1201)**, published
  3 December 2021: LAAF-accredited laboratories must hold **ISO/IEC 17025:2017**
  accreditation from an ILAC-MRA-signatory (now GAC) body, with records requirements at
  §1.1154 and FDA access on written request. **Narrow trigger** — LAAF-accredited
  testing is required only in specific circumstances: supporting removal from an import
  alert, supporting admission of an imported article, responding to an identified or
  suspected food-safety problem, or under a directed food laboratory order. Import
  requirements phase in per-analyte six months after FDA declares sufficient capacity
  (mycotoxins first, effective 1 December 2024). **Routine in-house pathogen monitoring
  is generally not covered.**

## Clinical / medical

- **ISO 15189:2022** (Edition 4) is the accreditation standard for medical
  laboratories — the counterpart to 17025 for human specimens. It replaced
  ISO 15189:2012 and absorbed ISO 22870:2016 (point-of-care). Structurally aligned to
  17025:2017, but **report content is clause 7.4**, so every 7.8 reference in the main
  skill shifts. Annex B provides an explicit comparison against ISO 9001:2015 and
  ISO/IEC 17025:2017. Accreditation to the 2012 edition ceased to be recognized under
  the ILAC Arrangement after 6 December 2025.
- **CLIA — 42 CFR part 493** is *not* an accreditation standard: it is mandatory US
  federal regulation (administered by CMS with CDC and FDA) that any laboratory testing
  human specimens for diagnosis or treatment must satisfy, regardless of accreditation.
  ISO 15189 is **not** recognized as CLIA-equivalent; a US clinical lab needs CLIA and
  may additionally seek ISO 15189 accreditation. Bodies such as A2LA offer combined
  programs precisely because the two are complementary layers.
  *Live development*: a CMS/CDC Request for Information on the CLIA regulations was
  published 16 July 2026 (91 FR 43586, CMS-3485-NC), comments due 14 September 2026.
  An RFI changes no requirement.

## Pharmaceutical / GMP

- **EU GMP Annex 11** applies to computerised systems in GMP-regulated activities for
  medicinal products. Binding text is the **January 2011** revision; the draft revision
  (7 July 2025, consultation closed 7 October 2025) is not yet final — expected late
  2026, application ~2027.
- **Draft Annex 22 (Artificial Intelligence)**, same track: would permit only static
  (locked) models in critical GMP applications affecting product quality, patient
  safety, or data integrity; dynamic/continuously-learning models, generative AI, and
  LLMs are excluded from critical applications and allowed only in non-critical uses
  with human oversight. Relevant if AI-assisted features are added to a GMP-facing lab
  system.
- **PIC/S PI 041-1** (in force 1 July 2021) — "Good Practices for Data Management and
  Integrity in Regulated GMP/GDP Environments." Requires risk-based audit-trail review
  with frequency based on criticality, using quality risk management principles, with
  documented evidence of what was reviewed and what was found. **This is the citable
  in-force authority for periodic audit-trail review** — use it rather than the draft
  Annex 11.
- **GAMP 5, 2nd edition** (ISPE, July 2022) — current. Custom/bespoke applications are
  **Category 5**, requiring the fullest lifecycle rigor. The 2nd edition emphasizes
  critical thinking over document box-ticking, accepts agile/iterative delivery,
  aligns with FDA's Computer Software Assurance (CSA) approach, and adds appendices on
  AI/ML, cloud, blockchain, and open-source software. It does **not** prescribe
  IQ/OQ/PQ terminology — that is legacy shorthand that regulators still accept.
