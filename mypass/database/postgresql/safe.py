from mypass.database.postgresql.connection import *
from mypass.core.response_status_codes import *

class Safe:
    async def create(self,token:str,name:str,description:str):
        connection = None
        try:
            connection = await Connection().connect()
            value:int = await connection.fetchval('SELECT create_safe($1, $2, $3)',token,name,description)
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