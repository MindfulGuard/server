from mindfulguard.core.response_status_codes import *
import mindfulguard.core.security.totp as secure_totp
from mindfulguard.database.postgresql import authentication
from mindfulguard.database.postgresql.user.settings import Settings

class Delete:
    async def execute(
            self,
            token:str,
            login:str,
            secret_string:str,
            code:str
            ):

        confirm:bool = await self.__confirm(
            login,
            secret_string,
            code
        )
        user_settings = Settings()
        return await user_settings.delete_user(
            token,
            secret_string,
            confirm
        )

    async def __confirm(self,login:str,secret_string:str,code:str):
        return await self.__basic_confirm(login,secret_string,code)

    async def __basic_confirm(self,login:str,secret_string:str,code:str):
        get_secret_code = await authentication.Authentication().get_secret_code(login,secret_string)
        if get_secret_code[1] != OK:
            return False

        secret_code:str = get_secret_code[0][0]['secret_code']
        totp = secure_totp.Totp(secret_code)
        return totp.verify(code)