IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = 'raw')
    EXEC('CREATE SCHEMA raw');

IF OBJECT_ID('raw.source_entity', 'U') IS NULL
BEGIN
    CREATE TABLE raw.source_entity (
        source_id         nvarchar(128) NOT NULL,
        source_updated_at datetime2     NOT NULL,
        payload           nvarchar(max) NOT NULL,
        ingested_at       datetime2     NOT NULL
            CONSTRAINT df_raw_source_entity_ingested_at DEFAULT SYSUTCDATETIME(),
        CONSTRAINT pk_raw_source_entity PRIMARY KEY (source_id, source_updated_at)
    );
END;
