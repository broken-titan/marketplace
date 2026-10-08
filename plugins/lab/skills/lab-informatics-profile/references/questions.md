# Intake questions (use this wording)

First bundle: Q1–Q10. Then ask only the conditionals the Q1/Q8 (and
Q2/Q4/Q5) answers require, including Q11–Q21, plus **Q22** (always
in the second bundle) and the Part 11 operational-review follow-up
when `part_11` is on. Letters are the options.
Multi means select all that apply. "None / unknown / other" never
turns a legal overlay on.

## Q1 — What does the software issue results for? (multi)

- A. Human care (diagnosis, treatment, or health assessment of a person)
- B. Human research (specimens; not reported for individual care)
- C. Animal / veterinary diagnostic
- D. Food or feed
- E. Environmental (water, soil, air, waste)
- F. Forensic
- G. Cannabis or hemp
- H. Pharmaceutical or medical-device QC
- I. Biobank / biorepository
- J. Calibration
- K. Other testing (describe in one line; does not enable a named overlay)

## Q2 — Authorities (multi)

- A. United States
- B. EU and/or UK
- C. Other (name the jurisdiction; does not invent a US/EU overlay)

## Q3 — Human specimens reported for diagnosis or treatment?

Ask only if Q1 includes A or B. If Q1 has neither A nor B, skip and
treat as B. If Q8 is Yes, CLIA is not decided by that skipped Q3 — use
the blood follow-up below.

- A. Yes — patient-specific results for care
- B. No
- C. Research only; no patient-specific care results
- D. Forensic only

## Q4 — FDA-predicate records kept electronically?

- A. Yes — a US FDA predicate requires these records, and they are electronic
- B. No
- C. Unknown

If Q5 is Yes, Q2 includes A (US), and this answer is C, do not treat C
as No. Re-ask Q4 once (wording under Follow-ups). Only then accept No.
Unknown after that re-ask stays off and is an open question.

## Q5 — Medicinal-product GMP activity?

- A. Yes — computerised system in GMP for medicinal products
- B. No
- C. Unknown (treat as No)

## Q6 — Nonclinical safety studies for a submission?

- A. Yes — 21 CFR 58 and/or OECD GLP
- B. No
- C. Unknown (treat as No)

## Q7 — Accreditation or program sought or held? (multi)

- A. ISO/IEC 17025
- B. ISO 15189
- C. AAVLD
- D. TNI / NELAP
- E. CAP
- F. AABB
- G. FSIS ALP
- H. LAAF (21 CFR part 1 subpart R)
- I. ISO 20387
- J. None
- K. Unknown (do not enable A–I)

## Q8 — Blood or transfusion products?

- A. Yes
- B. No

## Q9 — PHI or GDPR personal data?

- A. HIPAA PHI (US covered entity or business associate)
- B. GDPR / UK GDPR personal data
- C. Both
- D. Neither
- E. Unknown (treat as Neither)

## Q10 — Known retention floors?

- A. None known — configurable classes only
- B. User lists named floors (class, anchor, duration, source). Record
  only what they list. Do not add HIPAA six years as a lab-report floor.

## Q11 — Poultry / NPIP official assays? (ask only if Q1 includes C or D)

- A. NPIP-authorized lab or official Plan assays
- B. No / not applicable

## Q12 — Forensic DNA / CODIS / FBI QAS? (ask only if Q1 includes F)

- A. Yes — FBI QAS applies
- B. ANAB AR 3125 (forensic 17025 supplement) without QAS
- C. Forensic testing without those programs
- D. Not applicable

## Q13 — Clinical-trial / GCLP sample analysis? (ask if Q1 includes A or B)

- A. Yes — GCLP adopted for clinical-trial sample analysis
- B. No
- C. Unknown (leave `gclp` off)

Yes does **not** turn `clia` or `part_11` on.

## Q14 — NAHLN / APHIS network? (ask only if Q1 includes C)

- A. Yes — NAHLN / APHIS veterinary network participation
- B. No

Yes → `nahln`. `domain-veterinary.md` already loads from `animal`.

## Q15 — Open or closed system? (ask if Q4 is A, or Part 11 re-ask is A)

Closed = access controlled by those responsible for the content.
Open = records leave that control (21 CFR 11.30).

- A. Closed
- B. Open → `open_system`
- C. Unknown (leave `open_system` off)

Does **not** turn `part_11` on by itself.

## Q16 — HCT/P establishment? (ask if Q1 includes A or I)

21 CFR part 1271 tissue/cell products for therapeutic use. Not ISO 20387.

- A. Yes → `hctp`
- B. No
- C. Unknown (leave `hctp` off)

## Q17 — In-house IVD under IVDR Art. 5(5)? (ask if Q1 includes A or B and Q2 includes B)

- A. Yes — health-institution in-house IVD → `ivdr_inhouse`
- B. No
- C. Unknown (leave `ivdr_inhouse` off)

Does **not** turn `qmsr` or `iso_15189` on.

## Q18 — WADA / anti-doping laboratory? (ask if Q1 includes A, B, or F)

- A. Yes — WADA-accredited or WADA-approved ABP lab → `wada`
- B. No
- C. Unknown (leave `wada` off)

Does **not** turn `clia`, `part_11`, or `iso_17025` on.

## Q19 — EPA SEDD deliverables? (ask if Q1 includes E)

- A. Yes → `epa_sedd`
- B. No
- C. Unknown (leave `epa_sedd` off)

TNI / NELAP does **not** turn this on.

## Q20 — CJIS / criminal justice information? (ask if Q1 includes F)

- A. Yes — system handles CJI / CHRI under the CJIS Security Policy → `cjis`
- B. No
- C. Unknown (leave `cjis` off)

AR 3125 / QAS does **not** turn this on.

## Q21 — Autoverification? (ask if Q1 includes A)

- A. Yes — autoverification of clinical results (CLSI AUTO15) → `autoverification`
- B. No
- C. Unknown (leave `autoverification` off)

## Follow-ups (after Q1–Q10, only if the trigger hits)

### Blood / CLIA (ask if Q8 is A and Q2 includes A and Q3 was not A)

Including when Q3 was skipped and treated as B.

Is immunohematology / compatibility testing reported for patient care?

- A. Yes → `clia`
- B. No → `clia` stays off. Note in the profile that blood-product CGMP
  (21 CFR 606) is on without CLIA only if that is actually true.

### Part 11 re-ask (ask once if Q5 is A and Q2 includes A and Q4 was C)

Typical predicates: 21 CFR 211.194 (laboratory records) and 21 CFR 58
(GLP). Are FDA-predicate records kept electronically?

- A. Yes → `part_11`
- B. No → `part_11` off
- C. Unknown → `part_11` stays off; write as an open question, not a
  hidden No

## Q22 — GAMP 5 CSV of this informatics system? (always, second bundle)

Computerized-system validation of the LIMS, LIS, or ELN **itself**
(category, URS, risk, IQ/OQ/PQ, traceability). Distinct from design
overlays and from the GAMP laboratory GPG (instruments / interfaces).

- A. Yes → `system_csv`
- B. No → `system_csv` stays off
- C. Unknown → `system_csv` stays off

### Part 11 operational review (ask if `part_11` is on)

Periodic audit-trail review and ER/ES as an **operational procedure**.
Distinct from the design-control table in compliance overlays.

- A. Yes → `part_11_review`
- B. No → `part_11_review` stays off
- C. Unknown → `part_11_review` stays off
