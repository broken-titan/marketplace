# Food and feed laboratory overlay

Load when `food_feed`, `fsis_alp`, or `laaf` is on. **Poultry / NPIP is
not the food default.** If the work is official NPIP Plan assays, load
`poultry-veterinary.md` in addition — do not treat this file as NPIP.

Identifier kinds: lot, batch, commodity, establishment. Not patient.

## ISO 17025

Most accredited food-testing labs sit on 17025. Load
`iso-lab-agnostic.md` and `iso-17025-reporting.md` when `iso_17025` is
on. 17025 is still a trigger, not automatic because a CoA was issued.

## FSIS Accredited Laboratory Program (9 CFR parts 439 and 391)

Accredits non-federal labs analyzing meat, poultry, **and egg
products**. A 2022 final rule (87 FR 51861, 24 Aug 2022, effective
24 Oct 2022) expanded scope to microbial indicator organisms and
pathogen testing.

FSIS **declined to require** ISO/IEC 17025 for ALP. Laboratories may
choose 17025; FSIS will not require it, while accepting a 17025
management system (in good standing with an ILAC-recognized body) as
satisfying ALP's management-system requirement. Do not say "FSIS
recommends 17025."

**9 CFR 439.20(b)** is the retention rule for an ALP-accredited
**laboratory's own** records — a **three-year** floor, anchored per
record family (including "three years after the last recorded entry"
for prepared standards — rolling; certificates of analysis for
purchased standards "for at least the period of time that the
materials are in use" — in-use, no fixed term). This, not
establishment-facing 9 CFR 417.5, is the number a lab system must
implement when `fsis_alp` is on.

9 CFR 417.5 binds the **official establishment**, not the laboratory.
A CoA is supporting documentation under contract, not a 417.5(b)
monitoring record signed by an establishment employee.

## LAAF — 21 CFR part 1 subpart R

**Narrow trigger:** LAAF-accredited testing is required only for
specified circumstances (import-alert removal, admission of an imported
article, response to an identified or suspected food-safety problem, or
a directed food laboratory order). Routine in-house pathogen
monitoring is generally not covered. Import requirements phase in
per-analyte after FDA declares capacity (mycotoxins first,
1 December 2024).

LAAF incorporates ISO/IEC 17025:2017(E) by reference (§1.1101) and
hardens it:

- **§1.1152(d)(1):** full analytical report must include 17025
  7.8.2.1(a)–(p) and 7.8.3.1(a)–(d). The 7.8.2.1 "valid reasons"
  hatch does not survive. MU (7.8.3.1(c)) becomes unconditional.
  Serializer fail-closed.
- **§1.1154(c):** significant amendments trackable; conspicuous
  indication on the **original** that it was altered and a newer
  version exists. That **forward** notice breaks a pure append-only
  artifact. Options: `superseded_by` in the DB stamped at retrieval;
  or re-issue the original with the notice and retain both.
- **§1.1152** also requires name and signature of the analyst for
  **each analytical step**, retention of discarded/re-worked raw data
  with justification, and software identification. Three signature
  roles: per-step analyst, report authorizer, management certifier.

**Part 11 does not apply** to records required only by subpart R
(§11.1(p)). If another predicate also requires the record, Part 11
stays on.

**§1.1154(a)** retention floor in LAAF scope: **5 years** from record
creation (confirm current paragraph before coding).

## HACCP-plan authoring (LIMSpec 19.5)

**Not a software requirement** for this skill. A HACCP / food-safety
**authoring UI** is organizational / MES-adjacent. This overlay owns
the **data shape** of food/feed results (lot, commodity,
establishment), not a plan editor. Implement 19.5 only if the user
explicitly asks for a HACCP module.

## Food — what not to default

- Do not use NPIP flock/house identity as the food commodity model.
- Do not apply egg-producer 21 CFR 118.10 retention to the laboratory
  unless the lab is the producer (it almost never is).
- Do not apply 417.5's 1–2 year establishment floors to lab records.

## Sources

- [21 CFR part 1 subpart R](https://www.ecfr.gov/current/title-21/part-1/subpart-R)
- [21 CFR 11.1(p)](https://www.ecfr.gov/current/title-21/section-11.1)
- [9 CFR 439.20](https://www.ecfr.gov/current/title-9/section-439.20)
- 87 FR 51861 (24 Aug 2022)
