---
name: code-simplify
description: >-
  Use after the suite is green, or when asked to clean up overbuilt
  code.
---

# Simplify

## Files

| File | When |
|---|---|
| `references/tactics.md` | Inline, native APIs, when to extract |

## Hard rules

- Delete and flatten while preserving behavior.
- If an abstraction has one caller, inline it and leave the surrounding design alone.
- Use the language construct first; then a framework type already in the repo; then a library already in the repo, even if the call is a few lines longer.
- Do not extract a helper that only wraps one call.
- Do not add a dependency to replace a short function.
- Extract only when the rule is one the stdlib does not already make clear, or when a second caller exists now.

## Quality standards

- [ ] Behavior preserved (tests still green, or a minimal change if there are no tests)
- [ ] One-caller abstractions inlined
- [ ] No new one-off wrappers around a native or existing API
- [ ] No new dependency added to dodge a short function
- [ ] Extracts remaining have a rule the stdlib does not already make clear, or a second caller

## Easy mistakes

- If a helper only wraps `map` or `filter`, inline it.
- If you inlined one caller, leave the surrounding design alone.
- If you added a package to replace a few lines, delete the package and write the function.
