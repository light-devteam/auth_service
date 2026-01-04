alter table "auth".providers 
    alter column config drop not null,
    alter column config drop default;