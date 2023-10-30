from http.client import BAD_REQUEST
from mindfulguard.authentication.executors import get_authorization_token
from mindfulguard.configuration.configuration import Get
from mindfulguard.core.response_status_codes import OK
from mindfulguard.database.postgresql.admin import Admin
from mindfulguard.utils import Validation
from tests.api.secure.secure import sha256s


class GetSettings:
    def __init__(self):
        self.__admin_db = Admin()

    async def execute(self,token:str):
        validation = Validation()
        tokenf:str = get_authorization_token(token)

        if validation.validate_token(tokenf) == False:
            return (None,BAD_REQUEST)

        st = await self.__admin_db.is_admin(sha256s(tokenf))
        if st!=OK:
            return (None,st)
        
        config = Get().execute()
        authentication = await config.authentication()
        item = await config.item()
        registration_status = await config.registration_status()
        scan_time_routines_tokens = await config.scan_time_routines_tokens()
        scan_time_routines_users = await config.scan_time_routines_users()
        confirmation_period = await config.confirmation_period()
        disk_space_per_user = await config.disk_space_per_user()

        return (
            authentication[0],
            item[0],
            item[1],
            registration_status[0],
            scan_time_routines_tokens[0],
            scan_time_routines_users[0],
            confirmation_period[0],
            disk_space_per_user[0],
            st)
        

class UpdateSettings:
    def __init__(self):
        self.__admin_db = Admin()

    async def execute(self,token:str,key:str,value:str):
            validation = Validation()
            tokenf:str = get_authorization_token(token)

            if validation.validate_token(tokenf) == False:
                return BAD_REQUEST
            
            return await self.__admin_db.update_settings(
                sha256s(tokenf),
                key,
                str(value)
            )