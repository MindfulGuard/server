from mypass import utils
from mypass.core import security
from mypass.core.response_status_codes import *
from mypass.database.postgresql import authentication


class GetTokens:
    async def execute(self,token:str):
        valid = utils.Validation()
        if valid.validate_token(token) == False:
            return ([],BAD_REQUEST)
        return await authentication.Authentication().get_tokens(security.sha256s((token)))