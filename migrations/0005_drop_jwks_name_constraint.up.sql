do $$
declare
    constraint_name text;
begin
    select tc.constraint_name into constraint_name
    from information_schema.table_constraints tc
    where tc.table_name = 'jwks' 
        and tc.table_schema = 'auth'
        and tc.constraint_type = 'UNIQUE'
        and exists (
            select 1 from information_schema.key_column_usage kcu
            where kcu.constraint_name = tc.constraint_name
                and kcu.column_name = 'name'
        );
    
    if constraint_name is not null then
        execute format('alter table "auth"."jwks" drop constraint %I', constraint_name);
    end if;
end $$;