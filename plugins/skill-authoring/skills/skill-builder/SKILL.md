---
name: skill-builder
description: >-
  Use when creating a new skill or a plugin skill pack: a folder with
  SKILL.md, references/, and optional scripts, assets, or templates.
---

Author a **skill folder**, never a single giant markdown dump.

Layout and disclosure: `references/tree.md`. Trigger field: `references/trigger.md`. Interfaces: `references/interface.md`. Setup and memory: `references/setup.md`. Categories: `references/categories.md`.

## Interface

| Field | Shape |
|-------|--------|
| `name` | lowercase-hyphen; matches the skill directory |
| `description` | required when-to-use line, same voice as the body |
| body | map + product opinions + easy mistakes + quality standards |
| `references/` | procedures loaded when that step runs |
| `assets/` | templates the agent copies |
| `scripts/` | composition helpers the agent runs |

Host command names and instruction-file names vary. Write to the consuming repo’s agent-instruction files (`AGENTS.md`, `CLAUDE.md`, or the same pattern under another name) only when the skill’s setup step says so.

## Rules

1. **When to use.** YAML `description` is required. Write one or two specific sentences for when to load this skill, in the same voice as the body. Do not write a slogan, a keyword dump, or a second copy of a Hard rule unless that sentence is when to use the skill.
2. **Lightweight SKILL.md.** Opinions, knowledge, and easy mistakes particular to this product. Skip what the model already knows from the repo or from ordinary coding. House voice, banned terms, and numbered product rules stay.
3. **Progressive disclosure.** Name the files in the tree; the agent reads them at the right time. Do not inline every procedure.
4. **Flexibility first.** Over-constrain only safety, compliance, and destructive ops.
5. **Judgement over brittle absolutes.** Match surrounding idiom. Absolute always/never stays for safety, compliance, destructive ops, **and** named product opinions. Judgement does not authorize deleting a named product opinion.
6. **Interfaces over galleries.** Clear parameters, enums, outputs. One short contract beats a page of examples.
7. **Say it once.** An instruction lives in SKILL.md *or* one reference, not both.
8. **Easy mistakes grow.** Highest-signal failures only; leave room to add more from real misses.
9. **Setup in the consuming repo.** Ask once; write config there. Marketplace skills do not bake a sample tenant.
10. **Durable memory.** Repeated-workflow logs live in the consuming repo or a stable plugin-data path — not files that vanish on skill upgrade.
11. **Scripts for boilerplate.** Prefer something the agent can compose over reconstructing the same block each turn.
12. **One category** when possible (`references/categories.md`). Split or pick if a draft straddles several.
13. **One sentence per rule.** Write each Hard rule, Easy mistake, and Quality standards item as one specific instruction, with the condition and the action in that sentence.
14. Do not write a couplet: a short rule plus a second sentence that explains, restates, threatens a future, or scores the mistake.
15. Do not write a dunk (`X is not Y` / `it's X, not Y`).
16. A semicolon may join two closely related independent clauses that are both actions or both conditions.
17. A paragraph under `# Title` is not required. Keep a line there only when it is the actual first rule. Do not write a maxim, and do not restate the title or the YAML description.
18. The checklist heading is Quality standards.
19. Do not write disposition, carve-out, cannot state, without waiting, flag the cost, as a habit, style nit, name the X, courtroom evidence for why, with a name, or stay silent.
20. Prefer ask if; go ahead and add it; say why; which clarifies the rule; minimal for a small change; comments about formatting or naming.
21. Do not end a rule with a leftover closer of about 3-4 words that states a spare fact; put the fact in the sentence that needed it, or leave it out.
22. Do not write `table` as the unnamed grid of cases ("one table," "in one table," "stop at the table"); if you mean many cases of one behavior in a single test, say that, and leave table for a database table, an HTML table, or a documented table the sentence already named.

Do not name other marketplace plugins. Stay generic.

## Easy mistakes

- Write the YAML description as when to use the skill, in the same voice as the body.
- If the YAML description is a slogan, a keyword dump, or a couplet, rewrite it to one or two specific when-to-use sentences.
- If a line under `# Title` restates the title or the YAML description, delete it unless it is the actual first rule.
- Keep only opinions particular to this product.
- Write user config into the consuming repo.
- Teach with an interface contract, not an example gallery.
- If a Hard rule, Easy mistake, or Quality standards item is a dunk, a couplet, or a slogan, rewrite it to one specific sentence.
- If a sentence uses disposition, carve-out, cannot state, without waiting, flag the cost, as a habit, style nit, name the X, courtroom evidence for why, with a name, stay silent, or a leftover closer of about 3-4 words, rewrite it to ordinary speech.
- If a sentence uses `table` as the unnamed grid of cases ("one table," "in one table," "stop at the table"), rewrite it to many cases of one behavior in a single test, and leave table for a database table, an HTML table, or a documented table the sentence already named.

## Quality standards

- [ ] Folder tree, not one file
- [ ] YAML `description` is required, when-to-use only, same voice as the body
- [ ] No maxim under `# Title` unless it is the actual first rule
- [ ] SKILL.md is a map; procedures live in `references/`
- [ ] One category (or an explicit split)
- [ ] Interface contract present; no example gallery as the main teaching device
- [ ] Each Hard rule, Easy mistake, and Quality standards item is one specific sentence
- [ ] Easy mistakes from this product, not invented lore
- [ ] User config and logs land in the consuming repo / stable data path
- [ ] YAML `name` matches the directory
