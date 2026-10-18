# Veterinary diagnostic overlay (AAVLD, NAHLN / APHIS)

Load when `animal`, `aavld`, or `nahln` is on. **NPIP / poultry official
assays are not the default here.** Load `poultry-veterinary.md` only
when `npip` is on.

Identifier kinds: animal, herd/flock, premises. Not patient.

## AAVLD

AAVLD accredits against its own requirements: "Requirements for an
Accredited Veterinary Medical Diagnostic Laboratory," SOP 1137
Version 1 (approved 7 February 2023, carrying 2021-01 clause content).
Legacy document number **AC1** is an alias. Re-check Qualtrax at
aavld.org before citing a clause.

AAVLD numbers clauses on the **ISO/IEC 17025:2005** scheme (4.x / 5.x)
while 17025:2017 uses 7.x / 8.x. Carry both numbers in a traceability
matrix when both families are relevant.

| AAVLD (SOP 1137 v1) | ISO/IEC 17025:2017 | Subject |
|---|---|---|
| 5.10 | 7.8 | Report content |
| 5.10.2.3 | 7.8.2.1(d) | Report identification — AAVLD is stricter |
| 4.10 | 8.4 | Control of records |
| 4.4 (incl. 4.4.2) | 7.1 / 7.8.2.1(p) | Request review; subcontracting |
| 5.4.3 (incl. 5.4.3.2) | 7.2.2 / 8.4 | Method validation and its records |

AAVLD-specific design:

- **Per-page identification is required (5.10.2.3):** unique
  identification at the beginning and on each page, plus a clear end.
  Under 17025:2017, "Page X of Y" is only practice.
- **Retention keyed to the method lifecycle (5.4.3.2):** validation
  data and archived procedure text retained as long as the assay is in
  diagnostic use **and at least seven years after retirement**. Derive
  expiry as `max(assay in use, retirement + 7 years)`. The versioned
  procedure text sits on that clock, not only numeric data.
- **Receiving laboratory named to the client (4.4.2)** for
  subcontracted or referred work. The external-provider field is an
  identity, not a boolean.

AAVLD accredits the **entire laboratory**, unlike test-by-test bodies
(A2LA, ANAB). A per-assay `in_accreditation_scope` flag is needed under
a scoped posture and is inert under AAVLD-only — make it config-driven.

AAVLD accreditation is **not** ISO/IEC 17025 accreditation. AAVLD is
not an ILAC-MRA signatory. Do not put an ILAC-MRA mark on an
AAVLD-only report. Eligibility is restricted (the Committee does not
review commercial laboratories — per AAVLD's own requirements).

## NAHLN / APHIS

The National Animal Health Laboratory Network is an APHIS / state /
university partnership. Participation, approved-assay lists, and
messaging formats are **program documents**, not a single CFR part
this file will invent. When `nahln` is on:

- Treat approved-method identity as config (versioned).
- Outbreak / foreign-animal-disease reporting clocks and recipients
  are per-engagement configuration.
- Do not reuse NPIP 48-hour / 24-hour tables unless `npip` is also on.

Unverified here: a single APHIS CFR section that is "the NAHLN
regulation." Do not cite 9 CFR 71.22 or a proposed NLRAD part from
secondary summaries without re-reading eCFR.

## Sources

- AAVLD SOP 1137 v1 (Qualtrax, aavld.org)
- [ISO/IEC 17025:2017](https://www.iso.org/standard/66912.html)
- USDA-APHIS NAHLN program pages — confirm current participation
  requirements before coding a clock
