from http.client import BAD_REQUEST, OK
from typing import Any
from mindfulguard.classes.admin.base import AdminBase
from mindfulguard.configuration.public import ConfigurationPublic
from mindfulguard.database.postgresql.authentication import PostgreSqlAuthentication

class AdminConfigurationGet(AdminBase):
    def __init__(self) -> None:
        super().__init__()
        self.__public_configuration = ConfigurationPublic()
        self.__pgsql_auth_admin = PostgreSqlAuthentication(self._connection)

    @property
    def response(self) -> dict[str, Any]:
        return self._response

    async def execute(self, token: str) -> None:
        try:
            self._model_token.token = token

            db = self.__pgsql_auth_admin.is_auth_admin(
                self._model_token
            )
            await self._connection.open()
            await db.execute()
            self._status_code = db.status_code
            if db.status_code != OK:
                return
            
            await self.__public_configuration.execute()
            response: dict[str, Any] = self.__public_configuration.response
            response['registration_status'] = self.__public_configuration.settings['registration']
            response['scan_time_routines_tokens'] = self.__public_configuration.settings['scan_time_routines_tokens']
            response['scan_time_routines_users'] = self.__public_configuration.settings['scan_time_routines_users']
            response['confirmation_period'] = self.__public_configuration.settings['confirmation_period']
            response['disk_space_per_user'] = self.__public_configuration.settings['disk_space_per_user']

            self._response = response
            self._status_code = OK
            return
        except ValueError:
            self._status_code = BAD_REQUEST
        finally:
            await self._connection.close()