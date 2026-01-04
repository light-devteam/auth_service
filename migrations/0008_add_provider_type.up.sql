alter table "auth".providers 
add column if not exists type varchar(32) not null default 'unknown';
