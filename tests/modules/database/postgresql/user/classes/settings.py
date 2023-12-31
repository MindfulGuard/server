from http.client import BAD_REQUEST
from mindfulguard.classes.database import DataBase
from mindfulguard.classes.models.code import ModelCode
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.classes.models.user import ModelUser
from mindfulguard.database.postgresql.user import PostgreSqlUser
from mindfulguard.user.settings.model_user_extend import ModelUserExtend


class DbTestUserSettingsUpdateOneTimeCode:
    def __init__(self) -> None:
        self.__connection = DataBase().postgresql().connection()
        self.__pgsql_user: PostgreSqlUser = PostgreSqlUser(self.__connection)
        self.__model_user = ModelUser()
        self.__model_token: ModelToken = ModelToken()
        self.__model_code = ModelCode()

    async def execute(
        self,
        token: str,
        secret_string: str,
        secret_code: str
    ) -> int:
        try:
            self.__model_token.token = token
            self.__model_user.secret_string = secret_string
            self.__model_code.secret_code = secret_code

            db = self.__pgsql_user.settings().update_one_time_code(
                self.__model_user,
                self.__model_token,
                self.__model_code
            ).totp()
            await self.__connection.open()
            await db.execute()
            return db.status_code
        except ValueError:
            return BAD_REQUEST
        finally:
            await self.__connection.close()

class DbTestUserSettingsUpdateSecretString:
    def __init__(self) -> None:
        self.__connection = DataBase().postgresql().connection()
        self.__pgsql_user: PostgreSqlUser = PostgreSqlUser(self.__connection)
        self.__model_user_extend = ModelUserExtend()
        self.__model_token: ModelToken = ModelToken()

    async def execute(
        self,
        token: str,
        old_secret_string: str,
        new_secret_string: str
    ) -> int:
        try:
            self.__model_token.token = token
            self.__model_user_extend.old_secret_string = old_secret_string
            self.__model_user_extend.new_secret_string = new_secret_string

            db = self.__pgsql_user.settings().udpate_secret_string(
                self.__model_user_extend,
                self.__model_token
            )
            await self.__connection.open()
            await db.execute()
            return db.status_code
        except ValueError:
            return BAD_REQUEST
        finally:
            await self.__connection.close()

class DbTestUserSettingsDeleteAccount:
    def __init__(self) -> None:
        self.__connection = DataBase().postgresql().connection()
        self.__pgsql_user: PostgreSqlUser = PostgreSqlUser(self.__connection)
        self.__model_user = ModelUser()
        self.__model_token: ModelToken = ModelToken()

    async def execute(
        self,
        token: str,
        secret_string: str,
    ) -> int:
        try:
            self.__model_token.token = token
            self.__model_user.secret_string = secret_string

            db = self.__pgsql_user.settings().delete_account(
                self.__model_token,
                self.__model_user
            )
            await self.__connection.open()
            await db.execute(True)
            return db.status_code
        except ValueError:
            return BAD_REQUEST
        finally:
            await self.__connection.close()