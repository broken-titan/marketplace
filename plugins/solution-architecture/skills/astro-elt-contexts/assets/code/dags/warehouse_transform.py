import os
from datetime import datetime
from pathlib import Path

from cosmos import DbtDag, ExecutionConfig, ProfileConfig, ProjectConfig, RenderConfig
from cosmos.profiles import BaseProfileMapping

from include.pipeline_assets import RAW_SOURCE_ENTITY

DBT_PROJECT = Path(__file__).resolve().parent / "dbt" / "warehouse"


def _profile_mapping() -> BaseProfileMapping:
    dialect = os.environ.get("WAREHOUSE_DIALECT")
    if dialect == "postgres":
        from cosmos.profiles import PostgresUserPasswordProfileMapping

        return PostgresUserPasswordProfileMapping(
            conn_id="warehouse",
            profile_args={"schema": "public"},
        )
    if dialect in {"azure_sql", "mssql", "sqlserver"}:
        from cosmos.profiles import StandardSQLServerAuthProfileMapping

        return StandardSQLServerAuthProfileMapping(
            conn_id="warehouse",
            profile_args={
                "schema": "dbo",
                "database": os.environ.get("WAREHOUSE_DATABASE", "warehouse"),
                "driver": "ODBC Driver 18 for SQL Server",
            },
        )
    raise RuntimeError("Set WAREHOUSE_DIALECT to azure_sql or postgres")


warehouse_transform = DbtDag(
    dag_id="warehouse_transform",
    project_config=ProjectConfig(str(DBT_PROJECT)),
    profile_config=ProfileConfig(
        profile_name="warehouse",
        target_name="prod",
        profile_mapping=_profile_mapping(),
    ),
    execution_config=ExecutionConfig(
        dbt_executable_path=f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin/dbt",
    ),
    render_config=RenderConfig(select=["path:models"], emit_datasets=True),
    operator_args={"install_deps": True},
    schedule=[RAW_SOURCE_ENTITY],
    start_date=datetime(2026, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=["warehouse", "dbt"],
    default_args={"retries": 2},
)
