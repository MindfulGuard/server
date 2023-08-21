from mypass import utils
from mypass.authentication.executors import get_authorization_token
from mypass.core import security
from mypass.core.response_status_codes import BAD_REQUEST
from mypass.database.postgresql import authentication


class SignOut:
    async def execute(self,token:str,token_id:str):
        """
            Returns:
                400 - not valid email\n
                503 - registration is not allowed\n
                200 - registration was successful\n
                409 - the user already exists
        """
        valid = utils.Validation()
        tokenf:str = get_authorization_token(token)
        print(valid.validate_token(tokenf) == False or valid.validate_is_uuid(token_id) == False)
        if valid.validate_token(tokenf) == False or valid.validate_is_uuid(token_id) == False:
            return BAD_REQUEST
        return await authentication.Authentication().sign_out(
            security.sha256s(tokenf),
            token_id,
        )