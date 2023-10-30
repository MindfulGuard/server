import asyncio
import threading
from fastapi import Request, Response, UploadFile
from mindfulguard.core.languages import Language
from mindfulguard.core.languages.responses import Responses
from mindfulguard.core.response_status_codes import *
from mindfulguard.files.executors.get import Get
from mindfulguard.items.executors.create import Create
from mindfulguard.items.executors.favorite import Favorite
from mindfulguard.items.executors.move import Move
import mindfulguard.safe.executors.get as safe
import mindfulguard.items.executors.get as item
from mindfulguard.items.executors.update import Update
from mindfulguard.items.executors.delete import Delete
from mindfulguard.user.executors.info import UserInformation


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
    
    async def get(self, token: str, response: Response):
        semaphore = asyncio.Semaphore(2)

        async def get_item():
            async with semaphore:
                obj_item = item.Get()
                return await obj_item.execute(token)

        async def get_safe():
            async with semaphore:
                obj_safe = safe.Get()
                return await obj_safe.execute(token)

        async def get_files():
            async with semaphore:
                return await Get(token).execute()

        async def get_user_info():
            async with semaphore:
                user_info = UserInformation()
                information = await user_info.get_info(token)
                info = information[0]
                if information[-1] != OK:
                    return (0,0)
                user_disk = await user_info.get_disk_space(info['username'])
                return user_disk

        item_get, safe_get, fget, user_disk = await asyncio.gather(
            get_item(), get_safe(), get_files(), get_user_info()
        )

        status_code_item:int = item_get[3]
        status_code_safe:int = safe_get[1]

        if status_code_item == BAD_REQUEST or status_code_safe == BAD_REQUEST:
            response.status_code = BAD_REQUEST
            return self.__json_responses.data_not_valid()
        elif status_code_item == UNAUTHORIZED or status_code_safe == UNAUTHORIZED:
            response.status_code = UNAUTHORIZED
            return self.__json_responses.unauthorized()
        elif status_code_item == OK or status_code_safe == OK:
            result = {}
            safes_json = {"safes":safe_get[0]}
            tags_list = {"tags":item_get[1]}
            favorites_list = {"favorites":item_get[2]}
            files_json = {"files":fget[0]}
            disk_json = {"disk":{"total_space":user_disk[1],"filled_space":user_disk[0]}}

            result.update(safes_json)
            result.update({"count":len(safe_get[0])})

            result.update(tags_list)
            result.update(favorites_list)
            result.update(item_get[0])
            result.update(disk_json)
            result.update(files_json)

            response.status_code = OK
            return result
        else:
            response.status_code = INTERNAL_SERVER_ERROR
            return self.__json_responses.server_error()

    async def move(self,
                     token:str,
                     old_safe_id:str,
                     new_safe_id:str,
                     item_id:str,
                     response:Response):
        
        obj = Move()

        status_code = await obj.execute(token, old_safe_id, new_safe_id, item_id)
        response.status_code = status_code
        
        if status_code == BAD_REQUEST:
            return self.__json_responses.data_not_valid()
        elif status_code == OK:
            return {"msg":self.__lang.item_was_successfully_moved_to_safe()}
        elif status_code == UNAUTHORIZED:
            return self.__json_responses.unauthorized()
        else:
            return {"msg":self.__lang.failed_to_move_item_to_safe()}

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
            return {"msg":self.__lang.item_was_successfully_added_to_favorites()}
        elif status_code == UNAUTHORIZED:
            return self.__json_responses.unauthorized()
        else:
            return {"msg":self.__lang.failed_to_update_favorite()}