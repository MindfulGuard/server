from http.client import BAD_REQUEST, NOT_FOUND, OK
from typing import Any
from mindfulguard.classes.admin.base import AdminBase


class AdminUsersSearchUsers(AdminBase):
    def __init__(self) -> None:
        super().__init__()
        self.__response: dict[str, Any] = {}

    @property
    def response(self) -> dict[str, Any]:
        return self.__response

    async def execute(self, token: str, by: str, value: str) -> None:
        try:
            self._model_token.token = token
            if by == "id":
                self._model_user.id = value
            elif by == "username":
                self._model_user.login = value
            else:
                self._status_code = BAD_REQUEST
                return

            db = self._pgsql_admin.search_users(self._model_token, self._model_user)
            await self._connection.open()
            await db.execute(by)
            self._status_code = db.status_code
            if db.status_code != OK:
                return

            self.__response['id'] = db.response.id
            self.__response['username'] = db.response.login
            self.__response['ip'] = db.response.reg_ip
            self.__response['confirm'] = db.response.confirm
            self.__response['created_at'] = db.response.created_at
            return
        except ValueError:
            self._status_code = BAD_REQUEST
        finally:
            await self._connection.close()