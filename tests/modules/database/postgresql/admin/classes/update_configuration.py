from http.client import BAD_REQUEST
from mindfulguard.classes.database import DataBase
from mindfulguard.classes.models.settings import ModelSettings
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.admin import PostgreSqlAdmin


class DbTestAdminUpdateConfig:
    def __init__(self) -> None:
        self.__connection = DataBase().postgresql().connection()
        self.__pgsql_admin: PostgreSqlAdmin  = PostgreSqlAdmin(self.__connection)
        self.__model_token: ModelToken = ModelToken()
        self.__model_settings = ModelSettings()

    async def execute(self, token: str, key: str, value: str) -> int:
        try:
            self.__model_token.token = token
            self.__model_settings.key = key
            self.__model_settings.value = value
            
            db = self.__pgsql_admin.update_configuration(self.__model_token, self.__model_settings)
            await self.__connection.open()
            await db.execute()
            return db.status_code
        except ValueError:
            return BAD_REQUEST
        finally:
            await self.__connection.close()