# ISO 15189:2022 and CLIA — medical laboratory overlay

Load when `iso_15189` and/or `clia` is on. 15189 is an accreditation
standard. CLIA (42 CFR part 493) is mandatory US federal law for the
trigger below. **15189 does not replace CLIA.** A US care lab needs CLIA
and may additionally seek 15189.

## CLIA trigger and exceptions

**On:** testing of human specimens for diagnosis, prevention, or treatment
of disease or impairment, or assessment of the health of an individual
(42 CFR 493.3(a)).

**Off** (42 CFR 493.3(b)):

1. A facility or component that **only** performs testing for forensic
   purposes.
2. Research laboratories that test human specimens but **do not report
   patient-specific results** for diagnosis, prevention, treatment, or
   health assessment of individual patients.
3. SAMHSA-certified workplace drug testing under SAMHSA rules (other
   testing at that lab remains CLIA).

Silence does not enable CLIA. Forensic-only and non-reporting research
stay off.

ISO 15189:2022 edition 4 replaced 15189:2012 and absorbed ISO 22870:2016
(POCT). Accreditation to 2012 ceased to be recognized under the ILAC
Arrangement after 6 December 2025. Report content is **clause 7.4**, not
17025's 7.8.

## Report content (ISO 15189:2022 7.4)

Clause text paraphrased from 7.4.1.6 checklists aligned to the standard.
Consult the standard for normative wording. Reports include at least the
following **unless the laboratory has documented reasons for omitting**
an item:

- Unique **patient** identification, date of primary-sample collection,
  and date of issue of the report, **on each page**.
- Identification of the issuing laboratory.
- Name or unique identifier of the user (requester).
- Type of primary sample and information needed to describe it (source,
  site, macroscopic description).
- Clear identification of examinations performed and, where relevant, the
  method (harmonized electronic identification of the measurand when
  possible — LOINC / NPU / SNOMED CT are examples in the note).
- Results with units (SI, SI-traceable, or other applicable).
- Biological reference intervals, clinical decision limits, likelihood
  ratios, or supporting nomograms as necessary.
- Identification of examinations that are research/development with no
  measurement-performance claims.
- Person(s) reviewing results and authorizing release (on the report or
  readily available).
- Preliminary results marked as such.
- Critical results indicated.
- Unique identification that all components belong to a complete report,
  and a clear end (page n of m is an example in the standard's "e.g.").

Revised reports are identified as revisions and reference the original
(date and patient identity). Unverified: exact 7.4 revised-report
subclause letter — confirm in the standard before citing a letter.

**Schema consequences vs 17025:** patient ID is first-class; per-page
patient/date is the default (documented omission only); reference
intervals / decision limits replace 17025 measurement-uncertainty
triggers; method identification may need a code system, not only an
internal method key.

## ISO 15189:2022 7.6 — information systems (not 7.4)

Distinct from report content. Consult the standard. Publicly cited
subclauses (confirm letters before an audit matrix):

- **7.6.3** authorities over the information system; **interface
  verification**; cybersecurity (note pointing at ISO/IEC 27001)
- **7.6.4** downtime / contingency so examinations continue and
  records remain attributable
- Off-site / externally managed systems — the laboratory keeps the
  obligation (same idea as 17025 7.11.4)

These are software (`base-objects.md` O5, O14, O17). 7.4 does **not**
cover them.

## CLIA test report — 42 CFR 493.1291 (own list)

Do **not** pretend 15189 7.4 covers this. When `clia` is on, the
report / LIS delivery path must implement
[493.1291](https://www.ecfr.gov/current/title-42/section-493.1291):

- **(a)** accurate, reliable send from point of data entry (interface
  or manual) to final destination, including calculated results,
  network/interfaced systems, and referral / POCT / satellite
- **(c)** patient name+ID or unique identifier+ID; **name and address
  of the performing laboratory location**; report date; test; specimen
  source when appropriate; result + units/interpretation; disposition
  of unacceptable specimens
- **(d)** reference intervals / normal values **available** to the
  authorized person (not necessarily printed on every page)
- **(f)** release **only** to authorized persons (and, if applicable,
  persons responsible for using the results and the referring lab),
  except patient-access **(l)**
- **(g)–(h)** critical-result alert; delayed-result notification
- **(i)** referral: do not revise the testing lab’s interpretation;
  retain an exact duplicate; notify the orderer of each performing
  location
- **(k)** corrected reports: notify, issue promptly, keep original
  and corrected

## Pre- and post-examination

15189 treats the path as pre-examination, examination, post-examination.
Software that only models "result rows" misses:

- **Request / agreement** — unequivocal traceability of patient to
  request and sample; requester identity and contact; examinations
  requested; oral-request procedure.
- **Primary-sample collection and transport** — collection date/time,
  collector, container/additive, integrity on receipt.
- **Critical-result notification** — who was notified, when, escalation
  when the responsible person cannot be reached. Unverified: exact
  subclause number for notification — treat the obligation as in 7.4
  and confirm the number before an audit matrix.
- **Delayed results** — procedure to notify users based on patient
  impact (7.4.1.1).

## POCT

ISO 22870:2016 was absorbed into 15189:2022. POCT remains in 15189
scope when the medical laboratory is responsible for it. Design
consequences: the same record, trail, and authorized-release rules
apply to devices outside the central lab; operator identity and device
identity are snapshotted; connectivity failures are system-failure
events (see base skill rule 2 / R16). Do not invent a separate "POCT
lite" compliance path.

## CLIA design notes (US law overlay)

CLIA is not an accreditation checklist you implement instead of 15189.
For software:

- Personnel files stay organizational. PT **conduct** and QC
  **release gates** are software — see `domain-clinical.md` and
  `base-objects.md` O8. The system must **retrieve** who performed
  and who reviewed a patient-specific result, and retain records for
  the applicable CLIA / state / payer floor — not HIPAA's six-year
  documentation clock.
- Patient-specific reported results are the CLIA object. Research
  exports that never become care results stay off this overlay.
- CAP, Joint Commission, or state exemption programs sit **alongside**
  CLIA; they do not turn CLIA off unless the lab is CLIA-exempt under
  493.3(a)(2).

Exact CLIA record-retention intervals are spread across 42 CFR 493
subparts and state law. **Unverified as a single number in this
file.** Model a configurable class; store any known floor from the
profile; do not hardcode seven years.

## PHI and GDPR personal data

Load this section only when `hipaa` and/or `gdpr` is on.

- **HIPAA** (45 CFR parts 160/164): minimum necessary, access controls,
  audit logs of access to PHI, breach assessment. 45 CFR 164.530(j)
  retains **policies, procedures, and required documentation** for six
  years from creation or last effective date — **not** lab reports.
  Clinical-record retention is state law, CMS Conditions of
  Participation, or payer contract.
- **GDPR / UK GDPR**: lawful basis, purpose limitation, data-subject
  rights, storage limitation. Retention still comes from the lab
  overlay + contract, not from a GDPR-wide year.

Do not enable either flag from silence.

## Sources

- [ISO 15189:2022](https://www.iso.org/standard/76677.html)
- [42 CFR 493.3](https://www.ecfr.gov/current/title-42/section-493.3)
- [42 CFR 493.1291](https://www.ecfr.gov/current/title-42/section-493.1291)
- [45 CFR 164.530(j)](https://www.ecfr.gov/current/title-45/section-164.530)
- CLIA RFI 91 FR 43586 (16 Jul 2026) — no requirement change
