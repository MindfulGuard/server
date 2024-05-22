from http.client import BAD_REQUEST
from fastapi import Request, Response
from loguru import logger
from mindfulguard.classes.authentication.base import AuthenticationBase
from mindfulguard.net.ip import get_client_ip


class SignUp(AuthenticationBase):
    def __init__(self, request: Request) -> None:
        super().__init__(request)
        self.__secret_code: str = self._security.totp('').generate_secret_code()
        self.__backup_codes: list[int] = self._security.totp('').generate_backup_codes()

    @property
    def secret_code(self) -> str:
        return self.__secret_code

    @property
    def backup_codes(self) -> list[int]:
        return self.__backup_codes

    async def execute(
            self,
            login: str,
            secret_string: str,
            confirm: bool
        ) -> None:
            logger.debug(
                "Input data: login: {}, secret_string: {}, confirm: {}",
                login,
                secret_string,
                confirm
            )
            try:
                self._model_user.login = login
                self._model_user.secret_string = secret_string
                self._model_user.reg_ip = get_client_ip(self._request)
                self._model_user.confirm = confirm
                self._model_code.secret_code = self.__secret_code
                self._model_code.backup_codes = self.__backup_codes
                await self._connection.open()
                db = self._pgsql_auth.sign_up(self._model_user, self._model_code)
                await db.execute()
                self._status_code = db.status_code
            except ValueError:
                self._status_code = BAD_REQUEST
            finally:
                await self._connection.close()