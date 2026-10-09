---
name: market-research-brief
description: >-
  Use when sizing demand with cited sources.
---

# Market Research Brief

Write founder demand briefs only; stop if the ask is application code, a writing-voice pass, skill-pack authoring, a living engineering strategy, or laboratory informatics.

## Files

| File | When |
|------|------|
| `references/intake.md` | Offer and geography before any sizing |
| `references/evidence.md` | Claims, sources, and `[EVIDENCE NEEDED]` / `[DECISION NEEDED]` marks |
| `references/sizing.md` | Demand, segments, TAM, SAM, SOM, and trends |
| `references/close.md` | Weaknesses, open decisions, and next actions |

## Interface

| Input | Output |
|-------|--------|
| Offer, geography, and any sources the founder or an advisor already confirmed | `docs/<slug>-market-research-brief.md` |
| Stage or buyer notes when the founder already has them | Evidence rows, labeled assumptions, and sourced size figures only |

Ask if the slug is missing; go ahead and use `market-research-brief` when the founder has one offer.

## Hard rules

- Collect offer and geography from `references/intake.md` before drafting a section.
- Put each material claim on the evidence table in `references/evidence.md` and mark a missing source as `[EVIDENCE NEEDED]` and a missing choice as `[DECISION NEEDED]`.
- Follow `references/sizing.md` for demand, segments, TAM, SAM, SOM, and trends, and attach a URL plus a retrieval date on every size figure you keep.
- Leave a TAM, SAM, SOM, growth rate, or headcount blank or marked until a current source exists.
- Write complete sentences and cite a source on every non-obvious claim.
- Label each figure as a fact or an assumption in the same sentence that uses it.
- Recheck TAM, SAM, SOM, and other fast-moving market figures against a current source before you keep them.
- Ask for a source when a size figure is missing; do not invent a statistic to finish the brief.
- Close with weaknesses, open decisions, and next actions from `references/close.md`.

## Easy mistakes

- Inventing a TAM, SAM, SOM, growth rate, or buyer count to fill a blank.
- Keeping a size figure after the source page moved or the retrieval date is missing.
- Treating a worldwide total as the reachable market without a geography cut.
- Mixing a confirmed figure with a working assumption in the same cell without a label.
- Drafting code, a voice guide, a skill pack, an engineering strategy, or a lab protocol under this skill.

## Quality standards

- [ ] Intake recorded offer and geography
- [ ] Every material claim has a source, `[EVIDENCE NEEDED]`, or `[DECISION NEEDED]`
- [ ] Demand, segments, TAM, SAM, SOM, and trends follow `references/sizing.md`
- [ ] Each kept size figure has a URL and a retrieval date
- [ ] Sentences are complete; facts and assumptions are split
- [ ] Missing inputs were asked for and left marked
- [ ] Closing section lists weaknesses, open decisions, and next actions
- [ ] Output is a founder demand brief at `docs/<slug>-market-research-brief.md`
