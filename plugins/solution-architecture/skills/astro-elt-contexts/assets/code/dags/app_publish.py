from datetime import datetime

from airflow.decorators import dag, task

from include.app.publish import post_rows
from include.pipeline_assets import MART_APP_ENTITY
from include.sql_loader import read_sql
from include.warehouse import get_hook

_MART_COLUMNS = [
    "warehouse_id",
    "business_key",
    "state",
    "occurred_at",
    "source_updated_at",
    "contract_version",
]


def latest_publish_watermark(default: str = "1970-01-01T00:00:00Z") -> str:
    row = get_hook().get_first(read_sql("marts", "select_app_publish_watermark.sql"))
    if not row or row[0] is None:
        return default
    value = row[0]
    return value.strftime("%Y-%m-%dT%H:%M:%SZ") if hasattr(value, "strftime") else str(value)


@dag(
    dag_id="app_publish",
    start_date=datetime(2026, 1, 1),
    schedule=[MART_APP_ENTITY],
    catchup=False,
    max_active_runs=1,
    tags=["app", "publish"],
    default_args={"retries": 2},
)
def app_publish():
    @task
    def read_mart() -> list[dict]:
        records = get_hook().get_records(
            read_sql("marts", "select_app_entity.sql"),
            parameters=(latest_publish_watermark(),),
        )
        return [dict(zip(_MART_COLUMNS, row)) for row in records]

    @task
    def publish(rows: list[dict]) -> dict:
        return post_rows(rows)

    publish(read_mart())


app_publish()
