from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.connection import PostgreSqlConnection
from mindfulguard.database.postgresql.data_collection.update_token_information import PostgreSqlUpdateTokenInformation


class PostgreSqlDataCollection:
    def __init__(self, connection: PostgreSqlConnection):
        self.__connection: PostgreSqlConnection = connection

    def update_token_information(
        self, 
        model_token: ModelToken
    ) -> PostgreSqlUpdateTokenInformation:
        """
        Params:
            ModelToken().token,
            ModelToken().device,
            ModelToken().last_ip
        """
        obj: PostgreSqlQueriesBase = PostgreSqlUpdateTokenInformation(
            self.__connection,
            model_token
        )
        return obj