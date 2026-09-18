# Domain rules (not Astronomer)

Two hops. Two languages. Airflow does not own the app schema.

| Hop | Where | Speaks |
|---|---|---|
| 1 | dbt intermediate | warehouse ubiquitous language |
| 2 | app inbound port | app enums / keys |

## Source

Confirm path, pagination, and cursor from the source API doc. Template tokens are not a spec.
Set `SOURCE_ID_FIELD` and `SOURCE_UPDATED_FIELD` in extract, then normalize to `source_id` / `source_updated_at`.

WHEN extracting — REST + `HttpHook`.
DO NOT query a vendor graph from Airflow. DO NOT invent a vendor SDK.

Raw key `(source_id, source_updated_at)` unless the API documents another cursor.
Payload stored as the warehouse JSON/text type.
Idempotent upsert. Watermark `MAX(source_updated_at)` with lag if many rows share a timestamp.

## App

Mart columns + `contract_version` only.
POST an internal upsert route on `{app}_api`.
The app maps warehouse states onto its own model.

WHEN a second app needs the same warehouse entity — new mart, same `int_*`.
DO NOT load the app primary schema from Airflow.

## Layers

Cosmos runs whatever dbt project you give it. Folder names staging / intermediate / marts are dbt Labs. See `layers.md`.
