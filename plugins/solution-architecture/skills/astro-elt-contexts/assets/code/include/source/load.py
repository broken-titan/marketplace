import json

from include.sql_loader import read_sql
from include.warehouse import get_hook


def latest_watermark(default: str = "1970-01-01T00:00:00Z") -> str:
    row = get_hook().get_first(read_sql("raw", "select_source_watermark.sql"))
    if not row or row[0] is None:
        return default
    value = row[0]
    return value.strftime("%Y-%m-%dT%H:%M:%SZ") if hasattr(value, "strftime") else str(value)


def insert_payloads(items: list[dict]) -> int:
    if not items:
        return 0
    hook = get_hook()
    merge_sql = read_sql("raw", "merge_source_entity.sql")
    for item in items:
        hook.run(
            merge_sql,
            parameters=(item["source_id"], item["source_updated_at"], json.dumps(item["payload"])),
        )
    return len(items)
