from mindfulguard.core.response_status_codes import *
import mindfulguard.core.security.totp as secure_totp
from mindfulguard.database.postgresql import authentication
from mindfulguard.database.postgresql.user.settings import Settings

class SecretString:
    async def update(
            self,
            token:str,
            login:str,
            old_secret_string:str,
            new_secret_string:str,
            code:str
        ):
        confirm:bool = await self.__confirm(
            login,
            old_secret_string,
            code
        )
        if confirm == False:
            return NOT_FOUND
        user_settings = Settings()
        return await user_settings.update_secret_string(
            token,
            old_secret_string,
            new_secret_string
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