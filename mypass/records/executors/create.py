from mypass.authentication.executors import get_authorization_token
from mypass.core.response_status_codes import *
import mypass.database.postgresql.items as pgsql_items
from mypass.utils import Validation

#
class Create:
    def __init__(self):...
    async def execute(self,token:str,json:str):
        obj = pgsql_items.Item()
        validation = Validation()
        tokenf:str = get_authorization_token(token)
        
        #!!!You need to implement deserialization for json, etc. follow the documentation from github!!!
        
        if validation.validate_token(tokenf) == False and validation.validate_json(json):
            return BAD_REQUEST
        #return await obj.create()