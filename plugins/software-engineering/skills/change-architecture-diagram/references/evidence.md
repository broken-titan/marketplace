# Evidence

Read the pull request, the diff, and the cited paths before you write the document.

A box or edge is a **fact** only when a path, hunk, or pull-request sentence supports it. A box or edge is an **assumption** when you inferred a neighbor, a caller, or a store the change does not show.

Keep one evidence table next to the document.

| Node or edge | Kind | Source | Mark |
|---|---|---|---|
| The name as it will appear on the diagram | `fact` or `assumption` | `path:line` or the pull-request sentence | blank, `[EVIDENCE NEEDED]`, or omit the box |

Kind is `fact` only when the source exists in this change. Kind is `assumption` when the sentence is a working guess.

Use `[EVIDENCE NEEDED]` when a box would complete the picture and no source exists; leave the box off until a source appears, or draw it only as a labeled assumption.

Never invent a service, queue, database, or runtime the change does not name. A missing neighbor stays blank or marked; do not supply a placeholder system.

Blast radius is what this change touches. It is not a full-system map and it is not a C4 design of the product.

Copy each kept row into the schema document: `evidence`, `cite` for facts, and `delta` from the mark (`new`, `changed`, `removed`). Then run `renderer/render.mjs`.
