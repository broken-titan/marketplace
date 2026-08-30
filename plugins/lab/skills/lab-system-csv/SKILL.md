---
name: lab-system-csv
description: >-
  Use when GAMP 5 computerized-system validation of the LIMS, LIS, or ELN
  itself is in scope: category, URS, risk, IQ/OQ/PQ, and traceability.
  Needs the profile flag system_csv or an explicit user request.
---

Author the **computerized-system validation (CSV)** package for the informatics system itself (LIMS, LIS, or ELN). This is the GAMP 5 lifecycle of *that* system — category, URS, risk, qualification, traceability.

**Trigger.** Run only when `docs/lab-informatics-profile.md` (or `.yaml`) has `system_csv` on, or the user explicitly asked for this skill / GAMP 5 CSV of the informatics system. A quiet profile leaves this skill idle. Design overlays (`lab-informatics-compliance`, including `gamp-lab-systems.md`) stay the feature-design path; do not treat those overlays as this package.

GAMP is paywalled. Point at it. Do not dump the book. Pointers: `references/gamp.md`.

## Distinct from

| This skill | Elsewhere |
|------------|-----------|
| Category, URS, risk, IQ/OQ/PQ, RTM for the LIMS/LIS/ELN | `lab-informatics-compliance` design tables |
| GAMP 5 lifecycle of the informatics *product* | GAMP GPG laboratory computerized systems (instruments, raw data, interfaces) |

## Process

1. Read the profile. If `system_csv` is off and the user did not flag this skill, stop and say how to turn it on (profile Q22 or an explicit flag).
2. Classify the system (GAMP 5 category). Custom-built informatics software is typically **Category 5**. Record the category and the rationale; do not invent a lower category to skip work.
3. Draft the local package under `docs/csv/<system-slug>/` (or the repo's existing validation path):

   - `urs.md` — user requirements, IDs stable (`URS-n`)
   - `risk.md` — patient/product/data-integrity risk per URS; criticality
   - `iq.md` / `oq.md` / `pq.md` — installation, operational, performance protocols (or the repo's CSA-equivalent names if they already use them)
   - `trace.md` — URS → risk → protocol step → evidence

4. Reuse profile identifier kinds and signature posture. Do not invent CLIA, Part 11, or 15189 from the product name.
5. Leave written SOPs and wet-ink approvals as organizational actions (list them; do not fake signatures).

## Gotchas

- A quiet profile leaves this skill idle. Design overlays are not this package.
- Inventing a lower GAMP category to skip work fails the classification step.
- Silence does not enable CLIA, Part 11, or 15189 from the product name.

## Quality bar

- [ ] Trigger was a profile flag or an explicit ask
- [ ] Category is stated
- [ ] Every URS ID appears on the trace matrix
- [ ] Risk drove protocol depth
- [ ] GAMP is cited as a pointer, not quoted at length
