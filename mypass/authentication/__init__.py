from fastapi import Request, Response
from mypass.authentication.executors.sign_up import SignUp
from mypass.core.languages import Language
from mypass.core.models import SignInModel
import mypass.database.postgresql.authentication as authentication
from mypass.core.response_status_codes import *
import mypass.utils as utils

class Authentication():
    async def sign_up(self,model:SignInModel,request: Request,response:Response):
        lang = Language()
        sgn  = SignUp()
        client_ip:str = request.client.host
        execu = await sgn.execute(model.email,model.secret_string,model.secret_string,client_ip)
        response.status_code = execu
        if execu == SERVICE_UNAVAILABLE:
            return {"msg":lang.service_is_not_available()}
        elif execu == BAD_REQUEST:
            return {"msg":lang.data_not_valid()}
        elif execu == OK:
            return {"msg":lang.registration_was_successful()}
        elif execu == CONFLICT:
            print(lang.user_already_exists())
            return {"msg":lang.user_already_exists()}
        else:
            response.status_code = INTERNAL_SERVER_ERROR
            return {"msg":lang.server_error()}

#!REWRITE!
class SignIn():
    async def execute(self,email:str,secret_string:bytes,device:str,ip:str):
        """
            Returns:
                -1 - registration is not allowed\n
                1 - user not was successful\n
                0 - the user already exists
        """
        valid = utils.Validation()
        token:str = utils.generate_512_bit_token_string()
        if valid.validate(email) == False:
            return -2
        elif await authentication.Authentication().sign_in(
            email,
            secret_string,
            token,
            device,
            ip
        ) == True:
            return token
        else:
            return 0