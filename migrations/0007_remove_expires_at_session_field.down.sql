alter table "auth".sessions add column if not exists expires_at timestamptz default (now() + interval '30 days');

update "auth".sessions set expires_at = default where expires_at is null;

alter table "auth".sessions alter column expires_at set not null;