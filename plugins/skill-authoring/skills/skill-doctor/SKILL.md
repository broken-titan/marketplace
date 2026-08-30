---
name: skill-doctor
description: >-
  Use when rightsizing an existing SKILL.md, agent-instruction file
  (AGENTS.md, CLAUDE.md, or similar), or a skill pack: structure, trigger,
  over-constraint, and progressive disclosure. Edits structure; meaning
  stays. Does not create a new domain skill.
---

Rightsize existing skill and instruction files. Same skill, same meaning, restructured. Do **not** invent a new domain skill.

Pass: `references/pass.md`. Trigger rewrite: sibling `skill-builder/references/trigger.md`. Tree: sibling `skill-builder/references/tree.md`.

## Interface

| Input | Output |
|-------|--------|
| Path to a SKILL.md, instruction file, or skill pack | The same files, same meaning, restructured |
| Optional: product rules that must stay | Those rules kept, named in the report |

Report what moved, what was deleted (must be duplicate or ordinary tooling), and which product opinions were kept.

## Hard rules

- **Meaning-preserving.** If purpose, register, bans, numbered rules, or named thresholds would change, stop and keep the old meaning; only move files.
- **Keep product opinions.** Numbered rules, banned phrases, registers, voice, named thresholds, and always/never the product already decided stay. Move them to SKILL.md or `references/`. Do not paraphrase them into a different rule. Do not replace them with generic assistant defaults.
- **Do not import a sibling.** Resolve contradictions inside this skill only. Do not copy another skill's product (comments, test-first, error-message shape) into this one. An easy-mistake note that protects a product rule protects it in the skill that owns it.
- **"Obvious" is only ordinary tooling.** Delete git, markdown, and "read the file before editing." Do not delete distinctive style, house voice, domain rules, or worked examples of that voice.
- **Keep-one-opinion** means two rules in this file cannot both be true; keep the one this skill needs; drop or narrow the other. Treat that as two rules in this file.
- If a Hard rule, Easy mistake, or checklist item is a dunk, a couplet, or a vague rule plus a gloss, rewrite it to one specific sentence.
- Do not compress a dunk or a couplet into a punchier one-liner.
- Do not write `X is not Y`, `does not count`, `fails the bar`, `wearing a`, `evidence gate`, `ceremony`, or `shotgun` as a label.
- Do not add a why-sentence after a rule.
- If a Hard rule, Easy mistake, or checklist item uses disposition, carve-out, cannot state, without waiting, flag the cost, as a habit, style nit, name the X, Quality bar, or courtroom evidence for why, rewrite it to ordinary speech.
- If the YAML `description` is a slogan, a couplet, a keyword dump, or a Hard rule copied into the trigger, rewrite it to one or two specific when-to-use sentences in the same voice as the body.
- If a line under `# Title` restates the title or the YAML description, delete it unless it is the actual first rule.

## Pass (in order)

Follow `references/pass.md`. Short form:

0. Inventory product opinions. Preserve meaning. If meaning would change, stop; only move files.
1. Strip conflicting rules **in this file**. Keep the opinion this skill needs.
2. Move long procedure into `references/`. SKILL.md stays map + trigger + easy mistakes + quality standards.
3. Rewrite YAML `description` as when to use the skill, same voice as the body. If it is a slogan or a couplet, that is a fail.
4. Delete ordinary tooling only.
5. Collapse repeated instructions.
6. Move wrong/right pairs to `references/examples.md` when they illustrate a voice. Do not delete that voice.
7. Add or grow **Easy mistakes** from failures already visible in the skill or repo. Do not invent lore.
8. Leave a multi-skill plugin as multiple skills. No bibliography of people or books.
9. If a Hard rule, Easy mistake, checklist item, or YAML `description` is a dunk, a couplet, a slogan, or banned diction, rewrite it to one specific sentence in ordinary speech; do not invent a new maxim. If an H1 blurb restates the title or the YAML description, delete it unless it is the actual first rule.

Instruction files use the host’s names (`AGENTS.md`, `CLAUDE.md`, or similar). Mention the **pattern**, not a single vendor.

## Easy mistakes

- If a voice skill would become a comment policy or generic "lead with the answer," restore the old meaning.
- If you treated keep-one-opinion as one opinion per plugin, keep two rules that can both be true in this file.
- If "let judgement" would delete a named product opinion, keep that opinion.
- If you flattened several skills into one file, split them back into separate skills.
- If the pass only rewrote the title, keep going until structure, trigger, and disclosure change.
- If a Hard rule, Easy mistake, or checklist item is a dunk, a couplet, or a vague rule plus a gloss, rewrite it to one specific sentence.
- If a Hard rule, Easy mistake, or checklist item uses disposition, carve-out, cannot state, without waiting, flag the cost, as a habit, style nit, name the X, Quality bar, or courtroom evidence for why, rewrite it to ordinary speech.
- If the YAML `description` is a slogan or a couplet, rewrite it to when to use the skill.
- If a line under `# Title` restates the title or the YAML description, delete it unless it is the actual first rule.

## Quality standards

- [ ] Same job as before the pass
- [ ] Hard rules, Easy mistakes, and checklist items are one specific sentence each
- [ ] Product rules kept (numbered rules, bans, registers, voice, thresholds)
- [ ] Only structure changed
- [ ] Report lists what moved, what was deleted (duplicate or ordinary tooling), and which product opinions were kept
- [ ] YAML `description` is when to use the skill, same voice as the body
- [ ] No H1 blurb unless it is the actual first rule
- [ ] Long procedures live in `references/`
- [ ] Multi-skill packs still multi-skill
- [ ] No people/book bibliography
