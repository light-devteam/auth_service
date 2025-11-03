from enum import StrEnum


class PostgresLocks(StrEnum):
    FOR_UPDATE = 'FOR UPDATE'
    FOR_NO_KEY_UPDATE = 'FOR NO KEY UPDATE'
    FOR_SHARE = 'FOR SHARE'
    FOR_KEY_SHARE = 'FOR KEY SHARE'
