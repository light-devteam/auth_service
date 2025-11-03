create extension if not exists "uuid-ossp";

create schema if not exists "accounts";

create table if not exists "accounts"."accounts" (
    id uuid default uuid_generate_v4() primary key not null,
    telegram_id bigint not null unique
);