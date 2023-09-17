from typing import Annotated
from fastapi import Form, Header, Request, Response
from mypass.authentication.executors import get_authorization_token
from mypass.authentication.executors.get_tokens import GetTokens

from mypass.authentication.executors.sign_in import SignIn
from mypass.authentication.executors.sign_out import SignOut
from mypass.authentication.executors.sign_up import SignUp
from mypass.core import security
from mypass.core.languages import Language
from mypass.core.response_status_codes import *
from mypass.database.postgresql import authentication
import mypass.utils as utils

class Authentication:
    async def sign_up(self,
                      login:str,
                      secret_string:str,
                      request: Request,
                      response:Response):
        lang = Language()
        sign_up  = SignUp()
        client_ip:str = utils.get_client_ip(request)
        exec = await sign_up.execute(login,secret_string,client_ip)
        secret_code = exec[0]
        reserve_codes = exec[1]
        status_cod = exec[2]
        response.status_code = status_cod
        if status_cod == SERVICE_UNAVAILABLE:
            return {"msg":lang.service_is_not_available(),"secret_code":None,"reserve_codes":None}
        elif status_cod == BAD_REQUEST or utils.arguments(secret_string,login) == False:
            return {"msg":lang.data_not_valid(),"secret_code":None,"reserve_codes":None}
        elif status_cod == OK:
            return {"msg":lang.registration_was_successful(),"secret_code":secret_code,"reserve_codes":reserve_codes}
        elif status_cod == CONFLICT:
            return {"msg":lang.user_already_exists(),"secret_code":None,"reserve_codes":None}
        else:
            return {"msg":lang.server_error(),"secret_code":None,"reserve_codes":None}#INTERNAL_SERVER_ERROR

    async def sign_in(self,login:str,
                      secret_string:str,
                      code:str,type:str,
                      user_agent: str,
                      expiration:int,request:Request,
                      response:Response):
        lang = Language()
        sign_in  = SignIn()
        client_ip:str = utils.get_client_ip(request)
        exec = await sign_in.execute(login,secret_string,code,type,user_agent,client_ip,expiration)
        status_code:int = exec[1]
        token:str|None = exec[0]
        response.status_code = status_code
        if status_code == BAD_REQUEST:
            return {"msg":lang.data_not_valid(),"token":None}
        elif status_code == OK:
            return {"msg":lang.successful_login(),"token":token}
        elif status_code == NOT_FOUND:
            return {"msg":lang.user_not_found(),"token":None}
        else:
            return {"msg":lang.server_error(),"token":None}#INTERNAL_SERVER_ERROR

    async def sign_out(self,
                       token:str,
                       token_id,
                       response:Response):
        lang = Language()
        sign_out  = SignOut()
        status_code = await sign_out.execute(token,token_id)
        response.status_code = status_code
        if status_code == BAD_REQUEST:
            return {"msg":lang.data_not_valid()}
        elif status_code == OK:
            return {"msg":lang.session_token_has_been_deleted()}
        elif status_code == NOT_FOUND:
            return {"msg":lang.failed_to_delete_token()}
        else:
            return {"msg":lang.server_error()}#INTERNAL_SERVER_ERROR
        
    async def update_token_info(self,
                                token:str,
                                device:str,
                                request:Request)->None:
        client_ip:str = utils.get_client_ip(request)
        auth =  authentication.Authentication()
        await auth.update_token_info(security.sha256s(get_authorization_token(token)),device,client_ip)
    
    async def get_tokens(self,token:str,response:Response):
        auth =  GetTokens()

        tks = await auth.execute(get_authorization_token(token))
        data = tks[0]
        status_code = tks[1]

        response.status_code = status_code
        return {"list":data,"count":len(data)}