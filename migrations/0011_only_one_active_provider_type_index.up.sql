-- только один активнный provider на type
create unique index concurrently if not exists uidx_providers_type_active 
on "auth".providers(type) where is_active = true;