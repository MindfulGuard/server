from fastapi import Response
from mypass.core.languages import Language
from mypass.core.response_status_codes import *
from mypass.safe.executors.create import Create
from mypass.safe.executors.delete import Delete
from mypass.safe.executors.get import Get
from mypass.safe.executors.update import Update


class Safe:
    def __init__(self):...
    async def create(self,
                     token:str,
                     name:str,
                     description:str,
                     response:Response):
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
    
    async def get(self,token:str,response:Response):
        lang = Language()
        obj_get = Get()
        get = await obj_get.execute(token)
        status_code = get[1]

        response.status_code = status_code

        if status_code == BAD_REQUEST:
            return {"msg":lang.data_not_valid()}
        elif status_code == UNAUTHORIZED:
            return {"msg":lang.unauthorized()}
        elif status_code == NOT_FOUND:
            return {"msg":[],"count":0}
        elif status_code == OK:
            return {"list":get[0],"count":len(get[0])}#!the code analyzer may swear, but errors should not occur!
        else:
            return {"msg":lang.server_error()}
        
    async def update(self,token:str,
                     id:str,
                     name:str,
                     description:str,
                     response:Response):
        lang = Language()
        obj_update = Update()
        update = await obj_update.execute(token,id,name,description)
        status_code = update

        response.status_code = status_code

        if status_code == BAD_REQUEST:
            return {"msg":lang.data_not_valid()}
        elif status_code == UNAUTHORIZED:
            return {"msg":lang.unauthorized()}
        elif status_code == OK:
            return {"msg":lang.safe_was_successfully_updated()}
        else:
            return {"msg":lang.failed_to_update_safe()}

    async def delete(self,token:str,id:str,response:Response):
        lang = Language()
        obj_update = Delete()
        delete = await obj_update.execute(token,id)
        status_code = delete

        response.status_code = status_code

        if status_code == BAD_REQUEST:
            return {"msg":lang.data_not_valid()}
        elif status_code == UNAUTHORIZED:
            return {"msg":lang.unauthorized()}
        elif status_code == OK:
            return {"msg":lang.safe_has_been_successfully_deleted()}
        elif status_code == NOT_FOUND:
            return {"msg":lang.failed_to_delete_the_safe()}
        else:
            return {"msg":lang.server_error()}