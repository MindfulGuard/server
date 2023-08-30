from mypass import utils
from mypass.core.configuration import *
from mypass.core.response_status_codes import *
import mypass.core.security as security
from mypass.database.postgresql import authentication

#!need to rework the code, using SRP!
class SignIn:
    async def execute(self,email:str,secret_string:str,device:str,ip:str,expiration:int):
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
            security.sha256s(secret_string),
            security.sha256s(token),
            device,
            ip,
            utils.minutes_to_seconds(expiration)
        ),token)