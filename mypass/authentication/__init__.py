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

class Authentication():
    async def sign_up(self,email: Annotated[str, Form()], login: Annotated[str, Form()],secret_string:Annotated[bytes, Form()],request: Request,response:Response):
        lang = Language()
        sign_up  = SignUp()
        client_ip:str = utils.get_client_ip(request)
        exec = await sign_up.execute(email,secret_string,login,client_ip)
        response.status_code = exec
        if exec == SERVICE_UNAVAILABLE:
            return {"msg":lang.service_is_not_available()}
        elif exec == BAD_REQUEST or utils.arguments(email,secret_string,login) == False:
            return {"msg":lang.data_not_valid()}
        elif exec == OK:
            return {"msg":lang.registration_was_successful()}
        elif exec == CONFLICT:
            return {"msg":lang.user_already_exists()}
        else:
            return {"msg":lang.server_error()}#INTERNAL_SERVER_ERROR

    async def sign_in(self,email: Annotated[str, Form()],secret_string:Annotated[bytes, Form()],user_agent: Annotated[str, Header()],request: Request,response:Response):
        lang = Language()
        sign_in  = SignIn()
        client_ip:str = utils.get_client_ip(request)
        exec = await sign_in.execute(email,secret_string,user_agent,client_ip)
        status_code:int = exec[0]
        response.status_code = status_code
        if status_code == BAD_REQUEST:
            return {"msg":lang.data_not_valid(),"token":exec[1]}
        elif status_code == OK:
            return {"msg":lang.user_found(),"token":exec[1]}
        elif status_code == NOT_FOUND:
            return {"msg":lang.user_not_found(),"token":None}
        else:
            return {"msg":lang.server_error(),"token":None}#INTERNAL_SERVER_ERROR

    #!it is necessary to add the output of messages and updates of the token information!
    async def sign_out(self,token:str,token_id:Annotated[str, Form()],response:Response):
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
    
    async def update_token_info(self,token:str,device:str,request:Request)->None:
        client_ip:str = utils.get_client_ip(request)
        auth =  authentication.Authentication()
        await auth.update_token_info(security.sha256s(get_authorization_token(token)),device,client_ip)
    
    async def get_tokens(self,token:str,response:Response):
        lang = Language()
        auth =  GetTokens()

        tks = await auth.execute(get_authorization_token(token))
        data = tks[0]
        status_code = tks[1]

        response.status_code = status_code

        if status_code == BAD_REQUEST:
            return {"list":data}
        elif status_code == OK:
            return {"list":data}
        elif status_code == NOT_FOUND:
            return {"list":data}
        else:
            return {"list":data}#INTERNAL_SERVER_ERROR