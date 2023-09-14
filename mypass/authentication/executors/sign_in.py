from mypass.core.configuration import *
from mypass.core.response_status_codes import *
import mypass.core.security as security
import mypass.core.security.totp as secure_totp
from mypass.database.postgresql import authentication
from mypass.utils import Validation, minutes_to_seconds

TYPE_RESERVE = "reserve"
TYPE_BASIC = "basic"

class SignIn:
    async def execute(self,login:str,secret_string:str,code:str,type:str,device:str,ip:str,expiration:int):
        """
            Returns:
                -1 - registration is not allowed\n
                1 - user not was successful\n
                0 - the user already exists
        """
        valid = Validation()
        token:str = security.generate_512_bit_token_string()
        if valid.validate_login(login) == False or valid.validate_secret_string(secret_string) == False or expiration <1:
            return (None,BAD_REQUEST)
        return (
            token,
            await authentication.Authentication().sign_in(
            login,
            security.sha256s(secret_string),
            security.sha256s(token),
            device,
            ip,
            minutes_to_seconds(expiration),
            await self.__confirm(login,security.sha256s(secret_string),code,type)
        ))
    
    async def __confirm(self,login:str,secret_string:str,code:str,type:str):        
        if type == TYPE_BASIC:
            return await self.__basic_confirm(login,secret_string,code)
        elif type == TYPE_RESERVE:
            return await self.__reserve_confirm(login,secret_string,code)
        return False

    async def __basic_confirm(self,login:str,secret_string:str,code:str):
        get_secret_code = await authentication.Authentication().get_secret_code(login,secret_string)
        if get_secret_code[1] != OK:
            return False
        print("SECRET_CODE:",get_secret_code[0][0]['secret_code'])
        secret_code:str = get_secret_code[0][0]['secret_code']
        totp = secure_totp.Totp(secret_code)
        return totp.verify(secret_code)
    
    async def __reserve_confirm(self,login:str,secret_string:str,code:str):
        icode:int = int(code)
        auth = authentication.Authentication()
        get_secret_code = await auth.get_secret_code(login,secret_string)
        if get_secret_code[1] !=OK:
            return False
        reserve_codes:list[int] = list[int](get_secret_code[0][0]['reserves'])
        if icode in reserve_codes:
            print("RESERVE_CODES:",reserve_codes)
            reserve_codes.remove(icode)
            result:int = await auth.update_reserve_codes(login,secret_string,reserve_codes)
            return result == 200
        return False