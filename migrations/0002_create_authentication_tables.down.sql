drop index if exists idx_ips_ip;
drop index if exists idx_ips_session_id;
drop index if exists uq_ips_session_ip;

drop table if exists "auth".ips;



drop index if exists uq_refresh_tokens_session_active;
drop index if exists idx_refresh_tokens_session_id;

drop table if exists "auth".refresh_tokens;



drop index if exists idx_sessions_account_id;

drop table if exists "auth".sessions;



drop index if exists idx_identities_provider_id;
drop index if exists idx_identities_account_id;
drop index if exists uq_identities_account_main_true;

alter table if exists "auth".identities
    drop constraint if exists uq_identities_account_provider;

drop table if exists "auth".identities;



drop index if exists idx_providers_is_active;

alter table if exists "auth".providers
    drop constraint if exists uq_providers_name;

drop table if exists "auth".providers;



drop table if exists "auth".accounts;
