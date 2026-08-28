---
name: astro-elt-contexts
description: Design, generate, or review Astronomer Astro ELT that lands a source API into a warehouse, transforms with Cosmos dbt, and publishes a contract to a downstream app. Trigger on Astro, Cosmos, Airflow Assets, staging/intermediate/marts, bounded-context hops, provider hooks, or inbound publish APIs. Apply every gate. Keep vendor product names out of templates.
---

# Astro ELT contexts

Open a gate before writing files. Name the gate and its label (ASTRONOMER or DOMAIN).

Roles, not products.

| Role | Means |
|---|---|
| source | vendor API / SaaS / LIMS behind HTTP |
| warehouse | SQL warehouse Cosmos runs dbt against |
| app | downstream system that consumes a published contract |

Tokens in templates `{source}`, `{entity}`, `{app}`, `{warehouse}`. Replace from the user's systems. Do not keep example vendor names.

Read only if the gate is not enough.

- `references/astronomer.md` — Astro / Cosmos
- `references/domain.md` — ACL / hops
- `references/layers.md` — staging / intermediate / marts
- `references/add-entity.md` — new source entity
- `references/dialects.md` — warehouse SQL dialect cards

Copy from `assets/code/`.

Required env `WAREHOUSE_DIALECT` is `azure_sql` or `postgres`. Hooks and SQL paths fail closed if it is missing.

Default cut is three Dags, `dags/dbt/{warehouse}`, providers + Cosmos. Change a default only when a gate says so.

## Gate 1 — extract stack

Label ASTRONOMER.

WHEN landing a documented HTTP API into the warehouse.

THEN provider hooks (`HttpHook` plus the warehouse SQL hook / `SQLExecuteQueryOperator`). Conn ids `{source}_api`, `{warehouse}`.

WHEN NOT the user named a different extract library.

DO NOT invent a vendor SDK. DO NOT query a vendor graph database from Airflow. DO NOT add dlt unless the user names it.

## Gate 2 — one Dag or three

Label ASTRONOMER.

WHEN ingest cadence differs from transform, or a failed transform must not re-hit the source.

THEN three Dags + Assets. Names `{source}_ingest`, `{warehouse}_transform`, `{app}_publish`.

WHEN ingest and transform share cadence and the graph is small.

THEN one Dag, extract/load tasks, then `DbtTaskGroup`.

DO NOT use `ExternalTaskSensor` as the first cross-Dag link. DO NOT put extract + dbt + app write in one task.

## Gate 3 — DbtDag vs DbtTaskGroup

Label ASTRONOMER (Cosmos glossary).

WHEN the Dag contains only dbt.

THEN `DbtDag`.

WHEN dbt sits next to extract, load, or HTTP.

THEN `DbtTaskGroup`.

DO NOT wrap a whole ingest Dag in `DbtDag`.

## Gate 4 — dbt project path

Label ASTRONOMER.

WHEN this repo / no extra constraint.

THEN `dags/dbt/{warehouse}`. `ProjectConfig` from `Path(__file__)`.

WHEN dags-only deploys must not ship dbt.

THEN `include/dbt/{warehouse}`.

WHEN dbt lives in its own git repo.

THEN `astro dbt deploy`.

DO NOT hardcode `/usr/local/airflow/...`. DO NOT invent a fourth location.

## Gate 5 — schedule

Label ASTRONOMER.

WHEN a downstream Dag must wait on a table or model the upstream task just wrote.

THEN producer `outlets=[Asset(...)]`, consumer `schedule=[Asset(...)]`.

WHEN the job is time-only.

THEN cron or `@hourly`.

WHEN both time and data matter.

THEN `AssetOrTimeSchedule`.

DO NOT cron the transform Dag and hope ingest finished.

`catchup=False` unless the extract filter is the Airflow interval. A destination `MAX(updated_at)` plus `catchup=True` does not replay history.

## Gate 6 — Asset URI

Label ASTRONOMER (Cosmos OpenLineage).

WHEN the producer is an ingest load task.

THEN declare the URI in `include/pipeline_assets.py` and put it on that task's `outlets`.

WHEN the producer is a Cosmos model.

THEN copy the URI from the Airflow UI after first parse. Format depends on adapter and Airflow 2 vs 3. See `references/astronomer.md`.

DO NOT guess the Cosmos URI from a made-up host.

## Gate 7 — layer

Label DOMAIN for meaning. Folder names are dbt Labs, not Astro.

WHEN Airflow just landed the payload.

