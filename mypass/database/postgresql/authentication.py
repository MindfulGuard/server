from mypass.database.postgresql.connection import *
from mypass.core.response_status_codes import *
class Authentication:
    def __init__(self):pass
    async def sign_up(self,email:str,secret_string:str,login:str,reg_ip:str,avatar:str):
        connection = None
        try:
            connection = await Connection().connect()
            await connection.fetch('CALL sign_up($1, $2, $3, $4, $5, $6)', email, secret_string, login, reg_ip, avatar, True)
            return OK
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            return INTERNAL_SERVER_ERROR
        except asyncpg.exceptions.UniqueViolationError as e:
            print(e)
            return CONFLICT
        finally:
            if connection:
                await connection.close()

    async def sign_in(self,email:str,secret_string:str,token:str,device:str,ip:str,expiration:int):
        connection = None
        try:
            connection = await Connection().connect()
            value = await connection.fetch('SELECT sign_in($1,$2,$3,$4,$5,$6)',email,secret_string,token,device,ip,expiration)
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

    async def new_secret_string(self,token:str,old_secret_string:str,new_secret_string:str):
        connection = None
        try:
            connection = await Connection().connect()
            value = await connection.fetch('SELECT update_token_info($1,$2,$3);',old_secret_string,new_secret_string,token)
            if value[0]['update_token_info']:
                return OK
            else:
                return NOT_FOUND
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            return INTERNAL_SERVER_ERROR
        finally:
            if connection:
                await connection.close()