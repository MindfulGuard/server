from fastapi import Request, Response
from mypass.core.languages import Language
from mypass.core.languages.responses import Responses
from mypass.core.response_status_codes import *
from mypass.items.executors.create import Create
from mypass.items.executors.favorite import Favorite
from mypass.items.executors.update import Update
from mypass.items.executors.delete import Delete


class Item:
    def __init__(self):
        self.__lang = Language()
        self.__json_responses = Responses(self.__lang)
    
    async def create(self,
                     token:str,
                     json_item,
                     safe_id:str,
                     response:Response):
        
        obj_create = Create()

        status_code = await obj_create.execute(token, safe_id, json_item)
        response.status_code = status_code
        
        if status_code == BAD_REQUEST:
            return self.__json_responses.data_not_valid()
        elif status_code == OK:
            return {"msg":self.__lang.item_was_successfully_created()}
        elif status_code == UNAUTHORIZED:
            return self.__json_responses.unauthorized()
        else:
            return {"msg":self.__lang.failed_to_create_item()}
    
    async def update(self,
                     token:str,
                     json_item,
                     safe_id:str,
                     item_id:str,
                     response:Response):
        
        obj = Update()

        status_code = await obj.execute(token, safe_id, item_id, json_item)
        response.status_code = status_code
        
        if status_code == BAD_REQUEST:
            return self.__json_responses.data_not_valid()
        elif status_code == OK:
            return {"msg":self.__lang.item_has_been_successfully_updated()}
        elif status_code == UNAUTHORIZED:
            return self.__json_responses.unauthorized()
        else:
            return {"msg":self.__lang.failed_to_update_the_item()}
        
    async def delete(self,
                     token:str,
                     safe_id:str,
                     item_id:str,
                     response:Response):
        
        obj = Delete()

        status_code = await obj.execute(token, safe_id, item_id)
        response.status_code = status_code
        
        if status_code == BAD_REQUEST:
            return self.__json_responses.data_not_valid()
        elif status_code == OK:
            return {"msg":self.__lang.item_was_successfully_deleted()}
        elif status_code == UNAUTHORIZED:
            return self.__json_responses.unauthorized()
        else:
            return {"msg":self.__lang.failed_to_delete_item()}
        
    async def set_favorite(self,
                     token:str,
                     safe_id:str,
                     item_id:str,
                     response:Response):
        
        obj = Favorite()

        status_code = await obj.execute(token, safe_id, item_id)
        response.status_code = status_code
        
        if status_code == BAD_REQUEST:
            return self.__json_responses.data_not_valid()
        elif status_code == OK:
            return {"msg":"ok"}
        elif status_code == UNAUTHORIZED:
            return self.__json_responses.unauthorized()
        else:
            return {"msg":self.__lang.failed_to_update_favorite()}