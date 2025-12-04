create schema if not exists "auth";

create table if not exists "auth".app_types (
    id uuid default uuid_generate_v4() primary key not null,
    name varchar(16) not null unique
);

insert into "auth".app_types (name) values
('internal'),
('external');

create table if not exists "auth".apps (
    id uuid default uuid_generate_v4() primary key not null,
    account_id uuid not null,
    name varchar(64) not null,
    description varchar(255),
    type uuid not null references "auth".app_types(id) on delete cascade,
    created_at timestamptz default now() not null,
    constraint "uq_apps_account_id_name" unique(account_id, name)
);

create table "auth".app_tokens (
    id uuid default uuid_generate_v4() primary key not null,
    app_id uuid not null references "auth".apps(id) on delete cascade,
    name varchar(64) not null,
    hash text not null,
    created_at timestamptz default now() not null,
    constraint "uq_apps_tokens_app_id_name" unique(app_id, name)
);

create index if not exists idx_app_tokens_app_id on "auth".app_tokens(app_id);

