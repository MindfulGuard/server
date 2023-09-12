import hashlib
from typing import Any
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import serialization
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad

class PbkdF2HMAC:
    def __init__(self,iterations:int,SHA:str):
        self.__iterations = iterations
        self.__SHA = SHA
    def encrypt(self, password: str, private_key: bytes) -> bytes:
        if self.__SHA == "sha256":
            algorithm = hashes.SHA256()
        else:
            raise ValueError("Unsupported SHA algorithm")

        kdf = PBKDF2HMAC(
            algorithm=algorithm,
            iterations=self.__iterations,
            salt=private_key,
            length=64,
        )

        key = kdf.derive(bytes(password, 'utf-8'))
        return key

class AES_256:
    def encrypt_aes_256(self,key, message):
        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(message.encode('utf-8'))
        return ciphertext

    def aes_256_decrypt(self,key:bytes, ciphertext):
        decipher = AES.new(key, AES.MODE_EAX)
        plaintext = decipher.decrypt(ciphertext).decode('utf-8')
        return plaintext