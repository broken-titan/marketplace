from airflow.providers.http.hooks.http import HttpHook

SOURCE_ID_FIELD = "id"
SOURCE_UPDATED_FIELD = "updated_at"


def _normalize(item: dict) -> dict:
    return {
        "source_id": item[SOURCE_ID_FIELD],
        "source_updated_at": item[SOURCE_UPDATED_FIELD],
        "payload": item,
    }


def fetch_since(updated_after: str, page_size: int = 200) -> list[dict]:
    hook = HttpHook(http_conn_id="source_api", method="GET")
    offset = 0
    items: list[dict] = []
    while True:
        response = hook.run(
            endpoint="ENTITY_PATH",
            extra_options={
                "params": {
                    "updated_after": updated_after,
                    "offset": offset,
                    "limit": page_size,
                }
            },
        )
        response.raise_for_status()
        page = response.json()
        batch = page if isinstance(page, list) else page.get("items", [])
        if not batch:
            break
        items.extend(_normalize(row) for row in batch)
        if len(batch) < page_size:
            break
        offset += page_size
    return items
