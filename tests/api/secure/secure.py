import hashlib
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import pyotp

class PbkdF2HMAC:
    def __init__(self):...
    def encrypt(self, password: str, salt: bytes) -> bytes:
        kdf = PBKDF2(password, salt, 32, 100000)
        return kdf

class AES_256:
    def encrypt(self, private_key, message):
        cipher = AES.new(private_key, AES.MODE_GCM)
        ciphertext, auth_tag = cipher.encrypt_and_digest(message.encode())
        return cipher.nonce.hex() + ciphertext.hex() + auth_tag.hex()

    def decrypt(self, private_key: bytes, ciphertext: str):
        nonce = bytes.fromhex(ciphertext[:32])
        ciphertext_bytes = bytes.fromhex(ciphertext[32:-32])
        tag = bytes.fromhex(ciphertext[-32:])

        cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext_bytes, tag)
        return plaintext.decode()
    
def sha256s(string:str):
    sha256 = hashlib.sha256()
    
    sha256.update(string.encode('utf-8'))
    
    return sha256.hexdigest()

def totp_client(secret_code:str)->str:
    totp = pyotp.TOTP(secret_code)
    return totp.now()