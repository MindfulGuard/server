from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.record import ModelRecord
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.connection import PostgreSqlConnection
from mindfulguard.database.postgresql.items.create import PostgreSqlItemsCreate
from mindfulguard.database.postgresql.items.delete import PostgreSqlItemsDelete
from mindfulguard.database.postgresql.items.favorite import PostgreSqlItemsFavorite
from mindfulguard.database.postgresql.items.get import PostgreSqlItemsGet
from mindfulguard.database.postgresql.items.move import PostgreSqlItemsMove
from mindfulguard.database.postgresql.items.update import PostgreSqlItemsUpdate
from mindfulguard.items.model_record_extend import ModelRecordExtend


class PostgreSqlItems:
    def __init__(self, connection: PostgreSqlConnection):
        self.__connection: PostgreSqlConnection = connection
    
    def get(self, model_token: ModelToken) -> PostgreSqlItemsGet:
        """
        Params:
            ModelToken().token
        Return:
            returns everything except __Iterator().ModelRecord().user_id
        """
        obj: PostgreSqlQueriesBase = PostgreSqlItemsGet(self.__connection, model_token)
        return obj
    
    def create(
        self,
        model_token: ModelToken,
        model_record: ModelRecord
    ) -> PostgreSqlItemsCreate:
        """
        Params:
            ModelToken().token,
            ModelRecord().safe_id,
            ModelRecord().title,
            ModelRecord().item,
            ModelRecord().notes,
            ModelRecord().tags,
            ModelRecord().category
        """
        obj: PostgreSqlQueriesBase = PostgreSqlItemsCreate(
            self.__connection,
            model_token,
            model_record
        )
        return obj
    
    def update(
        self,
        model_token: ModelToken,
        model_record: ModelRecord
    ) -> PostgreSqlItemsUpdate:
        """
        Params:
            ModelToken().token,
            ModelRecord().id,
            ModelRecord().safe_id,
            ModelRecord().title,
            ModelRecord().item,
            ModelRecord().notes,
            ModelRecord().tags,
            ModelRecord().category
        """
        obj: PostgreSqlQueriesBase = PostgreSqlItemsUpdate(
            self.__connection,
            model_token,
            model_record
        )
        return obj
    
    def delete(
        self,
        model_token: ModelToken,
        model_record: ModelRecord
    ) -> PostgreSqlItemsDelete:
        """
        Params:
            ModelToken().token,
            ModelRecord().id,
            ModelRecord().safe_id
        """
        obj: PostgreSqlQueriesBase = PostgreSqlItemsDelete(
            self.__connection,
            model_token,
            model_record
        )
        return obj
    
    def favorite(
        self,
        model_token: ModelToken,
        model_record: ModelRecord
    ) -> PostgreSqlItemsFavorite:
        """
        Params:
            ModelToken().token,
            ModelRecord().id,
            ModelRecord().safe_id
        """
        obj: PostgreSqlQueriesBase = PostgreSqlItemsFavorite(
            self.__connection,
            model_token,
            model_record
        )
        return obj
    
    def move(
        self,
        model_token: ModelToken,
        model_record_extend: ModelRecordExtend
    ) -> PostgreSqlItemsMove:
        """
        Params:
            ModelToken().token,
            ModelRecordExtend().id,
            ModelRecordExtend().old_safe_id,
            ModelRecordExtend().new_safe_id,
            ModelRecordExtend().id
        """
        obj: PostgreSqlQueriesBase = PostgreSqlItemsMove(
            self.__connection,
            model_token,
            model_record_extend
        )
        return obj