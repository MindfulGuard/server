from mypass.authentication.executors import get_authorization_token
from mypass.core.response_status_codes import *
from mypass.core.security import sha256s
import mypass.database.postgresql.items as pgsql_items
from mypass.utils import Validation

class Get:
    async def execute(self,token:str):
        validation = Validation()
        tokenf:str = get_authorization_token(token)

        if validation.validate_token(tokenf) == False:
            return ([],[],[],BAD_REQUEST)
        obj_safe = await pgsql_items.Item().get(sha256s(tokenf))

        status_code:int = obj_safe[3]
        favorites:list[str] = obj_safe[2]
        tags:list[str] = obj_safe[1]
        json = obj_safe[0]

        return (json,tags,favorites,status_code)