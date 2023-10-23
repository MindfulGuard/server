from mindfulguard.authentication.executors import get_authorization_token
from mindfulguard.core.response_status_codes import *
from mindfulguard.core.security import sha256s
import mindfulguard.database.postgresql.safe as pgsql_safe
from mindfulguard.utils import Validation
import mindfulguard.safe.executors as const


class Update:
    def __init__(self):...
    async def execute(self,token:str,id:str,name:str,description:str):
        obj_safe = pgsql_safe.Safe()
        validation = Validation()
        tokenf:str = get_authorization_token(token)
        print(validation.validate_is_uuid(id))
        if validation.validate_token(tokenf) == False or len(name)>const.NAME_LENGTH or len(description)>const.DESCRIPTION_LENGTH or validation.validate_is_uuid(id) == False:
            return BAD_REQUEST
        return await obj_safe.update(sha256s(tokenf),id,name,description)