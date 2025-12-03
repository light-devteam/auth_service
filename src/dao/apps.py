from typing import Any, Optional

from asyncpg import Connection, Record

from src.dao.base import BaseDAO
from src.specifications import BaseSpecification
from src.enums import PostgresLocks


class AppsDAO(BaseDAO):
    _TABLE_NAME = 'auth.apps'

    __APP_TYPES_TABLE_NAME = 'auth.app_types'

    @classmethod
    async def create(
        cls,
        connection: Connection,
        columns_to_values: dict[str, Any],
        returning_columns: list[str] | None = None,
    ) -> Record:
        """Create a new row in the table.

        Args:
            connection (Connection): asyncpg connection.
            columns_to_values (dict[str, Any]): columns to be inserted with their values.
            returning_columns (list[str] | None, optional): list of columns names that values must be returned. Defaults to None.

        Returns:
            Record: asyncpg Record of the created row.
        """
        columns = []
        values = []
        for column, value in columns_to_values.items():
            columns.append(column)
            values.append(value)
        columns_pattern = ', '.join(columns)
        values_datas = []
        for index, column_name in enumerate(columns, 1):
            if column_name == 'type':
                values_datas.append(f'(select id from {cls.__APP_TYPES_TABLE_NAME} where name = ${index})')
                continue
            values_datas.append(f'${index}')
        values_pattern = ', '.join(values_datas)
        statement = f'insert into {cls._TABLE_NAME} ({columns_pattern}) values ({values_pattern})'
        if returning_columns:
            returning = ', '.join(returning_columns)
            statement += f' returning {returning}'
        return await connection.fetchrow(statement, *values)

    @classmethod
    async def get(
        cls,
        connection: Connection,
        columns: list[str],
        *specifications: BaseSpecification,
        page: int = 1,
        page_size: int = 100,
        lock: Optional[PostgresLocks] = None,
    ) -> list[Record]:
        """Select rows from the table.

        Args:
            connection (Connection): asyncpg connection.
            columns (list[str]): list of columns names to be selected.
            *specifications (BaseSpecification): conditions to filter rows.
            page (int, optional): page offset. Defaults to 1.
            page_size (int, optional): limit rows count. Defaults to 100.
            for_update (bool, optional): if you select data for update. Defaults to False.

        Returns:
            list[Record]: list of asyncpg Records.
        """
        statement_parameters = []
        column_names = []
        for column in columns:
            if column == 'type':
                column_names.append(f't.name {column}')
                continue
            column_names.append(f'a.{column}')
        columns_pattern = ', '.join(column_names)
        statement = f'select {columns_pattern} from {cls._TABLE_NAME} a'
        statement = f'{statement} left join {cls.__APP_TYPES_TABLE_NAME} t on t.id = a.type'
        if specifications:
            statement, statement_parameters = BaseDAO.add_conditions(
                statement,
                statement_parameters,
                *specifications,
            )
        offset = page_size * (page - 1)
        statement = f'{statement} limit {page_size} offset {offset}'
        if lock:
            statement = f'{statement} {lock.value}'
        return await connection.fetch(statement, *statement_parameters)
