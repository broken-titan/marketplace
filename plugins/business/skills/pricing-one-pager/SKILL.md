---
name: pricing-one-pager
description: >-
  Use when setting or defending a price.
---

# Pricing One Pager

Write founder pricing pages only; stop if the ask is application code, a writing-voice pass, skill-pack authoring, a living engineering strategy, or laboratory informatics.

## Files

| File | When |
|------|------|
| `references/intake.md` | Offer, buyer, and any price the founder already chose |
| `references/evidence.md` | Claims, sources, and `[EVIDENCE NEEDED]` / `[DECISION NEEDED]` marks |
| `references/model.md` | One-time, subscription, or hybrid; bands; comps; rationale |
| `references/close.md` | Weaknesses, open decisions, and next actions |

## Interface

| Input | Output |
|-------|--------|
| Offer, buyer, and any price or model the founder or an advisor already confirmed | `docs/<slug>-pricing-one-pager.md` |
| Competitor prices the founder already collected | Evidence rows, labeled assumptions, and a chosen or marked price |

Ask if the slug is missing; go ahead and use `pricing-one-pager` when the founder has one offer.

## Hard rules

- Collect offer, buyer, and any chosen price from `references/intake.md` before drafting a section.
- Put each material claim on the evidence table in `references/evidence.md` and mark a missing source as `[EVIDENCE NEEDED]` and a missing choice as `[DECISION NEEDED]`.
- Follow `references/model.md` and pick one model among one-time, subscription, or hybrid, or mark `[DECISION NEEDED]`.
- Write price bands and comparable public prices with a URL and a retrieval date on every kept figure.
- Mark `[DECISION NEEDED]` on the recommended price when the founder has not chosen it.
- Write complete sentences and cite a source on every non-obvious claim.
- Label each figure as a fact or an assumption in the same sentence that uses it.
- Ask for a paid invoice, a verbal yes, or a public comp when a number is missing; do not invent a price to finish the page.
- Close with weaknesses, open decisions, and next actions from `references/close.md`.

## Easy mistakes

- Inventing a list price, discount, or willingness-to-pay figure to fill a blank.
- Recommending a number while the founder still has not chosen, without `[DECISION NEEDED]`.
- Copying a competitor price without a URL and a retrieval date.
- Mixing a confirmed figure with a working assumption in the same cell without a label.
- Drafting code, a voice guide, a skill pack, an engineering strategy, or a lab protocol under this skill.

## Quality standards

- [ ] Intake recorded offer, buyer, and any chosen price
- [ ] Every material claim has a source, `[EVIDENCE NEEDED]`, or `[DECISION NEEDED]`
- [ ] Model, bands, comps, and rationale follow `references/model.md`
- [ ] An unchosen price is marked `[DECISION NEEDED]`
- [ ] Sentences are complete; facts and assumptions are split
- [ ] Missing inputs were asked for and left marked
- [ ] Closing section lists weaknesses, open decisions, and next actions
- [ ] Output is a founder pricing page at `docs/<slug>-pricing-one-pager.md`
