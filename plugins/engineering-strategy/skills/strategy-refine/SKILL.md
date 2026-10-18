---
name: strategy-refine
description: >-
  Use before org-wide pressure, when a strategy still has load-bearing
  uncertainty. Modes: test / map / model / both / skip. Strategy testing
  is a cheap narrow trial. Wardley mapping and systems modeling zoom out
  or close a loop. Writes docs/<slug>-strategy-refine.md.
---

Refine a strategy problem. **One skill, five modes.**

Playbook: sibling `engineering-strategy/references/refine.md`.

## Modes

Infer from the ask. If unclear, ask once.

- **test** — cheap narrow trial (one component, one module, or one integration) before rollout. Stop when the load-bearing uncertainty is resolved.
- **map** — Wardley (users, needs, capabilities; genesis → commodity × visibility)
- **model** — systems sketch (stocks, flows, feedback)
- **both** — more than one technique, one implications list
- **skip** — short internal loop; write the reason and stop

An untested strategy is org-wide pressure with no trial. Name that. Situational awareness first. Do not jump to a policy.

## Output

`docs/<slug>-strategy-refine.md`: mode, the test/map/model or skip-reason, implications for diagnosis and policy ids. The full `engineering-strategy` skill links this file.

Stay generic. Use the repo’s placeholders if it has them.

## Easy mistakes

- Skip used to dodge a load-bearing uncertainty is not a short internal loop.
- A map or model with no implications is decoration.
- Jumping to policy from this skill skips the living-doc skill.

## Quality bar

- [ ] Mode is named
- [ ] Skip is used only for a short internal loop, with a reason
- [ ] A test names scope, question, and outcome (or that it has not run)
- [ ] A map or model that ran has implications, not decoration
