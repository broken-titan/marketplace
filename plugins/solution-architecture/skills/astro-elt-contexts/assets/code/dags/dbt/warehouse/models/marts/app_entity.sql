{{ config(unique_key='warehouse_id') }}

select
    warehouse_id,
    business_key,
    state,
    occurred_at,
    source_updated_at,
    'app_entity_v1' as contract_version
from {{ ref('int_entity') }}
{% if is_incremental() %}
where source_updated_at >
      (select coalesce(max(source_updated_at), '1970-01-01') from {{ this }})
{% endif %}
