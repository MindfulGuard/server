from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.safe import ModelSafe
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.connection import PostgreSqlConnection
from mindfulguard.database.postgresql.safe.create import PostgreSqlSafeCreate
from mindfulguard.database.postgresql.safe.delete import PostgreSqlSafeDelete
from mindfulguard.database.postgresql.safe.get import PostgreSqlSafeGet
from mindfulguard.database.postgresql.safe.safe_exist import PostgreSqlSafeExist
from mindfulguard.database.postgresql.safe.update import PostgreSqlSafeUpdate


class PostgreSqlSafe:
    def __init__(self, connection: PostgreSqlConnection):
        self.__connection: PostgreSqlConnection = connection

    def create(
        self,
        model_token: ModelToken,
        model_safe: ModelSafe
    ) -> PostgreSqlSafeCreate:
        """
        Params:
            ModelToken().token,
            ModelSafe().name,
            ModelSafe().description
        """
        obj: PostgreSqlQueriesBase = PostgreSqlSafeCreate(
            self.__connection,
            model_token,
            model_safe
        )
        return obj
    
    def update(
        self,
        model_token: ModelToken,
        model_safe: ModelSafe
    ) -> PostgreSqlSafeUpdate:
        """
        Params:
            ModelToken().token,
            ModelSafe().id,
            ModelSafe().name,
            ModelSafe().description
        """
        obj: PostgreSqlQueriesBase = PostgreSqlSafeUpdate(
            self.__connection,
            model_token,
            model_safe
        )
        return obj
    
    def get(
        self,
        model_token: ModelToken
    ) -> PostgreSqlSafeGet:
        """
        Params:
            ModelToken().token
        Return:
            __Iterator() returns from ModelSafe() except ModelSafe().user_id
        """
        obj: PostgreSqlQueriesBase = PostgreSqlSafeGet(self.__connection, model_token)
        return obj
    
    def delete(
        self,
        model_token: ModelToken,
        model_safe: ModelSafe
    ) -> PostgreSqlSafeDelete:
        """
        Params:
            ModelToken().token,
            ModelSafe().id
        """
        obj: PostgreSqlQueriesBase = PostgreSqlSafeDelete(
            self.__connection,
            model_token,
            model_safe
        )
        return obj
    
    def safe_exist(
        self,
        model_token: ModelToken,
        model_safe: ModelSafe
    ) -> PostgreSqlSafeExist:
        """
        Params:
            ModelToken().token,
            ModelSafe().id
        """
        obj: PostgreSqlQueriesBase = PostgreSqlSafeExist(
            self.__connection,
            model_token,
            model_safe
        )
        return obj