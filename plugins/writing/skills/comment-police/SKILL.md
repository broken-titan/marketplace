---
name: comment-police
description: Use when writing or editing source code. Default is add no comments.
---

# Comment police

Default is **add no comments**. Prefer self-documenting code. Comments are a last resort.

This skill does not ask you to write why-comments as a habit. A why-comment is still a comment. Reach for a simpler design first.

## Rules

- Default to adding **no comments at all** when writing or modifying code.
- Never insert comments that describe what the code literally does.
- Only contemplate a comment when the logic is truly intricate and resists simplification and clear naming.
- When that happens (and it is not a carve-out):
  1. Do not write the comment yet.
  2. Propose a cleaner design.
  3. Ask: refactor to remove the need, or add a brief comment after approval?
  4. Wait for confirmation.
- Public-API contracts that types cannot state are a carve-out (below). You may add the contract comment without waiting.
- If the user explicitly requests comments in straightforward code, add them but remind them of the maintainability cost.

## Carve-outs (no wait)

Required legal or tooling marks, or a contract types cannot state. Add without asking. Not a license to add why-comments nearby.

- License, copyright, and SPDX headers the file or repo already uses.
- Lint or type-checker suppressions that name the rule and the smallest scope.
- Generated-file banners that tools require so humans do not edit the output.
- Public-API contracts that parameter names and types cannot state (units, preconditions, error cases the signature cannot express). Keep these to the contract; do not narrate the body.

Do not use a carve-out to smuggle a what-comment or a tour of the function.

## Quality bar

- [ ] No what-comments added.
- [ ] No why-comments added as a habit.
- [ ] Complex spots proposed for simpler design before a comment.
- [ ] Carve-outs limited to the four cases above.

## Gotchas

- "Leave documentation comments as appropriate" conflicts with this skill and with `writing-voice`. Keep **add no comments**.
- A public-API docstring that narrates the body is a what-comment wearing a carve-out.
- User-requested comments in straightforward code are allowed; still flag the cost.
