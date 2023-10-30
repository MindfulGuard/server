from mindfulguard.authentication.executors import get_authorization_token
from mindfulguard.core.response_status_codes import BAD_REQUEST, INTERNAL_SERVER_ERROR, OK
from mindfulguard.core.s3 import CONTENT_PATH, S3
from mindfulguard.core.security import sha256s
from mindfulguard.database.postgresql.user.information import Information
from mindfulguard.utils import Validation


class Download:
    def __init__(self,token:str):
        self.__token:str = get_authorization_token(token)
    
    async def execute(self,safe_id:str,object_name:str):
        validation = Validation()
        if (
            validation.validate_token(self.__token) == False
            or validation.validate_is_uuid(safe_id) == False
        ):
            return (bytes(),"",BAD_REQUEST)
        
        uinfo = await Information().get(sha256s((self.__token)))
        if uinfo[-1] != OK:
            return (bytes(),"",uinfo[-1])

        s3 = S3(uinfo[0]['username']).object().get_object(
            f"{CONTENT_PATH}/{safe_id}/{object_name}"
        )
        if s3 == None:
            return (bytes(),"",INTERNAL_SERVER_ERROR)

        return (s3[0],s3[1],OK)