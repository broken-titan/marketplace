import os

from airflow.providers.common.sql.hooks.sql import DbApiHook


def get_hook() -> DbApiHook:
    dialect = os.environ.get("WAREHOUSE_DIALECT")
    if dialect == "postgres":
        from airflow.providers.postgres.hooks.postgres import PostgresHook

        return PostgresHook(postgres_conn_id="warehouse")
    if dialect in {"azure_sql", "mssql", "sqlserver"}:
        from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook

        return MsSqlHook(mssql_conn_id="warehouse")
    raise RuntimeError("Set WAREHOUSE_DIALECT to azure_sql or postgres")
