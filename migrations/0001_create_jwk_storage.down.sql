drop index if exists "jwk".idx_jwk_keys_public_gin;
drop index if exists "jwk".idx_jwk_keys_is_active;

drop table if exists "jwk"."keys";

drop schema if exists "jwk";

drop extension if exists "uuid-ossp";