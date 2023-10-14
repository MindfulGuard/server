import pyotp


class TotpClient:
    def __init__(self,secret_code:str):
        self.__secret_code = secret_code
    
    def get(self)->str:
        totp = pyotp.TOTP(self.__secret_code)
        return totp.now()