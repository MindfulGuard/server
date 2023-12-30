from abc import ABC, abstractmethod
from typing import Any
from mindfulguard.classes.database import DataBase

from mindfulguard.classes.models.token import ModelToken
from mindfulguard.classes.models.user import ModelUser
from mindfulguard.classes.s3 import S3
from mindfulguard.database.postgresql.admin import PostgreSqlAdmin


class AdminBase(ABC):
    def __init__(self) -> None:
        super().__init__()
        self._status_code: int
        self._response: Any
        self._model_token = ModelToken()
        self._model_user = ModelUser()
        self._connection = DataBase().postgresql().connection()
        self._pgsql_admin = PostgreSqlAdmin(self._connection)
        self._s3 = S3()

    @abstractmethod
    async def execute(self) -> None:...

    @property
    def status_code(self) -> int:
        return self._status_code