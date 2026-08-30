---
name: c4-diagrams
description: >-
  Use when the deliverable is a C4 diagram: Context and Container, plus
  Deployment when asked. One skill, four modes (design, prose, review,
  update). Emit Mermaid, or PlantUML when the repo already uses it.
---

Produce a **standalone C4 diagram deliverable**. One skill, four modes. Do not split into four agents.

C4 *notation rules* that already belong in SAD overlays stay there (`rscop-analysis/references/overlays.md`). This skill writes the diagram.

Checklist: `references/checklist.md`. Emit rules: `references/emit.md`.

## Modes

Infer from the ask. If unclear, ask once.

| Mode | When | What you produce |
|------|------|------------------|
| **design** | Greenfield, or "draw the system" | Context + Container from evidence |
| **prose** | "Walk the model" before boxes | Short prose model, then the same diagrams |
| **review** | Diagrams already exist | Checklist findings only; no silent redraw |
| **update** | The system changed | Revised diagrams; list what moved |

**Deployment** is an extra diagram, only when the user asks or an Explicit deploy target exists. Leave deploy **Open** when the target is Open.

## Evidence

Read the repo, RSCOP, SAD, and named notes. Every box and edge must come from that evidence or a labeled working assumption. Do not import a prior engagement's nouns.

## Emit

Follow `references/emit.md`.

- Default: **Mermaid** (`C4Context`, `C4Container`, `C4Deployment`, or flowchart fallback).
- **PlantUML** only when the repo already has `.puml` / C4-PlantUML files.
- Always emit **Context** and **Container** unless the user asked for a single level.
- Write under the repo's existing diagram path, else `docs/c4/<slug>-context.md` and `docs/c4/<slug>-container.md` (Deployment beside them when asked).

A SAD may *link* these files. Do not recopy the full notation guide into the SAD.

## Review checklist (all modes that emit or review)

From `references/checklist.md`:

- Every box has a name
- No orphan edges
- Levels agree (a Container thing appears inside its Context system)
- People, systems, and containers stay on the level that owns them

Review mode reports fails; it does not "fix" by inventing boxes.

## Gotchas

- Review mode that silently redraws hides the findings.
- A Deployment diagram with an Open deploy target invents a runtime.
- PlantUML on a Mermaid-only repo (or the reverse) fights the existing tree.

## Quality bar

- [ ] Mode is named in the output
- [ ] Context and Container exist (or the user scoped to one level)
- [ ] Deployment exists only when asked or Explicit
- [ ] Emit format matches the repo (Mermaid vs existing PlantUML)
- [ ] Checklist passes, or review mode lists every fail
