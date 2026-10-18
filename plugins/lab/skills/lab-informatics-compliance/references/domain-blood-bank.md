# Blood and transfusion (21 CFR 606 + AABB)

Load when `blood` or `aabb` is on. Identifier kind: **donation / unit /
donor**, not patient-as-primary-key (a recipient may still appear on
compatibility records).

## 21 CFR 606.160 — records

Records are maintained **concurrently** with each significant step in
collection, processing, compatibility testing, storage, and
distribution so every step can be traced. Records are legible and
indelible; they identify the person performing the work, include dates,
show test results **and the interpretation**, show the expiration date
assigned, and are detailed enough for a complete history
([21 CFR 606.160(a)](https://www.ecfr.gov/current/title-21/section-606.160)).

A donor number relates the unit to that donor, the donor's medical
record, components, and all disposition records (606.160(c)).

**Retention floor (606.160(d)):** individual product records no less
than **10 years** after processing records are completed **or 6 months
after the latest expiration date**, whichever is later. No expiration
date → retain indefinitely. This is a floor for the profile, not a
hardcoded TTL in application code.

Deferred-donor cumulative records under 606.160(e) are a separate
family; FDA has treated reactivity-based deferral logs as cumulative
for operating establishments. Confirm current 606.160(e) text before
modeling "indefinite" as a class.

## AABB

AABB Standards (paywalled; chapter 6 documents/records) often add
record-content and retention rows marked with a records symbol. They
do not override a shorter reading of 606.160. If `aabb` is on, treat
AABB as **adopted program** and store any extra floors from the current
edition in the profile. Do not invent AABB clause numbers here.

## Stacking

A hospital transfusion service that also issues patient-care results
may stack `clia` / `iso_15189`. Compatibility testing on human
specimens for transfusion is care testing — do not apply the
forensic-only CLIA exception.
