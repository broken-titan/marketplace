---
name: go-to-market
description: >-
  Use when turning an offer into how customers find and buy it.
---

# Go To Market

Write founder go-to-market pages only; stop if the ask is application code, a writing-voice pass, skill-pack authoring, a living engineering strategy, or laboratory informatics.

## Files

| File | When |
|------|------|
| `references/intake.md` | Offer, buyer, budget, and channels the founder already can use |
| `references/evidence.md` | Claims, sources, and `[EVIDENCE NEEDED]` / `[DECISION NEEDED]` marks |
| `references/motion.md` | Channels, acquisition, conversion, and retention |
| `references/close.md` | Weaknesses, open decisions, and next actions |

## Interface

| Input | Output |
|-------|--------|
| Offer, buyer, and any budget, team, or channel the founder or an advisor already confirmed | `docs/<slug>-go-to-market.md` |
| Observed replies, closes, or renewals when they exist | Evidence rows, labeled assumptions, and a motion that fits those resources |

Ask if the slug is missing; go ahead and use `go-to-market` when the founder has one offer.

## Hard rules

- Collect offer, buyer, budget, and usable channels from `references/intake.md` before drafting a section.
- Put each material claim on the evidence table in `references/evidence.md` and mark a missing source as `[EVIDENCE NEEDED]` and a missing choice as `[DECISION NEEDED]`.
- Follow `references/motion.md` for channels, acquisition, conversion, and retention, and keep each channel inside the budget and people the founder already has or has chosen.
- Write complete sentences and cite a source on every non-obvious claim.
- Label each figure as a fact or an assumption in the same sentence that uses it.
- Leave CAC, LTV, conversion, or retention blank or marked until a source or a confirmed figure exists.
- Ask for a budget, a named channel, or an observed close rate when an input is missing; do not invent CAC or LTV to finish the page.
- Close with weaknesses, open decisions, and next actions from `references/close.md`.

## Easy mistakes

- Inventing a CAC, LTV, conversion rate, or retention figure to fill a blank.
- Naming a paid channel whose budget the founder has not chosen.
- Mixing a confirmed close with a working assumption in the same cell without a label.
- Writing a national campaign the current team cannot run.
- Drafting code, a voice guide, a skill pack, an engineering strategy, or a lab protocol under this skill.

## Quality standards

- [ ] Intake recorded offer, buyer, budget, and usable channels
- [ ] Every material claim has a source, `[EVIDENCE NEEDED]`, or `[DECISION NEEDED]`
- [ ] Channels, acquisition, conversion, and retention follow `references/motion.md`
- [ ] Named channels fit the stated budget and people
- [ ] CAC and LTV stay unmarked or sourced
- [ ] Sentences are complete; facts and assumptions are split
- [ ] Closing section lists weaknesses, open decisions, and next actions
- [ ] Output is a founder go-to-market page at `docs/<slug>-go-to-market.md`
