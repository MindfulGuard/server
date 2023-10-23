from mindfulguard.authentication.executors import get_authorization_token
from mindfulguard.core.response_status_codes import *
from mindfulguard.core.security import sha256s
import mindfulguard.database.postgresql.safe as pgsql_safe
import mindfulguard.safe.executors as const
from mindfulguard.utils import Validation


class Create:
    def __init__(self):...
    async def execute(self,token:str,name:str,description:str):
        obj_safe = pgsql_safe.Safe()
        validation = Validation()
        tokenf:str = get_authorization_token(token)
        
        if validation.validate_token(tokenf) == False or len(name)>const.NAME_LENGTH or len(description)>const.DESCRIPTION_LENGTH:
            return BAD_REQUEST
        return await obj_safe.create(sha256s(tokenf),name,description)