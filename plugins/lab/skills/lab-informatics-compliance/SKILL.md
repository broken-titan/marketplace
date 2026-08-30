---
name: lab-informatics-compliance
description: >-
  Use when designing, implementing, or reviewing LIMS, LIS, ELN, LES,
  SDMS, or CDS features that create, modify, store, sign, export, or
  report laboratory records, trails, signatures, retention, or
  verification. Load overlays only from a lab-informatics-profile or an
  explicit user flag.
---

Type-agnostic design reference for laboratory informatics records.

Read `docs/lab-informatics-profile.md` (or `.yaml`) first when it exists. Load only the overlay files it lists. If there is no profile, ask for the `lab-informatics-profile` intake or explicit flags.

**MUST** = in force for this deployment (trigger met, or adopted as design standard). **SHOULD** = an auditor will probe it. A cited clause makes a design defensible; it rarely makes a specific field required.

## Tree (load when needed)

- `references/base-rules.md` — rules 1–12, frameworks, design-review gate, currency
- `references/base-objects.md` — O1–O20
- `references/limspec-map.md` — E1578 / LIMSpec catalog
- `references/domain-regimes.md` — overlay router
- Overlay files — only when the profile or user turns that flag on (table below)

Same-plugin: `lab-system-csv` when `system_csv` is on; `lab-part-11-review` when `part_11` is on or flagged.

## Interface

| Input | Output |
|-------|--------|
| Profile flags or explicit user flags | Design that satisfies loaded overlays |
| Feature touching records / trails / signatures | Review against base-rules + O1–O20 |

Primary identifier comes from the profile. Never default it to patient.

## Load map

| File | Load when |
|---|---|
| `references/domain-regimes.md` | Always, to route |
| `references/base-rules.md` | Always with this skill |
| `references/base-objects.md` | Always with this skill |
| `references/limspec-map.md` | Always (MUST vs context) |
| `references/iso-lab-agnostic.md` | 17025, 15189, AAVLD, or family unknown |
| `references/iso-17025-reporting.md` | 17025 report/serializer (7.8) |
| `references/iso-17025-systems.md` | 17025 LIMS/equipment (6.4, 7.11) |
| `references/iso-15189-clinical.md` | 15189 and/or CLIA |
| `references/domain-clinical.md` | Human-care |
| `references/domain-blood-bank.md` | Blood / transfusion |
| `references/domain-gxp.md` | Part 11, Annex 11, PIC/S, GAMP, 211, 58/GLP, GCLP, QMSR |
| `references/gamp-lab-systems.md` | Any GxP flag, or `gamp_lab` |
| `references/usp-1058.md` | GxP / `pharma_qc` / `glp`, or `usp_1058` |
| `references/fda-oos.md` | `pharma_qc` or GMP activity |
| `references/domain-food.md` | Food/feed; LAAF; FSIS ALP |
| `references/domain-veterinary.md` | Animal / AAVLD / NAHLN |
| `references/poultry-veterinary.md` | NPIP or official poultry assays |
| `references/domain-environmental.md` | Environmental; TNI/NELAP; `epa_sedd` |
| `references/domain-forensic.md` | Forensic; ANAB AR 3125; FBI QAS; `cjis` |
| `references/domain-biobank.md` | ISO 20387 |
| `references/domain-hctp.md` | 21 CFR 1271 |
| `references/domain-ivdr.md` | IVDR Art. 5(5) |
| `references/domain-wada.md` | WADA ISL |
| `references/domain-cannabis-hemp.md` | Cannabis or hemp |

Poultry is not the food default. Silence leaves Part 11, CLIA, 15189, 17025, and the rest off.

## Gotchas

- Enabling an overlay from a product name (or from "we are a lab") invents a regime.
- A blank reviewer column implies a control the workflow does not have.
- In-row hashes next to writable data do not cross a trust boundary.
- HIPAA's six-year clock is compliance documentation, not lab-report retention.
- ISO/IEC 17025:2017 is current; a "2025 edition" is false.

## Quality bar

- [ ] Profile or explicit flags named
- [ ] Only listed overlays loaded
- [ ] Design-review gate in `base-rules.md` answered
- [ ] O1–O20 present in the design or explicitly N/A
