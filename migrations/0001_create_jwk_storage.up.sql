create extension if not exists "uuid-ossp";

create schema if not exists "jwk";

create table if not exists "jwk"."keys" (
    id uuid default uuid_generate_v4() primary key not null,
    name varchar(255) unique not null,
    public jsonb not null,
    private bytea not null,
    is_active boolean default true not null,
    created_at timestamptz default now() not null
);


create index if not exists idx_jwk_keys_is_active on "jwk"."keys" (is_active);

create index if not exists idx_jwk_keys_public_gin on "jwk"."keys" using gin(public);