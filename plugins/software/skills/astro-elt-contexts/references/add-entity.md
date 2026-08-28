# Gate 15 detail

WHEN adding a source collection. Worked example token is `{entity}`.

1. REST path, pagination, cursor from the source API doc.
2. `HttpHook` + `extra_options={"params": ...}` in `include/{source}/` (the template folder is `include/source/`; rename the token, do not add a second extract tree).
3. `include/sql/raw/create_{source}_{entity}.sql` and `merge_{source}_{entity}.sql`. Key `(source_id, source_updated_at)` unless documented otherwise.
4. Warehouse hook load. Asset only if another Dag waits on this entity.
5. dbt `source` on `raw.{source}_{entity}`.
6. `stg_{source}_{entity}.sql` — typed source columns only.
7. `int_{entity}.sql` only if Gate 8 says yes.
8. `marts/{app}_{entity}.sql` with `contract_version`.
9. `include/sql/marts/select_{app}_{entity}.sql` plus publish task.
10. Paste the Cosmos mart URI into `include/pipeline_assets.py` after first parse.

WHEN the extract is large — Gate 13.
DO NOT MERGE into the app. DO NOT add intermediate "for consistency."
