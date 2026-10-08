{{ config(materialized='view') }}

select
    source_id,
    source_updated_at,
    cast(null as {{ dbt.type_string() }}) as source_status
from {{ source('raw', 'source_entity') }}
