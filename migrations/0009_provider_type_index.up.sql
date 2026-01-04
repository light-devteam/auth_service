-- индекс type
create index concurrently if not exists idx_providers_type 
on "auth".providers(type);