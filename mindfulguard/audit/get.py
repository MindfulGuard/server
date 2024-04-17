from http.client import OK
from math import ceil
from typing import Any
from fastapi import Request
from mindfulguard.classes.audit.base import AuditBase


class AuditGet(AuditBase):
    def __init__(self, request: Request) -> None:
        super().__init__(request)
        self.__items_per_page: int
        self.__count_items: int = 0
        self.__total_pages: int = 0
        self.__response_list: list[dict[str, Any]] = []

    @property
    def items_per_page(self) -> int:
        return self.__items_per_page
    
    @property
    def count_items(self) -> int:
        return self.__count_items
    
    @property
    def total_pages(self) -> int:
        return self.__total_pages
    
    @property
    def response_list(self) -> list[dict[str, Any]]:
        return self.__response_list

    async def execute(
        self,
        token: str,
        page: int,
        items_per_page: int,
    ) -> None:
        try:
            self._model_token.token = token

            db = self._pgsql_audit.get(self._model_token)
            db_count_items = db.count()
            await self._connection.open()
            await db_count_items.execute()
            
            self.__count_items = db_count_items.count

            self.__items_per_page = items_per_page

            if db_count_items.count == 0:
                self._status_code = OK
                return

            self.__total_pages = self.__get_pages(self.__count_items)
            calculate_page = self.__calculate_page(page)

            await db.execute(calculate_page[0], calculate_page[1])

            self._status_code = db.status_code
            if page > self.__total_pages:
                return

            for i in db.response:
                dict = {
                    'id': i.id,
                    'created_at': i.created_at,
                    'ip': i.ip,
                    'object': i.object,
                    'action': i.action,
                    'device': i.device
                }
                self.__response_list.append(dict)
            return
        finally:
            await self._connection.close()

    def __calculate_page(self, page: int) -> tuple[int, int]:
        """
        Returns:
            (limit, offset)
        """
        pp: int = (self.__items_per_page * page)
        return (self.__items_per_page, pp - self.__items_per_page)
    
    def __get_pages(self, count_item: int) -> int:
        if self.__items_per_page <= 0:
            return 0
        return ceil(count_item / self.__items_per_page)