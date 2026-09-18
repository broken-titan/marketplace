---
name: complexity-refactor
description: >-
  Use when reviewing branching code, nested logic, or a large function,
  before merge.
---

# Complexity refactor

## Files

| File | When |
|---|---|
| `references/measure.md` | CC formula, tools, project vs default thresholds |
| `references/tactics.md` | Ordered refactor moves |
| `references/workflow.md` | Rank, edit one function, remesure, report |

## Hard rules

- Preserve behavior.
- Run tests before and after; if there are none, say so, suggest adding them, and keep the change minimal.
- Do not hide branches in dense one-liners to drop the number; move complexity into well-named units.
- Do not break public APIs or exported signatures without asking.
- Prefer a small named function over a comment that explains a section.
- If the function name needs "and", split the function.

## Quality standards

- [ ] Touched functions measured and ranked by CC descending
- [ ] Hotspots reported with numbers before the first edit
- [ ] Worst first; one function at a time
- [ ] Before/after table (function, CC before, CC after)
- [ ] Extracted names listed
- [ ] Write down how you checked behavior (tests, or a minimal change if there are no tests)

## Easy mistakes

- If a project tool can measure CC, run it.
- If a function scores 1–5, leave it.
- If the same type-switch appears in only one place, leave it as a switch or a table.
- If a comment narrates a section, extract a named function instead.
