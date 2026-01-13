from src.domain.value_objects import AccountID
from src.contexts.authentication.domain.value_objects.tokens.token import Token


class OpaqueToken(Token):
    hash: bytes
    account_id: AccountID
