---
name: skill-doctor
description: >-
  Use when rightsizing an existing SKILL.md, agent-instruction file
  (AGENTS.md, CLAUDE.md, or similar), or a skill pack: structure, trigger,
  over-constraint, and progressive disclosure. Edits structure; does not
  create a new domain skill.
---

Rightsize existing skill and instruction files. Do **not** invent a new domain skill.

Pass: `references/pass.md`. Trigger rewrite: sibling `skill-builder/references/trigger.md`. Tree: sibling `skill-builder/references/tree.md`.

## Interface

| Input | Output |
|-------|--------|
| Path to a SKILL.md, instruction file, or skill pack | The same files, restructured |
| Optional: product rules that must stay | Those rules kept, named in the report |

Report what moved, what was deleted as obvious, and which product opinions were kept.

## Pass (in order)

Follow `references/pass.md`. Short form:

1. Strip over-constraint and conflicting rules. Keep **one** opinion where the product actually needs it.
2. Move long procedure into `references/`. SKILL.md stays map + trigger + gotchas + quality bar.
3. Rewrite YAML `description` (or the instruction file’s “when to apply” line) as a when-to-invoke trigger.
4. Delete the obvious (repo-evident or ordinary coding).
5. Collapse repeated instructions.
6. Replace example galleries with interface contracts.
7. Add or grow **Gotchas** from evidence in the skill or repo — not invented lore.
8. Leave a multi-skill plugin as multiple skills. No bibliography of people or books.

Instruction files use the host’s names (`AGENTS.md`, `CLAUDE.md`, or similar). Mention the **pattern**, not a single vendor.

## Gotchas

- “Let judgement” must not undo a real product rule (e.g. a comment policy the writing pack already decided).
- Flattening several skills into one file loses invocable surfaces.
- A doctor pass that only rewrites the title is not a pass.

## Quality bar

- [ ] Trigger description
- [ ] Long procedures live in `references/`
- [ ] Conflicting rules reduced to one product opinion
- [ ] Gotchas from evidence
- [ ] Multi-skill packs still multi-skill
- [ ] No people/book bibliography
