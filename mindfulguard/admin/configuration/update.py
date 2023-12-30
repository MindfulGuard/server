from http.client import BAD_REQUEST
from mindfulguard.classes.admin.base import AdminBase
from mindfulguard.classes.models.settings import ModelSettings


class AdminConfigurationUpdate(AdminBase):
    def __init__(self) -> None:
        super().__init__()
        self.__model_settings = ModelSettings()

    async def execute(self, token: str, key: str, value: str) -> None:
        try:
            self._model_token.token = token
            self.__model_settings.key = key
            self.__model_settings.value = value

            db = self._pgsql_admin.update_configuration(
                self._model_token,
                self.__model_settings
            )
            await self._connection.open()
            await db.execute()
            self._status_code = db.status_code
            return
        except ValueError:
            self._status_code = BAD_REQUEST
        finally:
            await self._connection.close()