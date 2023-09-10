from mypass import utils
from mypass.core import configuration, security
from mypass.core.response_status_codes import *
from mypass.database.postgresql import authentication


class SignUp:
    async def execute(self,email:str,secret_string:str,login:str,ip:str):
        """
            Returns:
                400 - not valid email\n
                503 - registration is not allowed\n
                200 - registration was successful\n
                409 - the user already exists
        """
        valid = utils.Validation()
        print(valid.validate_email(email),valid.validate_secret_string(secret_string),valid.validate_login(login))
        if self.__permission() == False:
            return SERVICE_UNAVAILABLE
        elif valid.validate_email(email) == False or valid.validate_secret_string(secret_string) == False or valid.validate_login(login)==False:
            return BAD_REQUEST
        else:
            return await authentication.Authentication().sign_up(
                email,
                security.sha256s(secret_string),
                login,
                ip,
                'None'
                )
    def __permission(self)->bool:
        server_config = configuration.ServerConfiguration()
        return configuration.Authentication(server_config).get_registration()