CREATE UNIQUE INDEX CONCURRENTLY uq_search_provider_type_login
ON "auth".identities (
    provider_type,
    (credentials->>'login')
);