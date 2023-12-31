from http.client import BAD_REQUEST
from mindfulguard.classes.database import DataBase
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.authentication import PostgreSqlAuthentication


class DbTestsAuthenticationSignOut:
    def __init__(self) -> None:
        self.__connection = DataBase().postgresql().connection()
        self.__pgsql_auth: PostgreSqlAuthentication  = PostgreSqlAuthentication(self.__connection)
        self.__model_token: ModelToken = ModelToken()
        self.__secret_code_hashed: str

    @property
    def secret_string_hashed(self) -> str:
        return self.__secret_code_hashed

    async def ok(
        self,
        token: str,
        token_id: str
    ) -> int:
        try:
            self.__model_token.id = token_id
            self.__model_token.token= token 

            db = self.__pgsql_auth.sign_out(self.__model_token)
            await self.__connection.open()
            await db.execute()
            return db.status_code
        finally:
            await self.__connection.close()

    async def bad_request(
        self,
        token: str,
        token_id: str
    ) -> int:
        try:
            self.__model_token.id = token_id
            self.__model_token.token= token 

            db = self.__pgsql_auth.sign_out(self.__model_token)
            await self.__connection.open()
            await db.execute()
            return db.status_code
        except ValueError:
            return BAD_REQUEST
        finally:
            await self.__connection.close()