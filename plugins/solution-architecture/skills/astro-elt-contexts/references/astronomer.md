# Astronomer rules

Only Astro Learn, Astro product docs, or Cosmos docs.

## Project layout

`astro dev init` creates `dags/`, `include/`, `plugins/`, `tests/`, `Dockerfile`, `packages.txt`, `requirements.txt`, `airflow_settings.yaml`, `.env`.

Learn "Manage Airflow code" puts reusable scripts and SQL under `include/` (example `include/sql/transforms.sql`).

WHEN adding Python helpers or SQL that Dags import — `include/`.
WHEN adding a Dag — `dags/{dag_id}.py`.
WHEN adding an Airflow plugin — `plugins/`.
DO NOT invent a second top-level layout. DO NOT put credentials in a shared Dockerfile.

## Connections

Astro customers — Environment Manager first.
Local CLI — `airflow_settings.yaml` and `.env` (local only).
Shared or prod — secrets backend or UI.

WHEN referencing source, warehouse, or app — `conn_id` + hook.
DO NOT put URIs in Dag files.

## DAG writing (Learn "DAG best practices")

- Idempotent tasks. No `datetime.today()` for windows.
- Atomic tasks. Extract, load, and transform are separate retry surfaces.
- Incremental extract when a cursor exists (last-modified preferred, sequence id if append-only).
- Treat the Dag file as config. Heavy work in hooks, operators, and `include/`.
- Provider packages before custom Python.
- `retries` at least 2. Cosmos Learn repeats this for dbt tasks.
- No top-level I/O.

WHEN TaskFlow — paging, watermark, row mapping.
WHEN a plain operator — one provider action with no extra logic.
DO NOT one task that extracts, maps vendor codes, and writes the app.

## XCom

Metadata XCom is for small results.

WHEN the incremental page set is small — extract may return JSON to load.
WHEN the payload is large — object storage or write SQL in the load path.
DO NOT return unbounded source history through XCom.

## Split Dags

WHEN ingest cadence differs from transform, or a failed transform must not re-hit the source — separate Dags + Assets.
WHEN the hop is one small graph — one Dag + `DbtTaskGroup`.
DO NOT default to `ExternalTaskSensor`.

## Assets

Producer `outlets=[Asset(...)]`, consumer `schedule=[Asset(...)]`. Airflow does not inspect the table.

Import (Learn / Airflow 3) — `from airflow.sdk import Asset, dag, task`.
Airflow 2 — `from airflow.datasets import Dataset as Asset`.

`catchup=False` unless you backfill with an interval filter.

## Cosmos

`astronomer-cosmos` in `requirements.txt`.
dbt in a venv (`dbt_venv`) because dbt and Airflow conflict.

```
ExecutionConfig(dbt_executable_path=f"{AIRFLOW_HOME}/dbt_venv/bin/dbt")
```

dbt path (pick one per repo)

| Path | WHEN |
|---|---|
| `dags/dbt/{warehouse}` | Default. Path from `Path(__file__)`. |
| `include/dbt/{warehouse}` | Dags-only deploys must skip dbt. |
| `astro dbt deploy` | dbt has its own repo. |

`DbtDag` — the whole Dag is dbt.
`DbtTaskGroup` — dbt is one stage.

`emit_datasets` defaults True on LOCAL / VIRTUALENV / WATCHER / AIRFLOW_ASYNC.
URIs are OpenLineage. Adapter namespace + database/schema/table. Airflow 2 uses dots; Airflow 3 uses slashes. Copy from the UI after first parse.

Use the Cosmos profile mapping for the warehouse adapter (`conn_id={warehouse}`). DO NOT commit secrets in `profiles.yml`.

`operator_args={"install_deps": True}` when `packages.yml` exists and deps are not in the image.

`source_rendering_behavior` defaults to none. WHEN source freshness must block models — `WITH_TESTS_OR_FRESHNESS`.

## Transform home

WHEN the change is SQL in the warehouse — dbt + Cosmos.
WHEN the change is "POST these rows to an API" — provider hook after the mart.
DO NOT pandas-map vendor codes in Python if dbt can do it.
