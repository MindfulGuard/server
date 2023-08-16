from mypass.database.postgresql.connection import *

class Authentication:
    def __init__(self):pass
    async def sign_up(self,email:str,secret_string:bytes,login:bytes,reg_ip:str,avatar:str):
        connection = await Connection().connect()
        try:
            await connection.fetch('CALL sign_up($1,$2,$3,$4,$5,$6)',email,secret_string,login,reg_ip,avatar,False)
            return True
        except:
            return False
        finally:
            await connection.close()
    async def sign_in(self,email:str,secret_string:bytes,token:str,device:str,ip:str):
        connection = await Connection().connect()
        try:
            value = await connection.fetch('SELECT sign_in($1,$2,$3,$4,$5)',email,secret_string,token,device,ip)
            if value[0]['sign_in']:
                return True
            else:
                return False
        except:
            return False
        finally:
            await connection.close()