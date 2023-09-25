from mypass.authentication.executors import get_authorization_token
from mypass.core.response_status_codes import *
import mypass.database.postgresql.items as pgsql_items
from mypass.utils import Validation
from mypass.core.security import sha256s

class Favorite:
    async def execute(self,token:str,safe_id:str,item_id:str):
        obj = pgsql_items.Item()
        validation = Validation()
        tokenf:str = get_authorization_token(token)
        
        if (
            validation.validate_token(tokenf) == False
            or validation.validate_is_uuid(safe_id) == False
            or validation.validate_is_uuid(item_id) == False
            ):
            return BAD_REQUEST


        return await obj.set_favorite(
            sha256s(tokenf),
            safe_id,
            item_id
            )