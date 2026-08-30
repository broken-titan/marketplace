# Router — accreditation family × domain

Load this to decide which overlay files to open. Do not treat any row as
on unless the profile (or the user) turned it on. Silence stays off.

A deployment is a **product** of two axes:

- **Accreditation / program family** — 17025, 15189, AAVLD, TNI/NELAP,
  CAP, AABB, FSIS ALP, LAAF, ISO 20387, none, unknown. Multi-select.
- **Domain** — what results are issued for. Multi-select. Poultry/NPIP
  is a veterinary subsection, never the default food or veterinary
  example.

One installation can stack several of each (a 17025 food lab that also
holds LAAF for a narrow import-alert workflow; a 15189 clinical lab that
also runs CLIA; a forensic unit that is 17025 + ANAB AR 3125 + FBI QAS
for DNA only).

## Trigger table

| Flag | Turns on when the user (or profile) says | Overlay |
|---|---|---|
| `iso_17025` | Seeking or holding 17025, or a customer/regulator requires accredited 17025 results | `iso-lab-agnostic.md`, `iso-17025-reporting.md`, `iso-17025-systems.md` |
| `iso_15189` | Medical laboratory accreditation | `iso-lab-agnostic.md`, `iso-15189-clinical.md` (7.4 reporting **and** 7.6 systems) |
| `clia` | US human specimens reported for diagnosis, prevention, treatment, or health assessment of an individual | `iso-15189-clinical.md` (493.1291 list, distinct from 7.4), `domain-clinical.md` (PT). Exceptions: 42 CFR 493.3(b) |
| `aavld` | AAVLD veterinary diagnostic accreditation | `iso-lab-agnostic.md`, `domain-veterinary.md` |
| `tni_nelap` | TNI / NELAP environmental accreditation | `domain-environmental.md` (+ 17025 files if also `iso_17025`) |
| `cap` | CAP laboratory accreditation (paywalled checklist; treat as adopted program, not a substitute for CLIA) | `domain-clinical.md` |
| `aabb` | AABB (or equivalent) blood/transfusion accreditation | `domain-blood-bank.md` |
| `fsis_alp` | FSIS Accredited Laboratory Program (9 CFR 439) | `domain-food.md` |
| `laaf` | 21 CFR part 1 subpart R in scope | `domain-food.md`. Part 11 does **not** apply to LAAF-only records (§11.1(p)) |
| `iso_20387` | Biobank accreditation / 20387 adopted | `domain-biobank.md` |
| `part_11` | FDA predicate record kept electronically | `domain-gxp.md` |
| `annex_11` | Medicinal-product GMP computerised system (EU/UK) | `domain-gxp.md` |
| `glp` | Nonclinical safety studies for a submission (21 CFR 58 and/or OECD GLP) | `domain-gxp.md` |
| `gclp` | GCLP adopted for clinical-trial sample analysis (not a US statute) | `domain-gxp.md` |
| `qmsr` | Device QC under 21 CFR 820 (ISO 13485 incorporated; in force 2 Feb 2026) | `domain-gxp.md` |
| `hipaa` | PHI as a covered entity or business associate | `iso-15189-clinical.md` (privacy section) |
| `gdpr` | Personal data in EU/UK scope | `iso-15189-clinical.md` (privacy section) |
| `npip` | NPIP-authorized laboratory or official Plan assays | `poultry-veterinary.md` |
| `nahln` | NAHLN / APHIS veterinary network participation | `domain-veterinary.md` |
| `forensic` | Forensic testing (exhibit-centric) | `domain-forensic.md` |
| `cannabis_hemp` | Cannabis or hemp testing | `domain-cannabis-hemp.md` |
| `blood` | Blood or transfusion products | `domain-blood-bank.md` |
| `food_feed` | Food or feed results (not poultry-specific) | `domain-food.md` |
| `environmental` | Environmental matrices (water, soil, air, waste) | `domain-environmental.md` |
| `human_care` | Human specimens for care | `iso-15189-clinical.md`, `domain-clinical.md` |
| `human_research` | Human specimens for research (CLIA off unless patient-specific care results are reported) | `iso-15189-clinical.md` only if 15189/CLIA/HIPAA flags are also on |
| `animal` | Animal / herd diagnostic (not NPIP unless `npip`) | `domain-veterinary.md` |
| `pharma_qc` | Medicinal-product or device QC | `domain-gxp.md` |
| `biobank` | Biobanking (not food/feed production, not therapeutic use — ISO 20387 scope) | `domain-biobank.md` |
| `calibration` | Calibration certificates | `iso-17025-reporting.md` (MU unconditional) |
| `anab_ar3125` | ANAB forensic accreditation | `domain-forensic.md` |
| `fbi_qas` | Forensic DNA for CODIS / QAS | `domain-forensic.md` |
| `open_system` | Records created/modified/maintained/transmitted on a system whose access is not controlled by those responsible for the content (21 CFR 11.30) | `base-objects.md` (O10), `domain-gxp.md` |
| `wada` | WADA-accredited or WADA-approved ABP laboratory | `domain-wada.md` |
| `hctp` | 21 CFR part 1271 HCT/P establishment (therapeutic use; not 20387) | `domain-hctp.md` |
| `ivdr_inhouse` | EU IVDR 2017/746 Art. 5(5) in-house IVD | `domain-ivdr.md` |
| `epa_sedd` | EPA Staged Electronic Data Deliverable in scope | `domain-environmental.md` |
| `cjis` | Criminal justice information / CJIS Security Policy | `domain-forensic.md` |
| `autoverification` | Autoverification of clinical results (CLSI AUTO15) | `domain-clinical.md` |
| `gamp_lab` | GAMP GPG laboratory computerized systems adopted | `gamp-lab-systems.md` |
| `usp_1058` | USP ⟨1058⟩ Analytical Instrument Qualification adopted | `usp-1058.md` |
| `fda_oos` | FDA OOS guidance adopted without other 211/GMP flags | `fda-oos.md` |
| `system_csv` | GAMP 5 CSV of the LIMS/LIS/ELN itself (profile Q22 or explicit flag) | sibling skill `lab-system-csv` — no overlay file |
| `part_11_review` | Periodic audit-trail / ER/ES operational procedure (follow-up or explicit flag) | sibling skill `lab-part-11-review` — no overlay file |

