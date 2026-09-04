---
name: setup-checklist
description: >-
  Use when writing an ordered setup or ticket checklist that
  someone has to run.
---

# Setup checklists

Open with one line that states the purpose and the audience.

## Files

| File | When |
|------|------|
| `references/example.md` | Content craft only. Load when the draft is a dump, a ticket body, or a markup template. |

## Interface

| Input | Output |
|-------|--------|
| Notes for a setup or a ticket | Ordered items, one clear line each |
| Purpose and audience | One opening line that names both |

Ask if purpose or audience is missing; go ahead and draft when both are known.

## Hard rules

- Put purpose and audience in the first line, then write the items in the order the work runs.
- Keep a line only when skipping it would let a fault through.
- Write each item as an imperative action plus the path, field, or command needed to do it.
- Write one clear line per item and leave list markup to the host.
- Write active voice, present tense, and the fewest words that still run the item.
- Front-load the action; use a literal heading; spell an acronym once, then the short form.
- Link a deep doc; do not paste it.
- Leave Who and Status off every item.
- Leave out a ticket body, customer names, fluff, a literature review, and cute labels.

## Easy mistakes

- A first line that skips purpose or audience.
- An item that names a goal and omits the click, field, or command.
- A line that restates a policy and does not enable a correction.
- A draft that requires markdown bullets, checkbox marks, Who and Status columns, or a Jira or Notion template.
- A pasted ticket body or a customer name.
- A cute heading when the heading should be the work.
- An acronym used before it is spelled.
- A pasted runbook or deep procedure.

## Quality standards

- [ ] First line states purpose and audience
- [ ] Items are workflow-ordered and one clear line each
- [ ] Every item has an imperative action and the path, field, or command needed to do it
- [ ] Every kept item enables a correction
- [ ] Active voice, present tense, front-loaded action, literal headings
- [ ] Acronyms spelled once; deep docs linked, not pasted
- [ ] Who and Status stay off every item; no ticket body, customer names, fluff, or cute labels
- [ ] List markup is left to the host
- [ ] Content craft matches `references/example.md`
