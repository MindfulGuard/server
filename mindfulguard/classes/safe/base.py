from abc import ABC, abstractmethod
from mindfulguard.classes.database import DataBase
from mindfulguard.classes.models.safe import ModelSafe
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.safe import PostgreSqlSafe

class SafeBase(ABC):
    def __init__(self) -> None:
        self._status_code: int
        self._connection = DataBase().postgresql().connection()
        self._pgsql_safe =  PostgreSqlSafe(self._connection)
        self._model_token = ModelToken()
        self._model_safe = ModelSafe()

    @abstractmethod
    async def execute(self) -> None:...

    @property
    def status_code(self) -> int:
        return self._status_code