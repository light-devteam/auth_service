drop index if exists "idx_app_tokens_revoked_at";

drop index if exists "idx_apps_deleted_at";

alter table "auth".app_tokens drop constraint if exists "check_token_expires_at_gt_created_at";

drop index if exists "uq_app_tokens_app_id_name_not_revoked_not_expired";

alter table "auth".app_tokens
    drop column if exists expires_at,
    drop column if exists revoked_at,
    add constraint "uq_apps_tokens_app_id_name" unique(app_id, name);

drop index if exists "uq_apps_account_id_name_not_deleted";

create table "auth".app_types (
    id uuid default uuid_generate_v4() primary key not null,
    name varchar(16) not null unique
);

insert into "auth".app_types (name) values
    ('internal'),
    ('external');

alter table "auth".apps
    drop column if exists deleted_at,
    add column type uuid not null references "auth".app_types(id) on delete cascade,
    add constraint "uq_apps_account_id_name" unique(account_id, name);