---
name: strategy-diagnosis
description: >-
  Use when the challenge is unclear and a strategy needs a theory of the
  problem before policies. Diagnosis only: root causes, dissenting views,
  data when it exists. Writes docs/<slug>-strategy-diagnosis.md.
---

Write the **diagnosis only**. Do not author guiding policies or a vision.

Playbook: sibling `engineering-strategy/references/diagnosis.md`. Consume `docs/<slug>-strategy-explore.md` when it exists.

## Process

1. Read exploration if it exists. If exploration is empty, do a short gather first — still no vision.
2. Follow `references/diagnosis.md`: theory of the challenge, dissenting views, data or **Data: missing**. A complaint list or a restated preferred solution is unfinished.
3. Write `docs/<slug>-strategy-diagnosis.md`. Use `D1`, `D2`, … ids. Include what a good policy would have to survive.

Hand the file to `engineering-strategy` for policies and operations. Do not invent those here.

## Easy mistakes

- A restated preferred solution is not a theory.
- Missing data marked as a fact invents evidence.
- Policies authored here skip `engineering-strategy`.

## Quality bar

- [ ] Theory, not a complaint list
- [ ] At least one dissenting view is stated fairly
- [ ] Every cause has an evidence path or is marked missing
- [ ] No policy section
