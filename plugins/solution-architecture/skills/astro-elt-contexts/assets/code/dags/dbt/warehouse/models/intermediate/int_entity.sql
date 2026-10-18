{{ config(unique_key='warehouse_id') }}

select
    source_id as warehouse_id,
    source_id as business_key,
    case
        when source_status = 'SOURCE_CODE_A' then 'warehouse_state_a'
        when source_status = 'SOURCE_CODE_B' then 'warehouse_state_b'
        else 'unmapped'
    end as state,
    source_updated_at as occurred_at,
    source_updated_at
from {{ ref('stg_source_entity') }}
{% if is_incremental() %}
where source_updated_at >
      (select coalesce(max(source_updated_at), '1970-01-01') from {{ this }})
{% endif %}
