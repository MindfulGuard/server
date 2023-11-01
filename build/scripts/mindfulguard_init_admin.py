import argparse
import asyncio
import hashlib
import os
import re
import sys
import uuid
import asyncpg
import random
import pyotp

parser = argparse.ArgumentParser()
parser.add_argument('admin_login', type=str, help="Login")
parser.add_argument('admin_password', type=str, help="Password")
arguments = sys.argv
args = parser.parse_args()

class Config:
    def get_host(self)->str:
        return os.environ.get('DATABASE_HOST', 'localhost')
    def get_port(self)->str:
        return os.environ.get('DATABASE_PORT', '5432')
    def get_database(self)->str:
        return "mindfulguard_production"
    def get_user(self)->str:
        return os.environ.get('DATABASE_USER', '')
    def get_password(self)->str:
        return os.environ.get('DATABASE_PASSWORD', '')

class Connection:
    def __init__(self):
        self.__db_config = Config()
    async def connect(self):
        return await asyncpg.connect(database=self.__db_config.get_database(),
                                     user=self.__db_config.get_user(),
                                     password=self.__db_config.get_password(),
                                     host=self.__db_config.get_host(),
                                     port=self.__db_config.get_port())
    
class Db:
    async def sign_up(
            self,
            login:str,
            secret_string:str,
            secret_code:str,
            backup_codes:list[int]
        ):
        connection = None
        try:
            connection = await Connection().connect()
            value:int = await connection.fetchval('SELECT sign_up($1, $2, $3, $4, $5,$6)',login, secret_string, "127.0.0.1", True, secret_code,backup_codes)
            if value == 0 or value == 1 or value == 2:
                return 0
            return value
        except asyncpg.exceptions.DataError:
            return -6
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            return -6
        except asyncpg.exceptions.UniqueViolationError as e:
            print(e)
            return -1
        finally:
            if connection:
                await connection.close()
    
    async def set_admin_status(self,login:str,secret_string:str):
        connection = None
        try:
            connection = await Connection().connect()
            await connection.fetchval('''
            UPDATE u_users SET u_admin = TRUE WHERE u_login = $1 AND u_secret_string = $2;
            ''',login,secret_string)
        except Exception as e:
            print(e)
        finally:
            if connection:
                await connection.close()

    async def admin_exist(self)->bool:
        connection = None
        try:
            connection = await Connection().connect()
            value = await connection.fetchval('''
            SELECT u_id
            FROM u_users
            WHERE u_admin = TRUE;
            ''')
            print(value)
            return value == None
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            return False
        finally:
            if connection:
                await connection.close()

    async def get_settings(self)->dict:
        connection = None
        try:
            connection = await Connection().connect()
            values = await connection.fetch('''
            SELECT st_id, st_key, st_value
            FROM st_settings
            ''')

            settings_dict = {}
            for row in values:
                key, value = row['st_key'], row['st_value']
                settings_dict[key] = value
            return settings_dict
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            return {}
        finally:
            if connection:
                await connection.close()

NUMBER_OF_BACKUP_CODES = 6
class Totp:
    def __init__(self,secret_code:str):
        self.__secret_code = secret_code
    def generate_secret_code(self)->str:
        return pyotp.random_base32()
    
    def generate_backup_codes(self,length:int)->list[int]:
        arr:list[int] = []
        for _ in range(1,length):
            arr.append(random.randint(100000,999999))
        return arr
    
    def get(self)->str:
        totp = pyotp.TOTP(self.__secret_code)
        return totp.now()
    
    def verify(self,code:str)->bool:
        totp = pyotp.TOTP(self.__secret_code)
        return totp.verify(code)

class Run:
    def __init__(self):
        self.__db = Db()
    
    async def execute(self,login:str,password:str):
        if await self.__validate_data(login,password) == False:
            return ("","",[])
        elif await self.__db.admin_exist() == False:
            return ("","",[])
        totp = Totp("")
        secret_code:str = totp.generate_secret_code()
        backup_codes:list[int] = totp.generate_backup_codes(NUMBER_OF_BACKUP_CODES)

        salt:str = str(uuid.uuid4())
        get_secret_string = self.__get_secret_string(
            login,
            password,
            salt
        )

        result:int = await self.__db.sign_up(
            login=login,
            secret_string=get_secret_string,
            secret_code=secret_code,
            backup_codes=backup_codes
        )
        if result != 0:
            return ("","",[])
        
        await self.__db.set_admin_status(
            login=login,
            secret_string=get_secret_string
        )

        return (salt,secret_code,backup_codes)

    def __get_secret_string(self,login:str,password:str,salt:str)->str:
        secret_string = hashlib.sha256()
        secret_string.update(login.encode('utf-8'))
        secret_string.update(password.encode('utf-8'))
        secret_string.update(salt.encode('utf-8'))
        return secret_string.hexdigest()

    async def __validate_data(self,login:str,secret_string:str)->bool:
        def validate_login(login:str)->bool:
            """
            Can only be present: hyphen, underscore, Latin characters only
            """
            return bool(re.compile(r'^[A-Za-z0-9_-]{2,50}$').match(login))

        def validate_password(reg:str,password:str)->bool:
            return bool(re.compile(reg).match(password))

        get_settings = await self.__db.get_settings()
        password_rule:str = get_settings['password_rule']
        
        return (
            validate_login(login) == True
            and validate_password(password_rule,secret_string) == True
        )

async def main(login:str,password:str):
    exec = await Run().execute(
        login,
        password
    )
    if exec[0] == "":
        return

    print("Login:",login,"\nPassword:",password,"\nSalt:",exec[0],"\nSecret code:",exec[1],"\nBackup codes:",exec[2])

if __name__ == '__main__':
    if len(arguments) < 1:
        print("Error no args")

    login_arg = args.admin_login
    password_arg = args.admin_password

    asyncio.run(main(login_arg,password_arg))
