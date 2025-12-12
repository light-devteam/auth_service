create extension if not exists "uuid-ossp";

create schema if not exists "auth";

create table if not exists "auth"."jwks" (
    id uuid default uuid_generate_v4() primary key not null,
    name varchar(255) unique not null,
    public jsonb not null,
    private bytea not null,
    is_active boolean default true not null,
    is_primary boolean default false not null,
    created_at timestamptz default now() not null
);


create index if not exists idx_jwk_keys_is_active on "auth"."jwks" (is_active);

create index if not exists idx_jwk_keys_public_gin on "auth"."jwks" using gin(public);

create unique index if not exists idx_uq_jwk_is_primary
    on "auth"."jwks" (is_primary)
    where is_primary = true;