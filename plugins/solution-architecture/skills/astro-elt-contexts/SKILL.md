---
name: astro-elt-contexts
description: >-
  Use when designing, generating, or reviewing Astro / Airflow / dbt warehouse
  ELT that lands a source API, transforms, and publishes a contract. Apply
  every gate. Keep vendor product names out of templates.
---

Open a gate before writing files. Name the gate and its label (ASTRONOMER or DOMAIN).

Gates: `references/gates.md`. Roles, not products.

| Role | Means |
|---|---|
| source | vendor API or SaaS behind HTTP |
| warehouse | SQL warehouse Cosmos runs dbt against |
| app | downstream system that consumes a published contract |

Tokens in templates `{source}`, `{entity}`, `{app}`, `{warehouse}`. Replace from the user's systems. Do not keep example vendor names.

| File | When |
|---|---|
| `references/gates.md` | Before any file write |
| `references/astronomer.md` | Astro / Cosmos detail |
| `references/domain.md` | ACL / hops |
| `references/layers.md` | staging / intermediate / marts |
| `references/add-entity.md` | new source entity (gate 15) |
| `references/dialects.md` | warehouse SQL dialect cards |
| `assets/code/` | copy templates |

Required env `WAREHOUSE_DIALECT` is `azure_sql` or `postgres`. Hooks and SQL paths fail closed if it is missing.

Default cut is three Dags, `dags/dbt/{warehouse}`, providers + Cosmos. Change a default only when a gate says so.

## Always

ASTRONOMER — idempotent tasks, atomic extract vs load vs transform, retries >= 2, incremental cursor if one exists, providers before custom Python, no parse-time I/O.

DOMAIN — raw speaks the source, intermediate speaks the warehouse, marts speak the consumer, the app does hop 2.

## Output

State the gate you applied. Use role tokens, not vendor names. Keep snippets short. On review, name the failed gate before the patch.

## Easy mistakes

- Missing `WAREHOUSE_DIALECT` is fail-closed, not a guess.
- Folders named bronze/silver/gold are the wrong dialect.
- One task that extract + dbt + app-writes fails gate 2.
- Guessing a Cosmos Asset URI from a made-up host fails gate 6.
- Airflow SQL into the app primary schema fails hop 2.

## Quality bar

- [ ] Every write named a gate and label
- [ ] `WAREHOUSE_DIALECT` is set or the run stopped
- [ ] Three-Dag default unless a gate changed it
- [ ] No bronze/silver/gold folder names
- [ ] Tokens replaced from this project's systems
