from src.contexts.system.domain.repositories import IHealthProbe
from src.infrastructure.persistence.redis import RedisSession


class RedisProbe(IHealthProbe):
    @property
    def name(self) -> str:
        return 'Redis'

    async def probe(self, ctx: RedisSession) -> None:
        await ctx.connection.ping()
