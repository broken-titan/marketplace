# GxP computerised-system overlay

Load when any of `part_11`, `annex_11`, `glp`, `gclp`, `qmsr`, or
medicinal-product GMP activity is on. Each flag is independent.
Silence does not enable any of them.

## 21 CFR Part 11

**Trigger:** a record required by an FDA predicate rule is electronic
(§11.1(b)). Not triggered by being a laboratory.

**Carve-out:** Part 11 does **not** apply to records required only by
21 CFR part 1 subpart R (LAAF) — §11.1(p). If the same record is also
required by another predicate, Part 11 remains on.

When on: closed-system controls [§11.10](https://www.ecfr.gov/current/title-21/section-11.10)
including **(f)–(h) as schema** (sequencing, authority, device/
source-of-input — `base-objects.md` O9); signature manifestation
§11.50; signature/record linking [§11.70](https://www.ecfr.gov/current/title-21/section-11.70)
so signatures cannot be excised or transferred (O11). Identity
proofing, FDA certification, and two-component execution stay with
the identity platform (base skill rule 5).

**Open systems:** when `open_system` is on, [§11.30](https://www.ecfr.gov/current/title-21/section-11.30)
adds encryption and digital-signature measures from creation to
receipt (O10). Silence = closed / off.

## EU GMP Annex 11

**Trigger:** computerised systems in GMP-regulated activities for
medicinal products (human or veterinary). Narrower than "GxP."

Binding text is still the **January 2011** revision (EudraLex Volume 4).
The July 2025 draft is not in force. Do not cite draft audit-trail
lock language as current law.

Draft **Annex 22** (AI) is on the same track: static, locked models
only in critical applications. Relevant if AI-assisted features are
added; not in force.

## PIC/S PI 041-1

In force 1 July 2021. Good practices for data management and integrity
in regulated GMP/GDP environments. Citable authority **today** for
risk-based audit-trail review. Frequency from documented risk, not
from a vendor "monthly" article.

## GAMP 5 (2nd ed., 2022)

Validation lifecycle. Custom-built lab software is **Category 5**.
Emphasizes critical thinking, accepts agile, aligns with FDA CSA.
Does not prescribe IQ/OQ/PQ terminology. The informatics-system
package (category, URS, risk, IQ/OQ/PQ, traceability) is
`lab-system-csv` when `system_csv` is on or the user flags that
skill.

## GAMP GPG: laboratory computerized systems (2nd ed., 2012)

Distinct from GAMP 5. Instrument complexity, raw-data definition,
interfacing. Load `gamp-lab-systems.md`.

## USP ⟨1058⟩ Analytical Instrument Qualification

Groups A/B/C. Load `usp-1058.md` when GxP instrument fitness is in
scope (or `usp_1058` adopted).

## FDA OOS (211.192)

Phase I laboratory / Phase II full-scale. Load `fda-oos.md`.
https://www.fda.gov/media/158416/download

## 21 CFR 211 — drug QC laboratory

When the system holds CGMP laboratory records for finished
pharmaceuticals: 21 CFR 211.194 (laboratory records) and 211.180
(record retention). Typical 211.180 floor: at least **1 year after
expiry** of the batch, or **3 years after distribution** if no expiry
— confirm the current paragraph before coding a number. Model as a
class + floor, not a constant.

## 21 CFR 58 / OECD GLP

**Trigger:** nonclinical laboratory studies intended to support a
research or marketing permit (US 21 CFR part 58) and/or studies
claimed to follow OECD GLP.

Design notes (do not invent extra clause letters):

- Study / test-system / specimen identity is first-class.
- Raw data and the study file are retained to the part 58 / OECD
  archive rules. Exact year floors differ by study type — store the
  floor from the profile; do not hardcode.
- The study director and quality-assurance unit are organizational
  roles the system must be able to attribute, not optional comments.

## GCLP

Good Clinical Laboratory Practice (WHO / EMA / sponsor contracts) is
**not** a US statute. Turn on only when adopted. It does not replace
CLIA when patient-specific care results are reported, and it does not
replace 21 CFR 58 when the work is a nonclinical safety study.

## QMSR — device QC (21 CFR 820)

US device current good manufacturing practice is the **Quality
Management System Regulation**: 21 CFR part 820 incorporating
ISO 13485:2016 by reference, **in force 2 February 2026**. Do not cite
the retired QSR subsystem list as current law. ISO 13485 certification
is not automatic QMSR compliance; FDA-specific provisions remain.

Device QC laboratory records follow 820 / 13485 record-control
obligations. Retention class + floor from the quality system, not a
year in this file.

## Sources

- [21 CFR 11.10](https://www.ecfr.gov/current/title-21/section-11.10),
  [11.30](https://www.ecfr.gov/current/title-21/section-11.30),
  [11.70](https://www.ecfr.gov/current/title-21/section-11.70)
- [21 CFR part 11](https://www.ecfr.gov/current/title-21/part-11)
- [21 CFR 11.1(p)](https://www.ecfr.gov/current/title-21/section-11.1)
- EudraLex Volume 4, Annex 11 (January 2011)
- PIC/S PI 041-1 (1 Jul 2021)
- [21 CFR part 820](https://www.ecfr.gov/current/title-21/part-820) /
  [FDA QMSR page](https://www.fda.gov/medical-devices/postmarket-requirements-devices/quality-management-system-regulation-qmsr)
- [21 CFR part 58](https://www.ecfr.gov/current/title-21/part-58)
- [21 CFR 211.180](https://www.ecfr.gov/current/title-21/section-211.180),
  [211.194](https://www.ecfr.gov/current/title-21/section-211.194)
- OECD Principles of GLP (ENV/MC/CHEM(98)17) — confirm current OECD
  page before quoting a year
- [FDA OOS guidance](https://www.fda.gov/media/158416/download)
- [GAMP GPG laboratory computerized systems](https://ispe.org/publications/guidance-documents/gamp-good-practice-guide-gxp-compliant-laboratory-computerized-systems)
- USP ⟨1058⟩ (USP store; paywalled)
