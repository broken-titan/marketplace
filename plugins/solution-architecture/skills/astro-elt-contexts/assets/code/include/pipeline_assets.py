try:
    from airflow.sdk import Asset
except ImportError:
    from airflow.datasets import Dataset as Asset

RAW_SOURCE_ENTITY = Asset("REPLACE_AFTER_CONFIRMING_WAREHOUSE_URI/raw.source_entity")
MART_APP_ENTITY = Asset("REPLACE_AFTER_COSMOS_PARSE/marts.app_entity")
