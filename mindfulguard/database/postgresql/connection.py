import os
import asyncpg

from mindfulguard.core.configuration import *

class Config:
    def get_host(self)->str:
        return "postgresql"
    def get_port(self)->str:
        return os.environ.get('DATABASE_PORT', '5432')
    def get_database(self)->str:
        return "mindfulguard_production"
    def get_user(self)->str:
        return os.environ.get('DATABASE_USER', '')
    def get_password(self)->str:
        return os.environ.get('DATABASE_PASSWORD', '')

class Connection:
    def __init__(self):
        self.__db_config = Config()
    async def connect(self):
        return await asyncpg.connect(database=self.__db_config.get_database(),
                                     user=self.__db_config.get_user(),
                                     password=self.__db_config.get_password(),
                                     host=self.__db_config.get_host(),
                                     port=self.__db_config.get_port())
    async def create_pool(self):
        return await asyncpg.create_pool(database=self.__db_config.get_database(),
                                        user=self.__db_config.get_user(),
                                        password=self.__db_config.get_password(),
                                        host=self.__db_config.get_host(),
                                        port=self.__db_config.get_port())