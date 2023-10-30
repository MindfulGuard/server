from mindfulguard.core.response_status_codes import *
from mindfulguard.database.postgresql.settings import Settings

import ast

class Get:
    def execute(self):
        return ReadConfigs()

class ReadConfigs():
    def __init__(self):
        self.__settings = Settings()
    
    async def authentication(self):
        password_rule = await self.__settings.get()
        return (
            password_rule[0]['password_rule'],
            password_rule[1]
        )
    
    async def item(self):
        item = await self.__settings.get()
        return (
            ast.literal_eval(item[0]['item_categories']),
            ast.literal_eval(item[0]['item_types']),
        item[1]
        )
    
    async def registration_status(self):
        item = await self.__settings.get()
        return (
            bool(item[0]['registration']),
            item[1]
        )

    async def scan_time_routines_tokens(self):
        item = await self.__settings.get()
        return (
            int(item[0]['scan_time_routines_tokens']),
            item[1]
        )
    
    async def scan_time_routines_users(self):
        item = await self.__settings.get()
        return (
            int(item[0]['scan_time_routines_users']),
            item[1]
        )
    
    async def confirmation_period(self):
        item = await self.__settings.get()
        return (
            int(item[0]['confirmation_period']),
            item[1]
        )
    
    async def disk_space_per_user(self):
        item = await self.__settings.get()
        return (
            int(item[0]['disk_space_per_user']),
            item[1]
        )