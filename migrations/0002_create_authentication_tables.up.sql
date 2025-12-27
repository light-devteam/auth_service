create table if not exists "auth".accounts (
    id uuid default uuid_generate_v4() primary key not null
);

create table if not exists "auth".providers (
    id uuid default uuid_generate_v4() primary key not null,
    name varchar(255) not null,
    type varchar(32) not null,
    is_active boolean default true not null,
    created_at timestamptz default now() not null,
    config jsonb null
);

-- Уникальность name
alter table "auth".providers add constraint uq_providers_name unique(name);

-- Выборка только активных
create index if not exists idx_providers_is_active on "auth".providers(is_active);


create table if not exists "auth".identities (
    id uuid default uuid_generate_v4() primary key not null,
    account_id uuid references "auth".accounts not null,
    provider_id uuid references "auth".providers not null,
    provider_data jsonb not null,
    is_main boolean default false not null,
    created_at timestamptz default now() not null,
    last_used_at timestamptz default now() not null
);

-- По 1 провайдеру на каждый аккаунт
alter table "auth".identities
    add constraint uq_identities_account_provider unique(account_id, provider_id);

-- Только один основной провайдер
create unique index if not exists uq_identities_account_main_true
    on "auth".identities(account_id)
    where is_main = true;

--Выборка по id аккаунта
create index if not exists idx_identities_account_id on "auth".identities(account_id);
--Выборка по id провайдера
create index if not exists idx_identities_provider_id on "auth".identities(provider_id);

-- Общий GIN по всему JSONB
-- create index if not exists gin_identities_provider_data
--     on "auth".identities
--     using gin (provider_data);

-- Expression index, если часто надо фильтровать по конкретному полю
-- create index if not exists idx_identities_provider_subject
--     on "auth".identities ((provider_data->>'subject'));


create table if not exists "auth".sessions (
    id uuid default uuid_generate_v4() primary key not null,
    account_id uuid references "auth".accounts not null,
    provider_id uuid references "auth".providers not null,
    created_at timestamptz default now() not null,
    expires_at timestamptz not null,
    revoked_at timestamptz null
);

-- Выборка по аккаунту
create index if not exists idx_sessions_account_id on "auth".sessions(account_id);


create table if not exists "auth".refresh_tokens (
    id uuid default uuid_generate_v4() primary key not null,
    session_id uuid references "auth".sessions not null,
    hash bytea not null,
    created_at timestamptz default now() not null,
    expires_at timestamptz not null,
    revoked_at timestamptz null
);

-- Один активный refresh token на одну сессию
create unique index if not exists uq_refresh_tokens_session_active
    on "auth".refresh_tokens(session_id)
    where revoked_at is null;
    -- expires_at > now()

-- Выборка по id сессии
create index if not exists idx_refresh_tokens_session_id on "auth".refresh_tokens(session_id);


create table if not exists "auth".ips (
    id uuid default uuid_generate_v4() primary key not null,
    session_id uuid references "auth".sessions not null,
    ip inet not null,
    seen_at timestamptz default now() not null
);

-- Один ip на сессию, если еще раз встречается - просто нужно обновить seen_at
create unique index if not exists uq_ips_session_ip on "auth".ips(session_id, ip);

-- Выборка по id сессии
create index if not exists idx_ips_session_id on "auth".ips(session_id);
-- Выборка по ip
create index if not exists idx_ips_ip on "auth".ips(ip);