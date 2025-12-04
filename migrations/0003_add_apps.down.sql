drop index if exists idx_app_tokens_app_id;

drop table if exists "auth".app_tokens;
drop table if exists "auth".apps;
drop table if exists "auth".app_types;

drop schema if exists "auth";