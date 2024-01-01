from http.client import BAD_REQUEST, OK
from typing import Any
from mindfulguard.classes.user.base import UserBase


class UserInformation(UserBase):
    def __init__(self) -> None:
        super().__init__()
        self.__tokens: list[dict[str, Any]] = []

    @property
    def login(self) -> str:
        return self._model_user.login
    
    @property
    def reg_ip(self) -> str:
        return self._model_user.reg_ip

    @property
    def created_at(self) -> int:
        return self._model_user.created_at
    
    @property
    def tokens(self) -> list[dict[str, Any]]:
        return self.__tokens

    async def execute(self, token: str) -> None:
        try:
            self._model_token.token = token

            db_get_info = self._pgsql_user.get_information(self._model_token)
            await self._connection.open()
            await db_get_info.execute()
            self._status_code = db_get_info._status_code
            if self._status_code != OK:
                return

            db_get_tokens = self._pgsql_user.get_tokens(self._model_token)
            await db_get_tokens.execute()
            if db_get_tokens.status_code != OK:
                self._status_code = db_get_tokens.status_code
                return
            
            self._model_user.login = db_get_info.response.login
            self._model_user.reg_ip = db_get_info.response.reg_ip
            self._model_user.created_at = db_get_info.response.created_at

            for i in db_get_tokens.response:
                value_dict = {
                    'id': i.id,
                    'created_at': i.created_at,
                    'updated_at': i.updated_at,
                    'device': i.device,
                    'last_ip': i.last_ip,
                    'expiration': i.expiration
                }
                self.__tokens.append(value_dict)

            self._status_code = OK
            return
        except ValueError as e:
            self._status_code = BAD_REQUEST
        finally:
            await self._connection.close()