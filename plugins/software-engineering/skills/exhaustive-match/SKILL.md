---
name: exhaustive-match
description: >-
  Use when you write a switch, match, or map over a closed set of
  variants, status values, or keys.
---

# Exhaustive match

Handle every member of a closed set, or fail. A silent else, a default branch, or a missing map key hides the next variant.

## Hard rules

- Match every variant of a closed enum, union, or status set at compile time when the language can do that.
- In TypeScript, give the leftover value type `never` (an `assertNever` helper is fine) so a new union member fails the build.
- In Rust, match every enum variant and leave `_` off when the set is closed.
- If you look up a key in a map of handlers, a missing key is an error, not a skip.
- Do not add an else or default branch that returns, logs, or continues when the set is closed.

## Quality standards

- [ ] Every closed variant has a branch or a compile-time leftover check
- [ ] No else or default that swallows an unmatched member
- [ ] Map lookups fail when the key is absent
- [ ] A newly added key or variant would break the build or the test, not pass quietly

## Easy mistakes

- If a switch has a default that returns undefined or the input unchanged, delete that default and handle the leftover as `never` or an error.
- If a Rust match uses `_` on a closed enum, name the remaining variants instead.
- If a handler map uses a fallback for unknown keys, remove the fallback and fail when the key is missing.
