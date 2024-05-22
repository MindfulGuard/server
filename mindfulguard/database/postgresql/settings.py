from http.client import OK
from loguru import logger
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
import time

class PostgreSqlSettings(PostgreSqlQueriesBase):
    @property
    def response(self) -> dict[str, str]:
        return self._response

    async def execute(self):
        start_time = time.time()
        logger.debug("Executing SQL query...")
        
        values = await self._connection.connection.fetch('''
        SELECT st_id, st_key, st_value
        FROM st_settings
        ''')

        logger.debug("Fetch values: {}.", values)

        settings_dict = {}
        for row in values:
            key, value = row['st_key'], row['st_value']
            settings_dict[key] = value

        self._response = settings_dict
        self._status_code = OK
        logger.debug("Response: {}, status code: {}", self._response, self._status_code)
        logger.debug("SQL query executed successfully.")
        
        end_time = time.time()
        execution_time = end_time - start_time
        logger.trace("Query execution time: {} seconds", execution_time)

        return