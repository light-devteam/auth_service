from dependency_injector.wiring import inject, Provide

from src.contexts.authentication.domain.repositories import IAccountRepository
from src.domain.entities import Account
from src.domain.value_objects import AccountID
from src.domain import IDatabaseContext
from src.contexts.authentication.application.interfaces import IAccountService

class AccountApplicationService(IAccountService):
    @inject
    def __init__(
        self,
        repository: IAccountRepository = Provide['auth.accounts_repository'],
        database_context: IDatabaseContext = Provide['infrastructure.postgres_uow'],
    ) -> None:
        self._repository = repository
        self._db_ctx = database_context

    async def create(self) -> Account:
        account = Account.create()
        async with self._db_ctx as ctx:
            await self._repository.create(ctx, account)
        return account

    async def get_by_id(self, id: AccountID) -> Account:
        async with self._db_ctx as ctx:
            account = await self._repository.get_by_id(ctx, id)
            return account
