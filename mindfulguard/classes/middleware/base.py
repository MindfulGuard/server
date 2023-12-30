from mindfulguard.classes.database import DataBase
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.classes.responses import Responses
from mindfulguard.database.postgresql.data_collection import PostgreSqlDataCollection


class MiddlewareBase:
    def __init__(self) -> None:
        self._connection = DataBase().postgresql().connection()
        self._model_token = ModelToken()
        self._responses = Responses()
        self._pgsql_data_collection = PostgreSqlDataCollection(self._connection)