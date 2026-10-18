---
name: requesting-code-review
description: >-
  Use when a change is complete and you need a review before merge,
  looking for correctness, missing tests, broken contracts, and extra
  complexity.
---

# Requesting code review

## Files

| File | When |
|---|---|
| `references/pass.md` | What to read, how to file a finding |

## Hard rules

- Read the diff as an adversary.
- Write each finding as file:line plus severity.
- Read for correctness, missing tests, API contracts, and needless complexity.
- Do not rubber-stamp a diff you authored; if you cannot get a second reader, write findings against your own change as if you did not write it.
- If the finding list is empty, say you read the whole diff and found nothing on correctness, tests, contracts, or extra complexity.

## Quality standards

- [ ] Whole diff read
- [ ] Each finding has file:line and severity
- [ ] Correctness, tests, contracts, and needless complexity each considered
- [ ] Own-diff review is adversarial; recap the findings

## Easy mistakes

- If the review only recaps what the PR does, write findings as file:line plus severity.
- If you wrote LGTM on your own patch without findings, read the whole diff and write findings or an explicit empty pass.
- If most of the comments are about formatting or naming, put the actual contract break first.
