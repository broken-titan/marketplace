# Warehouse dialect cards

Set `WAREHOUSE_DIALECT` before parse. `sql_loader` and `get_hook` read it. Values `azure_sql` or `postgres`.

Do not mix dialects in one SQL file. Do not keep a third copy under `include/sql/raw`.

## azure_sql

Env `WAREHOUSE_DIALECT=azure_sql`.
Profile `StandardSQLServerAuthProfileMapping`.
Driver `ODBC Driver 18 for SQL Server`.
Adapter `dbt-sqlserver`.
JSON `nvarchar(max)` + `JSON_VALUE` / `TRY_CONVERT`.
Upsert `MERGE ... WHEN NOT MATCHED`.
Types `nvarchar`, `datetime2`.
Cosmos namespace `mssql://{host}:{port}`.
OS packages `unixodbc`, `unixodbc-dev`. Install `msodbcsql18` as root, then the venv as `astro`.

## postgres

Env `WAREHOUSE_DIALECT=postgres`.
Profile `PostgresUserPasswordProfileMapping`.
Adapter `dbt-postgres`.
JSON `jsonb` + `->>`.
Upsert `INSERT ... ON CONFLICT`.
Cosmos namespace `postgres://{host}:{port}`.
No ODBC packages.

## Other adapters

Same gates. Add `include/sql/{adapter}/` plus the Cosmos profile mapping. Extend `get_hook` and `dialect_root`.
