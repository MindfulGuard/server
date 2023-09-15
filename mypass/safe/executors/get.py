from mypass.authentication.executors import get_authorization_token
from mypass.core.response_status_codes import *
from mypass.core.security import sha256s
import mypass.database.postgresql.safe as pgsql_safe
from mypass.utils import Validation

class Get:
    def __init__(self):...

    async def execute(self,token:str):
        validation = Validation()
        tokenf:str = get_authorization_token(token)

        if validation.validate_token(tokenf) == False:
            return (None,BAD_REQUEST)
        obj_safe = await pgsql_safe.Safe().get(sha256s(tokenf))

        status_code:int = obj_safe[1]
        json = obj_safe[0]

        return (json,status_code)