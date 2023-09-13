import random
import pyotp


class Totp:
    def generate_secret_code(self)->str:
        return pyotp.random_base32()
    
    def generate_reserve_codes(self,length:int)->list[int]:
        arr:list[int] = []
        for _ in range(1,length):
            arr.append(random.randint(100000,999999))
        return arr
    
    def get(self,secret_code:str)->int:
        totp = pyotp.TOTP(secret_code)
        return int(totp.now())