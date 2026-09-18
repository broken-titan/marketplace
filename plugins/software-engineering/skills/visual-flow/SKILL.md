---
name: visual-flow
description: Use when the user asks for a data-flow, lineage, or "where does this field come from" diagram that crosses several systems (source app, warehouse, orchestrator, staging, promotion, domain models, UI), or asks for a swimlane picture like pr-lens. Produces one standalone HTML page holding a single SVG of horizontal lanes, one per system, with field-level cards and routed edges.
---

# Visual flow

## Map

- `references/spec.md` — the JSON contract for lanes, cards, edges and layout knobs; read before writing a spec.
- `references/procedure.md` — evidence gathering, spec authoring, build, verification, publish.
- `assets/diagram.css` — the theme tokens and every rule the SVG uses; inlined into the SVG itself and into the page.
- `assets/page.html` — page template with the `__TITLE__`, `__LEDE__`, `__COUNTS__`, `__CSS__` and `__SVG__` slots.
- `scripts/to_markdown.py` — `python to_markdown.py spec.json --images <prefix> [--svg <url>]` writes the pull-request description: the images, the views as collapsible sections, and a table linking every card to its source, which is the part a raster loses.
- `scripts/to_png.py` — `python to_png.py diagram.svg [out.png] [--scale 2] [--dark]` rasterises through headless Chrome or Edge, for anywhere that will not take an SVG. Nothing else will do: `color-mix()`, custom properties, `mix-blend-mode` and the blur filter defeat the standalone rasterisers.
- `scripts/check_spec.py` — `python check_spec.py spec.json --repo-root DIR` re-checks a built diagram: validation, a byte-identical rebuild, draw order, walkthrough and view integrity, that every lane source still pins its repository's HEAD, and that every linked path exists. Claims about the code the diagram describes go in `<spec>.claims.json` beside the spec.
- `scripts/build_lanes.py` — layout, measurement and the SVG emitter. `python build_lanes.py spec.json out.html [out.svg]`; `--pr` (or `--scale N`) for a render that will be shrunk into a pull-request comment; `--demo` runs the self-check.

## Product opinions

1. One lane per system, top to bottom in the order the data moves, so following any route downward reads as time.
2. One card per concrete artifact (workbook, function, table, DAG task, model, grid), and every card lists the fields it carries spelled as the code or source system spells them.
3. A column is a stream; keep an entity in the same column across lanes so the eye follows it vertically, and use `span` for a card that merges streams.
4. Open a card title or field with a delta marker when a change touches it: `+ ` new, `~ ` changed, `- ` removed. The builder lifts the marker off the text, so the delta is counted and coloured rather than read as punctuation.
5. Draw what the change removed as well as what it added; a removed card carries no routes and still earns its place. A `- ` marker means removed *against the base branch*: check `git diff --diff-filter=D base..head`, never what is merely absent from the working tree. Work a branch adds and then deletes is invisible in the pull request, and drawing it as a removal describes history the reviewer will never see.
6. Give a card the `files` it is drawn from, so a reader can open the source instead of trusting the picture, and a `kind` so its glyph says what sort of thing it is.
7. Mark the one hop the change is really about `hero`, and no more than one or two of them.
8. Give the diagram a walkthrough when the change has an order to it: a handful of steps, each naming the cards it lights, so a reader can be led through rather than left to scan.
9. Add a view for a part of the change someone would want on its own; it is laid out fresh, so a single stream is one column wide rather than the whole picture with the rest faded.
10. Label a route only when it carries a subset of the source card; an unlabeled route carries the whole card.
11. When a hop renames a field, put the new name on the target card and the old name on the route label.
12. The page is the diagram alone: a title, one lede sentence, the counts line, the SVG and any views, with no field matrix, model cards or legend unless the user asks for them.
13. Derive cards from code, SQL and DAG files, and confirm each hop against the actual file before drawing it.
14. A card fed by another card in the same lane drops to its own row beneath it, so a hop inside a system still reads downward; those routes are dotted rather than dashed to mark that they never leave the lane.
15. One colour per lane, carried by that lane's band, cards and outgoing routes, so a route's colour says which system it left.
16. Keep the diagram self-contained: the SVG carries its own stylesheet and its motion, so it survives being pulled out of the page, and `prefers-reduced-motion` stops the travelling dots.

## Easy mistakes

- Drawing the orchestrator lane from DAG ids that were since merged or renamed; re-read the `dags/` folder before listing them.
- Feeding one card from three unlabeled routes, which reads as three writers of the same field; label each route with the fields it carries.
- Marking a card removed because the file is not there now. Ask git what the pull request deletes; a file the branch created and then dropped nets to nothing.
- Pointing `files` at a path that has moved, or at a lane whose `source` pins a stale commit; the link is only worth drawing if it lands.
- Writing a delta into the prose ("added work_order") instead of using the marker, which keeps it out of the counts.
- Listing a translated or display name on a card when the system stores the source name; use the stored name.
- Leaving a card with a title and no fields, which hides what the hop adds or drops.
- Putting a card on the same row as the card that feeds it, which forces the route to double back and hides its arrowhead behind the target; rows come from the lane's own edges, so add the edge and the row follows.
- Publishing the HTML with `<!doctype>`, `<html>` or `<body>` tags when the destination is an artifact, which wraps the page twice.

## Quality standards

- [ ] Every lane maps to one real system and the lanes are in data-movement order.
- [ ] Every card names fields as the source spells them and comes from a real file, table or workbook.
- [ ] Every route names a source and target card that exist, and each labelled route names the subset it carries.
- [ ] The SVG opens on its own in light and dark, and fits its container width in the page.
- [ ] Every card and field a change touched carries a marker, and the counts line matches the diff.
- [ ] Every path in `files` exists at the commit its lane's `source` pins.
- [ ] Each walkthrough step lights something, and stepping through them tells the change in order.
- [ ] Nothing on the page besides the title, lede, counts and SVG unless the user asked for more.
