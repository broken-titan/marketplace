---
name: solutions-architecture-document
description: >-
  Use when authoring a Solutions Architecture Document from an RSCOP analysis
  and discovery notes: overview, business context, conceptual, six architecture
  views, implementation, management, and linked ADRs.
---

Author a **Solutions Architecture Document (SAD)** for the current engagement. Recipe and outline, not a filled project document. Do not copy facts, names, or decisions from any prior engagement.

**Layers.** Living spec is feature-level. RSCOP and this SAD are engagement-level. They are not two sources of truth. Paths: sibling `rscop-analysis/references/artifacts.md`.

Section spine: `references/spine.md`. ADR patterns: `references/adrs.md`. ID map: `references/id-map.md`. SOW input: `references/sow-handoff.md`. Well-formedness: `references/iso-42010.md`. Envelope: sibling `rscop-analysis/references/envelope.md`. Overlays off until flagged: sibling `rscop-analysis/references/overlays.md`.

Write ADRs with `architecture-decision-records`. The SAD appendix lists paths and status; it does not replace that skill.

## Interface

| Input | Output |
|-------|--------|
| `docs/rscop-<slug>.md` (required) | `docs/sad-<project-slug>.md` |
| SOW, discovery notes, optional NFR matrix | Views with **What is known** + **blocked on** |
| Envelope | Skip web/SaaS-only rows when not A |

If the RSCOP file does not exist, **stop and produce it first**. Do not author a SAD from a feature list alone.

## Hard rules

- **Never invent client facts.** Missing fact → section **blocked** or **Open**, with blocking requirement IDs.
- **Never mention a prior client.** Placeholders (`{Client}`, `{End customer}`, `{Upstream system}`, `{Source repo}`, `{Technical contact}`, `{Inheriting team}`) appear only in the generated SAD.
- **Defaults are load-bearing.** Do not silently promote a Default to a locked decision.
- **Open stays Open.** A working assumption is allowed only when labeled and the user asked to keep moving.
- **Cross-link, do not duplicate.** Cite RSCOP row IDs; do not recopy every NFR table.
- **Cite catalog IDs only.** `O-E26` not a guessed number. P-E1 is read latency.

## Distinct milestones

Treat **code complete** and **customer live** as distinct whenever the end customer is gated (`O-C5`). Warranty and load-test verification start at customer-live. Collapse the two only when the end customer *is* the client and no external gate exists.

## Deploy

`O-E26` Open: leave Open or ask. Do not default a cloud runtime. If the user names a working assumption, label it and keep the container twelve-factor / generic. Silence does not enable ECS/Fargate, DAST-every-build, HIBP, or a regime.

## Easy mistakes

- Authoring a SAD from a feature list with no RSCOP invents the NFR spine.
- A Default used as a design input without saying so looks locked.
- Catalog ID drift (`O-E29`, wrong P-E1) breaks the RSCOP handoff.
- Seven catalog ADR patterns inherited as Accepted from another engagement are the wrong status.

## Quality bar

- [ ] Filename is `docs/sad-<project-slug>.md` and the header links the RSCOP
- [ ] No proper nouns from any other engagement
- [ ] Every concrete number cites a row ID or is a labeled working assumption
- [ ] Code-complete and customer-live split iff an external gate exists
- [ ] Each Section 4 view has a "blocked on" list or "nothing blocking"
- [ ] Deploy target is Open or a *user-labeled* assumption
