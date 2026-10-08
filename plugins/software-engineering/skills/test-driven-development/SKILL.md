---
name: test-driven-development
description: >-
  Use when implementing a feature or bugfix, before writing production
  code.
---

# Test-driven development

Write a failing test for the missing behavior before you write production code.

## Files

| File | When |
|---|---|
| `references/cycle.md` | RED, GREEN, refactor while green |
| `references/scope.md` | Spikes, generated files, config, tests written after |

## Hard rules

- Write a failing test for the missing behavior before you write production code.
- Watch that test fail for the missing behavior before you write production code.
- Write the smallest production change that makes that test pass.
- Refactor only while the suite is green.
- If you spike, throw the spike away before you start the cycle.
- Leave generated files and config out of this skill.

## Quality standards

- [ ] Failing test exists before the production change
- [ ] RED command output shows the missing behavior
- [ ] Production change is the smallest that goes green
- [ ] GREEN command output
- [ ] Refactor, if any, happened while green

## Easy mistakes

- If the test fails on a typo or a missing import, fix that and watch it fail for the missing behavior.
- If you wrote the test after the production code and it passed on the first run, delete the production change and write the failing test first.
- If spike code landed in the branch, delete it and start with a failing test.
