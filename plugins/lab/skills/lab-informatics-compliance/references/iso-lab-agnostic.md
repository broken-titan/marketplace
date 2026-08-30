# ISO obligation map (no domain examples)

Load when ISO/IEC 17025, ISO 15189, or AAVLD is on, or the accreditation
family is not yet settled. Design against the **obligation**. Resolve the
clause number from the table once the family is known.

ISO 15189:2022 is structurally aligned with ISO/IEC 17025:2017; Annex B
compares 15189 to 17025 and ISO 9001. AAVLD SOP 1137 v1 (approved
7 February 2023, carrying 2021-01 clause content; legacy alias "AC1") is
derived from and congruent with 17025:2017 but numbered on the 2005 scheme.

Citing a 17025 number at a 15189 or AAVLD auditor is a credibility problem
even when the substance is right.

| Obligation | ISO/IEC 17025:2017 | ISO 15189:2022 | AAVLD SOP 1137 |
|---|---|---|---|
| Technical records / identity / contemporaneous capture | 7.5.1 | resolve via Annex B | 5.4 / 5.5 (verify current Qualtrax text) |
| Amendments keep the original | 7.5.2 | resolve via Annex B | verify current Qualtrax text |
| Unambiguous item identification | 7.4.2 | pre-examination / sample identification (7.2–7.3; verify Annex B) | 5.8 |
| Deviations on receipt | 7.4.3 | resolve via Annex B | verify current Qualtrax text |
| Storage / conditioning of items | 7.4.4 | resolve via Annex B | verify current Qualtrax text |
| Report content | 7.8 | **7.4** (verified) | 5.10 |
| Report identification / end marker | 7.8.2.1(d) | 7.4.1.6 (includes patient ID + dates on each page — see clinical overlay) | 5.10.2.3 (stricter: unique ID at beginning and on each page) |
| Customer-supplied data | 7.8.2.2 | resolve via Annex B | verify current Qualtrax text |
| Sampling on the report | 7.8.3.2 → 7.8.5 | resolve via Annex B | verify current Qualtrax text |
| Measurement uncertainty | 7.8.3.1(c) test / 7.8.4.1(a) calibration | not a 17025-style MU block; clinical decision limits live in 7.4 | verify current Qualtrax text |
| Statements of conformity | 7.8.6 | resolve via Annex B | verify current Qualtrax text |
| Opinions / interpretations | 7.8.7 | 7.4 interpretation / authorized release | verify current Qualtrax text |
| Amendments / re-issue of reports | 7.8.8 | 7.4 revised-report rules | verify current Qualtrax text |
| Issued reports retained as technical records | 7.8.1.2 | 7.4.1.1 / 8.4 | 4.10 |
| LIMS validation before introduction / after change | 7.11.2 | 7.6 / 8.x (verify Annex B) | verify current Qualtrax text |
| System failures recorded | 7.11.3(e) | resolve via Annex B | verify current Qualtrax text |
| External / off-site provider does not absorb the obligation | 7.11.4 | resolve via Annex B | 4.4.2 (name the receiving lab) |
| Calculations and data transfers checked | 7.11.6 | resolve via Annex B | verify current Qualtrax text |
| Control of records (ID, storage, protection, back-up, archive, retrieval, retention, disposal) | 8.4 (Option A) | 8.4 | 4.10 |

Rows marked "resolve via Annex B" or "verify current Qualtrax text" are
**unverified clause numbers** in this file. Do not invent a number. Read
15189 Annex B or the current AAVLD Qualtrax document.

## Records

**R1. One identity per activity; checker only where a check happens.**
The floor is one identity that resolves to a person without consulting
current state. Add the checker field where a review step exists.

**R2. Records are made at the time.** Original observations, data, and
calculations are recorded when they are made. In software: server-side
timestamp at request entry, never from a client payload.

**R3. Complete enough to repeat the activity.** Two limbs, both qualified
by "if possible": identify factors affecting the result and its
uncertainty; enable repetition under conditions close to the original.
The factors-affecting limb justifies snapshotting instrument, method,
environment, and configuration.

**R4. An amendment keeps the original.** Trackable to previous versions
or original observations. Retain both original and amended data, with
date, what changed, and who. When Part 11 is also on, cite §11.10(e)
alongside.

## Items and sampling

**R5. Items are unambiguously identified.** If the item identifier is not
unique in the database, the printed identity is ambiguous. Check for a
uniqueness constraint.

