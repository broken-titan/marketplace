# Emit rules

## Choose a syntax

1. If the repo already contains PlantUML or C4-PlantUML (`.puml`, `@startuml`, `!include` of C4), emit **PlantUML** in that style.
2. Otherwise emit **Mermaid**. Prefer `C4Context` / `C4Container` / `C4Deployment` when the host renders them. If the repo already uses `flowchart` / `graph` for architecture, match that.

Do not introduce PlantUML into a Mermaid-only tree.

## Levels

| Level | Show | Hide |
|-------|------|------|
| Context | People, this system, neighbor systems | Containers, components, classes |
| Container | Applications, data stores, queues inside this system | Component internals, class names |
| Deployment | Nodes, runtimes, the containers that sit on them | A second invent of the Context neighbors |

A name that appears on two levels must mean the same thing. A Container on the Container diagram is a child of exactly one system on the Context diagram.

## File shape

Wrap Mermaid in a fenced `mermaid` block inside markdown so the SAD can link the file. PlantUML stays in `.puml` when that is the repo convention.

Title each diagram. Caption each relationship with a verb (uses, reads, publishes). Unlabeled edges fail the checklist.
