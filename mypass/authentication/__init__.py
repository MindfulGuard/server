from mypass.authentication.authentication import *
import mypass.database.postgresql.authentication as authentication
from mypass.configuration.config import Configuration
from mypass.utils import validate_email

class SignUp(Authentication):
    async def execute(self,email:str,secret_string:bytes,login:bytes,ip:str):
        """
            Returns:
                -1 - registration is not allowed\n
                1 - registration was successful\n
                0 - the user already exists
        """
        if self._permission() == False:
            return -1
        elif validate_email(email) == False:
            return -2
        elif await authentication.Authentication().sign_up(
            email,
            secret_string,
            login,
            ip,
            'None'
            ) == True:
            return 1
        else:
            return 0
    def _permission(self)->bool:
        config = Configuration()
        match config.server_configuration('auth','registration').lower():
            case 'true':return True
            case 'false':return False
            case _:return False
class SignIn():
    def execute(self):...