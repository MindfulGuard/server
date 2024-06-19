import argparse
import asyncio
import hashlib
import json
import logging
import re
import sys
import uuid
import asyncpg
import random
import pyotp

parser = argparse.ArgumentParser()
parser.add_argument('admin_login', type=str, help="Login")
parser.add_argument('admin_password', type=str, help="Password")
parser.add_argument('database_host', type=str, help="")
parser.add_argument('database_name', type=str, help="")
parser.add_argument('database_port', type=str, help="")
parser.add_argument('database_user', type=str, help="")
parser.add_argument('database_password', type=str, help="")

arguments = sys.argv
args = parser.parse_args()

class Config:
    def get_host(self)->str:
        return args.database_host
    def get_port(self)->str:
        return args.database_port
    def get_database(self)->str:
        return args.database_name
    def get_user(self)->str:
        return args.database_user
    def get_password(self)->str:
        return args.database_password

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
        except asyncpg.exceptions.DataError as e:
            logging.fatal(e)
            return -6
        except asyncpg.exceptions.ConnectionDoesNotExistError as e:
            logging.fatal(e)
            return -6
        except asyncpg.exceptions.UniqueViolationError as e:
            logging.fatal(e)
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
            logging.fatal(e)
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
            logging.debug(f"Admin exists: {value}")
            return value == None
        except asyncpg.exceptions.ConnectionDoesNotExistError as e:
            logging.fatal(e)
            return False
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
            logging.warning("Failed to create an administrator because incorrect data entered.")
            return ("","",[])
        elif await self.__db.admin_exist() == False:
            logging.warning("Failed to create an administrator, it already exists.")
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

        ss_hash = hashlib.sha256()
        ss_hash.update(get_secret_string.encode('utf-8'))

        result:int = await self.__db.sign_up(
            login=login,
            secret_string=ss_hash.hexdigest(),
            secret_code=secret_code,
            backup_codes=backup_codes
        )
        if result != 0:
            return ("","",[])
        
        await self.__db.set_admin_status(
            login=login,
            secret_string=ss_hash.hexdigest()
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
        
        return (
            validate_login(login) == True
            and True
        )

def write_to_file(
    file_name: str,
    login: str,
    password: str,
    private_key: str,
    secret_code: str,
    backup_codes:  list[str]
) -> None:
    data: dict[str, str] = {
        "login": login,
        "password": password,
        "private_key": private_key,
        "secret_code": secret_code,
        "backup_codes": backup_codes
    }
    with open(file_name, "w") as f:
        json.dump(data, f)

    return

async def main(login:str,password:str):
    FILE_NAME: str = "build/admin_data.json"

    exec = await Run().execute(
        login,
        password
    )
    if exec[0] == "":
        return

    write_to_file(FILE_NAME, login, password, exec[0], exec[1], exec[2])
    logging.info("Administrator successfully created.")

if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    if len(arguments) < 7:
        logging.info("Error no args.")

    login_arg = args.admin_login
    password_arg = args.admin_password

    asyncio.run(main(login_arg,password_arg))