## Stacking examples (generic)

These are illustrations of *how axes combine*. They are not this user's lab.

| Stack | Load |
|---|---|
| 17025 testing lab, no sector program | `iso-lab-agnostic.md`, `iso-17025-reporting.md` |
| US clinical: CLIA + optional 15189 | `iso-15189-clinical.md`, `domain-clinical.md`; 17025 files stay off unless also flagged |
| Food 17025 + FSIS ALP | `iso-lab-agnostic.md`, `iso-17025-reporting.md`, `domain-food.md` |
| Food 17025 + LAAF (narrow trigger) | as above + LAAF hardening in `domain-food.md`; Part 11 off for LAAF-only records |
| Veterinary AAVLD, no NPIP | `iso-lab-agnostic.md`, `domain-veterinary.md` |
| Veterinary + NPIP official assays | above + `poultry-veterinary.md` |
| Forensic 17025 + ANAB AR 3125 | `iso-lab-agnostic.md`, `iso-17025-reporting.md`, `domain-forensic.md` |
| Forensic DNA | above + FBI QAS section in `domain-forensic.md` |
| Blood establishment | `domain-blood-bank.md` (+ CLIA/15189 if the same system issues patient-care results) |
| Device QC lab | `domain-gxp.md` (QMSR) |
| Environmental TNI | `domain-environmental.md` |
| Biobank 20387 | `domain-biobank.md` |
| Cannabis/hemp | `domain-cannabis-hemp.md` (state + 7 CFR 990; no single-state schema) |
| WADA ISL | `domain-wada.md` (off until `wada`; 2021 in force through 2026) |
| HCT/P 1271 | `domain-hctp.md` (not 20387) |
| Environmental + SEDD | `domain-environmental.md` with SEDD payload; TNI does not substitute |
| Forensic + CJIS | `domain-forensic.md` CJIS section; AR 3125/QAS do not cover it |

## Identifier kinds (derived, never defaulted to patient)

| Flags | Extra identifier kinds |
|---|---|
| `human_care` or `clia` | patient, specimen |
| `human_research` | subject / specimen (not a care medical-record number unless they said so) |
| `animal` or `aavld` or `nahln` | animal, herd/flock, premises |
| `npip` | flock, farm, house (see poultry overlay) |
| `food_feed` or `fsis_alp` or `laaf` | lot, batch, commodity, establishment |
| `environmental` or `tni_nelap` | station, matrix, field-sample |
| `forensic` | exhibit, case, item |
| `cannabis_hemp` | lot, batch, license |
| `blood` or `aabb` | donation, unit, donor |
| `pharma_qc` or `qmsr` or `glp` | batch, lot, study |
| `wada` | athlete, sample, aliquot (A/B) |
| `hctp` | donor, HCT/P, consignee |
| `biobank` | material, collection, aliquot |
| `calibration` | instrument, artifact |

If none of the human-care flags are on, **do not** make patient the
primary key.

## Posture

For each enabled overlay record **legally required** vs **adopted as
design standard**. The profile skill writes this. This router does not
guess.
