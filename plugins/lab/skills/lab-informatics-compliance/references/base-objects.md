# First-class lab objects and write-path gates

Load with the base skill. These are **software MUST** rules for any
lab informatics system this skill designs. Overlay files add
type-specific fields; they do not replace these objects.

Silence still does not enable Part 11, CLIA, 15189, 17025, WADA,
SEDD, or CJIS. When a cite is overlay-gated, the object still exists;
the cite is how you defend it.

LIMSpec 2022 R2:
https://www.limswiki.org/index.php/LII:LIMSpec_2022_R2

FDA CGMP data-integrity Q&A (Dec 2018):
https://www.fda.gov/regulatory-information/search-fda-guidance-documents/data-integrity-and-compliance-drug-cgmp-questions-and-answers-guidance-industry

## O1 — Equipment lock-out

Unique instrument/equipment ID. Status includes calibration,
maintenance, and investigation. The **write path refuses** devices
that are out-of-calibration, overdue, or under investigation. The
result binds the equipment ID used.

- ISO/IEC 17025:2017 **6.4** — equipment includes measuring
  instruments, **software**, measurement standards, reference
  materials, reagents, consumables, and auxiliary apparatus. **6.4.13**
  is the equipment-record list. Confirm letters in the standard.
- 21 CFR [211.194(d)](https://www.ecfr.gov/current/title-21/section-211.194)
- LIMSpec **10** (esp. 10.9, 10.13, 10.15)

## O2 — Reagent / standard / consumable lot gates

Lot, preparation, expiry, and approval-for-use travel with the test.
The selector filters expired, unapproved, and kit-interchanged
materials (unless the manufacturer permits interchange).

- 42 CFR [493.1252(c)–(e)](https://www.ecfr.gov/current/title-42/section-493.1252)
  — label; do not use expired/deteriorated/substandard; do not
  interchange kit components of different lots unless the
  manufacturer specifies otherwise
- 21 CFR [211.194(c)](https://www.ecfr.gov/current/title-21/section-211.194)
- LIMSpec **3** (3.1–3.3) and **14**

## O3 — Method as a versioned object

Every result carries `method_id` + revision. Operators see current.
Prior revisions archive. A modification stores reason + verification
that the modified method is at least as accurate and reliable.

- ISO/IEC 17025:2017 **7.2**
- 21 CFR [211.194(a)(2)](https://www.ecfr.gov/current/title-21/section-211.194)
  and **(b)**
- LIMSpec **7** (7.3–7.6)

## O4 — Metrological traceability

The result points at the **instrument calibration certificate** and
the **CRM / standard lot**, not only a method name.

- ISO/IEC 17025:2017 **6.5** (and 6.4.13 equipment records)
- LIMSpec 10.11

## O5 — Interfaces as named trust-boundary objects

Each interface is a named object with a **verification record**.
Validate including interfaces. Check calculations and transfers
systematically. Accurate send from entry to destination.

- ISO/IEC 17025:2017 **7.11.2**, **7.11.6**
- ISO 15189:2022 **7.6.3** (confirm letter in the standard)
- 42 CFR [493.1291(a)](https://www.ecfr.gov/current/title-42/section-493.1291)
- LIMSpec **27.15**, **26**

## O6 — Original dynamic instrument data

Store the reprocessable file plus metadata (units, instrument, user,
processing parameters), **dual-homed** with the result. A static
printout is not a true copy. Keep aborted runs and every reprocessed
chromatogram / equivalent.

- FDA DI Q&A **1.b / 1.d / 1.e**, **Q10**, **Q12**, **Q14**
- 21 CFR [211.194(a)(4)–(5)](https://www.ecfr.gov/current/title-21/section-211.194)
- LIMSpec **13**, **24** / ASTM E1578-18R26 **E-11**
- [ASTM E1578 store](https://store.astm.org/e1578-18r26.html)
  (paywalled). Use `limspec-map.md` for checklist content.

## O7 — OOS / OOT incident

A specification-limit breach opens a first-class incident, blocks
release, and forbids delete-and-replace. The original failing value
remains.

- FDA *Investigating Out-of-Specification (OOS) Test Results for
  Pharmaceutical Production* (Phase I laboratory / Phase II
  full-scale) under 21 CFR 211.192:
  https://www.fda.gov/media/158416/download
- FDA DI Q&A **Q2**
- 21 CFR [211.192](https://www.ecfr.gov/current/title-21/section-211.192)
- LIMSpec **16** (16.4–16.8)

GxP phase detail: `fda-oos.md` when a 211 / GMP flag is on.

## O8 — QC and PT as first-class sample / test types

Cannot report while required QC is missing or failing. PT is a
**distinct type**, not a flag on a patient (or other primary) row.

- 42 CFR [493.1256](https://www.ecfr.gov/current/title-42/section-493.1256)
- ISO/IEC 17025:2017 **7.7.2**
- LIMSpec **2.11**

CLIA PT conduct rules (no referral / no cross-site talk): clinical
overlay when `clia` is on.

## O9 — §11.10(f)–(h) as schema

When Part 11 is on, these are **software**, not SOP:

- **(f)** operational checks that enforce permitted sequencing
- **(g)** authority checks (who may use, sign, access a device, alter
  a record, or perform the operation)
- **(h)** device / source-of-input checks

https://www.ecfr.gov/current/title-21/section-11.10

When Part 11 is off, keep the same objects as design practice; do
not claim §11.10.

## O10 — Open systems (§11.30)

Profile switch `open_system`. When on (and Part 11 is on): all
applicable §11.10 controls **plus** extra encryption and digital-
signature measures from creation to receipt.

https://www.ecfr.gov/current/title-21/section-11.30

Do not leave this under “code cannot cover.” Closed vs open is a
deployment fact the profile records. Silence = closed / off.

## O11 — §11.70 signature / record linking

Electronic and handwritten-to-electronic signatures **cannot be
excised, copied, or transferred** to falsify a record by ordinary
means. Bind signature fields into the same immutable row / hashes
(base skill rule 5). Relational links are neither required nor
sufficient.

https://www.ecfr.gov/current/title-21/section-11.70

## O12 — Unique write identity

No shared write accounts. An admin role that can alter files or
settings is **not** assigned to people responsible for record
content.

- FDA DI Q&A **Q4**, **Q5**
- LIMSpec **31.6**

## O13 — Competency gate (write path)

Only personnel with **current mapped competency** for that method /
task may perform it. HR files (medical history, occupational
exposure, course catalogues) stay **organizational**. The gate is
software.

- ISO/IEC 17025:2017 **6.2**
- 21 CFR [11.10(i)](https://www.ecfr.gov/current/title-21/section-11.10)
  when Part 11 is on
- LIMSpec **7.7**, **8.8**

## O14 — Failure + downtime mode

Record system failures and the immediate and corrective actions
(17025 **7.11.3(e)**). Planned degraded mode for LIS/LIMS down,
including autoverification shutdown (15189 **7.6.4**; 42 CFR
[493.1251(b)(14)](https://www.ecfr.gov/current/title-42/section-493.1251)).
Identity and trail still hold.

## O15 — Config as a versioned, revalidated record

Runtime spec limits, calculation constants, and method parameters
in the database are configuration records — not only a git build
ID. Authorize, document, and validate before implementation.

- ISO/IEC 17025:2017 **7.11.2**
- 21 CFR [11.10(k)](https://www.ecfr.gov/current/title-21/section-11.10)
  when Part 11 is on
- FDA DI Q&A **Q3**
- LIMSpec **32**

## O16 — Chain of custody

Append-only movement events: person, location, time. Subdivisions
inherit tracking. Forensic overlay adds exhibit/seal rules; it does
**not** own CoC.

- LIMSpec **1.18** (and 21.6 for subdivided evidence)
- ISO/IEC 17025:2017 **7.4**

## O17 — Cybersecurity as a lab-system control

Independent of the HIPAA/GDPR privacy switch. A lab with no PHI
still protects the information system.

- ISO 15189:2022 **7.6.3** (note pointing at ISO/IEC 27001 —
  confirm wording in the standard)
- LIMSpec **35**

## O18 — Backup = verified true copy

Backup is a verified true copy of the **dual-home pair** in original
or compatible format for the retention period. Crash dumps do not
qualify.

- FDA DI Q&A **1.e**
- 21 CFR [211.68(b)](https://www.ecfr.gov/current/title-21/section-211.68)
  when 211 applies
- LIMSpec **27.11**

## O19 — Physical sample vs record retention

Return, destruction, and hold-time of the **physical sample** are a
different object from **record** retention classes (base skill
rule 8). Do not collapse them into one TTL.

## O20 — Privacy erase vs regulated keep

Refuse erasure or anonymization of a record still inside a
CLIA / 17025 / GLP / 606 (or other binding overlay) retention
floor. Label the conflict in the API and the UI. LIMSpec **36.3**
de-identification is **not** a software requirement while a
regulated keep is in force.
