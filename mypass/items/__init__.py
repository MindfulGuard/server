from fastapi import Request, Response
from mypass.core.languages import Language
from mypass.core.languages.responses import Responses
from mypass.core.response_status_codes import *
from mypass.items.executors.create import Create


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