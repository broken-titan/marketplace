# 21 CFR part 1271 — HCT/P establishments

Load when `hctp` is on. **Separate from ISO 20387.** 20387
excludes biological material intended for **therapeutic use**.
This overlay is the US tissue/cell (HCT/P) establishment path.

https://www.ecfr.gov/current/title-21/part-1271

## Software consequences

- Donor, product / HCT/P, and disposition identities — not
  patient-as-primary-key unless the same system also issues
  care results (`clia`).
- Tracking so a product can be followed from donor to
  consignee and back ([1271.290](https://www.ecfr.gov/current/title-21/section-1271.290)
  — confirm current paragraph text).
- Donor-eligibility determination records
  ([1271.50](https://www.ecfr.gov/current/title-21/section-1271.50) /
  [1271.55](https://www.ecfr.gov/current/title-21/section-1271.55)).
- Establishment records
  ([1271.270](https://www.ecfr.gov/current/title-21/section-1271.270)).

Exact retention floors vary by 1271 paragraph and product type.
Store class + floor from the profile; do not hardcode.

Do not apply this overlay to a research biobank just because
samples are stored. Do not apply 20387 to a 1271 establishment
just because material is banked.
