import datetime
from http.client import UNAUTHORIZED
from mindfulguard.authentication.executors import get_authorization_token
from mindfulguard.core.response_status_codes import BAD_REQUEST, INTERNAL_SERVER_ERROR, OK
from mindfulguard.core.s3 import CONTENT_PATH, S3
from mindfulguard.core.security import sha256s
from mindfulguard.database.postgresql.safe import Safe
from mindfulguard.database.postgresql.user.information import Information
from mindfulguard.utils import Validation


class Get:
    def __init__(self,token:str):
        self.__token:str = get_authorization_token(token)
    
    async def execute(self):
        validation = Validation()
        if validation.validate_token(self.__token) == False:
            return ({},BAD_REQUEST)
        
        uinfo = await Information().get(sha256s((self.__token)))
        if uinfo[-1] != OK:
            return ({},uinfo[-1])

        response_dict = {"list": []}
        safe_id_set = set()
        
        s3 = S3(uinfo[0]['username'])
        object_list = map(
            lambda x: x,
            s3.object().get_all_objects(prefix=f"{CONTENT_PATH}/"),
        )

        for raw in object_list:
            safe_id = raw.object_name.split('/')[1]
            if safe_id not in safe_id_set:
                safe_id_set.add(safe_id)
                file_info = {
                    "safe_id": safe_id,
                    "objects": []
                }
                response_dict["list"].append(file_info)
            
            resp = {
                "content_path": (raw.object_name).replace(CONTENT_PATH, "safe", 1)+"/content",
                "name":s3.object().get_stat(raw.object_name).metadata['X-Amz-Meta-Object_name'],
                "updated_at": int(datetime.datetime.fromisoformat(str(raw.last_modified)).timestamp()),
                "size": raw.size
            }
            file_info["objects"].append(resp)

        return (response_dict,OK)