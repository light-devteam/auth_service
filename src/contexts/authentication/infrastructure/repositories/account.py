from dependency_injector.wiring import inject, Provide

from src.contexts.authentication.domain.repositories import IAccountRepository
from src.infrastructure.repositories import AccountRepository as AccountWithoutIdentitiesRepo
from src.infrastructure.persistence.postgres import PostgresUnitOfWork
from src.contexts.authentication.domain import entities, exceptions, mappers
from src.domain.value_objects import AccountID


class AccountRepository(AccountWithoutIdentitiesRepo, IAccountRepository):
    @inject
    def __init__(
        self,
        mapper: mappers.AccountMapper = Provide['account_auth_mapper'],
    ) -> None:
        self._mapper = mapper

    async def get_by_id_with_identities(self, ctx: PostgresUnitOfWork, id: AccountID) -> entities.Account:
        account = await ctx.connection.fetchrow(
            f'select * from {self._table_name} where id = $1',
            id,
        )
        if not account:
            raise exceptions.AccountNotFound()
        return self._mapper.to_entity(account)
