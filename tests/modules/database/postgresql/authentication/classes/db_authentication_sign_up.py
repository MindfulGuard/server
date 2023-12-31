from http.client import BAD_REQUEST
from mindfulguard.classes.database import DataBase
from mindfulguard.classes.models.code import ModelCode
from mindfulguard.classes.models.user import ModelUser
from mindfulguard.database.postgresql.authentication import PostgreSqlAuthentication
  
class DbTestsAuthenticationSignUp:
    def __init__(self) -> None:
        self.__connection = DataBase().postgresql().connection()
        self.__pgsql_auth: PostgreSqlAuthentication  = PostgreSqlAuthentication(self.__connection)
        self.__model_user: ModelUser = ModelUser()
        self.__model_code: ModelCode = ModelCode()
        self.__secret_code_hashed: str

    @property
    def secret_string_hashed(self) -> str:
        return self.__secret_code_hashed

    async def ok(
        self,
        login: str,
        secret_string: str,
        secret_code: str,
        backup_codes: list[int],
        reg_ip: str = '127.0.0.1',
        confirm: bool = False
    ) -> int:
        try:
            self.__model_user.login = login
            self.__model_user.secret_string = secret_string
            self.__model_user.reg_ip = reg_ip
            self.__model_user.confirm = confirm
            self.__model_code.secret_code = secret_code
            self.__model_code.backup_codes = backup_codes

            db = self.__pgsql_auth.sign_up(self.__model_user, self.__model_code)
            await self.__connection.open()
            await db.execute()
            self.__secret_code_hashed = self.__model_user.secret_string
            return db.status_code
        finally:
            await self.__connection.close()

    async def bad_request(
        self,
        login: str,
        secret_string: str,
        secret_code: str,
        backup_codes: list[int],
        reg_ip: str = '127.0.0.1',
        confirm: bool = False
    ) -> int:
        try:
            self.__model_user.login = login
            self.__model_user.secret_string = secret_string
            self.__model_user.reg_ip = reg_ip
            self.__model_user.confirm = confirm
            self.__model_code.secret_code = secret_code
            self.__model_code.backup_codes = backup_codes

            db = self.__pgsql_auth.sign_up(self.__model_user, self.__model_code)
            await self.__connection.open()
            await db.execute()
            return db.status_code
        except ValueError:
            return BAD_REQUEST
        finally:
            await self.__connection.close()