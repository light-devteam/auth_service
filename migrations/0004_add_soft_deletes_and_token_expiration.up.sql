alter table "auth".apps
    add column deleted_at timestamptz null,
    drop constraint "uq_apps_account_id_name",
    drop column type;

drop table if exists "auth".app_types;

create unique index "uq_apps_account_id_name_not_deleted"
    on "auth".apps(account_id, name)
    where deleted_at is null;

alter table "auth".app_tokens
    add column expires_at timestamptz null,
    add column revoked_at timestamptz null,
    drop constraint "uq_apps_tokens_app_id_name";

create unique index "uq_app_tokens_app_id_name_not_revoked_not_expired"
    on "auth".app_tokens(app_id, name)
    where revoked_at is null and expires_at > created_at;

alter table "auth".app_tokens add constraint "check_token_expires_at_gt_created_at"
    check (expires_at is null or expires_at > created_at);

create index "idx_apps_deleted_at"
    on "auth".apps(deleted_at)
    where deleted_at is null;

create index "idx_app_tokens_revoked_at"
    on "auth".app_tokens(revoked_at)
    where revoked_at is null;