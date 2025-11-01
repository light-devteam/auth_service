alter table "jwk"."keys" add column if not exists is_primary boolean default false not null;

create unique index if not exists idx_uq_jwk_is_primary
on "jwk"."keys" (is_primary)
where is_primary = true;