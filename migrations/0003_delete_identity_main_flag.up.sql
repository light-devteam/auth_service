drop index if exists "auth".uq_identities_account_main_true;

alter table "auth".identities drop column if exists is_main;
