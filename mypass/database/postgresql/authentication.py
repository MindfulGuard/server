from mypass.database.postgresql.connection import *

class Authentication:
    def __init__(self):pass
    async def sign_up(self,email:str,secret_string:bytes,login:bytes,reg_ip:str,avatar:str):
        connection = await Connection().connect()
        try:
            await connection.execute('CALL sign_up($1,$2,$3,$4,$5,$6)',email,secret_string,login,reg_ip,avatar,False)
            return True
        except:
            return False
        finally:
            await connection.close()