import random
import pyotp

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