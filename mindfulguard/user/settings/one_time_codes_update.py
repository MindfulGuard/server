from http.client import BAD_REQUEST
from typing import Literal
from mindfulguard.classes.user.base import UserBase

class UserSettingsUpdateOneTimeCodes(UserBase):
    def __init__(self) -> None:
        super().__init__()

    @property
    def response(self) -> str | list[int]:
        return self._response

    async def execute(
        self,
        token: str,
        secret_string: str,
        type: Literal['basic', 'backup']
    ) -> None:
        try:
            self._model_token.token = token
            self._model_user.secret_string = secret_string

            if type == 'basic':
                secret_code: str = self._security.totp('').generate_secret_code()
                self._response = secret_code
                self._model_code.secret_code = secret_code
                await self.__totp()
                return
            elif type == 'backup':
                backup_codes: list[int] = self._security.totp('').generate_backup_codes()
                self._response = backup_codes
                self._model_code.backup_codes = backup_codes
                await self.__backup_codes()
                return
            else:
                self._status_code = BAD_REQUEST
                return
        except ValueError:
            self._status_code = BAD_REQUEST
    
    async def __totp(self) -> None:
        try:
            db = self._pgsql_user.settings().update_one_time_code(
                self._model_user,
                self._model_token,
                self._model_code
            ).totp()
            await self._connection.open()
            await db.execute()
            self._status_code = db.status_code
        finally:
            await self._connection.close()

    async def __backup_codes(self):
        try:
            db = self._pgsql_user.settings().update_one_time_code(
                self._model_user,
                self._model_token,
                self._model_code
            ).backup()
            await self._connection.open()
            await db.execute()
            self._status_code = db.status_code
        finally:
            await self._connection.close()