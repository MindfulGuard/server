import hashlib
from typing import Any
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import serialization

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