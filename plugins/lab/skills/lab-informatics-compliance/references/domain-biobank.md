# Biobank overlay (ISO 20387:2018)

Load when `iso_20387` or `biobank` is on. Identifier kinds: material,
collection, aliquot.

[ISO 20387:2018](https://www.iso.org/standard/67888.html),
*Biotechnology — Biobanking — General requirements for biobanking*,
covers competence, impartiality, and consistent operation of biobanks,
including QC of biological material and associated data. It applies to
biobanking of material from multicellular organisms and microorganisms
for **research and development**.

**Out of scope of 20387:** biological material intended for food/feed
production, laboratories undertaking analysis for food/feed
production, and/or therapeutic use. Do not apply this overlay to a
food lab or a transfusion service just because samples are stored.

ISO catalogue status: 2018-08, marked for revision (stage 90.92) —
confirm whether a successor has published before citing 2018 as
current.

## Design notes (clause families)

- **Traceability** of biological material and associated data across
  acquisition, preparation, storage, and distribution (clause 7.5 in
  the 2018 table of contents).
- **QC of processes and of data** (7.8): planned intervals; retain
  documented information of QC activities and results; identify
  critical data.
- **Control of records** (8.4, Option A) — same idea as 17025 8.4:
  class + floor, not a year in this file.
- Fitness for intended purpose is explicit. Rare or legacy material
  may justify QC exceptions — record the justification.

Unverified: a single 20387 retention year. Do not invent one.

When the same system also issues diagnostic results, stack the
clinical or 17025 overlay independently. 20387 does not replace CLIA
or 17025.

**Therapeutic use / HCT/P** is **not** this file. Load
`domain-hctp.md` when `hctp` is on (21 CFR part 1271). 20387
explicitly excludes material intended for therapeutic use.
