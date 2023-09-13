from mypass import utils
from mypass.core import configuration, security
from mypass.core.response_status_codes import *
from mypass.core.security.totp import Totp
from mypass.database.postgresql import authentication


class SignUp:
    async def execute(self,login:str,secret_string:str,ip:str):
        """
            Returns:
                400 - not valid email\n
                503 - registration is not allowed\n
                200 - registration was successful\n
                409 - the user already exists
        """
        valid = utils.Validation()
        print(valid.validate_secret_string(secret_string),valid.validate_login(login))
        if self.__permission() == False:
            return (None,None,SERVICE_UNAVAILABLE)
        elif valid.validate_secret_string(secret_string) == False or valid.validate_login(login)==False:
            return (None,None,BAD_REQUEST)
        totp = Totp()
        secret_code = totp.generate_secret_code()
        reserve_codes = totp.generate_reserve_codes(5)
        return (secret_code,reserve_codes, await authentication.Authentication().sign_up(
            login,
            security.sha256s(secret_string),
            ip,
            secret_code,
            reserve_codes
        ))
    def __permission(self)->bool:
        server_config = configuration.ServerConfiguration()
        return configuration.Authentication(server_config).get_registration()