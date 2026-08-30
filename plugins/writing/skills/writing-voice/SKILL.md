---
name: writing-voice
description: Use when drafting or revising documents, guides, notes, or short messages.
---

# Writing voice

Apply this register when writing. **Add no comments.** That is a product rule — do not treat it as optional judgement.

## Files

| File | When |
|---|---|
| `references/registers.md` | Extra registers (lists, technical, short, user-facing, documentation) |
| `references/examples.md` | Wrong / right pairs. Load if a draft is still off-register. |
| Claude extra `hooks/strip-em-dash.mjs` | Host extra that replaces U+2014 with `-`. Hyphen is the house mark. |

## Core

- Lead with the answer.
- State facts literally. Do not invent metaphors, idioms, or catchy labels.
- Open with what is true or what to do. Contrast with a negation only if it adds information.
- Write for a reader who has not seen the tool calls or workspace documents. Restate what you did in plain language.
- Define project-specific terms on first use.
- Use formatting sparingly: bold only the few words that matter; backticks for file, function, and command names.
- Prefer hyphens (`-`) over em dashes (`—`).

## Add no comments

Do not add comments to existing or new code. The product opinion is **add no comments**. Do not weaken it with "unless asked" or "leave docs as appropriate."

## Quality bar

- [ ] Answer first, then supporting detail.
- [ ] No invented metaphors or labels.
- [ ] No comments added.
- [ ] Hyphens, not em dashes.
- [ ] Registers loaded when the draft is a list, technical note, short message, user-facing copy, or documentation.

## Gotchas

- "Leave documentation comments as appropriate" conflicts with **add no comments**. Keep the latter.
- A gallery of wrong/right pairs in the skill itself shrinks the exploration space. Keep pairs in `references/examples.md`.
- Extra registers belong in `references/registers.md`, not restated here.
