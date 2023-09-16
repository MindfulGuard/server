import asyncpg
from mypass.database.postgresql.authentication import Authentication
from mypass.database.postgresql.connection import Connection
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
    
    async def get(self, token: str):
        connection = None
        try:
            connection = await Connection().connect()
            is_auth = await Authentication().is_auth(connection,token)

            if not is_auth:
                return (None, UNAUTHORIZED)

            records = await connection.fetch('''
                SELECT s_id, s_name, s_description, s_created_at, s_updated_at
                FROM s_safes
                JOIN t_tokens
                ON t_tokens.t_u_id = s_safes.s_u_id
                WHERE t_tokens.t_token = $1
                AND active_token($1) = True
            ''', token)

            value_list = []
            for record in records:
                value_dict = {
                    'id': record['s_id'],
                    'name': record['s_name'],
                    'description': record['s_description'],
                    'created_at': record['s_created_at'],
                    'updated_at': record['s_updated_at'],
                }
                value_list.append(value_dict)

            if not value_list:
                return (None, NOT_FOUND)

            return (value_list, OK)
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            return (None, INTERNAL_SERVER_ERROR)
        finally:
            if connection:
                await connection.close()
    
    async def update(self,token,id,name,description):
        connection = None
        try:
            connection = await Connection().connect()
            value:int = await connection.fetchval('SELECT update_safe($1,$2,$3,$4)',token,id,name,description)
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

    async def delete(self,token,id):
        connection = None
        try:
            connection = await Connection().connect()
            value:int = await connection.fetchval('SELECT delete_safe($1,$2)',token,id)
            if value == 0:
                return OK
            elif value == -1:
                return UNAUTHORIZED
            elif value == -2:
                return NOT_FOUND
            else:
                return INTERNAL_SERVER_ERROR
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            return INTERNAL_SERVER_ERROR
        finally:
            if connection:
                await connection.close()