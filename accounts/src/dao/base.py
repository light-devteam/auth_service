from abc import ABC, abstractmethod
from typing import Any, Optional

from asyncpg import Record
from asyncpg.connection import Connection

from src.exceptions import DeleteAllRowsException, UpdateAllRowsException
from src.specifications import AndSpecification, BaseSpecification
from src.enums import PostgresLocks


class BaseDAO(ABC):
    _TABLE_NAME: str

    @staticmethod
    def add_conditions(
        statement: str,
        statement_parameters: list[Any],
        *specifications: BaseSpecification,
        index: int = 1,
    ) -> tuple[str, list[Any]]:
        combined_specifications = AndSpecification(*specifications)
        filters, parameters = combined_specifications.to_sql(index)
        statement = f'{statement} where {filters}'
        statement_parameters.extend(parameters)
        return statement, statement_parameters

    @classmethod
    @abstractmethod
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
        values_pattern = ', '.join(f'${index}' for index in range(1, len(columns)+1))
        statement = f'insert into {cls._TABLE_NAME} ({columns_pattern}) values ({values_pattern})'
        if returning_columns:
            returning = ', '.join(returning_columns)
            statement += f' returning {returning}'
        return await connection.fetchrow(statement, *values)

    @classmethod
    @abstractmethod
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
        columns_pattern = ', '.join(columns)
        statement = f'select {columns_pattern} from {cls._TABLE_NAME}'
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

    @classmethod
    @abstractmethod
    async def update(
        cls,
        connection: Connection,
        columns_to_values: dict[str, Any],
        *specifications: BaseSpecification,
        update_all: bool = False,
    ) -> str:
        """Update rows in the table.

        Args:
            connection (Connection): asyncpg connection
            columns_to_values (dict[str, Any]): columns to be updated with their new values
            *specifications (BaseSpecification): conditions to filter rows to be updated
            update_all (bool, optional): are you really want update all of rows? Defaults to False.

        Raises:
            UpdateAllRowsException: if you are trying to update all rows without update_all=True

        Returns:
            str: postgres execute result (UPDATE <number_of_updated_rows>)
        """
        if not specifications and not update_all:
            raise UpdateAllRowsException(
                f'You are trying to update all rows from a table {cls._TABLE_NAME}. '
                'If you are sure, set update_all to True.'
            )
        start_conditions_index = 1
        columns = []
        statement_parameters = []
        for index, update_data in enumerate(columns_to_values.items(), 1):
            column, value = update_data
            start_conditions_index = index
            columns.append(f'{column} = ${index}')
            statement_parameters.append(value)
        set_statement = ', '.join(columns)
        statement = f'update {cls._TABLE_NAME} set {set_statement}'
        if specifications:
            statement, statement_parameters = BaseDAO.add_conditions(
                statement,
                statement_parameters,
                *specifications,
                index=start_conditions_index+1,
            )
        return await connection.execute(statement, *statement_parameters)

    @classmethod
    @abstractmethod
    async def delete(
        cls,
        connection: Connection,
        *specifications: BaseSpecification,
        delete_all: bool = False,
    ) -> str:
        """Delete rows from the table.

        Args:
            connection (Connection): asyncpg connection.
            *specifications (BaseSpecification): conditions to filter rows to be deleted.
            delete_all (bool, optional): are you really want to delete all of rows? Defaults to False.

        Raises:
            DeleteAllRowsException: if you are trying to delete all rows without delete_all=True

        Returns:
            str: postgres execute result (DELETE <number_of_deleted_rows>)
        """
        if not specifications and not delete_all:
            raise DeleteAllRowsException(
                f'You are trying to delete all rows from a table {cls._TABLE_NAME}. '
                'If you are sure, set delete_all to True.'
            )
        statement_parameters = []
        statement = f'delete from {cls._TABLE_NAME}'
        if specifications:
            statement, statement_parameters = BaseDAO.add_conditions(
                statement,
                statement_parameters,
                *specifications,
            )
        return await connection.execute(statement, *statement_parameters)
