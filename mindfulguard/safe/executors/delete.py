from mindfulguard.authentication.executors import get_authorization_token
from mindfulguard.core.response_status_codes import *
from mindfulguard.core.security import sha256s
from mindfulguard.utils import Validation
import mindfulguard.database.postgresql.safe as pgsql_safe


class Delete:
    async def execute(self,token:str,id:str):
        validation = Validation()
        tokenf:str = get_authorization_token(token)

        if validation.validate_token(tokenf) == False or validation.validate_is_uuid(id) == False:
            return BAD_REQUEST
        obj_safe = await pgsql_safe.Safe().delete(sha256s(tokenf),id)

        return (obj_safe)