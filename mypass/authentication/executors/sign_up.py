from mypass import utils
from mypass.core import configuration, security
from mypass.core.response_status_codes import *
from mypass.database.postgresql import authentication

class SignUp:
    async def execute(self,email:str,secret_string:bytes,login:str,ip:str):
        """
            Returns:
                400 - not valid email\n
                503 - registration is not allowed\n
                200 - registration was successful\n
                409 - the user already exists
        """
        valid = utils.Validation()
        if self._permission() == False:
            return SERVICE_UNAVAILABLE
        elif valid.validate(email,secret_string) == False:
            return BAD_REQUEST
        return await authentication.Authentication().sign_up(
            email,
            security.sha256b(secret_string),
            login,
            ip,
            'None'
            )
    def _permission(self)->bool:
        server_config = configuration.ServerConfiguration()
        return configuration.Authentication(server_config).get_registration()