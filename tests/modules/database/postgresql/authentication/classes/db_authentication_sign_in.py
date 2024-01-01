from http.client import BAD_REQUEST
from mindfulguard.classes.database import DataBase
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.classes.models.user import ModelUser
from mindfulguard.database.postgresql.authentication import PostgreSqlAuthentication
  
class DbTestsAuthenticationSignIn:
    def __init__(self) -> None:
        self.__connection = DataBase().postgresql().connection()
        self.__pgsql_auth: PostgreSqlAuthentication  = PostgreSqlAuthentication(self.__connection)
        self.__model_user: ModelUser = ModelUser()
        self.__model_token: ModelToken = ModelToken()
        self.__token_hashed: str

    @property
    def token_hashed(self) -> str:
        return self.__token_hashed

    async def ok(
        self,
        login: str,
        secret_string: str,
        token: str,
        is_verified_code: bool,
        device: str = 'Python client 0.0.0/Windows',
        last_ip: str = '127.0.0.1',
        expiration: int = 2
    ) -> int:
        try:
            self.__model_user.login = login
            self.__model_user.secret_string = secret_string
            self.__model_token.token = token
            self.__model_token.device = device
            self.__model_token.last_ip = last_ip
            self.__model_token.expiration = expiration

            db = self.__pgsql_auth.sign_in(self.__model_user, self.__model_token)
            await self.__connection.open()
            await db.execute(is_verified_code)
            self.__token_hashed = self.__model_token.token
            return db.status_code
        finally:
            await self.__connection.close()

    async def bad_request(
        self,
        login: str,
        secret_string: str,
        token: str,
        is_verified_code: bool,
        device: str = 'Python client 0.0.0/Windows',
        last_ip: str = '127.0.0.1',
        expiration: int = 2
    ) -> int:
        try:
            self.__model_user.login = login
            self.__model_user.secret_string = secret_string
            self.__model_token.token = token
            self.__model_token.device = device
            self.__model_token.last_ip = last_ip
            self.__model_token.expiration = expiration

            db = self.__pgsql_auth.sign_in(self.__model_user, self.__model_token)
            await self.__connection.open()
            await db.execute(is_verified_code)
            self.__token_hashed = self.__model_token.token
            return db.status_code
        except ValueError:
            return BAD_REQUEST
        finally:
            await self.__connection.close()