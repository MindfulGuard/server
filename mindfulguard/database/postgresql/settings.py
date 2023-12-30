from http.client import OK
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase

class PostgreSqlSettings(PostgreSqlQueriesBase):
    @property
    def response(self) -> dict[str, str]:
        return self._response

    async def execute(self):
        values = await self._connection.connection.fetch('''
        SELECT st_id, st_key, st_value
        FROM st_settings
        ''')

        settings_dict = {}
        for row in values:
            key, value = row['st_key'], row['st_value']
            settings_dict[key] = value

        self._response = settings_dict
        self._status_code = OK
        return