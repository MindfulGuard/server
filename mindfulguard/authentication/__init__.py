from typing import Annotated
from fastapi import Form, Header, Request, Response
from mindfulguard.authentication.executors import get_authorization_token

from mindfulguard.authentication.executors.sign_in import SignIn
from mindfulguard.authentication.executors.sign_out import SignOut
from mindfulguard.authentication.executors.sign_up import SignUp
from mindfulguard.core import security
from mindfulguard.core.languages import Language
from mindfulguard.core.languages.responses import Responses
from mindfulguard.core.response_status_codes import *
from mindfulguard.database.postgresql import authentication
import mindfulguard.utils as utils

class Authentication:
    def __init__(self):
        self.__lang = Language()
        self.__json_responses = Responses(self.__lang)
    async def sign_up(self,
                      login:str,
                      secret_string:str,
                      confirm:bool,
                      request: Request,
                      response:Response):

        sign_up  = SignUp()
        client_ip:str = utils.get_client_ip(request)
        exec = await sign_up.execute(login,secret_string,client_ip,confirm)
        secret_code = exec[0]
        reserve_codes = exec[1]
        status_cod = exec[2]
        response.status_code = status_cod
        if status_cod == SERVICE_UNAVAILABLE:
            return self.__json_responses.service_is_not_available()
        elif status_cod == BAD_REQUEST or utils.arguments(secret_string,login) == False:
            return self.__json_responses.data_not_valid()
        elif status_cod == OK:
            return {"msg":self.__lang.registration_was_successful(),"secret_code":secret_code,"backup_codes":reserve_codes}
        elif status_cod == CONFLICT:
            return {"msg":self.__lang.user_already_exists()}
        else:
            return self.__json_responses.server_error()

    async def sign_in(self,login:str,
                      secret_string:str,
                      code:str,type:str,
                      user_agent: str,
                      expiration:int,request:Request,
                      response:Response):
        sign_in  = SignIn()
        client_ip:str = utils.get_client_ip(request)
        exec = await sign_in.execute(login,secret_string,code,type,user_agent,client_ip,expiration)
        status_code:int = exec[1]
        token:str|None = exec[0]
        response.status_code = status_code
        if status_code == BAD_REQUEST:
            return self.__json_responses.data_not_valid()
        elif status_code == OK:
            return {"msg":self.__lang.successful_login(),"token":token}
        elif status_code == NOT_FOUND:
            return {"msg":self.__lang.user_not_found()}
        else:
            return self.__json_responses.server_error()#INTERNAL_SERVER_ERROR

    async def sign_out(self,
                       token:str,
                       token_id,
                       response:Response):
        sign_out  = SignOut()
        status_code = await sign_out.execute(token,token_id)
        response.status_code = status_code
        if status_code == BAD_REQUEST:
            return self.__json_responses.data_not_valid()
        elif status_code == UNAUTHORIZED:
            return self.__json_responses.unauthorized()
        elif status_code == OK:
            return {"msg":self.__lang.session_token_has_been_deleted()}
        elif status_code == NOT_FOUND:
            return {"msg":self.__lang.failed_to_delete_token()}
        else:
            return self.__json_responses.server_error()#INTERNAL_SERVER_ERROR
        
    async def update_token_info(self,
                                token:str,
                                device:str,
                                request:Request)->None:
        client_ip:str = utils.get_client_ip(request)
        auth =  authentication.Authentication()
        validate = utils.Validation()
        if validate.validate_token(token) == False or validate.validate_user_agent(device) == False:
            return
        await auth.update_token_info(security.sha256s(get_authorization_token(token)),device,client_ip)