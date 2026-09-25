# EU IVDR 2017/746 Article 5(5) — in-house IVD

Load when `ivdr_inhouse` is on. This is **not** QMSR /
manufacturer QC (`qmsr`). It is the health-institution exemption
for devices manufactured and used only within a Union health
institution.

EUR-Lex: Regulation (EU) 2017/746 Art. 5(5).
MDCG 2023-1 (health-institution exemption guidance):
https://health.ec.europa.eu/document/download/05b15d55-1bcf-4e17-99c4-15c706325847_en

## Conditions (paraphrase — read the Regulation)

Annex I general safety and performance requirements still apply.
The rest of the IVDR does not, if **all** of (a)–(i) are met,
including: no transfer to another legal entity; appropriate QMS;
laboratory compliant with **EN ISO 15189** or applicable national
provisions; public declaration; documentation; review of clinical
use. Devices manufactured on an **industrial scale** are outside
the exemption.

**Staged application** (Regulation (EU) 2022/112 and later
amendments): several 5(5) letters applied from 26 May 2024;
Art. 5(5)(d) (no equivalent CE-marked device) is deferred —
**31 December 2030** in the sources checked. Confirm EUR-Lex
before coding a deadline.

## Software consequences

- Each in-house IVD is a **versioned method / device object**
  (aligns with `base-objects.md` O3) with GSPR documentation
  links, public-declaration identity, and clinical-use review
  events.
- Stack `iso_15189` independently when that accreditation is
  actually held or sought. Art. 5(5)(c) names 15189; it does
  not turn the flag on from silence.
- Do not treat this as 21 CFR 820 / QMSR.
