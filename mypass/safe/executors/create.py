from mypass.authentication.executors import get_authorization_token
from mypass.core.configuration import Safe, ServerConfiguration
from mypass.core.response_status_codes import *
from mypass.core.security import sha256s
import mypass.database.postgresql.safe as pgsql_safe
from mypass.utils import Validation


class Create:
    def __init__(self):...
    async def execute(self,token:str,name:str,description:str):
        obj_safe = pgsql_safe.Safe()
        validation = Validation()
        safe_lengths_conf = self.__get_lengths()
        tokenf:str = get_authorization_token(token)
        
        if validation.validate_token(tokenf) == False or len(name)>safe_lengths_conf.get_name_length() or validation.validate_description(description) == False:
            return BAD_REQUEST
        return await obj_safe.create(sha256s(tokenf),name,description)
    
    def __get_lengths(self):
        server_conf = ServerConfiguration()
        return Safe(server_conf).lengths() 