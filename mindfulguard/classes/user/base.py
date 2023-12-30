from abc import ABC, abstractmethod
from typing import Any
from mindfulguard.classes.database import DataBase
from mindfulguard.classes.models.code import ModelCode
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.classes.models.totp_code import ModelTotpCode
from mindfulguard.classes.models.user import ModelUser
from mindfulguard.classes.s3 import S3
from mindfulguard.classes.security import Security
from mindfulguard.settings import Settings

class UserBase(ABC):
    def __init__(self) -> None:
        from mindfulguard.database.postgresql.user import PostgreSqlUser
        self._status_code: int
        self._response: Any
        self._settings = Settings()
        self._security = Security()
        self._connection = DataBase().postgresql().connection()
        self._pgsql_user = PostgreSqlUser(self._connection)
        self._model_token = ModelToken()
        self._model_user = ModelUser()
        self._model_code = ModelCode()
        self._model_totp_code = ModelTotpCode()
        self._s3 = S3()

    @abstractmethod
    async def execute(self) -> None:...

    @property
    def status_code(self) -> int:
        return self._status_code