MERGE raw.source_entity AS target
USING (SELECT %s AS source_id, %s AS source_updated_at, %s AS payload) AS source
ON target.source_id = source.source_id
AND target.source_updated_at = source.source_updated_at
WHEN NOT MATCHED THEN
    INSERT (source_id, source_updated_at, payload)
    VALUES (source.source_id, source.source_updated_at, source.payload);
