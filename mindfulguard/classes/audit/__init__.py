from typing import Any
from fastapi import Request, Response
from mindfulguard.audit.get import AuditGet
from mindfulguard.audit.insert import AuditInsert

class Audit:
    def __init__(self, request: Request) -> None:
        self.__request = request

    async def insert(
        self,
        token: str,
        device: str
    ) -> None:
        return await AuditInsert(self.__request).execute(
            token,
            device
        )
    
    async def get(self, token: str, page: int, items_per_page: int, response: Response):
        obj = AuditGet(self.__request)
        await obj.execute(token, page, items_per_page)

        response.status_code = obj.status_code
        result: dict[str, Any] = {
            'page': page,
            'total_pages': obj.total_pages,
            'items_per_page': obj.items_per_page,
            'total_items': obj.count_items,
            'list': obj.response_list
        }

        return result