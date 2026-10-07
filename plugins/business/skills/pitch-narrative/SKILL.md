---
name: pitch-narrative
description: >-
  Use when compressing a finished plan into a pitch.
---

# Pitch Narrative

Write founder investor or lender pitches only; stop if the ask is application code, a writing-voice pass, skill-pack authoring, a living engineering strategy, or laboratory informatics.

## Files

| File | When |
|------|------|
| `references/intake.md` | Path to an approved plan and the audience for the pitch |
| `references/evidence.md` | Claims copied from that plan, with gaps left marked |
| `references/spine.md` | Short story order for an investor or lender |
| `references/close.md` | Weaknesses, open decisions, and next actions already in the plan |

## Interface

| Input | Output |
|-------|--------|
| Path to an approved founder plan and whether the reader is an investor or a lender | `docs/<slug>-pitch-narrative.md` |
| Only the claims, figures, and marks that already sit in that plan | A short story that adds no new market or finance facts |

Ask if the slug or the plan path is missing; do not draft until the founder points at an approved plan.

## Hard rules

- Collect the approved-plan path and the reader type from `references/intake.md` before drafting a section.
- Refuse a draft when the plan is missing, unapproved, or still a pile of notes.
- Put each material claim on the evidence table in `references/evidence.md` by copying the plan's source, kind, and mark; do not add a new market or finance fact.
- Follow `references/spine.md` for story order and keep every sentence traceable to a plan sentence.
- Leave `[EVIDENCE NEEDED]` and `[DECISION NEEDED]` in place when the plan still has those marks.
- Write complete sentences and keep the plan's fact-versus-assumption labels.
- Ask for a missing plan path or an approval; do not fill a gap with a new statistic.
- Close with weaknesses, open decisions, and next actions copied from the plan via `references/close.md`.

## Easy mistakes

- Inventing a market size, price, or return to make the pitch sound finished.
- Adding a rival, a channel, or a figure that is absent from the approved plan.
- Dropping a gap mark so the pitch looks cleaner than the plan.
- Drafting from notes the founder has not approved as a plan.
- Drafting code, a voice guide, a skill pack, an engineering strategy, or a lab protocol under this skill.

## Quality standards

- [ ] Intake recorded an approved-plan path and the reader type
- [ ] Every material claim is copied from that plan with the same source and mark
- [ ] Story order follows `references/spine.md`
- [ ] No new market or finance fact appears
- [ ] Plan gaps stay marked
- [ ] Sentences are complete; facts and assumptions stay split as in the plan
- [ ] Closing section copies weaknesses, open decisions, and next actions from the plan
- [ ] Output is a founder pitch at `docs/<slug>-pitch-narrative.md`
