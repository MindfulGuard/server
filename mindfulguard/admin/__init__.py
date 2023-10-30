from typing import Any
from fastapi import Request, Response

from mindfulguard.admin.executors.settings import GetSettings, UpdateSettings
from mindfulguard.admin.executors.get_users import GetUsers, SearchUsers
from mindfulguard.admin.executors.user_management import CreateUser, DeleteUser
from mindfulguard.core.languages import Language
from mindfulguard.core.languages.responses import Responses
from mindfulguard.core.response_status_codes import BAD_REQUEST, CONFLICT, FORBIDDEN, INTERNAL_SERVER_ERROR, NOT_FOUND, OK, SERVICE_UNAVAILABLE, UNAUTHORIZED
from mindfulguard.core.s3 import S3
import mindfulguard.utils as utils


class Admin:
    def __init__(self):
        self.__lang = Language()
        self.__json_responses = Responses(self.__lang)
    
    async def get_users(self,token:str,page:int,response:Response):
        obj = await GetUsers().execute(token,page)
        total_pages:int = obj[0]
        count_users:int = obj[1]
        arr:list = obj[2][0]
        status_code:int = obj[2][1]

        response.status_code = status_code
        
        if status_code == BAD_REQUEST:
            return self.__json_responses.data_not_valid()
        elif status_code == UNAUTHORIZED:
            return self.__json_responses.unauthorized()
        elif status_code == FORBIDDEN:
            return self.__json_responses.forbidden()
        elif status_code == OK:
            s3 = S3("")
            return {
                "page":page,
                "total_pages":total_pages,
                "total_users":count_users,
                "total_storage_size":s3.bucket().total_size,
                "list":arr
            }
        else:
            return self.__json_responses.server_error()
        
    async def search_users(self,token:str,key:str,value:str,response:Response):
        obj = await SearchUsers(key,value).execute(token)
        arr = obj[0]
        status_code:int = obj[1]

        response.status_code = status_code

        if status_code == BAD_REQUEST:
            return self.__json_responses.data_not_valid()
        elif status_code == UNAUTHORIZED:
            return self.__json_responses.unauthorized()
        elif status_code == NOT_FOUND:
            return {"msg":self.__lang.user_not_found()}
        elif status_code == FORBIDDEN:
            return self.__json_responses.forbidden()
        elif status_code == OK:
            return arr
        else:
            return self.__json_responses.server_error()
        
    async def get_settings(self,token:str,response:Response):
        st = await GetSettings().execute(token)
        status_code:int = st[-1]
        response.status_code = status_code

        if status_code == BAD_REQUEST:
            return self.__json_responses.data_not_valid()
        elif status_code == UNAUTHORIZED:
            return self.__json_responses.unauthorized()
        elif status_code == FORBIDDEN:
            return self.__json_responses.forbidden()
        elif status_code == OK:
            return {
                "password_rule":st[0],
                "item_categories":st[1],
                "item_types":st[2],
                "registration_status":st[3],
                "scan_time_routines_tokens":st[4],
                "scan_time_routines_users":st[5],
                "confirmation_period":st[6],
                "disk_space_per_user":st[7]
            }
        else:
            return self.__json_responses.server_error()#INTERNAL_SERVER_ERROR
        
    async def create_user(
            self,
            token:str,
            login:str,
            secret_string:str,
            request:Request,
            response:Response
        ):
        obj = await CreateUser().execute(
            token,
            login,
            secret_string,
            utils.get_client_ip(request),
            True
        )
        secret_code = obj[0]
        backup_codes = obj[1]
        status_code:int = obj[-1]

        response.status_code = status_code

        if status_code == SERVICE_UNAVAILABLE:
            return self.__json_responses.service_is_not_available()
        elif status_code == BAD_REQUEST or utils.arguments(secret_string,login) == False:
            return self.__json_responses.data_not_valid()
        elif status_code == UNAUTHORIZED:
            return self.__json_responses.unauthorized()
        elif status_code == FORBIDDEN:
            return self.__json_responses.forbidden()
        elif status_code == OK:
            return {"msg":self.__lang.registration_was_successful(),"secret_code":secret_code,"backup_codes":backup_codes}
        elif status_code == CONFLICT:
            return {"msg":self.__lang.user_already_exists()}
        else:
            return self.__json_responses.server_error()
        
    async def delete_user(self,token:str,user_id:str,response:Response):
        obj = await DeleteUser().execute(token,user_id)
        status_code:int = obj

        response.status_code = status_code

        if status_code == BAD_REQUEST:
            return self.__json_responses.data_not_valid()
        elif status_code == UNAUTHORIZED:
            return self.__json_responses.unauthorized()
        elif status_code == FORBIDDEN:
            return self.__json_responses.forbidden()
        elif status_code == OK:
            return {"msg":self.__lang.user_has_been_successfully_deleted()}
        else:
            return {"msg":self.__lang.failed_to_delete_user()}
        
    async def update_settings(self,token:str,key:str,value:Any,response:Response):
        obj = await UpdateSettings().execute(token,key,value)
        status_code:int = obj

        response.status_code = status_code
        if status_code == BAD_REQUEST:
            return self.__json_responses.data_not_valid()
        elif status_code == UNAUTHORIZED:
            return self.__json_responses.unauthorized()
        elif status_code == FORBIDDEN:
            return self.__json_responses.forbidden()
        elif status_code == OK:
            return {"msg":self.__lang.settings_have_been_successfully_updated()}
        else:
            return {"msg":self.__lang.failed_to_update_settings()}