THEN `raw` table. Source document. `include/sql/raw`.

WHEN you only rename, cast, or extract JSON fields.

THEN `stg_{source}_{entity}`.

WHEN meaning, grain, or a shared warehouse entity changes.

THEN `int_{entity}`.

WHEN an app or BI tool may read the table.

THEN `marts/{app}_{entity}` plus `contract_version`.

WHEN hop 2 maps warehouse language into the app.

THEN the app inbound port (HTTP/ORM). Not Airflow SQL into the app primary schema.

DO NOT put source vendor codes on a mart. DO NOT parse source JSON in a mart. DO NOT put `contract_version` on intermediate. DO NOT name folders bronze/silver/gold.

## Gate 8 — intermediate yes or no

Label DOMAIN applied to dbt Labs layers. Details in `references/layers.md`.

WHEN any of meaning change, grain change, two marts share the entity, copied CASE/JOIN, or tests must lock warehouse language.

THEN add `int_*`.

WHEN all of staging already is the published entity, one consumer, aliases only, mart would be `select` from `stg_`.

THEN skip intermediate. Staging → mart.

DO NOT add `int_{app}_{entity}` that duplicates a mart. DO NOT add intermediate "for consistency."

## Gate 9 — SQL home

Label ASTRONOMER (`include/sql`) plus DOMAIN (no app-primary-schema SQL).

WHEN DDL, MERGE/upsert into raw, watermark, or mart SELECT.

THEN `include/sql/{dialect}/...` via `include.sql_loader`. Dialect from `references/dialects.md`.

WHEN the SQL is a warehouse model.

THEN `dags/dbt/{warehouse}/models/...`.

DO NOT embed warehouse SQL in `dags/*.py`. DO NOT MERGE into the app primary schema.

## Gate 10 — load vs transform

Label ASTRONOMER (atomic tasks) plus DOMAIN (dialect).

WHEN writing source bytes into the warehouse.

THEN idempotent upsert on `(source_id, source_updated_at)` (or the documented cursor). Payload as the warehouse JSON/text type.

WHEN changing meaning or grain inside the warehouse.

THEN dbt incremental merge in intermediate or marts.

DO NOT map vendor status codes in Python if dbt can do it.

## Gate 11 — app write

Label DOMAIN.

WHEN the app must see a warehouse entity.

THEN incremental mart SELECT (watermark bound), POST `{app}_api`. Persist the last posted cursor after a successful POST. The template `select_app_publish_watermark.sql` is an epoch stub so copy-paste does not look like it already tracks state; replace it with last-successful-POST storage before using this in anger.

WHEN a second app needs the same warehouse entity.

THEN new mart from the same `int_*`. Do not fork intermediate.

DO NOT INSERT/MERGE the app primary schema from Airflow. DO NOT give Airflow the app DB as a load destination.

## Gate 12 — HTTP call shape

Label ASTRONOMER.

WHEN GET with query params.

THEN `HttpHook.run(endpoint, extra_options={"params": {...}})`.

WHEN one POST of a ready body.

THEN `HttpOperator` or Hook with `json=`.

WHEN paging or a watermark.

THEN Hook inside `@task`.

DO NOT pass GET query params as `data=` (that is a body). Confirm path and cursor from the source API doc.

## Gate 13 — XCom size

Label ASTRONOMER.

WHEN the incremental batch is a small page set.

THEN extract may return JSON to load.

WHEN the body is large or unbounded.

THEN land object storage or write SQL in the load task. Return a count or path.

DO NOT XCom full source history.

## Gate 14 — connections

Label ASTRONOMER.

WHEN local Astro CLI.

THEN `airflow_settings.yaml` / `.env`. Local only.

WHEN Astro Deployment.

THEN Environment Manager or a secrets backend.

DO NOT put connection strings in Dag files or a committed `profiles.yml`.

## Gate 15 — new source entity

Label DOMAIN process, Astronomer files.

WHEN adding a collection other than the first entity.

THEN follow `references/add-entity.md` in order. Confirm the REST path from the source API doc first.

DO NOT guess field names. DO NOT treat template tokens as a vendor spec.

## Always

ASTRONOMER — idempotent tasks, atomic extract vs load vs transform, retries >= 2, incremental cursor if one exists, providers before custom Python, no parse-time I/O.

DOMAIN — raw speaks the source, intermediate speaks the warehouse, marts speak the consumer, the app does hop 2.

## Output

State the gate you applied. Use role tokens, not vendor names. Keep snippets short. On review, name the failed gate before the patch.
