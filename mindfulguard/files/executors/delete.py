from mindfulguard.authentication.executors import get_authorization_token
from mindfulguard.core.response_status_codes import BAD_REQUEST, INTERNAL_SERVER_ERROR, OK
from mindfulguard.core.s3 import CONTENT_PATH, S3
from mindfulguard.core.security import sha256s
from mindfulguard.database.postgresql.user.information import Information
from mindfulguard.utils import Validation


class Delete:
    def __init__(self,token:str):
        self.__token:str = get_authorization_token(token)

    async def execute(self, safe_id:str, files:list[str]):
        validation = Validation()
        if (
            validation.validate_token(self.__token) == False
            or validation.validate_is_uuid(safe_id) == False
            or len(files) == 0
        ):
            return BAD_REQUEST
        uinfo = await Information().get(sha256s((self.__token)))
        
        if uinfo[-1] != OK:
            return uinfo[-1]

        s3 = S3(uinfo[0]['username'])
        if s3.object().delete_objects(files,prefix_object_name_=f"{CONTENT_PATH}/{safe_id}/"):
            return OK
        return INTERNAL_SERVER_ERROR