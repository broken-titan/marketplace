# Doctor pass

Work file by file. Do not invent findings. Hard rules stay in SKILL.md.

## 0. Preserve meaning

Before deleting or rewriting anything, inventory the product opinions in **this** skill: numbered rules, banned phrases, registers and voice, named thresholds, always/never the product already decided, and purpose (what job this skill does).

Write them down. If purpose, register, bans, numbered rules, or named thresholds would change, **stop**. Keep the old meaning. Only move files (SKILL.md map vs `references/`).

Do not import a sibling skill's product to fill a gap or to settle a contradiction.

## 1. Over-constraint and conflicts

Find pairs **in this file** that cannot both be true. Keep the rule **this skill** needs. Drop the other or narrow it to the surface it actually governs.

Treat keep-one-opinion as two rules in this file that cannot both be true. Do not collapse this skill into a neighboring product rule. Move product opinions; do not paraphrase them into a different rule; do not replace them with generic assistant defaults.

## 2. Progressive disclosure

If SKILL.md is a procedure, split: keep the map and the trigger; move steps to `references/<step>.md`. Point at those files once.

## 3. Trigger

Rewrite `description` per `skill-builder/references/trigger.md`. YAML `description` is required and when-to-use only, in the same voice as the body. A slogan or couplet in `description:` is a fail.

## 4. The obvious

Delete only ordinary tooling: git, markdown, or "read the file before editing," unless this product breaks that default.

Do **not** delete distinctive style, house voice, domain rules, banned terms, numbered product rules, or worked examples of that voice. Those are not obvious.

## 5. Repeats

One home per instruction. SKILL.md xor a reference.

## 6. Galleries

Move wrong/right pairs into `references/examples.md` when they illustrate a voice or a rule. Replace a long teaching gallery with an interface contract when the contract is the point.

When you move wrong/right pairs, keep the voice they illustrate.

## 7. Easy mistakes

Add an **Easy mistakes** section (or grow it) from failures already visible in the skill, its tests, or the repo. Do not invent lore.

## 8. Pack shape

A plugin with several skills stays several skills. Do not merge them into one markdown file. Do not add a bibliography.

## 9. Skill sentences

If a Hard rule, Easy mistake, or checklist item is a dunk (`X is not Y` / `it's X, not Y`), a couplet (a short rule, then a second sentence that explains, restates, threatens a future, or scores the mistake), or a vague rule plus a gloss, rewrite it to one specific sentence.

Do not compress that item into a punchier one-liner.
Do not write `X is not Y`, `does not count`, `fails the bar`, `wearing a`, `evidence gate`, `ceremony`, or `shotgun` as a label.
Do not add a why-sentence after a rule.
If the item uses disposition, carve-out, cannot state, without waiting, flag the cost, as a habit, style nit, name the X, Quality bar, or courtroom evidence for why, rewrite it to ordinary speech.
Do not invent a new maxim under the title.
If a line under `# Title` restates the title or the YAML description, delete it unless it is the actual first rule.
The checklist heading is Quality standards.
