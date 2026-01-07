ALTER TABLE "auth".identities ADD COLUMN IF NOT EXISTS provider_type varchar(32);


UPDATE "auth".identities i
SET provider_type = p.type
FROM "auth".providers p
WHERE p.id = i.provider_id
    AND i.provider_type IS NULL;


ALTER TABLE "auth".identities
    ALTER COLUMN provider_type SET NOT NULL,
    ADD CONSTRAINT chk_provider_type_not_empty CHECK (provider_type <> '');


CREATE OR REPLACE FUNCTION sync_provider_type()
RETURNS TRIGGER AS $$
BEGIN
    NEW.provider_type := (SELECT type FROM "auth".providers WHERE id = NEW.provider_id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_sync_provider_type
    BEFORE INSERT OR UPDATE OF provider_id ON "auth".identities
FOR EACH ROW EXECUTE FUNCTION sync_provider_type();