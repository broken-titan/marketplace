---
name: systematic-debugging
description: >-
  Use when a bug, a failing test, or surprising behavior appears, before
  proposing a fix.
---

# Systematic debugging

## Files

| File | When |
|---|---|
| `references/pass.md` | Reproduce → locate → hypothesize → change |
| `references/stop.md` | After failed fixes: re-diagnose, do not stack patches |

## Hard rules

- Do not start editing until you can reproduce the bug.
- State one hypothesis; change only what that hypothesis predicts.
- If a few patches in a row fail, undo them and locate the failing line again.
- Write a failing test that shows the bug, then the smallest change that makes it pass.

## Quality standards

- [ ] Write down how you reproduced it (command or test) before the first edit
- [ ] Location narrowed before the first edit
- [ ] Hypothesis stated before the first edit
- [ ] Fix is a failing test, then code
- [ ] If a fix failed, revert it and re-diagnose before the next patch

## Easy mistakes

- If you cannot reproduce the bug, stop editing and reproduce it.
- If you stacked unrelated edits in one pass, undo them and change one thing at a time.
- If you have not found the failing line, do not form a hypothesis yet.
