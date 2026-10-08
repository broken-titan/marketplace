INSERT INTO raw.source_entity (source_id, source_updated_at, payload)
VALUES (%s, %s, %s::jsonb)
ON CONFLICT (source_id, source_updated_at) DO NOTHING;
