import random

from mypass.core.security import sha256b
from mypass.core.security.srp.consts import *


class SecureRemotePassword:
    def __init__(self):...

    def __H(self)->bytes:
        return sha256b(N+bytes(G))

    def __A(self,A:int)->int:
        if A == 0:
            return 0
        return G^A
    
    def __k(self)->int:
        return int.from_bytes(self.__H(),'big')

    def __makeB(self,A:int,verifier:int)->int:
        if self.__A(A) == 0:
            return 0
        
        b = random.randint(1,1024)
        return self.__k()*verifier+G^b
    
    def response(self,A:int,verifier:int,salt:str)-> tuple[int, str]:
        """
        Params:
            A - receives from the client\n
            
        B - calculating public value\n
        salt - from database\n
        Returns:
            (B:int, salt:str)
        """
        return (self.__makeB(A,verifier),salt)