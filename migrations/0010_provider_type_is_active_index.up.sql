-- индекс type + is_active
create index concurrently if not exists idx_providers_type_active 
on "auth".providers(type, is_active) where is_active = true;