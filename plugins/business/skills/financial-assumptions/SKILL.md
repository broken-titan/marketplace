---
name: financial-assumptions
description: >-
  Use when building assumption-driven projections, not a spreadsheet
  replacement.
---

# Financial Assumptions

Write founder year-one drivers only; stop if the ask is application code, a writing-voice pass, skill-pack authoring, a living engineering strategy, or laboratory informatics.

## Files

| File | When |
|------|------|
| `references/intake.md` | Offer, stage, and any figures the founder already confirmed |
| `references/evidence.md` | Claims, sources, and `[EVIDENCE NEEDED]` / `[DECISION NEEDED]` marks |
| `references/drivers.md` | Year-one price, volume, COGS, and opex |
| `references/breakeven.md` | Break-even logic and clarifying questions |
| `references/close.md` | Weaknesses, open decisions, and next actions |

## Interface

| Input | Output |
|-------|--------|
| Offer, stage, and any price, volume, cost, or opex the founder or an advisor already confirmed | `docs/<slug>-financial-assumptions.md` |
| Labels, units, and formulas for the year-one drivers | Evidence rows, assumed versus observed marks, and break-even logic |

Ask if the slug is missing; go ahead and use `financial-assumptions` when the founder has one offer.

## Hard rules

- Collect offer, stage, and any confirmed figures from `references/intake.md` before drafting a section.
- Put each material claim on the evidence table in `references/evidence.md` and mark a missing source as `[EVIDENCE NEEDED]` and a missing choice as `[DECISION NEEDED]`.
- Follow `references/drivers.md` for year-one price, volume, COGS, and opex, and label each factor `observed` or `assumed` in the same sentence that uses it.
- Follow `references/breakeven.md` for break-even logic and ask those clarifying questions when an input is missing.
- Write complete sentences and cite a source or a founder confirmation date on every kept number.
- Leave a dollar, unit, or rate blank or marked until a source or a confirmed figure exists.
- Ask for the missing driver; do not invent a ledger, a bank balance, or a month-by-month book to make the page look finished.
- Close with weaknesses, open decisions, and next actions from `references/close.md`.

## Easy mistakes

- Inventing revenue, COGS, opex, or a cash balance to fill a blank.
- Writing a fake month-by-month ledger when only drivers exist.
- Mixing an observed invoice with a working assumption in the same cell without a label.
- Treating this page as a finished spreadsheet the founder can file.
- Drafting code, a voice guide, a skill pack, an engineering strategy, or a lab protocol under this skill.

## Quality standards

- [ ] Intake recorded offer, stage, and any confirmed figures
- [ ] Every material claim has a source, `[EVIDENCE NEEDED]`, or `[DECISION NEEDED]`
- [ ] Year-one price, volume, COGS, and opex follow `references/drivers.md`
- [ ] Each kept figure is marked assumed or observed
- [ ] Break-even logic and missing-input questions follow `references/breakeven.md`
- [ ] Sentences are complete; no invented ledger
- [ ] Closing section lists weaknesses, open decisions, and next actions
- [ ] Output is a founder assumptions page at `docs/<slug>-financial-assumptions.md`
