import asyncio
from http.client import OK
import time
from routines.pgsql.sql import Sql

class Tokens:
    def __init__(self,update_settings_time: int):
        self.__sql = Sql()
        self.__update_settings_time = update_settings_time
    
    async def execute(self):
        await asyncio.sleep(self.__update_settings_time)
        tr = await self.__get_scan_time_routines()
        if tr == -1:
            return
        print("1. Tokens")
        await self.__sql.delete_tokens()
        await asyncio.sleep(tr)

    async def __get_scan_time_routines(self) -> int:
        get = await self.__sql.get_settings()
        if get[1] != OK:
            return -1
        
        return int(get[0]['scan_time_routines_tokens'])