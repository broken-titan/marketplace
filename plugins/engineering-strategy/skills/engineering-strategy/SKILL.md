---
name: engineering-strategy
description: >-
  Use when staff-plus, architecture, or engineering-lead work needs a living
  engineering strategy: migrations, platform bets, API deprecation, hiring
  concentration, or "what is our engineering strategy." Runs explore,
  diagnose, refine, policy, and operations. Writes
  docs/engineering-strategy.md (or docs/<slug>-engineering-strategy.md)
  in reader order.
---

Craft a **living engineering strategy** in the consuming repo.

Write-order playbooks: `references/exploration.md`, `references/diagnosis.md`, `references/refine.md`, `references/policy.md`, `references/operations.md`. Publish shape: `references/template.md`.

Sibling skills: `strategy-explore`, `strategy-diagnosis`, `strategy-refine`, `strategy-operations`, `strategy-evaluate`. Consume their artifacts when they are current.

**Coherent action** lives in specs, architecture decisions, and living design docs already in the repo. This skill **links** those files.

A single ticket or a feature living spec is the wrong altitude. Point the user at those artifacts instead.

## Refuse

- Starting with a vision statement. Explore and diagnose come first.
- Inventing a strategy with no evidence in the repo. Interview or stop.
- A “policy” that names no tradeoff.
- Named-company examples. Keep the repo’s own placeholders if it already uses them.
- Setting **In force** without a cheap test (unless refine was skipped as a short internal loop) or without human sign-off.

## Write order

Skip refine only when `references/refine.md` says the problem is a short internal loop — and say why.

1. **Explore** — industry / state of the art plus implicit strategy already in this repo. Consider alternatives before attaching to one approach. Reuse `strategy-explore` when current.
2. **Diagnose** — theory of the challenge; dissenting views; data or missing. Reuse `strategy-diagnosis` when current.
3. **Refine** — pick what fits: strategy testing (cheap narrow trial), systems modeling, Wardley mapping. Reuse `strategy-refine` when current.
4. **Set policy** — explicit tradeoffs mapped to diagnoses. Stays in this skill.
5. **Operations** — inspect / exception / cadence. Reuse `strategy-operations` when current.

## Publish order (the file readers see)

Invert for readers: **Policy, Operations, Refine, Diagnose, Explore**. Same file. Do not split a “thinking” doc from a “policy-only” doc.

## Output

Write `docs/engineering-strategy.md`, or `docs/<slug>-engineering-strategy.md` when the repo already scopes by slug. Follow `references/template.md`.

Status is **Draft** until a named human signs off **and** a cheap test exists (or refine was explicitly skipped). Only then set **In force**.

## Gotchas

- Write order is explore → diagnose → refine → policy → operations. Publish inverted. A file that leads with exploration hides the policy from readers.
- In force without a named human and a cheap test (or a justified skip) is unfinished.
- A policy that names no tradeoff is a vision statement.
- Named-company examples leak a prior engagement.

## Quality bar

- [ ] Exploration listed (repo paths, alternatives, state of the art)
- [ ] Diagnosis is a theory; dissenting views are represented
- [ ] Refine named: test / map / model / both / skip (with reason)
- [ ] Each policy has a tradeoff, a diagnosis map, and an operation
- [ ] File is in reader order
- [ ] Status is Draft until sign-off and a cheap test (or justified skip)
