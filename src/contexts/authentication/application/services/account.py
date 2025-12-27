from dependency_injector.wiring import inject, Provide

from src.contexts.authentication.domain.repositories import IAccountRepository
from src.contexts.authentication.domain.entities import Account
from src.contexts.authentication.domain.services import IdentityDomainService
from src.infrastructure.persistence import PostgresUnitOfWork

class AccountApplicationService:
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
