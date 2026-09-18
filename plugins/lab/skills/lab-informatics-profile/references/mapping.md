# Answer → overlay flags

Apply only what the answers support. Do not add flags for "unknown"
or "other."

| Condition | Flags on |
|---|---|
| Q1 A | `human_care` |
| Q1 B | `human_research` |
| Q1 C | `animal` |
| Q1 D | `food_feed` |
| Q1 E | `environmental` |
| Q1 F | `forensic` |
| Q1 G | `cannabis_hemp` |
| Q1 H | `pharma_qc` |
| Q1 I | `biobank` |
| Q1 J | `calibration` |
| Q1 K | none (note in profile prose) |
| Q2 A | `authorities: us` (not an overlay file by itself) |
| Q2 B | `authorities: eu_uk` |
| Q3 A **and** Q2 includes A | `clia` |
| Q3 B, C, or D | `clia` stays off (C and D match 42 CFR 493.3(b) exceptions when that is actually the work) |
| Q4 A | `part_11` |
| Q4 B | `part_11` off |
| Q4 C | see Part 11 re-ask below — do **not** treat first-pass Unknown as a hidden No when Q5 A and Q2 includes A |
| Q5 A **and** Q2 includes B | `annex_11` |
| Q5 A | also load `domain-gxp.md` as adopted GMP activity even if Annex 11 is off (US-only GMP still uses PIC/S/GAMP/211 as applicable) — set `gmp_activity` in profile prose; enable `annex_11` only for EU/UK |
| Q6 A | `glp` |
| Q7 A | `iso_17025` |
| Q7 B | `iso_15189` |
| Q7 C | `aavld` |
| Q7 D | `tni_nelap` |
| Q7 E | `cap` |
| Q7 F | `aabb` |
| Q7 G | `fsis_alp` |
| Q7 H | `laaf` |
| Q7 I | `iso_20387` |
| Q7 J or K | none of Q7 A–I |
| Q8 A | `blood` |
| Q9 A or C | `hipaa` |
| Q9 B or C | `gdpr` |
| Q11 A | `npip` |
| Q12 A | `fbi_qas` and `forensic` |
| Q12 B | `anab_ar3125` and `forensic` |
| Q12 C | `forensic` only |
| Q13 A | `gclp` only — not `clia`, not `part_11` |
| Q13 B or C | `gclp` off |
| Q14 A | `nahln` (`domain-veterinary.md` already loads from `animal`) |
| Q14 B | `nahln` off |
| Blood follow-up A | `clia` |
| Blood follow-up B | `clia` stays off; profile note: 606 without CLIA only if that is actually true |
| Part 11 re-ask A | `part_11` |
| Part 11 re-ask B | `part_11` off |
| Part 11 re-ask C | `part_11` off; write as an open question, not a hidden No |
| Q15 B | `open_system` (requires Part 11 path; does not enable `part_11`) |
| Q15 A or C | `open_system` off |
| Q16 A | `hctp` |
| Q16 B or C | `hctp` off |
| Q17 A | `ivdr_inhouse` — not `qmsr`, not `iso_15189` |
| Q17 B or C | `ivdr_inhouse` off |
| Q18 A | `wada` — not `clia`, not `part_11` |
| Q18 B or C | `wada` off |
| Q19 A | `epa_sedd` |
| Q19 B or C | `epa_sedd` off |
| Q20 A | `cjis` |
| Q20 B or C | `cjis` off |
| Q21 A | `autoverification` |
| Q21 B or C | `autoverification` off |
| Q22 A | `system_csv` — enables `lab-system-csv`; no compliance overlay file |
| Q22 B or C | `system_csv` stays off |
| Part 11 operational review A | `part_11_review` — enables `lab-part-11-review` (requires `part_11` already on) |
| Part 11 operational review B or C | `part_11_review` stays off |

Q7 H (`laaf`) does **not** turn `part_11` on. If Q4 A and Q7 H both
hit, set `signature.laaf_carve_out: true` and note that LAAF-only
records stay outside Part 11 (§11.1(p)); other predicate records stay
in.

Q4 C when Q5 is A **and** Q2 includes A: do **not** default `part_11`
off. Re-ask Q4 once, naming 211.194 / 58 as typical predicates. Only
then accept No. Unknown after that re-ask stays off and is an open
question in the profile. Q4 C in any other case: `part_11` stays off
(silence; not written as a decided No).

Q8 A **and** Q2 includes A: do not silently leave `clia` off. If Q3
was A, `clia` is already on. If Q3 was not A (including skipped-as-B),
ask the blood follow-up. Yes → `clia`. No → leave off and note that
blood-product CGMP (21 CFR 606) is on without CLIA only if that is
actually true.

Q1 H + Q2 A: mention QMSR (21 CFR 820) in profile prose; set `qmsr`
when the user confirms device QC (if they only said "pharma QC", do
not enable `qmsr` without asking one follow-up: drug 211 vs device
820). Q1 H does not by itself enable `annex_11` or `part_11`; those
still need Q5 / Q4.

## Identifier derivation

Use the table in `lab-informatics-compliance` `references/domain-regimes.md`.
If `human_care` and `clia` are off, primary is **not** patient.

Suggested primary when several apply: the object the software issues
as its main result row (ask one follow-up if two primaries are
plausible). Extra kinds are the rest.

## Load list (always start with the router)

Always: `references/domain-regimes.md`, `references/base-objects.md`,
`references/limspec-map.md`

Then union of files from the router table for every flag that is on.
If only `iso_17025` / `calibration` is on, add `iso-lab-agnostic.md`,
`iso-17025-reporting.md`, and `iso-17025-systems.md`.
Any GxP flag also loads `gamp-lab-systems.md` and `usp-1058.md`
(adopted unless the user said they are out of scope). `pharma_qc`
or Q5 A also loads `fda-oos.md`.

`system_csv` and `part_11_review` do **not** add overlay files.
They turn on sibling skills (`lab-system-csv`, `lab-part-11-review`).
An explicit user flag on those skills also turns them on. Silence
leaves both off. `lab-part-11-review` also runs when `part_11` is
on and the user invokes that skill directly.

Report-content field:

- `iso-15189-clinical` if `iso_15189` or `clia`
- else `iso-17025-reporting` if `iso_17025` or `calibration`
- else `domain-veterinary` if `aavld`
- else `none`
