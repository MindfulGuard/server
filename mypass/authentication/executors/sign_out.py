from mypass import utils
from mypass.authentication.executors import get_authorization_token
from mypass.core import security
from mypass.core.response_status_codes import BAD_REQUEST
from mypass.database.postgresql import authentication


class SignOut:
    async def execute(self,token:str,token_id:str):
        valid = utils.Validation()
        get_token:str = get_authorization_token(token)
        if valid.validate_token(get_token) == False or valid.validate_is_uuid(token_id) == False:
            return BAD_REQUEST
        return await authentication.Authentication().sign_out(
            security.sha256s(get_token),
            token_id,
        )