from hashlib import sha256
import secrets
import uuid
from fastapi.testclient import TestClient
from mypass.__main__ import app
from mypass.settings import *
from tests.api.secure import *

client = TestClient(app)

EMAIL = "user64@femail.com"
LOGIN = "user64"
PASSWORD = "12345"
SALT = uuid.uuid4().hex

def generate_random_bytes(length=16):
    # Генерируем случайные байты указанной длины
    random_bytes = secrets.token_bytes(length)
    
    return random_bytes

def test_auth_config():
    response = client.get(VERSION1+PATH_AUTH+"/config")
    assert response.status_code == 200

def auth_config():
    response = client.get(VERSION1+PATH_AUTH+"/config")
    return response.json()

def generate_aes256key():
    iterations:int = auth_config()["pbkdf2"]["iterations"]
    SHA:str = auth_config()["pbkdf2"]["client_SHA"]
    secure = PbkdF2HMAC(iterations,SHA)
    prvaite_key = str(SALT).replace("-", "")
    return (secure.encrypt(PASSWORD,bytes.fromhex(prvaite_key)))

def encrypt_password():
    return sha256(bytes(PASSWORD,'utf-8')+generate_aes256key()).hexdigest()

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
    response = client.post(VERSION1+PATH_AUTH+"/sign_up", data=data,headers=headers)

    assert len(encrypt_password())==64
    assert response.status_code == 200

def test_sign_in():
    data = {
        "email": EMAIL,
        "secret_string": encrypt_password(),
        "expiration": 10
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Real-IP':'192.168.1.1',
        'User-Agent':'python/win'
    }
    response = client.post(VERSION1+PATH_AUTH+"/sign_in", data=data,headers=headers)
    
    assert response.status_code == 200

    print("Response JSON:", response.json())

def sign_in()->str:
    data = {
        "email": EMAIL,
        "secret_string": encrypt_password(),
        "expiration": 10
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Real-IP':'192.168.1.1',
        'User-Agent':'python/win'
    }
    response = client.post(VERSION1+PATH_AUTH+"/sign_in", data=data,headers=headers)

    print("Response JSON:", response.json())

    return response.json()["token"]

def test_get_tokens():
    headers = {
        'Authorization':'Bearer '+sign_in(),
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Real-IP':'192.168.1.1',
        'User-Agent':'python/win'
    }
    response = client.request(method="GET",url=VERSION1+PATH_AUTH+"/sessions",headers=headers)

    assert response.status_code == 200,response.json()

def get_tokens()->str:
    headers = {
        'Authorization':'Bearer '+sign_in(),
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Real-IP':'192.168.1.1',
        'User-Agent':'python/win'
    }
    response = client.request(method="GET",url=VERSION1+PATH_AUTH+"/sessions",headers=headers)

    #print(response.json()["list"][0])
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
    response = client.request(method="DELETE",url=VERSION1+PATH_AUTH+"/sign_out",data=data,headers=headers)
    
    assert response.status_code == 200,get_tokens()