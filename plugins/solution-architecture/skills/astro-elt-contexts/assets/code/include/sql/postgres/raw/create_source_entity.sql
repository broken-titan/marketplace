CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.source_entity (
    source_id         text        NOT NULL,
    source_updated_at timestamptz NOT NULL,
    payload           jsonb       NOT NULL,
    ingested_at       timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (source_id, source_updated_at)
);
