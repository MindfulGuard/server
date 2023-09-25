from mypass.database.postgresql.connection import Connection
from mypass.core.response_status_codes import *
import asyncpg

class Item:
    async def create(
            self,
            token:str,
            safe_id:str,
            title:str,
            item,
            notes:str,
            tags:list[str],
            category:str
            ):
        connection = None
        try:
            connection = await Connection().connect()
            value:int = await connection.fetchval('SELECT create_item($1, $2, $3, $4, $5, $6, $7, $8)',
                                                  token,safe_id,title,item,notes,tags,category,False)
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
        except asyncpg.exceptions.ForeignKeyViolationError:
            return INTERNAL_SERVER_ERROR
        except asyncpg.exceptions.UniqueViolationError as e:
            print(e)
            return INTERNAL_SERVER_ERROR
        finally:
            if connection:
                await connection.close()
            
    async def update(
            self,
            token:str,
            safe_id:str,
            item_id:str,
            title:str,
            item,
            notes:str,
            tags:list[str],
            ):
        connection = None
        try:
            connection = await Connection().connect()
            value:int = await connection.fetchval('SELECT update_item($1, $2, $3, $4, $5, $6, $7)',
                                                  token,safe_id,item_id,title,item,notes,tags)
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
        except asyncpg.exceptions.ForeignKeyViolationError:
            return INTERNAL_SERVER_ERROR
        except asyncpg.exceptions.UniqueViolationError as e:
            print(e)
            return INTERNAL_SERVER_ERROR
        finally:
            if connection:
                await connection.close()

    async def delete(
            self,
            token:str,
            safe_id:str,
            item_id:str
            ):
        connection = None
        try:
            connection = await Connection().connect()
            value:int = await connection.fetchval('SELECT delete_item($1, $2, $3)',
                                                  token,safe_id,item_id)
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
        except asyncpg.exceptions.ForeignKeyViolationError:
            return INTERNAL_SERVER_ERROR
        except asyncpg.exceptions.UniqueViolationError as e:
            print(e)
            return INTERNAL_SERVER_ERROR
        finally:
            if connection:
                await connection.close()