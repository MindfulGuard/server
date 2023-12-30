from abc import ABC, abstractmethod
from fastapi import Request
from mindfulguard.classes.database import DataBase
from mindfulguard.classes.models.code import ModelCode
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.classes.models.user import ModelUser
from mindfulguard.classes.s3 import S3
from mindfulguard.classes.security import Security
from mindfulguard.database.postgresql.authentication import PostgreSqlAuthentication


class AuthenticationBase(ABC):
    def __init__(self, request: Request) -> None:
        self._status_code: int
        self._connection = DataBase().postgresql().connection()
        self._pgsql_auth = PostgreSqlAuthentication(self._connection)
        self._model_user = ModelUser()
        self._model_code = ModelCode()
        self._model_token = ModelToken()
        self._s3 = S3()
        self._security = Security()
        self._request: Request = request

    @abstractmethod
    async def execute(self) -> None:...

    @property
    def status_code(self) -> int:
        return self._status_code