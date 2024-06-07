from abc import ABC, abstractmethod
from typing import Any

from mindfulguard.database.postgresql.connection import PostgreSqlConnection


class PostgreSqlQueriesBase(ABC):
    def __init__(self, connection: PostgreSqlConnection) -> None:
        self._connection: PostgreSqlConnection = connection
        self._status_code: int
        self._response: Any

    @abstractmethod
    async def execute(self) -> None:...

    @property
    def status_code(self) -> int:
        return self._status_code