---
name: writing-error-messages
description: Use when writing or revising an error the user will see.
---

# Error messages

Every user-facing error has three parts, in this order:

1. **What happened** — the failure in plain language.
2. **Why** — the cause the user can act on.
3. **Next steps** — what the user should do now.

Write for the **user**, not the implementing engineer. Load overlays only when the host matches.

## Files

| File | When |
|---|---|
| `references/catalogs.md` | Overlay map (web, CLI, API, logs) |
| `references/examples.md` | Wrong / right pairs. Load if a draft is still engineer-facing. |

## Quality bar

- [ ] All three parts present, in order.
- [ ] Next steps are for the user.
- [ ] Overlay loaded only when the host matches.
- [ ] No stack traces or request IDs in the user-facing line unless the product requires them.

## Easy mistakes

- A message that names a missing column or a 500 is what happened, not why, and not next steps.
- "Contact support" without a next action fails the third part.
- Overlay catalogs must not rewrite the three-part contract.
