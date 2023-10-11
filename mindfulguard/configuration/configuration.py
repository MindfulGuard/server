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
        return ({
            "password_rule": password_rule[0]['password_rule']
            },
            password_rule[1])
    
    async def item(self):
        item = await self.__settings.get()
        return ({
            "categories":ast.literal_eval(item[0]['item_categories']),
            "types":ast.literal_eval(item[0]['item_types'])
        },
        item[1])