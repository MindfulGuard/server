from mypass.database.postgresql.connection import *
from mypass.core.response_status_codes import *

class Authentication:
    def __init__(self):pass
    async def sign_up(self,login:str,secret_string:str,reg_ip:str,secret_code:str,reserves:list[int]):
        connection = None
        try:
            connection = await Connection().connect()
            value:int = await connection.fetchval('SELECT sign_up($1, $2, $3, $4, $5,$6)',login, secret_string, reg_ip, False, secret_code,reserves)#needs to be changed to False
            if value == 0 or value == 1 or value == 2:
                return OK
            elif value == -1:
                return CONFLICT
            elif value == -2 or value == -3 or value == -4:
                return NOT_FOUND
            else:
                return INTERNAL_SERVER_ERROR
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            return INTERNAL_SERVER_ERROR
        except asyncpg.exceptions.UniqueViolationError as e:
            print(e)
            return CONFLICT
        finally:
            if connection:
                await connection.close()
    
    async def get_secret_code(self,login:str,secret_string:str):
        connection = None
        try:
            connection = await Connection().connect()
            value = await connection.fetch('''
            SELECT c_secret_code, c_reserves
            FROM c_codes 
            JOIN u_users ON u_users.u_id = c_codes.c_u_id 
            WHERE u_users.u_login = $1
            AND u_users.u_secret_string = $2
            ''',login, secret_string)

            value_list = []
            print("VALUE:",value)
            if len(value) == 0:
                return (value_list,NOT_FOUND)
            for record in value:
                value_dict = {
                    'secret_code': record['c_secret_code'],
                    'reserves':record['c_reserves']
                }
                value_list.append(value_dict)
            return (value_list,OK)
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            return ([],INTERNAL_SERVER_ERROR)
        finally:
            if connection:
                await connection.close()

    async def update_reserve_codes(self, login: str, secret_string: str, reserve_codes: list[int]):
        connection = None
        try:
            connection = await Connection().connect()
            result = await connection.fetch(
                '''
                UPDATE c_codes SET c_reserves = $3
                WHERE c_u_id =(
                    SELECT u_id FROM u_users
                    WHERE u_login = $1 AND u_users.u_secret_string = $2
                    )
                RETURNING c_id;
                ''', login, secret_string, reserve_codes)

            if result:
                return OK
            else:
                return NOT_FOUND
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            return INTERNAL_SERVER_ERROR
        finally:
            if connection:
                await connection.close()
    
    async def sign_in(self,login:str,secret_string:str,token:str,device:str,ip:str,expiration:int,is_verified_code:bool):
        connection = None
        try:
            connection = await Connection().connect()
            value = await connection.fetch('SELECT sign_in($1,$2,$3,$4,$5,$6,$7)',login,secret_string,token,device,ip,expiration,is_verified_code)
            if value[0]['sign_in']:
                return OK
            else:
                return NOT_FOUND
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            return INTERNAL_SERVER_ERROR
        finally:
            if connection:
                await connection.close()

    async def sign_out(self,token:str,token_id:str):
        connection = None
        try:
            connection = await Connection().connect()
            value = await connection.fetch('SELECT sign_out($1,$2);',token,token_id)
            
            if value[0]['sign_out']:
                return OK
            else:
                return NOT_FOUND
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            return INTERNAL_SERVER_ERROR
        finally:
            if connection:
                await connection.close()
     
    async def update_token_info(self,token,device,ip):
        connection = None
        try:
            connection = await Connection().connect()
            value = await connection.fetch('SELECT update_token_info($1,$2,$3);',token,device,ip)
            if value[0]['update_token_info']:
                return OK
            else:
                return NOT_FOUND
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            return INTERNAL_SERVER_ERROR
        finally:
            if connection:
                await connection.close()

    async def get_tokens(self, token:str):
        connection = None
        try:
            connection = await Connection().connect()
            records = await connection.fetch('''
                SELECT t_id, t_first_login, t_last_login, t_device, t_last_ip, t_expiration
                FROM t_tokens
                WHERE t_u_id IN (
                    SELECT t_u_id
                    FROM t_tokens
                    WHERE t_token = $1
                );
                ''', token)
            
            value_list = []
            if records == None:
                return (value_list,NOT_FOUND)
            for record in records:
                value_dict = {
                    'id': record['t_id'],
                    'first_login': record['t_first_login'],
                    'last_login': record['t_last_login'],
                    'device': record['t_device'],
                    'last_ip': record['t_last_ip'],
                    'expiration': record['t_expiration']
                }
                value_list.append(value_dict)

            print(value_list)

            return (value_list,OK)
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            return ([],INTERNAL_SERVER_ERROR)
        finally:
            if connection:
                await connection.close()

    async def new_secret_string(self,token:str,old_secret_string:str,new_secret_string:str):...