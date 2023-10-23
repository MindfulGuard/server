from fastapi import Response
from mindfulguard.core.languages import Language
from mindfulguard.core.languages.responses import Responses
from mindfulguard.core.response_status_codes import *
from mindfulguard.safe.executors.create import Create
from mindfulguard.safe.executors.delete import Delete
from mindfulguard.safe.executors.get import Get
from mindfulguard.safe.executors.update import Update


class Safe:
    def __init__(self):
        self.__lang = Language()
        self.__json_responses = Responses(self.__lang)

    async def create(self,
                     token:str,
                     name:str,
                     description:str,
                     response:Response):
        obj_create = Create()
        status_code = await obj_create.execute(token,name,description)
        response.status_code = status_code
        
        if status_code == BAD_REQUEST:
            return self.__json_responses.data_not_valid()
        elif status_code == OK:
            return {"msg":self.__lang.safe_was_successfully_created()}
        elif status_code == UNAUTHORIZED:
            return self.__json_responses.unauthorized()
        else:
            return {"msg":self.__lang.failed_to_create_a_safe()}
        
    async def update(self,token:str,
                     id:str,
                     name:str,
                     description:str,
                     response:Response):
        obj_update = Update()
        update = await obj_update.execute(token,id,name,description)
        status_code = update

        response.status_code = status_code

        if status_code == BAD_REQUEST:
            return self.__json_responses.data_not_valid()
        elif status_code == UNAUTHORIZED:
            return self.__json_responses.unauthorized()
        elif status_code == OK:
            return {"msg":self.__lang.safe_was_successfully_updated()}
        else:
            return {"msg":self.__lang.failed_to_update_safe()}

    async def delete(self,token:str,id:str,response:Response):
        obj_update = Delete()
        delete = await obj_update.execute(token,id)
        status_code = delete

        response.status_code = status_code

        if status_code == BAD_REQUEST:
            return self.__json_responses.data_not_valid()
        elif status_code == UNAUTHORIZED:
            return self.__json_responses.unauthorized()
        elif status_code == OK:
            return {"msg":self.__lang.safe_has_been_successfully_deleted()}
        elif status_code == NOT_FOUND:
            return {"msg":self.__lang.failed_to_delete_the_safe()}
        else:
            return self.__json_responses.server_error()