import asyncpg
from loguru import logger
from mindfulguard.classes.database.postgresql.connection_base import PostgreSqlConnectionBase

class PostgreSqlConnection(PostgreSqlConnectionBase):
    def __init__(self):
        super().__init__()

    async def open(self) -> None:
        try:
            self.connection = await asyncpg.connect(
                database=self._database,
                user=self._user,
                password=self._password,
                host=self._host,
                port=self._port
            )
            logger.debug("Connection to PostgreSQL database opened. Database: {}, User: {}, Host: {}, Port: {}", self._database, self._user, self._host, self._port)
        except asyncpg.exceptions.ConnectionDoesNotExistError as e:
            logger.critical("Error when connecting to PostgreSQL database. Error: {}", e)

    async def close(self) -> None:
        if self.connection:
            await self.connection.close()
            logger.debug("Connection to PostgreSQL database closed.")
