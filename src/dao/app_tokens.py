from src.dao.base import BaseDAO


class AppTokensDAO(BaseDAO):
    _TABLE_NAME = 'auth.app_tokens'
