import os
from pathlib import Path

_SQL_ROOT = Path(__file__).resolve().parent / "sql"
_ALIASES = {"mssql": "azure_sql", "sqlserver": "azure_sql"}


def dialect_root() -> Path:
    raw = os.environ.get("WAREHOUSE_DIALECT")
    if not raw:
        raise RuntimeError("Set WAREHOUSE_DIALECT to azure_sql or postgres")
    folder = _ALIASES.get(raw, raw)
    path = _SQL_ROOT / folder
    if not path.is_dir():
        raise RuntimeError(f"No SQL dialect folder at {path}")
    return path


def read_sql(*parts: str) -> str:
    return dialect_root().joinpath(*parts).read_text()


def sql_path(*parts: str) -> str:
    return str(dialect_root().joinpath(*parts))
