from mindfulguard.authentication.executors import get_authorization_token
from mindfulguard.core.response_status_codes import *
import mindfulguard.database.postgresql.items as pgsql_items
from mindfulguard.utils import Validation
from mindfulguard.core.security import sha256s


class Delete:
    def __init__(self):...
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


        return await obj.delete(
            sha256s(tokenf),
            safe_id,
            item_id
            )