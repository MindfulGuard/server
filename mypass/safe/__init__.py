from fastapi import Response
from mypass.core.languages import Language
from mypass.core.response_status_codes import *
from mypass.safe.executors.create import Create


class Safe:
    def __init__(self):...
    async def create(self,token:str,name:str,description:str,response:Response):
        lang = Language()
        obj_create = Create()
        status_code = await obj_create.execute(token,name,description)
        response.status_code = status_code
        
        if status_code == BAD_REQUEST:
            return {"msg":lang.data_not_valid()}
        elif status_code == OK:
            return {"msg":lang.safe_was_successfully_created()}
        elif status_code == UNAUTHORIZED:
            return {"msg":lang.unauthorized()}
        else:
            return {"msg":lang.server_error()}