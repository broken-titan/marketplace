---
name: parameterized-testing
description: >-
  Use when one behavior has many cases, a boundary matrix, copy-pasted
  test functions, or a request to cover all of these inputs.
---

# Parameterized testing

## Files

| File | When |
|---|---|
| `references/table.md` | When to parameterize, named rows, repo idiom |
| `references/overlay.md` | Property-based checks (algebraic properties only) |

## Hard rules

- Put every case for one behavior in one table.
- Give each parameterized row a name.
- If a row needs a different assertion, a different setup, or a different mock, split it into its own test.
- Use whatever the repo already uses (`parametrize`, table-driven tests, `test.each`, `Theory`).
- Use a named table as the default; add a property-based check only for an algebraic property (round-trip, inverse).
- Write the failing row first; then add the other rows.
- If the test body still has an if or else, split it into two tests.

## Quality standards

- [ ] One table, one behavior
- [ ] Every row has a name
- [ ] Failing row added before the production change
- [ ] Setup and control flow are the same across rows
- [ ] Repo idiom used; no new harness invented

## Easy mistakes

- If two rows share a table but need different assertions or setup, split them into two tests.
- If a row has no name, give it one.
- If you wrapped cases in a for-loop, put them in a parameterized table.
