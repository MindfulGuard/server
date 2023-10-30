import hashlib
import secrets


def generate_512_bit_token_string()->str:
    token_bytes = secrets.token_bytes(64)
    token_string = token_bytes.hex()
    return token_string

def sha256s(text:str)->str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def sha512s(text:str)->str:
    return hashlib.sha512(text.encode('utf-8')).hexdigest()

def sha256b(text:bytes)->bytes:
    return hashlib.sha256(text).digest()