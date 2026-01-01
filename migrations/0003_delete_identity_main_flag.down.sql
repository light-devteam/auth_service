alter table "auth".identities add column if not exists is_main boolean default false not null;

-- Только один основной провайдер
create unique index if not exists uq_identities_account_main_true
    on "auth".identities(account_id)
    where is_main = true;
