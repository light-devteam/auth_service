from src.system.domain.repositories import IHealthProbe
from src.infrastructure.persistence import PostgresUnitOfWork


class PostgresProbe(IHealthProbe):
    def __init__(self) -> None:
        ...

    @property
    def name(self) -> str:
        return 'PostgreSQL'

    async def probe(self, ctx: PostgresUnitOfWork) -> None:
        await ctx.connection.execute('select 1')
