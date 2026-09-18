---
name: competitive-teardown
description: >-
  Use when mapping rivals for a founder plan.
---

# Competitive Teardown

Write founder rivalry maps only; stop if the ask is application code, a writing-voice pass, skill-pack authoring, a living engineering strategy, or laboratory informatics.

## Files

| File | When |
|------|------|
| `references/intake.md` | Offer, geography, and named rivals the founder already knows |
| `references/evidence.md` | Claims, sources, and `[EVIDENCE NEEDED]` / `[DECISION NEEDED]` marks |
| `references/map.md` | Direct rivals, indirect rivals, substitutes, and doing nothing |
| `references/teardown.md` | Strengths, weaknesses, pricing, positioning, and the wedge |
| `references/close.md` | Weaknesses, open decisions, and next actions |

## Interface

| Input | Output |
|-------|--------|
| Offer, geography, and any rival names the founder or an advisor already confirmed | `docs/<slug>-competitive-teardown.md` |
| Pricing pages or notes the founder already collected | Evidence rows, labeled assumptions, and a named wedge |

Ask if the slug is missing; go ahead and use `competitive-teardown` when the founder has one offer.

## Hard rules

- Collect offer, geography, and any named rivals from `references/intake.md` before drafting a section.
- Put each material claim on the evidence table in `references/evidence.md` and mark a missing source as `[EVIDENCE NEEDED]` and a missing choice as `[DECISION NEEDED]`.
- Follow `references/map.md` and name at least one direct rival, one indirect rival or substitute, and the status-quo alternative of doing nothing.
- Follow `references/teardown.md` for strengths, weaknesses, pricing, positioning, and the wedge the founder can hold.
- Write complete sentences and cite a source on every non-obvious claim.
- Label each figure as a fact or an assumption in the same sentence that uses it.
- Recheck pricing pages and positioning copy against a current source before you keep them.
- Ask for a rival name or a source when the map is thin; do not write that the field is empty.
- Close with weaknesses, open decisions, and next actions from `references/close.md`.

## Easy mistakes

- Writing that there are no competitors because no identical product is listed.
- Leaving substitutes, contractors, spreadsheets, or inertia off the map.
- Copying a price without a URL and a retrieval date.
- Mixing a confirmed figure with a working assumption in the same cell without a label.
- Drafting code, a voice guide, a skill pack, an engineering strategy, or a lab protocol under this skill.

## Quality standards

- [ ] Intake recorded offer, geography, and any named rivals
- [ ] Every material claim has a source, `[EVIDENCE NEEDED]`, or `[DECISION NEEDED]`
- [ ] The map names a direct rival, an indirect rival or substitute, and doing nothing
- [ ] Strengths, weaknesses, pricing, positioning, and the wedge follow `references/teardown.md`
- [ ] Sentences are complete; facts and assumptions are split
- [ ] Missing inputs were asked for and left marked
- [ ] Closing section lists weaknesses, open decisions, and next actions
- [ ] Output is a founder rivalry map at `docs/<slug>-competitive-teardown.md`