**R6. Deviations are recorded on receipt; the disclaimer is per result.**
Where the customer wants the item tested anyway, the report must indicate
*which results may be affected*. A report-level condition string cannot
express that.

**R7. Specified storage or conditioning conditions are monitored and
recorded.**

**R8. Who collected the sample is a schema-level switch.** When the lab
is responsible for sampling, additional per-sample fields become required
report content. Model sampling responsibility explicitly.

## Reports

**R9. Every report carries a fixed content set** owned by the active
overlay (`iso-17025-reporting.md`, `iso-15189-clinical.md`, or
`domain-veterinary.md`). Do not apply 17025's 16-item list to a medical
or AAVLD-only deployment from this file.

**R10. Customer-supplied data is marked as such**, with a disclaimer when
that data can affect validity. Where the lab did not sample, state that
results apply to the item as received.

**R11. Measurement uncertainty has named triggers** on 17025 test
reports and is unconditional on 17025 calibration certificates. 15189
uses biological reference intervals / clinical decision limits instead.
Do not copy 17025 MU rules onto a medical report.

**R12. A pass/fail field is a statement of conformity.** Once present:
scope, specification, and decision rule. Companion guidance:
ILAC-G8:09/2019 (cite by number).

**R13. An interpretation is not another result column.** Authorized
person, documented basis, clearly identified as interpretation. A verbal
interpretation is itself a record.

**R14. A replacement report names the specific document it replaces.**
Gate this: if every generation allocates a fresh unique number, the
replacement clause never engages.

## The information system

**R15. Validate before introduction, and after every change** — including
configuration and modifications to commercial software. When `iso_17025`
is on, also load `iso-17025-systems.md` for 6.4 and the full 7.11 list.

**R16. A system failure is a recordable event** (render raise, failed
upload, hash mismatch). A log line is not a record.

**R17. An external provider does not absorb the obligation.** Cloud
hosting does not transfer it.

**R18. Calculations and data transfers are checked systematically.**
Parity tests and verification tooling cite this obligation.

## Retention

**R19. Retention is a per-family class with its own anchor and a stored
floor.** Controls cover identification, storage, protection, back-up,
archive, retrieval, retention time, and disposal. Records stay readily
available; access matches confidentiality commitments.

Do not hardcode a year here. Do not use another domain's floors as
examples. Overlay files name floors that actually bind. A
`created_at + TTL` policy cannot express method-lifecycle, rolling
last-entry, or in-use anchors. Option B management systems satisfy
record control through an ISO 9001-conformant system instead.

## What is not agnostic

1. **Report-content clause numbers** — 17025 7.8 vs 15189 7.4 vs AAVLD 5.10.
2. **Per-page identification** — 17025: end marker is required, "Page X of Y"
   is practice. AAVLD 5.10.2.3 requires the unique identifier at the
   beginning and on each page. 15189 7.4.1.6 requires patient ID and
   dates on each page (unless documented reasons to omit).
3. **Omission hatches** — 17025 7.8.2.1 allows documented valid reasons.
   Some sector rules remove that hatch (see the overlay that owns the
   sector). The serializer needs a fail-closed mode when the hatch is gone.
4. **Measurement uncertainty vs clinical decision limits.**
5. **Scope posture** — some bodies accredit test-by-test (flag assays
   outside scope on reports that claim accreditation). AAVLD accredits
   the laboratory as a whole (that flag is inert). Make it config-driven.

## Sources

- [ISO/IEC 17025:2017](https://www.iso.org/standard/66912.html), edition 3,
  confirmed 2023.
- [ISO 15189:2022](https://www.iso.org/standard/76677.html), edition 4.
  Report content is clause 7.4. Annex B vs 17025.
- AAVLD, "Requirements for an Accredited Veterinary Medical Diagnostic
  Laboratory", SOP 1137 Version 1 (approved 7 February 2023). Qualtrax at
  aavld.org. Legacy "AC1" is an alias. Re-check Qualtrax before citing.
- ILAC-G8:09/2019. ILAC ceased 31 December 2025; functions passed to the
  Global Accreditation Cooperation 1 January 2026.

## Currency

ISO/IEC 17025:2017 is current. Pages claiming ISO/IEC 17025:2025 are
false. Accreditation to ISO 15189:2012 stopped being recognized under the
ILAC Arrangement after 6 December 2025.
