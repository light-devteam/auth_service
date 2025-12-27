from dependency_injector.wiring import inject, Provide

from src.domain.repositories import IAccountRepository
from src.infrastructure.persistence.postgres import PostgresUnitOfWork
from src.domain import entities, value_objects, exceptions, mappers


class AccountRepository(IAccountRepository):
    _table_name = 'auth.accounts'

    @inject
    def __init__(
        self,
        mapper: mappers.AccountMapper = Provide['account_mapper'],
    ) -> None:
        self._mapper = mapper

    async def create(
        self,
        ctx: PostgresUnitOfWork,
        account: entities.Account,
    ) -> None:
        query = f"""
        insert into {self._table_name} (
            id
        ) values ($1)
        """
        await ctx.connection.execute(query, account.id)

    async def get_by_id(
        self,
        ctx: PostgresUnitOfWork,
        id: value_objects.AccountID,
    ) -> entities.Account:
        account = await ctx.connection.fetchrow(
            f'select * from {self._table_name} where id = $1',
            id,
        )
        if not account:
            raise exceptions.AccountNotFound()
        return self._mapper.to_entity(account)
