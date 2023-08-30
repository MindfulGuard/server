import random
from mypass.core.security import *
from tests.security.srp.consts import *


class SecureRemotePassword:
    def __init__(self):
        self.a = random.randint(0, 1024)
    def __k(self)->int:
        return int.from_bytes(sha256b(N+bytes(G)),'big')

    def __H(self,uuid:str,email:str,password:str)->bytes:
        return sha256b(bytes(uuid,'utf-8')+sha256b(bytes(email,'utf-8')+b':'+bytes(password,'utf-8'),))
    
    def __verifier(self,uuid:str,email:str,password:str)->int:
        return G ^ int.from_bytes(self.__H(uuid,email,password),'big')
    
    def registration(self,uuid:str,email:str,password:str)-> tuple[str, int, str]:
        """
        this data is sent to the database\n
        RETURNS:
            (email:str, __verifier:int, salt:str)
        """
        return (email,self.__verifier(uuid,email,password),uuid)
    
    def A(self)->int:
        return G^self.a
    
    def x(self,password:str,salt)->int:
        return int.from_bytes(sha256b(sha256b(bytes(salt,'utf-8')+b':'+bytes(password,'utf-8'))),'big')
    
    def u(self,A:int,B:int)->int:
        return int.from_bytes(sha256b(bytes(A)+sha256b(bytes(B))),'big')
    
    def S(self,B:int,password,salt):
        return (B - self.__k()*G^self.x(password,salt))^self.a
    