# Profile write targets

Write only after the user confirms the preview. Replace these targets; do not invent others.

## `docs/lab-informatics-profile.md`

Human- and agent-readable. Sections, in order:

1. Title and date
2. Enabled overlays (flag, posture, one-line trigger)
3. Open questions (flags left off after a re-ask, or 606-without-CLIA when that note applies). Omit the section if none.
4. Identifier model
5. Report-content overlay (which reference file, or none)
6. Signature posture (Part 11 on/off; LAAF carve-out if applicable)
7. Retention classes (name, anchor, floor or "none recorded")
8. Design-review gate — the questions from `lab-informatics-compliance` (including named objects O1–O20), with overlay names filled in
9. **Load these files** — bullet list of reference paths under `lab-informatics-compliance`
10. **Sibling skills** — `lab-system-csv` and/or `lab-part-11-review` only when their flags are on; omit the section when both are off

## `docs/lab-informatics-profile.yaml` (same flags)

```yaml
version: 1
updated: <ISO date>
results_for: []      # from Q1
authorities: []      # us | eu_uk | other
overlays:            # flag: legally_required | design_standard
  iso_17025: design_standard
identifiers:
  primary: <kind>
  extra: []
report_content: <iso-17025-reporting | iso-15189-clinical | domain-veterinary | none>
signature:
  part_11: off
  laaf_carve_out: false
retention_classes: []
open_questions: []   # omit or empty if none
system_csv: off      # omit key when off; on only from Q22 A or an explicit flag
part_11_review: off  # omit key when off; on from the Part 11 operational follow-up
load:
  - references/domain-regimes.md
```

Omit overlay keys that are off. Do not list every possible flag as `false`.

`report_content` values: `iso-17025-reporting`, `iso-15189-clinical`, `domain-veterinary`, or `none`.

## Agent-instruction block

Write a bounded `## Lab informatics` section into the consuming repo’s agent-instruction files that already exist or that the user named (`AGENTS.md`, `CLAUDE.md`, or the same pattern). Prefer `AGENTS.md` as the home. Create `AGENTS.md` if missing. If `## Lab informatics` exists, replace **that section only**.

```markdown
## Lab informatics
Profile: docs/lab-informatics-profile.md
Overlays: <comma-separated flags that are on>
Load from lab-informatics-compliance: <short file list>
Skills: <lab-system-csv and/or lab-part-11-review when their flags are on; omit this line when both are off>
Do not enable additional compliance frameworks from silence.
```

Do **not** dump 17025 or any clause list into the instruction file.

If a host-specific instruction file exists **and** has no conflicting lab-compliance block, you may append a single line pointing at `AGENTS.md`. Do not create a host-only file as the only target.

## Preview fields (before write)

- enabled overlay flags
- files to load from `lab-informatics-compliance`
- sibling skills on (`lab-system-csv` when `system_csv`; `lab-part-11-review` when `part_11` or `part_11_review`)
- identifier kinds
- report-content overlay
- signature posture
- open questions (if any)
- retention classes (floors named only when a binding overlay supplied one; otherwise "configurable class, no floor recorded")
- the exact instruction-file block
