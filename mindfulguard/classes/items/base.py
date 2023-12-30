from abc import ABC, abstractmethod

from mindfulguard.classes.database import DataBase
from mindfulguard.classes.models.item_json import Item
from mindfulguard.classes.models.record import ModelRecord
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.items import PostgreSqlItems


class ItemsBase(ABC):
    def __init__(self) -> None:
        self._status_code: int
        self._connection = DataBase().postgresql().connection()
        self._pgsql_items = PostgreSqlItems(self._connection)
        self._model_token = ModelToken()
        self._model_record = ModelRecord()

    @abstractmethod
    async def execute(self) -> None:...

    @property
    def status_code(self) -> int:
        return self._status_code