from mypass import utils
from mypass.core import configuration
from mypass.core.response_status_codes import *
from mypass.database.postgresql import authentication
from mypass.utils import arguments


class SignUp:
    async def execute(self,email:str,secret_string:bytes,login:bytes,ip:str):
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
        elif valid.validate(email) == False:
            return BAD_REQUEST
        elif await authentication.Authentication().sign_up(
            email,
            secret_string,
            login,
            ip,
            'None'
            ) == True:
            return OK
        else:
            return CONFLICT
    def _permission(self)->bool:
        server_config = configuration.ServerConfiguration()
        return configuration.Authentication(server_config).get_registration()