from http.client import OK
from math import ceil
from typing import Any
from fastapi import Request
from mindfulguard.classes.audit.base import AuditBase
from loguru import logger


class AuditGet(AuditBase):
    def __init__(self, request: Request) -> None:
        super().__init__(request)
        self.__items_per_page: int
        self.__count_items: int = 0
        self.__total_pages: int = 0
        self.__response_list: list[dict[str, Any]] = []
        logger.debug("AuditGet initialized with request: {}", request)

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
        logger.debug("Executing audit get with token: {}, page: {}, items_per_page: {}", token, page, items_per_page)
        try:
            self._model_token.token = token

            db = self._pgsql_audit.get(self._model_token)
            db_count_items = db.count()
            logger.debug("Opening database connection")
            await self._connection.open()
            await db_count_items.execute()
            
            self.__count_items = db_count_items.count
            logger.debug("Total count items: {}", self.__count_items)

            self.__items_per_page = items_per_page

            if db_count_items.count == 0:
                self._status_code = OK
                logger.debug("No items found. Setting status code to OK")
                return

            self.__total_pages = self.__get_pages(self.__count_items)
            logger.debug("Total pages calculated: {}", self.__total_pages)
            calculate_page = self.__calculate_page(page)
            logger.debug("Calculated page: {}", calculate_page)

            await db.execute(calculate_page[0], calculate_page[1])

            self._status_code = db.status_code
            if page > self.__total_pages:
                logger.warning("Page number {} exceeds total pages {}", page, self.__total_pages)
                return

            for i in db.response:
                item_dict = {
                    'id': i.id,
                    'created_at': i.created_at,
                    'ip': i.ip,
                    'object': i.object,
                    'action': i.action,
                    'device': i.device
                }
                self.__response_list.append(item_dict)
                logger.debug("Added item to response list: {}", item_dict)
            return
        except Exception as e:
            logger.error("An error occurred during audit get execution: {}", e)
            raise
        finally:
            logger.debug("Closing database connection")
            await self._connection.close()

    def __calculate_page(self, page: int) -> tuple[int, int]:
        """
        Returns:
            (limit, offset)
        """
        pp: int = (self.__items_per_page * page)
        logger.debug("Calculating page - Limit: {}, Offset: {}", self.__items_per_page, pp - self.__items_per_page)
        return (self.__items_per_page, pp - self.__items_per_page)
    
    def __get_pages(self, count_item: int) -> int:
        if self.__items_per_page <= 0:
            logger.warning("Items per page is less than or equal to 0. Returning 0 pages.")
            return 0
        total_pages = ceil(count_item / self.__items_per_page)
        logger.debug("Total pages: {}", total_pages)
        return total_pages
