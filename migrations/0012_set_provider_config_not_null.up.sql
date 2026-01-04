update "auth".providers set config = '{}' where config is null or config = 'null';

alter table "auth".providers
    alter column config set not null,
    alter column config set default '{}';