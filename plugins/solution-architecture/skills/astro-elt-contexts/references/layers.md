# Gate 8 detail

dbt Labs names. `raw` is pre-dbt. No bronze/silver/gold folders.

## Staging

One model per source table. Folder by source system. Name `stg_{source}_{entity}`. Usually a view.

WHEN — rename, cast, JSON field extract, drop untyped rows.
WHEN NOT — status maps, new ids, grain change, consumer column names, `contract_version`.

## Intermediate

Optional. Name `int_{entity}` or `int_{entity}_{verb}`.

WHEN any of

- meaning changes (vendor code → warehouse state)
- grain changes (array → child rows)
- two marts need the same warehouse entity
- the CASE/JOIN would be copied into every mart
- tests must lock warehouse language before a consumer contract

WHEN NOT all of

- staging already is the published entity
- one consumer
- mapping is aliases
- the mart would be `select ... from stg_`

DO NOT `int_{app}_{entity}` that duplicates a mart.
DO NOT `contract_version` here.
DO NOT leftover source JSON extract here.

## Marts

Public product. Name `{app}_{entity}` after the consumer thing.

WHEN — an app or BI tool may read this table.
WHEN NOT — dump intermediate plus extra source columns.

Incremental merge on the published key. Include `contract_version`.

`contract: enforced` on every mart. Tests are gates, not comments: `unique`, `not_null`, `accepted_values`, `relationships`, and source freshness. A failing test blocks the transform Dag. Keep dbt Labs layer names (staging / intermediate / marts) as the default. Medallion rename only if flagged.
