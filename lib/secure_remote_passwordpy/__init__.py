import random

class Srp:
    def __init__(self, g: int, N: int,sha):
        self.__g = g
        self.__N = N
        self.__sha = sha

    def H(self,*a)->int:
        return int(self.__sha(bytes(str(a),'utf-8')).hexdigest(), 16) % self.__N
    
    def cryptrand(self,n:int=1024)->int:  
        return random.SystemRandom().getrandbits(n) % self.__N
    
    def client(self,a: int, salt: str, login:str, password: str) -> tuple[str, int, int]:
        x = self.H(salt,password)
        v = pow(self.__g,x,self.__N)
        A = self.A(a)
        return (login,A,v)

    def server(self, b: int, v: int, salt: str) -> tuple[int, str]:
        B = (self.__k()*v+pow(self.__g,b,self.__N))
        return (B, salt)
    
    def calculate_random(self,A:int,B:int) -> int:
        u = self.H(A,B)
        return u

    def session_key_client(self,a:int,salt:str,password:str,B:int,u:int) -> tuple[int, int]:
        x = self.H(salt,password)
        S = pow(B - self.__k()*pow(self.__g,x,self.__N),a+u*x,self.__N)
        K = self.H(S)
        return (S,K)
    
    def session_key_server(self,v:int,A:int,b:int,u:int) -> tuple[int, int]:
        S = pow(A * pow(v, u, self.__N), b, self.__N)
        K = self.H(S)
        return (S,K)
    
    def client_send_proof(self,login:str,salt:str,A:int,B:int,Ks:int) -> int:
        M = self.H(self.H(self.__N) ^ self.H(self.__g), self.H(login), salt, A, B, Ks)
        return M
    
    def server_send_proof(self,A:int,Mc:int,Kc:int) -> int:
        M = self.H(A, Mc, Kc)
        return M
    
    def new_user(self, login: str, password: str, salt: str) -> tuple[str, int, str]:
        x = self.H(salt,password)
        v = pow(self.__g, x, self.__N)
        return (login, v, salt)

    def A(self, a: int) -> int:
        return pow(self.__g, a, self.__N)

    def __k(self) -> int:
        return self.H(self.__N,self.__g)

    def cmp(self, client: int, server: int) -> bool:
        return client == server