---
name: comment-police
description: Use when writing or editing source code, to add no comments unless an exception applies.
---

# Comment police

## Rules

- Add no comments when writing or modifying code.
- Never insert a comment that describes what the code does.
- If a comment would explain why the code is awkward, change the design first.
- If the logic resists simplification and clear naming, and it is not an exception:
  1. Do not write the comment yet.
  2. Propose a cleaner design.
  3. Ask if we should refactor to remove the need, or add a brief comment after you approve.
  4. Wait for confirmation.
- If the comment is a public-API contract the types do not already make clear, go ahead and add it.
- If the user explicitly requests comments in straightforward code, add them.

## Exceptions

Go ahead and add required legal or tooling marks, or a contract the types do not already make clear; leave why-comments out of the nearby body.

- License, copyright, and SPDX headers the file or repo already uses.
- Lint or type-checker suppressions which clarify the rule and the smallest scope.
- Generated-file banners that tools require so humans do not edit the output.
- Public-API contracts that parameter names and types do not cover (units, preconditions, error cases the signature does not cover); keep these to the contract and do not narrate the body.

Do not use an exception to add a what-comment or a tour of the function.

## Quality standards

- [ ] No what-comments added.
- [ ] No why-comments added.
- [ ] Complex spots proposed for simpler design before a comment.
- [ ] Exceptions limited to the four cases above.

## Easy mistakes

- If another instruction says to leave documentation comments as appropriate, add no comments.
- If a public-API docstring narrates the body, delete the narration and keep only the contract the types do not already make clear.
- If the user requested comments in straightforward code, add them.
