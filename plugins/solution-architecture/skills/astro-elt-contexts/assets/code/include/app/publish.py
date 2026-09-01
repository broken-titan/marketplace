from airflow.providers.http.hooks.http import HttpHook


def post_rows(rows: list[dict]) -> dict:
    if not rows:
        return {"posted": 0}
    hook = HttpHook(http_conn_id="app_api", method="POST")
    response = hook.run(
        endpoint="/internal/entities/upsert",
        json={"contract_version": "app_entity_v1", "records": rows},
        headers={"Content-Type": "application/json"},
    )
    response.raise_for_status()
    return {"posted": len(rows), "status": response.status_code}
