from mindfulguard import utils
from mindfulguard.authentication.executors import get_authorization_token
from mindfulguard.core import security
from mindfulguard.core.response_status_codes import *
from mindfulguard.database.postgresql import authentication
from mindfulguard.database.postgresql.user.information import Information

class UserInformation:
    async def get_tokens(self,token:str):
        get_token:str = get_authorization_token(token)
        valid = utils.Validation()
        if valid.validate_token(get_token) == False:
            return ([],BAD_REQUEST)
        return await authentication.Authentication().get_tokens(security.sha256s((get_token)))
    
    async def get_info(self,token:str):
        get_token:str = get_authorization_token(token)
        valid = utils.Validation()
        if valid.validate_token(get_token) == False:
            return ([],BAD_REQUEST)
        return await Information().get(security.sha256s((get_token)))