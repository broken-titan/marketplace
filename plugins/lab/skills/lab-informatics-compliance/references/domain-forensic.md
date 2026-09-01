# Forensic overlay (ISO 17025 + ANAB AR 3125 + FBI QAS)

Load when `forensic`, `anab_ar3125`, or `fbi_qas` is on. Identifier
kinds: **exhibit, case, item**. CLIA is off for forensic-only
components (42 CFR 493.3(b)(1)). Do not default a patient primary key.

## ISO/IEC 17025

Forensic testing and calibration labs are commonly accredited to 17025.
Load `iso-lab-agnostic.md` and `iso-17025-reporting.md` when
`iso_17025` is on.

## ANAB AR 3125

[AR 3125:2023](https://anab.ansi.org/standard/ar-3125/), Accreditation
Requirements for Forensic Testing and Calibration Laboratories
(effective 2023-02-01), supplements ISO/IEC 17025:2017 with ILAC
policies and forensic-specific requirements (impartiality, ethics code
with annual review record, personnel, evidence control, technical
records, reporting, management system). A requirement that does not
apply to the work is "not applicable."

Design notes from the public AR 3125 framing (confirm current PDF
before a clause letter in a matrix):

- Evidence / item continuity is first-class (seal, transfer, storage).
- Technical records must support reinterpretation by another competent
  examiner.
- Code-of-ethics review is a **recordable event**.

Do not invent AR 3125 subclause numbers not verified in the current
document.

## FBI Quality Assurance Standards (DNA)

When the lab uploads to CODIS or claims QAS compliance:

- *Quality Assurance Standards for Forensic DNA Testing Laboratories*
  and *Quality Assurance Standards for DNA Databasing Laboratories*,
  **effective 1 July 2025**, not retroactive
  ([SWGDAM publications](https://www.swgdam.org/publications)).
- ANAB is approved by the FBI NDIS program to assess QAS alongside
  17025.

QAS covers personnel, validation, analytical procedures, reports,
review, proficiency testing, audits, and (2025) Rapid DNA. Software
consequences: method/validation identity, two-person review where QAS
requires it, and proficiency-test records retrievable by analyst and
date. Exact Standard numbers belong in a matrix built from the 2025
PDF — do not invent them here.

AR 3125 and QAS do **not** cover criminal-justice information
security. That is `cjis`.

## FBI CJIS Security Policy

When `cjis` is on. Silence does not enable it.

https://le.fbi.gov/cjis-division/cjis-security-policy-resource-center

Confirm the **current** Policy edition before citing a section
number — later editions renumber. Software themes (LIMSpec 21.7–
21.17 as a map, not as frozen 5.x cites): unique identity; CHRI
secondary-dissemination log; NCIC/III transaction identity;
encryption in transit and at rest for CJI; no commercial use of
unencrypted CJI metadata in a cloud; password/certificate
authenticators as configured. CoC remains the base object
(`base-objects.md` O16); this overlay adds CJI handling, not
exhibit/seal ownership.

## Sources

- [ISO/IEC 17025:2017](https://www.iso.org/standard/66912.html)
- [ANAB AR 3125](https://anab.ansi.org/standard/ar-3125/)
- [42 CFR 493.3(b)(1)](https://www.ecfr.gov/current/title-42/section-493.3)
- FBI QAS effective 1 July 2025 (SWGDAM)
- [FBI CJIS Security Policy](https://le.fbi.gov/cjis-division/cjis-security-policy-resource-center)
