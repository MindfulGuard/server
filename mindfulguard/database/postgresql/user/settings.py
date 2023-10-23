import asyncpg

from mindfulguard.core.response_status_codes import *
from mindfulguard.database.postgresql.connection import Connection


class Settings:
    async def update_one_time_codes(self,token:str,secret_string:str,data:str|list[int]):
        connection = None
        try:
            query = "SELECT update_c_codes_code($1,$2,$3);"
            if type(data) == list:
                query = "SELECT update_c_codes_code($1,$2,$3::INTEGER[]);"
            connection = await Connection().connect()
            value:int = await connection.fetchval(query,token,secret_string,data)
            if value == 0:
                return OK
            elif value == -1:
                return UNAUTHORIZED
            elif value == -2:
                return INTERNAL_SERVER_ERROR
            else:
                return INTERNAL_SERVER_ERROR
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            return INTERNAL_SERVER_ERROR
        except asyncpg.exceptions.UniqueViolationError as e:
            print(e)
            return INTERNAL_SERVER_ERROR
        finally:
            if connection:
                await connection.close()

    async def update_secret_string(
            self,
            token:str,
            old_secret_string:str,
            new_secret_string:str
        ):
        connection = None
        try:
            connection = await Connection().connect()
            value:int = await connection.fetchval("SELECT update_secret_string($1,$2,$3);",
                                                  token,old_secret_string,new_secret_string)
            if value == 0:
                return OK
            elif value == -1:
                return UNAUTHORIZED
            elif value == -2:
                return INTERNAL_SERVER_ERROR
            else:
                return INTERNAL_SERVER_ERROR
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            return INTERNAL_SERVER_ERROR
        except asyncpg.exceptions.UniqueViolationError as e:
            return INTERNAL_SERVER_ERROR
        finally:
            if connection:
                await connection.close()

    async def delete_user(
            self,
            token:str,
            secret_string:str,
            code_confirm:bool
        ):
        connection = None
        try:
            connection = await Connection().connect()
            value:int = await connection.fetchval("SELECT delete_user($1,$2,$3);",token,secret_string,code_confirm)
            if value == 0:
                return OK
            elif value == -1:
                return UNAUTHORIZED
            elif value == -2:
                return INTERNAL_SERVER_ERROR
            else:
                return INTERNAL_SERVER_ERROR
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            return INTERNAL_SERVER_ERROR
        finally:
            if connection:
                await connection.close()