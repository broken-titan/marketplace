# WADA International Standard for Laboratories (ISL)

Load when `wada` is on. **Off until the profile turns it on.**
Silence does not enable WADA.

https://www.wada-ama.org/en/resources/lab-times/international-standard-laboratories-isl

**In force through 2026:** ISL **2021**. A 2027 ISL was approved
5 December 2025 and **comes into force 1 January 2027**. Do not
cite 2027 as current before that date. Do not invent ISL clause
letters here — confirm in the PDF in force for the engagement.

## Software consequences (design, not a clause matrix)

- Athlete / sample / aliquot identity; A/B sample handling as
  distinct items; inherited CoC (`base-objects.md` O16).
- Method and accreditation-scope flags so reports do not carry
  a WADA mark for out-of-scope work (LIMSpec 3.14).
- Original dynamic data and reprocessing history (O6).
- Long-term sample and record retention as **classes + floors
  from the current ISL / TD** — do not hardcode a year.

WADA Technical Documents (TDs) and the International Standard
for the Protection of Privacy and Personal Information (ISPPPI)
are companion texts. ISPPPI is not HIPAA; do not enable `hipaa`
from `wada`.

Not a substitute for 17025. Most WADA labs also hold 17025 —
stack `iso_17025` independently.
