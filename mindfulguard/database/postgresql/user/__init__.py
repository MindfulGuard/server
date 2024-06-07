from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.connection import PostgreSqlConnection
from mindfulguard.database.postgresql.user.get_tokens import PostgreSqlUserGetTokens
from mindfulguard.database.postgresql.user.info import PostgreSqlUserInformation
from mindfulguard.database.postgresql.user.settings import PostgreSqlUserSettings


class PostgreSqlUser:
    def __init__(self, connection: PostgreSqlConnection) -> None:
        self.__connection: PostgreSqlConnection = connection

    def get_information(self, model_token: ModelToken) -> PostgreSqlUserInformation:
        """
        Params:
            ModelToken().token
        Return:
            ModelUser().login, ModelUser().created_at, ModelUser().reg_ip
        """
        obj: PostgreSqlQueriesBase = PostgreSqlUserInformation(
            self.__connection,
            model_token
        )
        return obj
    
    def get_tokens(self, model_token: ModelToken) -> PostgreSqlUserGetTokens:
        """
        Params:
            ModelToken().token
        Return:
            returns everything except __Iterator().ModelToken().user_id
        """
        obj: PostgreSqlQueriesBase = PostgreSqlUserGetTokens(
            self.__connection,
            model_token
        )
        return obj
    
    def settings(self) -> PostgreSqlUserSettings:
        obj = PostgreSqlUserSettings(self.__connection)
        return obj