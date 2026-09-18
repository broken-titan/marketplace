from datetime import datetime

from airflow.decorators import dag, task
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

from include.pipeline_assets import RAW_SOURCE_ENTITY
from include.source.extract import fetch_since
from include.source.load import insert_payloads, latest_watermark
from include.sql_loader import sql_path


@dag(
    dag_id="source_ingest",
    start_date=datetime(2026, 1, 1),
    schedule="*/15 * * * *",
    catchup=False,
    max_active_runs=1,
    tags=["source", "ingest"],
    default_args={"retries": 2},
)
def source_ingest():
    ensure_raw = SQLExecuteQueryOperator(
        task_id="ensure_raw_table",
        conn_id="warehouse",
        sql=sql_path("raw", "create_source_entity.sql"),
    )

    @task
    def extract() -> list[dict]:
        return fetch_since(latest_watermark())

    @task(outlets=[RAW_SOURCE_ENTITY])
    def load(items: list[dict]) -> dict:
        return {"rows": insert_payloads(items)}

    ensure_raw >> load(extract())


source_ingest()
