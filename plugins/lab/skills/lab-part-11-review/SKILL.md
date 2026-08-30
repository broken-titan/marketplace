---
name: lab-part-11-review
description: >-
  Use when 21 CFR 11 / Annex 11 electronic records and signatures need an
  operational procedure, including periodic audit-trail review. Needs
  part_11 on the profile or an explicit user flag.
---

Author the **operational** ER/ES procedure: how the lab reviews electronic records, signatures, and the **audit trail** on a schedule. This is a procedure, not a schema design.

**Trigger.** Run only when the profile has `part_11` on, or the user explicitly asked for this skill / `part_11_review`. A quiet profile (no Part 11, no flag) leaves this skill idle. The design-control table in `lab-informatics-compliance` (`domain-gxp.md`, base objects O9–O11) stays the software-design path.

Pointers: `references/eres.md`. Do not paste 21 CFR 11 or Annex 11.

## Distinct from

| This skill | `lab-informatics-compliance` |
|------------|------------------------------|
| Periodic audit-trail review SOP, reviewers, frequency, exceptions | Schema / sequencing / signature-linking controls |
| Who reviews, what they look at, how findings close | Whether the trail exists and is attributable |

## Process

1. Confirm the trigger. If `part_11` is off and the user did not flag this skill, stop and say how to turn it on (profile Q4 / Part 11 re-ask, or an explicit flag).
2. Read the profile (open vs closed system, LAAF carve-out, identifier kinds).
3. Write `docs/part-11-audit-trail-review.md` (or the repo's existing SOP path) covering:

   - **Scope** — which records and which trail(s)
   - **Frequency** — from documented risk (PIC/S PI 041-1), not a vendor default
   - **Reviewer** — role that is independent of the operator under review when the regime expects that
   - **What is reviewed** — create/modify/delete, signature meaning, breaks, clock, filters used
   - **Outcome** — pass, investigate, CAPA link
   - **Annex 11** — only when `annex_11` is on: same procedure, EU/UK citations beside Part 11

4. Leave identity proofing and two-component signature *execution* with the identity platform. This file is the **review** of what that platform and the LIMS already recorded.

## Gotchas

- A quiet profile (no Part 11, no flag) leaves this skill idle.
- Recopying design-control tables here duplicates `lab-informatics-compliance`.
- "Monthly" as a universal frequency ignores documented risk.

## Quality bar

- [ ] Trigger was `part_11` or an explicit flag
- [ ] Frequency cites risk, not "monthly" as a universal
- [ ] Design-control rows are linked, not recopied
- [ ] LAAF-only records stay out when the profile carved them out
