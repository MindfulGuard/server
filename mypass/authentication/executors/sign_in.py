from mypass import utils
from mypass.core.configuration import *
from mypass.core.response_status_codes import *
import mypass.core.security as security
from mypass.database.postgresql import authentication


class SignIn:
    async def execute(self,email:str,secret_string:bytes,device:str,ip:str):
        """
            Returns:
                -1 - registration is not allowed\n
                1 - user not was successful\n
                0 - the user already exists
        """
        valid = utils.Validation()
        token:str = security.generate_512_bit_token_string()
        if valid.validate(email,secret_string) == False:
            return (BAD_REQUEST,None)
        return (
            await authentication.Authentication().sign_in(
            email,
            security.sha256b(secret_string),
            security.sha256s(token),
            device,
            ip,
            self.__get_expiration()
        ),token)
    
    def __get_expiration(self)->int:
        cfg= ServerConfiguration()
        exec = Authentication(cfg)
        return utils.minutes_to_seconds(exec.get_token_expiration_default())