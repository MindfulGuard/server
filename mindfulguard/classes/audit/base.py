from abc import ABC, abstractmethod
from fastapi import Request
from mindfulguard.classes.database import DataBase
from mindfulguard.classes.models.audit import ModelAudit
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.audit import PostgreSqlAudit


class AuditBase(ABC):
    def __init__(self, request: Request) -> None:
        self._status_code: int
        self._connection = DataBase().postgresql().connection()
        self._pgsql_audit = PostgreSqlAudit(self._connection)
        self._model_audit = ModelAudit()
        self._model_token = ModelToken()
        self._request: Request = request

    @abstractmethod
    async def execute(self) -> None:...

    @property
    def status_code(self) -> int:
        return self._status_code