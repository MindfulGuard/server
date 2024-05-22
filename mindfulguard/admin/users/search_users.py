from http.client import BAD_REQUEST, OK
from typing import Any
from loguru import logger
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
            logger.info("Executing 'AdminUsersSearchUsers' with token: {}, by: {}, value: {}", token, by, value)
            self._model_token.token = token
            if by == "id":
                self._model_user.id = value
            elif by == "username":
                self._model_user.login = value
            else:
                self._status_code = BAD_REQUEST
                logger.error("Invalid search criteria: {}", by)
                return

            db = self._pgsql_admin.search_users(self._model_token, self._model_user)
            await self._connection.open()
            await db.execute(by)
            self._status_code = db.status_code
            if db.status_code != OK:
                logger.warning("Failed to execute search query. Status Code: {}", db.status_code)
                return

            self.__response['id'] = db.response.id
            self.__response['username'] = db.response.login
            self.__response['ip'] = db.response.reg_ip
            self.__response['confirm'] = db.response.confirm
            self.__response['created_at'] = db.response.created_at
            logger.info("User search successful. Result: {}", self.__response)
            return
        except ValueError as e:
            self._status_code = BAD_REQUEST
            logger.error("An error occurred: {}", e)
        finally:
            await self._connection.close()
            logger.debug("Connection closed.")
