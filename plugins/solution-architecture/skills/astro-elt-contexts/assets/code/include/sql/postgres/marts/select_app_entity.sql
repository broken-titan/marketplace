SELECT
    warehouse_id,
    business_key,
    state,
    occurred_at,
    source_updated_at,
    contract_version
FROM marts.app_entity
WHERE source_updated_at > %s;
