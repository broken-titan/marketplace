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
| `description` | **trigger** — when to invoke, not a summary |
| body | map + product opinions + gotchas + quality bar |
| `references/` | procedures loaded when that step runs |
| `assets/` | templates the agent copies |
| `scripts/` | composition helpers the agent runs |

Host command names and instruction-file names vary. Write to the consuming repo’s agent-instruction files (`AGENTS.md`, `CLAUDE.md`, or the same pattern under another name) only when the skill’s setup step says so.

## Rules

1. **Trigger, not blurb.** YAML `description` answers “when do I load this?”
2. **Lightweight SKILL.md.** Opinions, knowledge, and gotchas particular to this product. Skip what the model already knows from the repo or from ordinary coding.
3. **Progressive disclosure.** Name the files in the tree; the agent reads them at the right time. Do not inline every procedure.
4. **Flexibility first.** Over-constrain only safety, compliance, and destructive ops.
5. **Judgement over brittle absolutes.** Match surrounding idiom. Absolute “always / never” only when the product truly requires it.
6. **Interfaces over galleries.** Clear parameters, enums, outputs. One short contract beats a page of examples.
7. **Say it once.** An instruction lives in SKILL.md *or* one reference, not both.
8. **Gotchas grow.** Highest-signal failures only; leave room to add more from real misses.
9. **Setup in the consuming repo.** Ask once; write config there. Marketplace skills do not bake a sample tenant.
10. **Durable memory.** Repeated-workflow logs live in the consuming repo or a stable plugin-data path — not files that vanish on skill upgrade.
11. **Scripts for boilerplate.** Prefer something the agent can compose over reconstructing the same block each turn.
12. **One category** when possible (`references/categories.md`). Split or pick if a draft straddles several.

Do not name other marketplace plugins. Stay generic.

## Gotchas

- A description that summarizes the skill will not fire when the user needs it.
- A SKILL.md that restates the repo will drown the product-specific bits.
- Config written into the marketplace skill dir is lost on upgrade and leaks a sample tenant.
- Example galleries shrink the exploration space; agents copy the gallery instead of the interface.

## Quality bar

- [ ] Folder tree, not one file
- [ ] `description` is a trigger
- [ ] SKILL.md is a map; procedures live in `references/`
- [ ] One category (or an explicit split)
- [ ] Interface contract present; no example gallery as the main teaching device
- [ ] Gotchas from this product, not invented lore
- [ ] User config and logs land in the consuming repo / stable data path
- [ ] YAML `name` matches the directory
