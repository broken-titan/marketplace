# Clinical domain extras (anatomic pathology, public-health diagnostic)

Load when `human_care` is on, in addition to `iso-15189-clinical.md` when
15189 or CLIA is on. This file does not turn CLIA or 15189 on.

## Anatomic pathology

AP reports are still medical-examination reports. Extra identifier and
content kinds that chemistry/hematology schemas often omit:

- Accession / case, specimen part, block, slide — a uniqueness
  constraint at each level.
- Gross description and diagnosis text as controlled, versioned
  artifacts (amendments keep the original; see base skill rule 2).
- Intraoperative / frozen-section results marked preliminary; final
  diagnosis is a later authorized release.
- Synoptic / structured data (e.g. CAP cancer protocols) when the lab
  uses them — treat as adopted templates, not a universal statute.

Unverified: a single federal clause that lists AP field names. Do not
invent one. State and CAP checklists (paywalled) may add floors; record
them in the profile if known.

## Public-health diagnostic

Public-health diagnostic testing of human specimens for care or
notifiable-disease reporting still hits the CLIA trigger when
patient-specific results go to a clinician or to a public-health
authority as care results.

Surveillance-only testing that never reports patient-specific care
results may fall under the 42 CFR 493.3(b)(2) research-style exception
— **only if that is actually true**. Do not assume "public health"
means CLIA-off.

Reportable-condition messaging (HL7 / ELR) is a connector, not a
substitute for the canonical record. Dual-home still applies.

Notifiable-disease lists and clocks are **jurisdiction config**, not
constants in this skill.

## CLIA proficiency testing (42 CFR 493.801 / 493.1236)

When `clia` is on. PT is a **distinct sample/test type**
(`base-objects.md` O8), not a flag on a patient row.

[493.801](https://www.ecfr.gov/current/title-42/section-493.801):

- Test PT like patient specimens, same workload, routine methods,
  same number of times
- Analyst **and** director **attest** routine integration
- Document handling/preparation/testing/reporting; keep PT records
  including the signed attestation **at least 2 years** from the
  event
- **No referral** of PT samples (or portions) for an analysis the
  lab is certified to perform; a receiving lab must notify CMS
- **No inter-laboratory or cross-site discussion** of PT results
  before the program close date
- Send-out / reflex that would happen for a patient: the system
  must know **this is PT** so the interface does not silently
  refer a PT item as a patient send-out

[493.1236](https://www.ecfr.gov/current/title-42/section-493.1236):
evaluate PT performance; document evaluation and twice-yearly
accuracy verification for tests not in subpart I / without compatible
PT samples.

## CDC PHIN / HL7 / USCDI

When `human_care` is on: ELR / PHIN / HL7 / [USCDI](https://www.healthit.gov/isp/united-states-core-data-interoperability-uscdi)
are **connectors**, not the canonical record. Dual-home still
applies. Do not invent a USCDI version as a floor; store the version
the profile names.

## CLSI AUTO15 autoverification

When `autoverification` is on. [CLSI AUTO15](https://clsi.org/)
(paywalled). Software: validate the ruleset; **rapid shutdown**
(manual or automatic) when the LIS is degraded or rules change;
revalidate after change (LIMSpec 4.7). Downtime mode:
`base-objects.md` O14. Silence does not enable this flag.

## CAP / NYS CLEP

Extra accreditors. They do **not** invent a new record type. CAP
is the `cap` flag. NYS CLEP is context only unless the profile
names a floor — do not invent CLEP clause numbers.

## Sources

- [42 CFR 493.801](https://www.ecfr.gov/current/title-42/section-493.801)
- [42 CFR 493.1236](https://www.ecfr.gov/current/title-42/section-493.1236)
- [USCDI](https://www.healthit.gov/isp/united-states-core-data-interoperability-uscdi)
- CLSI AUTO15 (clsi.org; paywalled)
