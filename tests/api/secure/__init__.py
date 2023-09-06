from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib


class Security:
    def __init__(self,iterations:int,SHA:str):
        self.__iterations = iterations
        self.__SHA = SHA
    def encrypt(self,text:str,password:str,private_key:bytes)->bytes:
        """
        Args:
            text (str): the text that needs to be encrypted\n
            password (str)\n
            private_key (bytes): uuid.uuid4().bytes
        """

        key = hashlib.pbkdf2_hmac(self.__SHA, password.encode('utf-8'), private_key, self.__iterations)
        
        # Generate a random IV
        iv = private_key
        
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(text.encode('utf-8'), AES.block_size))
        
        # Return the IV along with the ciphertext
        return iv + ciphertext
    
    def decrypt(self,text:bytes,password:str,private_key:bytes)->str:

        key = hashlib.pbkdf2_hmac(self.__SHA, password.encode('utf-8'), private_key, self.__iterations)
        
        iv = text[:AES.block_size]
        ciphertext = text[AES.block_size:]
        
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
        
        return decrypted.decode('utf-8')