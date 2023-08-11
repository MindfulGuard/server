import asyncpg

from mypass.configuration.config import Configuration


class Connection:
    async def connect(self):
        config = Configuration()
        return await asyncpg.connect(database=config.server_configuration('pgsql', 'database'),
                                     user=config.server_configuration('pgsql', 'user'),
                                     password=config.server_configuration('pgsql', 'password'),
                                     host=config.server_configuration('pgsql', 'host'),
                                     port=config.server_configuration('pgsql', 'port'))