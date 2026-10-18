---
name: lab-informatics-profile
description: >-
  Use when starting a laboratory-informatics repo, designing a LIMS, LIS, or
  ELN, or when compliance overlays are unknown. Closed-question intake that
  writes a durable profile into the consuming repo. Silence does not enable
  Part 11, CLIA, 15189, WADA, SEDD, or CJIS.
---

Closed-question quiz. Inspect first. Ask only judgment questions, bundled. Map answers to overlay flags. Write the profile in the **consuming repo**.

Questions: `references/questions.md`. Mapping: `references/mapping.md`. Write targets: `references/write.md`. Example files in `references/` show output shape only — not this user's lab.

Do not write a sample tenant into the marketplace plugin. Do not name other marketplace plugins.

## Interface

| Input | Output |
|-------|--------|
| Q1–Q10, then required conditionals + Q22 | Overlay flags, posture, identifier kinds |
| User confirmation of the preview | `docs/lab-informatics-profile.md` + `.yaml` + instruction-file block |

Primary identifier comes from the mapping. Never default it to patient.

## Process

1. **Inspect** — existing `docs/lab-informatics-profile.md` or `.yaml`. If present, summarize and ask update or leave. Do not infer CLIA, Part 11, or 15189 from a product name.
2. **Ask** — Q1–Q10 from `questions.md` first. Then only the conditionals those answers require, always including Q22. Exact option labels.
3. **Map** — `mapping.md` with no extra flags. Unknown accreditation stays off.
4. **Preview** — fields in `write.md`. Wait for confirmation.
5. **Write** — `write.md` targets only, idempotent.
6. **Close** — which overlays are on, where files landed, which same-plugin skills the flags turn on.

Same-plugin: later design reads this profile, then loads matching files from `lab-informatics-compliance`. `lab-system-csv` when `system_csv` is on; `lab-part-11-review` when `part_11` is on.

## Easy mistakes

- Enabling an overlay from a product name (or from "we are a lab") invents a regime.
- Writing the profile into the marketplace skill dir loses it on upgrade and bakes a sample tenant.
- A skipped accreditation is `unknown`, not a hidden 17025/15189 enable.
- Poultry/NPIP is not the food or veterinary default.
- Do not dump clause lists into the instruction-file block.

## Quality bar

- [ ] Profile written in the consuming repo, not this plugin
- [ ] Only flags the answers turned on
- [ ] Preview confirmed before write
- [ ] Instruction-file block is bounded
- [ ] Silence left Part 11, CLIA, 15189, 17025, and the rest off
