# Spec contract

One JSON object with `schemaVersion`, `title`, `lede`, `lanes`, `cards`, `edges`, and optional `layout`.

`schemaVersion` is a semver string; this build speaks `1.0.0` and accepts any `1.x`. The builder validates the whole spec before drawing and reports every problem at once, including unknown keys, so a typo fails loudly rather than silently dropping.

## lanes

Ordered top to bottom.

| Field | Required | Meaning |
|-------|----------|---------|
| `id` | yes | Referenced by `cards[].lane`. |
| `label` | yes | System name shown at the left edge. |
| `sub` | no | One short line under the label: what this system does to the data. |
| `color` | no | CSS colour for this lane, overriding the palette slot (`--l0`..`--l7` by lane order). |
| `source` | no | URL template for this lane's repository, with a `{path}` placeholder and an optional `{line}`. Required before any card in the lane may list `files`. |

## cards

| Field | Required | Meaning |
|-------|----------|---------|
| `id` | yes | Referenced by edges. |
| `lane` | yes | A `lanes[].id`. |
| `col` | yes | Zero-based stream column; same column across lanes means the same stream. |
| `title` | yes | The artifact as the system names it (workbook, function, table, DAG task, model, grid). |
| `fields` | yes | Strings, one per field or tight field group, spelled as the system spells them. |

A `title` or a `fields` entry may open with a delta marker: `+ ` new, `~ ` changed, `- ` removed. `build_lanes.py` strips the marker, records the delta on the card or field, colours it and counts it into the line under the lede. A card's delta comes from its title. Text that legitimately starts with one of those markers has to be reworded.
| `span` | no | Number of columns the card covers, default 1. |
| `y` | no | Order inside a column when two cards share a lane, column and row, default 0. |
| `kind` | no | What the card is, drawn as a glyph: `workbook`, `function`, `module`, `table`, `query`, `task`, `endpoint`, `model`, `command`, `grid`, `other`. |
| `files` | no | Repository-relative paths backing this card, each `path` or `path:line`. Rendered as links in the card footer through the lane's `source`. |

A card fed by another card in the same lane is placed on its own row below it; the rows come from the lane's own edges, not from the spec.

## edges

Each edge is `[sourceCardId, targetCardId, label]`, or `[sourceCardId, targetCardId, label, emphasis]` where emphasis is `normal` (default), `hero` or `muted`.

An empty label means the whole source card flows. A non-empty label names the subset or the rename. `hero` draws the one hop the change is really about: solid and heavy against the dashed rest. `muted` fades a hop to context and stops its pulse. More than one or two `hero` edges and the emphasis stops meaning anything.

## walkthrough

Optional. Two to twelve steps; one step is a caption, and a longer tour loses the reader.

| Field | Required | Meaning |
|-------|----------|---------|
| `heading` | yes | The step's title, shown in the rail. |
| `body` | yes | One line under it. |
| `cards` | yes | Card ids this step lights. |
| `lanes` | no | Lane ids to name alongside the cards. |
| `routes` | no | Extra routes as `"from>to"`. A route whose two ends are both lit is included already, so most steps need none. |

The builder warns on stderr, without refusing to draw, when a card is lit by no step: it would stay dimmed for the whole tour.

The rail draws a numbered chip per step plus a reset. Clicking one lights that step's cards and routes and dims the rest. Stepping is `:target` in the stylesheet, not script, so it works in a standalone SVG and in the page, and a fragment in the URL (`diagram.svg#vfs4`) opens on that step. There is no autoplay and no keyboard shortcut; both would need script.

Two things the stepping rules must keep. Every element a step dims is named by id rather than by `.card:not([data-step~="n"])`: the compact form matches when asked and still never repaints on a hash change. And nothing carries an opacity transition: it stopped the browser settling on the new target's style, so stepping from one step to the next left the previous one lit.

## views

Optional, up to 8. A view is a drill-down: the part of the diagram it names, laid out on its own rather than the whole picture dimmed.

| Field | Required | Meaning |
|-------|----------|---------|
| `id` | yes | Used in the side-car filename, `out.<id>.svg`. |
| `title` | yes | The `<summary>` line in the page. |
| `summary` | no | One sentence under it. |
| `cards` | no | Card ids in scope. |
| `lanes` | no | Lane ids whose every card is in scope. |

At least one of `cards` and `lanes` must put a card in scope. An edge survives only when both its ends do, a lane only when it still holds a card, and the stream columns close up, so a view of one stream is one column wide. Views carry no walkthrough.

Each view renders into the page as a `<details>` section and, when a third path is given, as its own SVG beside the main one.

## layout

Optional overrides of the renderer constants.

| Key | Default | Meaning |
|-----|---------|---------|
| `colw` | 214 | Column width in px. |
| `gut` | 22 | Gap between columns. |
| `laneLabelW` | 150 | Width of the lane label gutter. |
| `columns` | max `col + span` across cards | Total stream columns. |

Field lines wrap to the card's own width; there is no character count to set.

## Output

`scripts/build_lanes.py spec.json out.html [out.svg] [--pr | --scale N]` lays the diagram out in Python and writes the SVG into a page with no `<!doctype>`, `<html>` or `<body>` wrapper, ready to publish as an artifact or open directly. Pass a third path to also write the bare SVG.

The SVG carries its own stylesheet and its motion is `animateMotion` in the markup, so it renders and animates on its own, including where scripts are stripped. Text is measured against a fixed advance width and pinned with `textLength`, so the same spec produces the same bytes anywhere; a line that would need a hard squeeze is cut with an ellipsis instead.

`--pr` grows the type and the vertical rhythm by 1.45 and leaves the stream columns alone. A diagram embedded in a fixed-width column is scaled to fit, so widening it with the type would cancel out; holding the width and letting cards run taller is what makes the text bigger once the column has shrunk it. On this diagram it takes field text from 7.0px to 9.5px effective in a 780px column, for 7% more width and 60% more height.

`scripts/build_lanes.py --demo` runs the self-check over marker parsing, measurement, layout and the emitted SVG.
