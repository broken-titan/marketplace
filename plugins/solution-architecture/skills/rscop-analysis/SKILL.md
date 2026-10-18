---
name: rscop-analysis
description: >-
  Use when producing a non-functional requirements analysis (Reliability,
  Security, Cost, Operations, Performance) from a SOW, discovery notes, or
  client intake. Every row gets a measurable target and an evidence basis.
---

**Hard rule:** Never mention a prior client, person, repository, product, or industry from any earlier engagement. Substitute `{Client}`, `{End customer}`, `{Upstream system}`, `{Source repo}`, and `{Technical contact}` only inside the OUTPUT document — fill those tokens from THIS project's sources, or leave the brace tokens when the source is silent.

This file is a **recipe**. Copy the starter catalog into a new analysis. Do not ship this skill's wording as the deliverable.

Pass: `references/pass.md`. Envelope: `references/envelope.md`. Catalog: `references/catalog.md`. Overlays off until flagged: `references/overlays.md`. Paths: `references/artifacts.md`. Context-only: `references/context.md`.

## Interface

| Field | Shape |
|-------|--------|
| Evidence | **Explicit** / **Implied** / **Default** / **Open** — exact names |
| IDs | `R-C#` `R-E#` `S-*` `C-*` `O-*` `P-*` `T#` from `catalog.md` |
| Output | `docs/rscop-<project-slug>.md` |

Ask the envelope (web/SaaS vs data pipeline vs API vs other) before loading page-load, session, WCAG, or admin-UI rows.

SOW is an input. Next file is typically `docs/sad-<slug>.md` via `solutions-architecture-document`.

## Easy mistakes

- Silence is Open or a flagged Default — not a "no", and not ECS/Fargate, DAST-every-build, or HIBP.
- A Default promoted to Explicit without a cited sentence invents a lock.
- O-E26 (deploy target) left Open must stay Open or be asked; do not assume a cloud runtime.
- Prior-engagement nouns in the output fail the hard rule.

## Quality bar

- [ ] Envelope asked first
- [ ] Every row has a measurable target or a named Open owner
- [ ] Evidence names are the four above
- [ ] No prior-client names
- [ ] File path is `docs/rscop-<project-slug>.md`
