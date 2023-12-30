from http.client import BAD_REQUEST, OK
from math import ceil
from typing import Any
from mindfulguard.classes.admin.base import AdminBase


class AdminUsersGetByPage(AdminBase):
    def __init__(self) -> None:
        super().__init__()
        self.__PER_PAGE: int = 10
        self.__users_list: list[dict[str, Any]] = []
        self.__total_pages: int = 0
        self.__total_users: int = 0 
        self.__total_storage_size: int = 0

    @property
    def total_users(self) -> int:
        return self.__total_users

    @property
    def total_pages(self) -> int:
        return self.__total_pages
    
    @property
    def total_storage_size(self) -> int:
        return self.__total_storage_size

    @property
    def users_list(self) -> list[dict[str, Any]]:
        return self.__users_list

    async def execute(self, token: str, page: int) -> None:
        try:
            self._model_token.token = token

            db = self._pgsql_admin.get_users(
                self._model_token
            )
            count_users = db.count_users()
            await self._connection.open()
            await count_users.execute()

            self.__total_users = count_users.count
            self.__total_pages = self.__get_pages(self.__total_users)
            calculate_page = self.__calculate_page(page)

            await db.execute(
                calculate_page[0],
                calculate_page[1]
            )
            if db.status_code != OK:
                self._status_code = db.status_code
                return
            
            self.__total_storage_size = self._s3.bucket().total_size

            self._status_code = OK
            if page > self.__total_pages:
                return

            for i in db.response:
                value_dict = {
                    'id': i.id,
                    'username': i.login,
                    'ip': i.reg_ip,
                    'confirm': i.confirm,
                    'created_at': i.created_at,
                }
                self.__users_list.append(value_dict)

        except ValueError:
            self._status_code = BAD_REQUEST
        finally:
            await self._connection.close()

    def __calculate_page(self, page: int) -> tuple[int, int]:
        """
        Returns:
            (limit, offset)
        """
        pp = (self.__PER_PAGE * page)
        return (pp, pp - self.__PER_PAGE)
    
    def __get_pages(self, count_users: int)->int:
        return ceil(count_users / self.__PER_PAGE)