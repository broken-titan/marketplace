---
name: receiving-code-review
description: Use when review comments arrive on a change.
---

# Receiving code review

## Files

| File | When |
|---|---|
| `references/respond.md` | fix, reject, or ask |

## Hard rules

- Open the code the comment points at before you answer.
- For every comment, pick one: fix it, reject it, or ask if you need more.
- If you reject, say why, using the code, a test, or the API contract.
- Do not apply a change you believe is wrong to close the thread.

## Quality standards

- [ ] Each comment checked against the code
- [ ] Each comment has fix / reject / ask
- [ ] Each rejection says why
- [ ] No cooperative-but-wrong edits

## Easy mistakes

- If you have not opened the line the comment points at, open it before you answer.
- If you would apply every comment about formatting or naming to look responsive, reject the finding that is wrong and fix the rest.
- If you already know the code contradicts the comment, reject it and say why, using the code, a test, or the API contract.
