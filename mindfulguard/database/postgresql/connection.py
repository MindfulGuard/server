import asyncpg
from mindfulguard.classes.database.postgresql.connection_base import PostgreSqlConnectionBase

class PostgreSqlConnection(PostgreSqlConnectionBase):
    def __init__(self):
        super().__init__()

    async def open(self) -> None:
        try:
            self.connection = await asyncpg.connect(
                database=self._DATABASE,
                user=self._user,
                password=self._password,
                host=self._host,
                port=self._port
            )
        except asyncpg.exceptions.ConnectionDoesNotExistError as e:
            print(e)

    async def close(self) -> None:
        if self.connection:
            await self.connection.close()