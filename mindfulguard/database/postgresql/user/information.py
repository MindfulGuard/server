import asyncpg
from mindfulguard.database.postgresql.authentication import Authentication

from mindfulguard.database.postgresql.connection import Connection
from mindfulguard.core.response_status_codes import *

class Information:
    async def get(self,token:str):
        connection = None
        try:
            connection = await Connection().connect()
            is_auth:bool = await Authentication().is_auth(connection,token)
            value_dict:dict = {}
            if is_auth == False:
                return (value_dict,UNAUTHORIZED)
            
            values = await connection.fetch("""
            SELECT u_login, u_reg_ip, u_created_at FROM u_users
            WHERE u_id = (
                SELECT t_u_id FROM t_tokens
                WHERE t_token = $1
                );
            """,token)
            for val in values:
                value_dict = {
                    'username': val['u_login'],
                    'created_at': val['u_created_at'],
                    'ip': val['u_reg_ip'],
                }
            return (value_dict,OK)
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            return (None,INTERNAL_SERVER_ERROR)
        finally:
            if connection:
                await connection.close()