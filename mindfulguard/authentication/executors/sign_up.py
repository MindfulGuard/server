from mindfulguard import utils
from mindfulguard.core import configuration, security
from mindfulguard.core.response_status_codes import *
from mindfulguard.core.security.totp import Totp
from mindfulguard.database.postgresql import authentication


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
        totp = Totp("")
        secret_code = totp.generate_secret_code()
        backup_codes = totp.generate_backup_codes(self.__get_reserve_codes_length())
        return (secret_code,backup_codes, await authentication.Authentication().sign_up(
            login,
            security.sha256s(secret_string),
            ip,
            secret_code,
            backup_codes
        ))
    def __permission(self)->bool:
        server_config = configuration.ServerConfiguration()
        return configuration.Authentication(server_config).get_registration()
    
    def __get_reserve_codes_length(self)->int:
        server_config = configuration.ServerConfiguration()
        return configuration.Authentication(server_config).totp().lengths().get_reserve_codes_length()