drop index if exitst "auth".idx_uq_jwk_is_primary
drop index if exists "auth".idx_jwk_keys_public_gin;
drop index if exists "auth".idx_jwk_keys_is_active;

drop table if exists "auth"."jwks";

drop schema if exists "auth";

drop extension if exists "uuid-ossp";