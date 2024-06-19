from http.client import BAD_REQUEST, INTERNAL_SERVER_ERROR
from typing import Any
from fastapi import Request
from loguru import logger
from mindfulguard.classes.authentication.base import AuthenticationBase
from mindfulguard.net.ip import get_client_ip
from mindfulguard.settings import Settings

class SignUp(AuthenticationBase):
    def __init__(self, request: Request) -> None:
        super().__init__(request)
        self.__settings = Settings()
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

                settings_dict: dict[str, Any] = await self.__settings.get()
                registration_allowed: bool = settings_dict['registration']

                await self._connection.open()
                db = self._pgsql_auth.sign_up(self._model_user, self._model_code)
                await db.execute(registration_allowed=registration_allowed)
                self._status_code = db.status_code
            except ValueError:
                self._status_code = BAD_REQUEST
            except KeyError as e:
                 logger.error("Failed to retrieve value by key from settings. Error: {}", e)
                 self._status_code = INTERNAL_SERVER_ERROR
            finally:
                await self._connection.close()