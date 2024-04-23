from typing import Any
from fastapi import Response
from mindfulguard.classes.models.item_json import Item
from mindfulguard.classes.responses import HttpResponse
from mindfulguard.items.create import Create
from mindfulguard.items.delete import Delete
from mindfulguard.items.favorite import Favorite
from mindfulguard.items.move import Move
from mindfulguard.items.update import Update

class Items:
    def __init__(self, response: Response) -> None:
        self.__http_response = HttpResponse()
        self.__response: Response = response

    async def create(self, token: str, safe_id: str, item: Item) -> dict[str, Any]:
        obj = Create()
        await obj.execute(token, safe_id, item)
        self.__response.status_code = obj.status_code
        response = self.__http_response.get(obj.status_code).to_json()
        return response
    
    async def update(
        self,
        token: str,
        safe_id: str,
        record_id: str,
        item: Item
    ) -> dict[str, Any]:
        obj = Update()
        await obj.execute(
            token,
            safe_id,
            record_id,
            item
        )
        self.__response.status_code = obj.status_code
        response = self.__http_response.get(obj.status_code).to_json()
        return response
    
    async def delete(
        self,
        token: str,
        safe_id: str,
        record_id: str
    ) -> dict[str, Any]:
        obj = Delete()
        await obj.execute(
            token,
            safe_id,
            record_id
        )
        self.__response.status_code = obj.status_code
        response = self.__http_response.get(obj.status_code).to_json()
        return response
    
    async def favorite(
        self,
        token: str,
        safe_id: str,
        record_id: str
    ) -> dict[str, Any]:
        obj = Favorite()
        await obj.execute(token, safe_id, record_id)
        self.__response.status_code = obj.status_code

        response = self.__http_response.get(obj.status_code).to_json()
        return response
    
    async def move(
        self,
        token: str,
        old_safe_id: str,
        new_safe_id: str,
        record_id: str
    ) -> dict[str, Any]:
        obj = Move()
        await obj.execute(
            token,
            old_safe_id,
            new_safe_id,
            record_id
        )
        self.__response.status_code = obj.status_code

        response = self.__http_response.get(obj.status_code).to_json()
        return response