from http.client import NOT_FOUND
from fastapi import Response
from mindfulguard.core.languages import Language
from mindfulguard.core.languages.responses import Responses
from mindfulguard.core.response_status_codes import BAD_REQUEST, OK, UNAUTHORIZED
from mindfulguard.user.executors.__settings__ import UserSettings
from mindfulguard.user.executors.info import UserInformation

class User:
    def __init__(self):
        self.__lang = Language()
        self.__json_responses = Responses(self.__lang)
    
    async def settings_one_time_codes(
            self,
            token:str,
            secret_string:str,
            type:str,
            response:Response
        ):
        obj = UserSettings()
        ot_codes = await obj.one_time_codes(token,secret_string,type)
        data = ot_codes[0]
        status_code:int = ot_codes[1]

        response.status_code = status_code
        if status_code == BAD_REQUEST:
            return self.__json_responses.data_not_valid()
        elif status_code == UNAUTHORIZED:
            return self.__json_responses.unauthorized()
        elif status_code == OK:
            return {"msg":self.__lang.successfully_updated(),"data":data}
        else:
            return {"msg":self.__lang.failed_to_update()}
        
    async def settings_secret_string(
            self,
            token:str,
            login:str,
            old_secret_string:str,
            new_secret_string:str,
            code:str,
            response:Response
        ):
        obj = UserSettings()
        sc = await obj.secret_string_(
            token,
            login,
            old_secret_string,
            new_secret_string,
            code
        )
        status_code:int = sc

        response.status_code = status_code
        if status_code == BAD_REQUEST:
            return self.__json_responses.data_not_valid()
        elif status_code == UNAUTHORIZED:
            return self.__json_responses.unauthorized()
        elif status_code == OK:
            return {"msg":self.__lang.successfully_updated()}
        elif status_code == NOT_FOUND:
            return {"msg":self.__lang.failed_to_update()}
        else:
            return {"msg":self.__lang.failed_to_update()}
    
    async def get_info(
            self,
            token:str,
            response:Response
            ):
        user_info =  UserInformation()

        tks = await user_info.get_tokens(token)
        data:list = tks[0]
        status_code = tks[1]

        information = await user_info.get_info(token)
        info = information[0]

        response.status_code = status_code

        if status_code == OK:
            user_disk = await user_info.get_disk_space(info['username'])
            return {
                "tokens":data,
                "count_tokens":len(data),
                "information":info,
                "disk":{
                    "total_space":user_disk[1],
                    "filled_space":user_disk[0]
                }
            }
        elif status_code == BAD_REQUEST:
            return self.__json_responses.data_not_valid()
        elif status_code == UNAUTHORIZED:
            return self.__json_responses.unauthorized()
        else:
            return self.__json_responses.server_error()
        
    async def delete_user(
        self,
        token:str,
        login:str,
        secret_string:str,
        code:str,
        response:Response
    ):
        user_settings = UserSettings()
        status_code = await user_settings.delete_user(
            token,
            login,
            secret_string,
            code
        )
        response.status_code = status_code

        if status_code == BAD_REQUEST:
            return self.__json_responses.data_not_valid()
        elif status_code == UNAUTHORIZED:
            return self.__json_responses.unauthorized()
        elif status_code == OK:
            return {"msg":self.__lang.user_has_been_successfully_deleted()}
        else:
            return {"msg":self.__lang.failed_to_delete_user()}