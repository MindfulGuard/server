from http.client import FORBIDDEN, INTERNAL_SERVER_ERROR, OK, UNAUTHORIZED
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.settings import ModelSettings
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.connection import PostgreSqlConnection


class PostgreSqlAdminConfigurationUpdate(PostgreSqlQueriesBase):
    def __init__(
        self,
        connection: PostgreSqlConnection,
        model_token: ModelToken,
        model_settings: ModelSettings
    ) -> None:
        super().__init__(connection)
        self.__model_token: ModelToken = model_token
        self.__model_settings: ModelSettings = model_settings

    async def execute(self) -> None:
        response: int = await self._connection.connection.fetchval('''
        SELECT update_settings_admin($1,$2,$3);
        ''',
        self.__model_token.token,
        self.__model_settings.key,
        self.__model_settings.value
        )
        if response == 0:
            self._status_code = OK
            return
        elif response == -1:
            self._status_code = UNAUTHORIZED
            return
        elif response == -2:
            self._status_code = FORBIDDEN
            return
        else:
            self._status_code = INTERNAL_SERVER_ERROR
            return