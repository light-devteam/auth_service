from dependency_injector.wiring import inject, Provide

from src.contexts.authentication.domain.repositories import IAccountRepository
from src.contexts.authentication.domain.entities import Account
from src.contexts.authentication.domain.services import IdentityDomainService
from src.domain.value_objects import AccountID
from src.infrastructure.persistence import PostgresUnitOfWork
from src.contexts.authentication.application.interfaces import IAccountService

class AccountApplicationService(IAccountService):
    @inject
    def __init__(
        self,
        repository: IAccountRepository = Provide['accounts_auth_repository'],
        database_context: PostgresUnitOfWork = Provide['postgres_uow'],
        identity_domain_service: IdentityDomainService = Provide['identity_domain_service'],
    ) -> None:
        self._repository = repository
        self._db_ctx = database_context
        self._identity_domain_service = identity_domain_service

    async def create(self) -> Account:
        account = Account.create()
        async with self._db_ctx as ctx:
            await self._repository.create(ctx, account)
        return account

    async def get_by_id(self, id: AccountID) -> Account:
        async with self._db_ctx as ctx:
            account = await self._repository.get_by_id_with_identities(ctx, id)
            return account
