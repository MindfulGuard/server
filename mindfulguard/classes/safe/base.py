from abc import ABC, abstractmethod
from mindfulguard.classes.database import DataBase
from mindfulguard.classes.database.redis import Redis
from mindfulguard.classes.models.safe import ModelSafe
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.classes.s3 import S3
from mindfulguard.database.postgresql.safe import PostgreSqlSafe
from mindfulguard.database.postgresql.user import PostgreSqlUser

class SafeBase(ABC):
    def __init__(self) -> None:
        self._status_code: int
        self._connection = DataBase().postgresql().connection()
        self._pgsql_user = PostgreSqlUser(self._connection)
        self._pgsql_safe =  PostgreSqlSafe(self._connection)
        self._model_token = ModelToken()
        self._model_safe = ModelSafe()
        self._s3 = S3()
        self._redis = Redis()

    @abstractmethod
    async def execute(self) -> None:...

    @property
    def status_code(self) -> int:
        return self._status_code