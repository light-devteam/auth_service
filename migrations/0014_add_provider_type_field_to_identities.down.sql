DROP TRIGGER IF EXISTS trg_sync_provider_type ON "auth".identities;
DROP FUNCTION IF EXISTS sync_provider_type();
ALTER TABLE "auth".identities DROP CONSTRAINT IF EXISTS chk_provider_type_not_empty;
ALTER TABLE "auth".identities DROP COLUMN IF EXISTS provider_type;