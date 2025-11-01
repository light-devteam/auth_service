drop index if exists idx_uq_jwk_is_primary;

alter table "jwk"."keys" drop column if exists is_primary;
