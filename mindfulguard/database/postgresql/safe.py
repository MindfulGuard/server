import asyncpg
from mindfulguard.database.postgresql.authentication import Authentication
from mindfulguard.database.postgresql.connection import Connection
from mindfulguard.core.response_status_codes import *

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
                return ([], UNAUTHORIZED)
            records = await connection.fetch('''
            SELECT s.s_id, s.s_name, s.s_description, s.s_created_at, s.s_updated_at, COUNT(r.r_id) AS r_count
            FROM s_safes AS s
            JOIN t_tokens AS t ON t.t_u_id = s.s_u_id
            LEFT JOIN r_records AS r ON r.r_s_id = s.s_id
            WHERE t.t_token = $1
            AND active_token($1) = True
            GROUP BY s.s_id, s.s_name, s.s_description, s.s_created_at, s.s_updated_at;
            ''', token)

            value_list = []
            for record in records:
                value_dict = {
                    'id': record['s_id'],
                    'name': record['s_name'],
                    'description': record['s_description'],
                    'created_at': record['s_created_at'],
                    'updated_at': record['s_updated_at'],
                    'count_items':record['r_count']
                }
                value_list.append(value_dict)

            if not value_list:
                return ([], OK)

            return (value_list, OK)
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            return ([], INTERNAL_SERVER_ERROR)
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