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
from src.domain.value_objects import AccountID
from src.infrastructure.persistence.postgres import get_constraint_name


class IdentityRepository(repositories.IIdentityRepository):
    _table_name = 'auth.identities'

    __only_one_provider_on_account_uq_constraint = 'uq_identities_account_provider'
    __only_one_login_on_type_uq_constraint = 'uq_search_provider_type_login'

    @inject
    def __init__(
        self,
        mapper: mappers.IdentityMapper = Provide['auth.identity_mapper'],
    ) -> None:
        self._mapper = mapper

    async def create(
        self,
        ctx: PostgresUnitOfWork,
        identity: entities.Identity,
    ) -> None:
        query = f"""
        insert into {self._table_name} (
            id,
            account_id,
            provider_id,
            credentials,
            created_at,
            last_used_at
        ) values ($1, $2, $3, $4, $5, $6)
        """
        try:
            await ctx.connection.execute(
                query,
                identity.id,
                identity.account_id,
                identity.provider_id,
                json.dumps(identity.credentials),
                identity.created_at,
                identity.last_used_at,
            )
        except UniqueViolationError as exc:
            constraint_name = get_constraint_name(exc)
            match constraint_name:
                case self.__only_one_provider_on_account_uq_constraint:
                    raise exceptions.IdentityForProviderAlreadyExists()
                case self.__only_one_login_on_type_uq_constraint:
                    raise exceptions.IdentityLoginAlreadyExists()
                case _:
                    raise exceptions.InfrastructureException()

    async def get_by_account_id(
        self,
        ctx: PostgresUnitOfWork,
        account_id: AccountID,
        page: int = 1,
        page_size: int = 100,
    ) -> list[entities.Identity]:
        offset = (page - 1) * page_size
        query = f"""
        select * from {self._table_name}
        where account_id = $3
        order by created_at desc
        offset $1 limit $2
        """
        raw_identities = await ctx.connection.fetch(
            query,
            offset,
            page_size,
            account_id,
        )
        identities = []
        for raw_identity in raw_identities:
            identities.append(self._mapper.to_entity(raw_identity))
        return identities

    async def get_by_account_and_provider(
        self,
        ctx: PostgresUnitOfWork,
        account_id: AccountID,
        provider_type: value_objects.ProviderType,
    ) -> entities.Identity:
        query =f"""
        select * from {self._table_name}
        where
            account_id = $1
            and provider_type = $2
        """
        identity = await ctx.connection.fetchrow(
            query,
            account_id,
            provider_type.value,
        )
        if not identity:
            raise exceptions.IdentityNotFound()
        return self._mapper.to_entity(identity)

    async def get_by_id(
        self,
        ctx: PostgresUnitOfWork,
        id: value_objects.IdentityID,
    ) -> entities.Provider:
        identity = await ctx.connection.fetchrow(
            f'select * from {self._table_name} where id = $1',
            id,
        )
        if not identity:
            raise exceptions.IdentityNotFound()
        return self._mapper.to_entity(identity)

    async def get_by_provider_and_login(
        self,
        ctx: PostgresUnitOfWork,
        provider_type: value_objects.ProviderType,
        login: str,
    ) -> entities.Identity:
        query =f"""
        select * from {self._table_name}
        where
            provider_type = $1
            and (credentials ->> 'login') = $2
        """
        identity = await ctx.connection.fetchrow(
            query,
            provider_type.value,
            login,
        )
        if not identity:
            raise exceptions.IdentityNotFound()
        return self._mapper.to_entity(identity)

    async def update(
        self,
        ctx: PostgresUnitOfWork,
        *identities: entities.Identity,
    ) -> None:
        if not identities:
            return
        query = f"""
        update {self._table_name}
        set 
            account_id = $2,
            provider_id = $3,
            credentials = $4,
            created_at = $5,
            last_used_at = $6
        where id = $1
        """
        values = [(
            identity.id,
            identity.account_id,
            identity.provider_id,
            json.dumps(identity.credentials),
            identity.created_at,
            identity.last_used_at,
        ) for identity in identities]
        try:
            await ctx.connection.executemany(query, values)
        except UniqueViolationError as exc:
            constraint_name = get_constraint_name(exc)
            match constraint_name:
                case self.__only_one_provider_on_account_uq_constraint:
                    raise exceptions.IdentityForProviderAlreadyExists()
                case self.__only_one_login_on_type_uq_constraint:
                    raise exceptions.IdentityLoginAlreadyExists()
                case _:
                    raise exceptions.InfrastructureException()
