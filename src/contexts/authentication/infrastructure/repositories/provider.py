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
from src.infrastructure.persistence.postgres import get_constraint_name


class ProviderRepository(repositories.IProviderRepository):
    _table_name = 'auth.providers'

    __name_uq_constraint = 'uq_providers_name'
    __type_active_uq_constraint = 'uidx_providers_type_active'

    @inject
    def __init__(
        self,
        mapper: mappers.ProviderMapper = Provide['auth.provider_mapper'],
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
        config = provider.config
        if config is not None:
            config = json.dumps(provider.config)
        try:
            await ctx.connection.execute(
                query,
                provider.id,
                provider.name,
                provider.type.value,
                provider.is_active,
                provider.created_at,
                config,
            )
        except UniqueViolationError as exc:
            constraint_name = get_constraint_name(exc)
            if constraint_name == self.__name_uq_constraint:
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

    async def get_by_type(
        self,
        ctx: PostgresUnitOfWork,
        type: value_objects.ProviderType,
        page: int = 1,
        page_size: int = 100,
    ) -> list[entities.Provider]:
        offset = (page - 1) * page_size
        query = f"""
            select * from {self._table_name}
            where type = $3
            order by is_active desc, created_at desc
            offset $1 limit $2
        """
        raw_providers = await ctx.connection.fetch(query, offset, page_size, type)
        providers = []
        for raw_provider in raw_providers:
            providers.append(self._mapper.to_entity(raw_provider))
        return providers

    async def get_active_by_type(
        self,
        ctx: PostgresUnitOfWork,
        type: value_objects.ProviderType,
    ) -> entities.Provider:
        query = f"""
            select * from {self._table_name}
            where
                type = $1 and
                is_active = true
        """
        provider = await ctx.connection.fetchrow(query, type)
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
            type= $3,
            is_active = $4,
            created_at = $5,
        where id = $1
        """
        values = []
        for provider in providers:
            values.append((
                provider.id,
                provider.name,
                provider.type.value,
                provider.is_active,
                provider.created_at,
            ))
        try:
            await ctx.connection.executemany(query, values)
        except UniqueViolationError as exc:
            constraint_name = get_constraint_name(exc)
            match constraint_name:
                case self.__name_uq_constraint:
                    raise exceptions.ProviderAlreadyExists()
                case self.__type_active_uq_constraint:
                    exc_detail: str = exc.as_dict().get('detail', '')
                    try:
                        value_part = exc_detail.split('=', 1)[1]
                    except:
                        value_part = ''
                    start = value_part.find('(')
                    end = value_part.rfind(')', start)
                    if start == -1 or end == -1:
                        provider_type = '?'
                    provider_type = value_part[start + 1 : end].strip()
                    raise exceptions.ProviderAlreadyExists(
                        f'Active provider for type `{provider_type}` already exists',
                    )
                case _:
                    raise exceptions.InfrastructureException()
