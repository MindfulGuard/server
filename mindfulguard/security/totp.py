import random
import pyotp

from mindfulguard.validation import Validation

class Totp:
    def __init__(self, secret_code: str) -> None:
        self.__secret_code = secret_code

    def generate_secret_code(self) -> str:
        return pyotp.random_base32()
    
    def generate_backup_codes(self, number_of_backup_codes: int = 6) -> list[int]:
        arr:list[int] = []
        for _ in range(1, number_of_backup_codes):
            arr.append(random.randint(100000, 999999))
        return arr
    
    def get(self) -> str:
        totp = pyotp.TOTP(self.__secret_code)
        return totp.now()
    
    def verify(self, code: str) -> bool:
        totp = pyotp.TOTP(self.__secret_code)
        return totp.verify(code)