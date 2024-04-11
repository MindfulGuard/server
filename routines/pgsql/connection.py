import asyncio
import logging
import os
import asyncpg

class Config:
    def get_host(self) -> str:
        return os.environ.get('POSTGRES_HOST', '')

    def get_port(self) -> str:
        return os.environ.get('POSTGRES_PORT', '')

    def get_database(self) -> str:
        return os.environ.get('POSTGRES_DB', '')

    def get_user(self) -> str:
        return os.environ.get('POSTGRES_USER', '')

    def get_password(self) -> str:
        return os.environ.get('POSTGRES_PASSWORD', '')

class Connection:
    def __init__(self):
        self.__db_config = Config()

    async def connect(self):
        try:
            return await asyncpg.connect(
                database = self.__db_config.get_database(),
                user = self.__db_config.get_user(),
                password = self.__db_config.get_password(),
                host = self.__db_config.get_host(),
                port = self.__db_config.get_port()
            )
        except (ConnectionRefusedError, asyncpg.CannotConnectNowError) as e:
            logging.error(e)
            await asyncio.sleep(5)
            return await self.connect()
        except asyncpg.InvalidAuthorizationSpecificationError as e:
            logging.error(e)
            await asyncio.sleep(5)
            return await self.connect()