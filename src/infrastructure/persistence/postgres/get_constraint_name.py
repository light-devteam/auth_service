from asyncpg import PostgresError


def get_constraint_name(exc: PostgresError) -> str:
        return exc.as_dict().get('constraint_name')
