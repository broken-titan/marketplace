# Procedure

## 1. Gather evidence

Walk the data path once, in movement order, and note for each hop the file that proves it:

- The base branch: `git merge-base <base> <head>`, then `git diff --diff-filter=D --name-only base..head` for what the change actually deletes. Intra-branch churn does not appear in a pull request and must not appear on the diagram.
- Source system: the workbooks, forms or API objects users fill in and the field names they show.
- Puller or sync code: the function that copies each source object, and which fields it strips, renames or drops.
- Warehouse or database: the table and column names, from migrations or DDL.
- Orchestrator: the DAG file and its task ids as they exist now, plus the SQL each task runs.
- Staging or landing: the model fields and any key such as `source_id` that identifies the feed.
- Promotion or transform: the command or job, the lookups it does, and the outputs it writes.
- Domain models: the model class and the fields the previous step fills.
- Presentation: the grid, report or endpoint and the columns it shows.

Use grep on model files, SQL files and DAG folders rather than memory; a lane drawn from memory is the usual source of stale task ids.

## 2. Write the spec

Copy the contract from `spec.md`. Assign columns by stream first (for example receipt, prep, results, instrument), then place each card. Give every card its fields. Add edges hop by hop, labelling only subsets and renames.

## 3. Build

```
python <skill-dir>/scripts/build_lanes.py spec.json out.html
```

The script fails on an edge that names an unknown card or a card that names an unknown lane.

## 4. Verify

Open `out.html` in the browser pane and check: no console errors, all lanes present in order, no route crossing a card it does not touch, labels readable, dark theme legible, page width fits without horizontal scroll of the body.

## 5. Re-check

```
python <skill-dir>/scripts/check_spec.py spec.json --repo-root <repos>
```

Run it whenever the spec, the renderer or the branch moves. A diagram goes stale quietly: a file gets renamed, a lane's pinned commit falls behind, a constant the diagram quotes gets edited. Put those quotes in `<spec>.claims.json` so the script can hold the picture to the code.

## 6. Publish

Somewhere that refuses SVG (Azure DevOps pull-request attachments among them) takes a PNG:

```
python <skill-dir>/scripts/to_png.py diagram.svg diagram.png --scale 2
```

A PNG is a still. The pulses, the walkthrough and the file links live only in the SVG, so put the SVG where the reader can still reach it and let the PNG be the picture in the thread. A scoped view rasterises far more legibly than the whole diagram, because it is fewer columns wide.

Publish as an artifact when the user wants a link, or send the file when they want the HTML. On a redeploy keep the same file path so the URL is stable.
