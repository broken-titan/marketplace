# ISO/IEC 17025:2017 — LIMS / equipment (6.4 and 7.11)

Load when `iso_17025` is on. This is **not** report content.
Clause **7.8** stays in `iso-17025-reporting.md`.

Consult the standard for normative wording.
[ISO catalogue](https://www.iso.org/standard/66912.html) — 2017,
confirmed 2023. There is no 2025 edition.

## 6.4 Equipment

Software, measurement standards, reference materials, reagents,
consumables, and auxiliary apparatus are **equipment**. Do not
model “instruments only.”

Design (see also `base-objects.md` O1, O2, O4):

- Unique identification; calibration / maintenance / investigation
  status on the write path (6.4.7–6.4.9 — confirm letters).
- **6.4.13** equipment records (identity, software version,
  calibration dates, results, maintenance, damage). Do not invent
  extra letters.
- Result binds the equipment ID actually used.

## 6.5 Metrological traceability

The result points at the calibration certificate and the CRM /
standard lot, not only a method name (`base-objects.md` O4).

## 7.11 Control of data and information management

Full list; 7.11 **ends at 7.11.6**:

- **7.11.1** access to data needed for laboratory activities
- **7.11.2** validate LIMS **including interfaces** before
  introduction; authorize, document, and validate changes
  (including configuration and COTS modifications)
- **7.11.3(a)–(e)** protect from unauthorized access; safeguard
  against tampering and loss; operate in a compliant environment;
  maintain integrity; **record system failures and immediate and
  corrective actions**
- **7.11.4** off-site / external provider does not absorb the
  obligation (cite 7.11.4, not 7.11.3)
- **7.11.5** instructions, manuals, reference data available
- **7.11.6** calculations and data transfers checked systematically

Interfaces are named trust-boundary objects with a verification
record (`base-objects.md` O5). Config in the DB is a versioned,
revalidated record (`base-objects.md` O15).

## Sources

- [ISO/IEC 17025:2017](https://www.iso.org/standard/66912.html)
- Companion reporting: `iso-17025-reporting.md`
