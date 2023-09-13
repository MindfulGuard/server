from mypass.core.configuration import *
from mypass.core.response_status_codes import *
import mypass.core.security as security
from mypass.database.postgresql import authentication
from mypass.utils import Validation, minutes_to_seconds


class SignIn:
    async def execute(self,login:str,secret_string:str,device:str,ip:str,expiration:int):
        """
            Returns:
                -1 - registration is not allowed\n
                1 - user not was successful\n
                0 - the user already exists
        """
        valid = Validation()
        token:str = security.generate_512_bit_token_string()
        if valid.validate_login(login) == False or valid.validate_secret_string(secret_string) == False:
            return (None,BAD_REQUEST)
        return (
            token,
            await authentication.Authentication().sign_in(
            login,
            security.sha256s(secret_string),
            security.sha256s(token),
            device,
            ip,
            minutes_to_seconds(expiration)
        ))