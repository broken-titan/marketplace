# LIMSpec 2022 R2 map (chapters 1–36)

Source (CC BY-SA): https://www.limswiki.org/index.php/LII:LIMSpec_2022_R2

LIMSpec is the functional-requirements catalog built on
[ASTM E1578-18R26](https://store.astm.org/e1578-18r26.html)
(*Standard Guide for Laboratory Informatics*, reapproved 2026).
E1578 is paywalled. This file is how the skill keeps the **full**
spec in view without treating scheduling, lean, AI, or EHR modules
as lab-record obligations.

**Labels**

- **software MUST** — design so the requirement is met (base
  `base-objects.md` or an overlay that is on)
- **software SHOULD** — strong expectation; build when the workflow
  exists
- **not a software requirement (context only)** — why labs care;
  not required for this skill’s software design **unless** a named
  overlay below is on

Introduction / methodology and “putting LIMSpec to use” are
**context only** (how to write a spec, not a record rule).

| Ch | Title | Label | Notes |
|---|---|---|---|
| 1 | Sample and experiment registration | software MUST | Unique ID (1.13), receipt (1.14), CoC (1.18 → O16). 1.3 NPI/ORI and 1.7 safety cards are SHOULD / product. |
| 2 | Sample management | mixed | **2.11 QC/PT types are MUST (O8).** 2.1–2.6 reagent CoC/location overlap O2. 2.12 project/study UI is SHOULD unless GLP/`glp` is on. |
| 3 | Core laboratory testing | software MUST | Lot gates (3.1–3.3 → O2). Complete test data (3.13 → O6). 3.6 spreadsheet entry is SHOULD. |
| 4 | Results review and verification | software MUST | Spec checks, trail, review levels. 4.2/4.7 autoverification is MUST only when `autoverification` is on; otherwise context. |
| 5 | Approval and disposition | software MUST | Final disposition of the **physical** sample (O19) is distinct from record retention. Statuses (approved/rejected/cancelled) MUST. |
| 6 | Reporting | software MUST | Issued report is a technical record. Content lists live in report overlays (17025 7.8 / 15189 7.4 / CLIA 493.1291 / AAVLD 5.10). 6.8 custom report catalogue is SHOULD / product. |
| 7 | Document and records management | mixed | Method as versioned object (7.3–7.6 → O3) and competency link (7.7 → O13) are MUST. Employee medical records in the LIMS (7.2) are **not a software requirement** (organizational / HR). |
| 8 | Resource management | mixed | **8.8 competency gate is MUST (O13).** 8.1 demographics/medical/occupational-exposure files are **not a software requirement**. 8.3–8.7 training LMS features are organizational / SHOULD. |
| 9 | Compliance management | software MUST | Trail, reason-for-change, e-sign manifestation — base rules 2 and 5; O9–O11 when Part 11 is on. |
| 10 | Instrument and equipment management | software MUST | Unique ID, lock-out, calibration records (O1, O4). 10.2 reservation / capacity is SHOULD (see ch. 28). |
| 11 | Batch and lot management | software SHOULD | MUST when `pharma_qc` / 211 / food batch release is on. Otherwise efficiency. |
| 12 | Scheduled event management | mixed | Scheduler that **creates QC/calibration samples** is SHOULD. Due-date lock-out of instruments is MUST (O1). Capacity UI is ch. 28 (not software). |
| 13 | Instrument data capture and control | software MUST | Dynamic data + metadata (O6). Bidirectional robotics APIs are SHOULD. |
| 14 | Standard and reagent management | software MUST | Lot / expiry / approval (O2). Reorder lists are ch. 15 extras (not software). |
| 15 | Inventory management | mixed | Tracking **test materials that gate results** is MUST (O2). Reorder / PO / vendor master / pretty-print labels are **not a software requirement** (efficiency / product). |
| 16 | Investigation and quality management | software MUST | OOS/OOT incident (O7). 16.1–16.2 IND/device case-history and 16.9 animal-welfare IACUC fields are **not a software requirement** unless that study overlay is on. |
| 17 | Production / MES | **not a software requirement (context only)** | Yield, device master/history, batch production records, recall of **manufactured product**. Labs care when they sit inside a plant. Not a LIMS/LIS lab-record obligation unless a manufacturing system is in scope (out of this skill). |
| 18 | Statistical trending and control charts | **not a software requirement (context only)** except QC release-gate | Pretty charts are efficiency. **Control data required to release a run** is already O8. Do not treat SPC dashboards as a record MUST. |
| 19 | Agriculture and food data | mixed | Lot/site identity when `food_feed` is on is MUST. **19.5 HACCP-plan authoring UI** is **not a software requirement**; food overlay owns data shape for results, not a HACCP editor. 19.1 ORA DX and 19.7 audit-activity tagging are SHOULD when that program is on. |
| 20 | Environmental data | mixed | Station/matrix/field-sample when `environmental` is on is MUST. **EPA SEDD (20.3)** is MUST only when `epa_sedd` is on. TNI does not substitute. ISO 19115 metadata and ERT spreadsheets are SHOULD / context. |
| 21 | Forensic case and data | mixed | Exhibit/case/item + inherited CoC when `forensic` is on is MUST. **CJIS/CJI (21.7–21.17)** is MUST only when `cjis` is on. AR 3125/QAS do not cover CJIS. Examiner-testimony evaluation (21.20) is organizational. |
| 22 | Clinical and public health data | mixed | Patient/specimen when `human_care`/`clia` is on is MUST. **CDC PHIN / HL7 / USCDI (22.1, 22.4–22.5)** are SHOULD connectors when `human_care` is on; they do not replace the canonical record. 22.6 information-blocking is legal context, not a schema. |
| 23 | Veterinary data | mixed | Animal/herd/premises when `animal` is on is MUST. NAHLN HL7 (23.3) is SHOULD when `nahln` is on. VeNom/SNOMED-vet (23.1) is SHOULD. Poultry/NPIP is **not** this chapter’s default — `npip` overlay only. |
| 24 | Scientific data management | software MUST | Raw file + metadata, checksum across trust boundary, no silent delete, ALCOA as lens (O6, base rules 1–2, 9). |
| 25 | Health information technology / certified EHR | **not a software requirement (context only)** | 45 CFR 170.315 CPOE, med lists, e-prescribing, patient portal. Labs care when they sit behind an EHR. Not a LIMS/LIS lab-record obligation. |
| 26 | Instrument data systems functions | software SHOULD | API to CDS/SDMS, order-down / result-up. Becomes MUST for the named interface object (O5) once that instrument class is in scope. |
| 27 | Systems integration | mixed | Named-payload interfaces (SEDD, PHIN, NAHLN) are MUST when that flag is on. Archive/retrieve/backup true copy (27.3–27.4, 27.11 → O18) is MUST. **Generic ERP connectors (27.17–27.18)** are **not a software requirement**. Third-party reporting tools (27.6) are product. |
| 28 | Laboratory scheduling and capacity | **not a software requirement (context only)** | Throughput gauges, staff/instrument calendars, cytology slide-hour caps. Efficiency / org planning. 28.4 CLIA cytology workload is organizational unless the lab asks for a counter. |
| 29 | Lean laboratory / continuous improvement | **not a software requirement (context only)** | Workload leveling, value-stream maps. Efficiency. |
| 30 | Artificial intelligence and smart systems | **not a software requirement (context only)** | Voice agents, ontology ML, AI-optimized parameters. Draft EU Annex 22 is not in force. If AI later touches a regulated result, treat it as a validated interface (O5) — do not enable from this chapter. Facility/instrument **monitoring logs** (30.8–30.11) that feed O1/O14 are SHOULD, not an AI product. |
| 31 | Data integrity | software MUST | ALCOA++ lens, original dynamic data, unique write ID (31.6 → O12), trail off-switch forbidden. Aligns with base rules 1–5, 9 and O6, O11, O12. |
| 32 | Configuration management | mixed | Versioned spec limits / constants / method parameters (O15) are MUST. SSO (32.24), i18n (32.20) are **not a software requirement** (product). Password/MFA policy UI is identity-platform (organizational) except unique write ID (O12). |
| 33 | System validation and commission | mixed | Validate including interfaces (O5, 17025 7.11.2) is MUST as a **gate**. Vendor SDLC evidence, **source-code escrow (33.2)**, and staff-certification packets are **not a software requirement** (organizational / procurement). |
| 34 | System administration | mixed | Role/access that implements O12/O13 is MUST. Mobile clients (34.14), batch HR edits (34.2), vendor help-desk SLAs are **not a software requirement** (product / org). |
| 35 | Cybersecurity | software MUST | Lab-system control independent of HIPAA/GDPR (O17). TLS/encryption/MFA **mechanisms** are in scope; which product implements MFA is identity-platform. |
| 36 | Information privacy | mixed | HIPAA/GDPR overlays when those flags are on. **Erase/anonymize vs regulated keep (O20)** is MUST. 36.1 “comply with HIPAA” as a blanket is the privacy overlay, not a default. |

## Extra accreditors (no new record type)

**CAP** and **NYS CLEP** (and similar state/program checklists) are
extra accreditors. They do **not** invent a new record type. CAP is
already a profile flag (`cap`) that loads `domain-clinical.md`.
NYS CLEP is **not a software requirement** unless the profile names
a floor; do not invent CLEP clause numbers.

## How to use this file

1. Designing a feature: find the chapter, then the label.
2. If MUST — implement via `base-objects.md` and the loaded overlay.
3. If context only — keep the paragraph in design notes; do not
   add columns “because LIMSpec listed it.”
4. Do not enable WADA, SEDD, CJIS, IVDR, HCT/P, or Part 11 from
   a LIMSpec row. Those need the profile flag.
