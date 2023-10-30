from mindfulguard.authentication.executors import get_authorization_token
from mindfulguard.core.response_status_codes import *
from mindfulguard.core.s3 import CONTENT_PATH, S3
from mindfulguard.core.security import sha256s
from mindfulguard.database.postgresql.user.information import Information
from mindfulguard.utils import Validation
import mindfulguard.database.postgresql.safe as pgsql_safe


class Delete:
    async def execute(self,token:str,id:str):
        validation = Validation()
        tokenf:str = get_authorization_token(token)

        if validation.validate_token(tokenf) == False or validation.validate_is_uuid(id) == False:
            return BAD_REQUEST
        obj_safe = await pgsql_safe.Safe().delete(sha256s(tokenf),id)

        if obj_safe != OK:
            return obj_safe
        
        uinfo = await Information().get(sha256s((tokenf)))
        if uinfo[-1] != OK:
            return uinfo[-1]

        s3 = S3(uinfo[0]['username'])
        prefix:str = f"{CONTENT_PATH}/{id}/"
        object_list = [obj.object_name for obj in s3.object().get_all_objects(prefix)]

        s3.object().delete_objects(object_list)
        return OK