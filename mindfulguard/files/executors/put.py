from fastapi import UploadFile
from mindfulguard.authentication.executors import get_authorization_token
from mindfulguard.core.response_status_codes import BAD_REQUEST, INTERNAL_SERVER_ERROR, OK
from mindfulguard.core.s3 import CONTENT_PATH, S3
from mindfulguard.database.postgresql.safe import Safe
from mindfulguard.database.postgresql.settings import Settings
from mindfulguard.database.postgresql.user.information import Information
from mindfulguard.utils import Validation
from tests.api.secure.secure import sha256s


class Put:
    def __init__(self,token:str):
        self.__token:str = get_authorization_token(token)
        self.__settings_db = Settings()
        
    async def auth(self,safe_id:str):
        validation = Validation()
        if (
            validation.validate_token(self.__token) == False
            or validation.validate_is_uuid(safe_id) == False
        ):
            return BAD_REQUEST
        
        item:int = await Safe().safe_exist(
            sha256s(self.__token),
            safe_id,
        )
        if item != OK:
            print(item)
            return item
        return item

    async def execute(self, safe_id:str, files:list[UploadFile]):
        if await self.__free_disk_space(sum([file.size for file in files])) == False:
            return INTERNAL_SERVER_ERROR

        uinfo = await Information().get(sha256s((self.__token)))
        s3 = await S3(uinfo[0]['username']).object().put_objects(
            [file for file in files],
            prefix_object_name_=f"{CONTENT_PATH}/{safe_id}/"
        )
        if not s3:
            return INTERNAL_SERVER_ERROR
        return OK
        
    async def __free_disk_space(self,file_size:int)->bool:
        settings = await self.__settings_db.get()
        if settings[1] != OK:
            return False
        space_per_user:int = int(settings[0]['disk_space_per_user'])
        user_info = await Information().get(sha256s(self.__token))  
        user_obj = user_info[0]
        s3 = S3(user_obj['username'])
        
        if s3.bucket().get_size+file_size > space_per_user:
            print("False")
            return False
        return True