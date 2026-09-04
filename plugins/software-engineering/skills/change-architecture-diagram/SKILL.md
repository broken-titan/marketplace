---
name: change-architecture-diagram
description: >-
  Use when turning a pull request or a diff into blast-radius and
  data-flow diagrams without inventing architecture.
---

# Change architecture diagram

## Files

| File | When |
|---|---|
| `references/evidence.md` | Facts, assumptions, and what the change actually touches |
| `references/schema.md` | How to write a schema-valid document |
| `schema/schema.json` | Document contract |
| `renderer/render.mjs` | First-party SVG renderer |

## Interface

| Input | Output |
|---|---|
| A pull request, a diff, or cited changed paths | A schema-valid JSON document, then self-contained SVG from `renderer/render.mjs` |

## Hard rules

- Load `references/evidence.md`, gather cited evidence, and write one schema-valid document; invent no service, store, or edge.
- Mark every node `new`, `changed`, or `removed` from that evidence, or `unchanged` only as a labeled assumption.
- Set `evidence` to `fact` or `assumption` on every node and edge, and cite a path or hunk on every fact.
- Run this skill's `renderer/render.mjs` on that document and write or attach the SVG it emits.
- Emit no Mermaid, as a primary path or as a fallback.
- Do not vendor, fork, wrap, or call `@coldtea/pr-lens-*`, `npx @coldtea/pr-lens-cli`, or any Coldtea package.

## Quality standards

- [ ] Evidence table exists and every box or edge is a cited fact or a labeled assumption
- [ ] Document validates against `schema/schema.json` and names only evidence-backed parts
- [ ] First-party renderer wrote a self-contained SVG with lanes, cards, and green / amber / red delta
- [ ] Ordered data-flow steps are numbered so a human can trace the route
- [ ] No Mermaid was emitted
- [ ] No Coldtea package or CLI was used
- [ ] Facts and assumptions are split in the sentence that uses them

## Easy mistakes

- If you drew a service the diff does not name, delete it or mark it as an assumption with no claimed fact.
- If the blast-radius diagram is an unmarked full-system map, cut it to the files and modules the change touches and mark new, changed, and removed.
- If you skipped the data-flow pipeline, add the ordered steps the change actually moves.
- If you emitted Mermaid or a hand-authored SVG as the diagram, delete that emit and run `renderer/render.mjs` on a schema-valid document.
- If you reached for Node packages other than this skill's renderer, stop and run `renderer/render.mjs`.
