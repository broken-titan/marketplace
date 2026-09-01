def upsert_records(payload: dict) -> dict:
    contract = payload.get("contract_version")
    if contract != "app_entity_v1":
        return {"error": "unsupported contract", "status": 400}
    return {"upserted": len(payload.get("records", []))}
