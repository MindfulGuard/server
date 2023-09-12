from hashlib import sha256
import re
import secrets
import uuid
from fastapi.testclient import TestClient
from mypass.__main__ import app
from tests.api.secure import *

client = TestClient(app)
client_safe = TestClient(app)

AUTH_PATH_V1 = "/v1/auth"
SAFE_PATH_V1 = "/v1/safe"

EMAIL = "use7fv5r5fg43tf23@tmail.com"
LOGIN = "use5vrt51f331g6f3"
PASSWORD = "u2Hv6t5ffdgso%fmnrmfsfsfsd"
SALT = uuid.uuid4().hex

def generate_random_bytes(length=16):
    random_bytes = secrets.token_bytes(length)
    
    return random_bytes

def test_auth_config():
    response = client.get(AUTH_PATH_V1+"/config")
    assert response.status_code == 200

def auth_config():
    response = client.get(AUTH_PATH_V1+"/config")
    return response.json()

def test_is_valid_password():
    pattern:str = auth_config()["authentication_rule"]["password_rule"]
    print(pattern)
    assert re.match(pattern, PASSWORD) != None

def is_valid_password(password)->bool:
    pattern:str = auth_config()["authentication_rule"]["password_rule"]
    print(pattern)
    return re.match(pattern, password) is not None

def generate_aes256key_abnd()->bytes:
    iterations:int = auth_config()["pbkdf2"]["iterations"]
    SHA:str = auth_config()["pbkdf2"]["SHA"]
    secure = PbkdF2HMAC(iterations,SHA)
    prvaite_key = str(SALT).replace("-", "")
    return (secure.encrypt(PASSWORD,bytes.fromhex(prvaite_key)))

def encrypt_password():
    if is_valid_password(PASSWORD) == False:
        return b""
    return sha256(bytes(EMAIL,'utf-8')+bytes(PASSWORD,'utf-8')+bytes(SALT,'utf-8')).hexdigest()

def test_sign_up():
    data = {
        "email": EMAIL,
        "login": LOGIN,
        "secret_string": encrypt_password()
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Real-IP':'192.168.1.1'
    }
    response = client.post(AUTH_PATH_V1+"/sign_up", data=data,headers=headers)

    assert len(encrypt_password())==64
    assert response.status_code == 200

def test_sign_in():
    data = {
        "email": EMAIL,
        "secret_string": encrypt_password(),
        "expiration": 60
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Real-IP':'192.168.1.1',
        'User-Agent':'python/win'
    }
    response = client.post(AUTH_PATH_V1+"/sign_in", data=data,headers=headers)
    
    assert response.status_code == 200

    print("Response JSON:", response.json())

def sign_in()->str:
    data = {
        "email": EMAIL,
        "secret_string": encrypt_password(),
        "expiration": 60
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Real-IP':'192.168.1.1',
        'User-Agent':'python/win'
    }
    response = client.post(AUTH_PATH_V1+"/sign_in", data=data,headers=headers)

    print("Response JSON:", response.json(),"\nEMAIL:",EMAIL,"\nSECRET_STRING:",encrypt_password())

    return response.json()["token"]

def test_get_tokens():
    headers = {
        'Authorization':'Bearer '+sign_in(),
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Real-IP':'192.168.1.1',
        'User-Agent':'python/win'
    }
    response = client.request(method="GET",url=AUTH_PATH_V1+"/sessions",headers=headers)

    assert response.status_code == 200,response.json()

def get_tokens()->str:
    headers = {
        'Authorization':'Bearer '+sign_in(),
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Real-IP':'192.168.1.1',
        'User-Agent':'python/win'
    }
    response = client.request(method="GET",url=AUTH_PATH_V1+"/sessions",headers=headers)

    return response.json()["list"][0]["id"]


def test_sign_out():
    data = {
        "id": get_tokens(),
    }
    headers = {
        'Authorization':'Bearer '+sign_in(),
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Real-IP':'192.168.1.1',
        'User-Agent':'python/win'
    }
    response = client.request(method="DELETE",url=AUTH_PATH_V1+"/sign_out",data=data,headers=headers)
    
    assert response.status_code == 200,get_tokens()

def generate_aes256_key_from_password(password:bytes,salt:bytes):
    key = hashlib.sha256(password+salt).digest()
    return key

def encrypt_AES256(text_bytes: str):
    obj = AES_256()
    salt = bytes(str(SALT).replace("-", ""),'utf-8')
    password = bytes(PASSWORD,'utf-8')
    return obj.encrypt_aes_256(generate_aes256_key_from_password(password,salt), text_bytes).hex()


def test_create():
    text = 'hello its my v72m40389m0v47358297m085v49v427m089v4325m7089v3452708078951 safe'
    data = {
        "name": "safe1",
        "description": encrypt_AES256(text),
    }
    headers = {
        'Authorization': 'Bearer ' + sign_in(),
        'User-Agent': 'python/win',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Real-IP': '192.168.1.1'
    }
    response = client_safe.post(SAFE_PATH_V1 + "/create", data=data, headers=headers)
    assert response.status_code == 200, sign_in()