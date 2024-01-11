import hashlib

def get_secret_string(login: str, password: str, salt: str)->str:
    secret_string = hashlib.sha256()
    secret_string.update(login.encode('utf-8'))
    secret_string.update(password.encode('utf-8'))
    secret_string.update(salt.encode('utf-8'))
    return secret_string.hexdigest()