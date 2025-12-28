from dependency_injector.wiring import inject, Provide
from asyncpg import UniqueViolationError
import json

from src.infrastructure.persistence.postgres import PostgresUnitOfWork
from src.contexts.authentication.domain import (
    value_objects,
    entities,
    repositories,
    mappers,
    exceptions,
)


class ProviderRepository(repositories.IProviderRepository):
    _table_name = 'auth.providers'

    @inject
    def __init__(
        self,
        mapper: mappers.ProviderMapper = Provide['provider_auth_mapper'],
    ) -> None:
        self._mapper = mapper

    async def create(
        self,
        ctx: PostgresUnitOfWork,
        provider: entities.Provider,
    ) -> None:
        query = f"""
        insert into {self._table_name} (
            id,
            name,
            type,
            is_active,
            created_at,
            config
        ) values ($1, $2, $3, $4, $5, $6)
        """
        try:
            await ctx.connection.execute(
                query,
                provider.id,
                provider.name,
                provider.type,
                provider.is_active,
                provider.created_at,
                json.dumps(provider.config),
            )
        except UniqueViolationError:
            raise exceptions.ProviderAlreadyExists()

    async def get_all(
        self,
        ctx: PostgresUnitOfWork,
        page: int = 1,
        page_size: int = 100,
        only_active: bool = True,
    ) -> list[entities.Provider]:
        offset = (page - 1) * page_size
        where_clause = ''
        params = [offset, page_size]
        if only_active:
            where_clause = 'where is_active = $3'
            params.append(only_active)
        query = f"""
        select * from {self._table_name}
        {where_clause}
        order by is_active desc, created_at desc
        offset $1 limit $2
        """
        raw_providers = await ctx.connection.fetch(query, *params)
        providers = []
        for raw_provider in raw_providers:
            providers.append(self._mapper.to_entity(raw_provider))
        return providers

    async def get_by_id(
        self,
        ctx: PostgresUnitOfWork,
        id: value_objects.ProviderID,
    ) -> entities.Provider:
        provider = await ctx.connection.fetchrow(
            f'select * from {self._table_name} where id = $1',
            id,
        )
        if not provider:
            raise exceptions.ProviderNotFound()
        return self._mapper.to_entity(provider)

    async def update(
        self,
        ctx: PostgresUnitOfWork,
        *providers: entities.Provider,
    ) -> None:
        if not providers:
            return
        query = f"""
        update {self._table_name}
        set 
            name = $2,
            type = $3,
            is_active = $4,
            created_at = $5,
            config = $6
        where id = $1
        """
        values = [(
            provider.id,
            provider.name,
            provider.type,
            provider.is_active,
            provider.created_at,
            json.dumps(provider.config),
        ) for provider in providers]
        try:
            await ctx.connection.executemany(query, values)
        except UniqueViolationError:
            raise exceptions.ProviderAlreadyExists()
