# Schema document

Load `references/evidence.md` first. Write one JSON document that validates against `schema/schema.json`. Do not invent architecture to fill lanes.

## File

Use the repo's existing diagram path when it already has one. Otherwise write `docs/change-architecture/<slug>.json` and run the renderer to `docs/change-architecture/<slug>.svg`.

Ask if the slug is missing; go ahead and use the pull-request number or a short change name when one is already in the ask.

## Shape

| Field | Required | Meaning |
|---|---|---|
| `kind` | yes | Always `graph` |
| `title` | yes | Change name as it should appear on the SVG |
| `source` | no | Pull-request URL or diff ref |
| `lenses` | yes | Must include `architecture`; add `data-flow` when you have an ordered route |
| `lanes` | yes | Swimlanes (`id`, `label`) |
| `nodes` | yes | Cards: `id`, `label`, `lane`, `delta`, `evidence`; optional `kind`, `subtitle`, `cite` |
| `edges` | yes | Links: `from`, `to`, `evidence`; optional `label`, `delta`, `animated`, `cite` |
| `flows` | when `data-flow` | Routes: `id`, optional `label`, `steps` of `{ from, to, label?, kind?, animated? }` |
| `views` | no | Drill-down: `id`, `title`, `nodeIds[]` |

`delta` is `new`, `changed`, `removed`, or `unchanged`. `evidence` is `fact` or `assumption`. Node `kind` is `route`, `service`, `store`, `job`, or `other`. Flow hop `kind` is `sync`, `async`, or `return`. Ids match `^[A-Za-z][A-Za-z0-9_-]*$`.

A fact without `cite` fails validation. An assumption may omit `cite`. `unchanged` is only for a labeled assumption that the change does not touch.

Every `node.lane` must be a lane id. Every edge or flow-step `from` / `to` must be a node id. A `data-flow` lens requires at least one flow, and each flow needs at least one hop.

## Renderer

From this skill folder:

```bash
node renderer/render.mjs <document.json> <output.svg>
```

The script is first-party Node with no package dependencies. It writes one self-contained SVG: lane columns with headers, pastel node cards with NEW / CHANGED / REMOVED badges, ghost-and-strike on removed, and a thin left-to-right edge chain with sparse, even-spaced inline chevrons whose height matches the path stroke. Data-flow pulses new-path chevrons one hop at a time. Light and dark follow `prefers-color-scheme`. Do not draw a New / Changed / Removed legend or architecture step-number badges.

Do not emit Mermaid. Do not hand-author the SVG. Do not call a Coldtea CLI or package.
