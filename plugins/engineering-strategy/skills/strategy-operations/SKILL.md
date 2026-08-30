---
name: strategy-operations
description: >-
  Use when guiding policies exist and need inspection: how you tell they
  are followed, the exception path, and review cadence. Writes an
  operations table the full engineering-strategy skill can consume.
---

Write **operations** for existing policies. Do not invent a new strategy or a project plan.

Playbook: sibling `engineering-strategy/references/operations.md`.

## Process

1. Load policies from `docs/engineering-strategy.md`, `docs/<slug>-engineering-strategy.md`, or the user’s list. If there are no policies, stop and send the user to `engineering-strategy` (or `strategy-diagnosis` if the challenge is still unstated).
2. For each policy, name inspect (cannot fail silent), written exception path, and cadence (`references/operations.md`). Prefer nudges on paths people already use.
3. Prefer mechanisms this organization already runs. A new ritual needs a reason.
4. Write `docs/<slug>-strategy-operations.md` (table keyed by `P-n`). The full skill copies or links it.

## Gotchas

- Inventing a new ritual when one already exists is extra process.
- Inspect that can fail silent is not inspect.
- No policies yet: stop; do not invent a strategy here.

## Quality bar

- [ ] Every policy has inspect / exception / cadence
- [ ] Exceptions are written and findable
- [ ] Inspect and cadence cannot fail silently
- [ ] Each new ritual has a reason

