import asyncpg

from mindfulguard.core.response_status_codes import *
from mindfulguard.database.postgresql.authentication import Authentication
from mindfulguard.database.postgresql.connection import Connection
from mindfulguard.database.postgresql.settings import Settings


class Admin:
    async def get_all_users(self,token:str,limit:int,offset:int):
        connection = None
        try:
            connection = await Connection().connect()
            is_auth:int = await Authentication().is_auth_admin(connection,token)
            if is_auth != OK:
                return ([],is_auth)

            values = await connection.fetch('''
            SELECT u_id, u_login, u_reg_ip, u_confirm, u_created_at
            FROM u_users
            ORDER BY u_id
            LIMIT $1 OFFSET $2;
            ''',limit,offset)

            value_list = []
            for record in values:
                value_dict = {
                    'id': record['u_id'],
                    'login': record['u_login'],
                    'ip': record['u_reg_ip'],
                    'confirm': record['u_confirm'],
                    'created_at': record['u_created_at'],
                }
                value_list.append(value_dict)
            if not value_list:
                return ([], OK)
            return (value_list,OK)
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            return ([],INTERNAL_SERVER_ERROR)
        finally:
            if connection:
                await connection.close()

    async def search_users(self,token:str,key:str,value:str):
        connection = None
        try:
            connection = await Connection().connect()
            is_auth:int = await Authentication().is_auth_admin(connection,token)
            value_dict = {}
            if is_auth != OK:
                return (value_dict,is_auth)

            if key == "u_id":
                values = await connection.fetch("SELECT u_id, u_login, u_reg_ip, u_confirm, u_created_at FROM u_users WHERE u_id = $1;",value)
            elif key == "u_login":
                values = await connection.fetch("SELECT u_id, u_login, u_reg_ip, u_confirm, u_created_at FROM u_users WHERE u_login = $1;",value)
            else:
                values = await connection.fetch("SELECT u_id, u_login, u_reg_ip, u_confirm, u_created_at FROM u_users WHERE True = False;")

            for record in values:
                value_dict = {
                    'id': record['u_id'],
                    'login': record['u_login'],
                    'ip': record['u_reg_ip'],
                    'confirm': record['u_confirm'],
                    'created_at': record['u_created_at'],
                }
            if not values:
                return ({}, NOT_FOUND)
            return (value_dict,OK)
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            return ({},INTERNAL_SERVER_ERROR)
        finally:
            if connection:
                await connection.close()
    
    async def get_count_users(self)->int:
        connection = None
        try:
            connection = await Connection().connect()

            value:int = await connection.fetchval('''
            SELECT count(*) FROM u_users;
            ''')
            if value == None:
                return 0
            return value
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            return 0 
        finally:
            if connection:
                await connection.close()

    async def is_admin(self,token:str):
        connection = None
        try:
            connection = await Connection().connect()
            is_auth:int = await Authentication().is_auth_admin(connection,token)
            if is_auth != OK:
                return is_auth
            return OK
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            return INTERNAL_SERVER_ERROR
        finally:
            if connection:
                await connection.close()

    async def delete_user_admin(
            self,
            user_id:str
        ):
        connection = None
        try:
            connection = await Connection().connect()
            value:int = await connection.fetchval("SELECT delete_user($1);",user_id)
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
    
    async def update_settings(
            self,
            token:str,
            key:str,
            value:str
        ):
        connection = None
        try:
            connection = await Connection().connect()
            response:int = await connection.fetchval("SELECT update_settings_admin($1,$2,$3);",token,key,value)
            if response == 0:
                return OK
            elif response == -1:
                return UNAUTHORIZED
            elif response == -2:
                return FORBIDDEN
            else:
                return INTERNAL_SERVER_ERROR
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            return INTERNAL_SERVER_ERROR
        finally:
            if connection:
                await connection.close()