---
name: business-plan
description: >-
  Use when turning a business idea into a grounded plan without inventing
  demand or dollars.
---

# Business Plan

Write founder planning documents only; stop if the ask is application code, a writing-voice pass, skill-pack authoring, a living engineering strategy, or laboratory informatics.

## Files

| File | When |
|------|------|
| `references/intake.md` | Mission, offer, audience, stage, and constraints |
| `references/evidence.md` | Claims, sources, and `[EVIDENCE NEEDED]` / `[DECISION NEEDED]` marks |
| `references/draft-order.md` | Section order, including executive summary last |
| `references/financials.md` | Year-one structure and clarifying questions |
| `references/close.md` | Weaknesses, open decisions, and next actions |

## Interface

| Input | Output |
|-------|--------|
| Idea notes plus any figures the founder or an advisor already confirmed | `docs/<slug>-business-plan.md` |
| Stage and constraints from intake | Evidence rows, labeled assumptions, and a last-written executive summary |

Ask if the slug is missing; go ahead and use `business-plan` when the founder has one idea.

## Hard rules

- Collect mission, offer, audience, stage, and constraints before drafting a section.
- Put each material claim on the evidence table in `references/evidence.md` and mark a missing source as `[EVIDENCE NEEDED]` and a missing choice as `[DECISION NEEDED]`.
- Leave market size and finance blank or marked until a source or a confirmed figure exists.
- Draft in the order in `references/draft-order.md` and write the executive summary last.
- Write complete sentences and cite a source on every non-obvious claim.
- Label each figure as a fact or an assumption in the same sentence that uses it.
- Keep year-one financials as an assumption-driven structure until the founder or an advisor confirms the numbers; ask the clarifying questions in `references/financials.md`.
- Name at least one substitute, adjacent offer, or status-quo alternative in Competition.
- Recheck TAM, SAM, SOM, and other fast-moving market figures against a current source before you keep them.
- Close with weaknesses, open decisions, and next actions from `references/close.md`.

## Easy mistakes

- Inventing a TAM, SAM, SOM, or dollar figure to fill a blank.
- Writing the executive summary before the other sections exist.
- Calling the market empty because no identical product is listed.
- Mixing a confirmed figure with a working assumption in the same cell without a label.
- Drafting code, a voice guide, a skill pack, an engineering strategy, or a lab protocol under this skill.

## Quality standards

- [ ] Intake recorded mission, offer, audience, stage, and constraints
- [ ] Every material claim has a source, `[EVIDENCE NEEDED]`, or `[DECISION NEEDED]`
- [ ] Market size and finance stay unmarked or sourced
- [ ] Draft order matches `references/draft-order.md` and the executive summary is last
- [ ] Sentences are complete; facts and assumptions are split
- [ ] Year-one financials are structure plus questions until numbers are confirmed
- [ ] Closing section lists weaknesses, open decisions, and next actions
- [ ] Output is a founder planning document at `docs/<slug>-business-plan.md`
