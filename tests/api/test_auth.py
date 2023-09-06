import codecs
import secrets
import string
from fastapi.testclient import TestClient
from mypass.__main__ import app
from mypass.settings import *
from tests.api.secure import *

client = TestClient(app)

EMAIL = "user2@femail.com"
LOGIN = "user2"
PASSWORD = "12345"
PRIVATE_KEY = '729f2d0b625124bcf0e60d42bd8f57a2'

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

def encrypt_password():
    iterations:int = auth_config()["pbkdf2"]["iterations"]
    SHA:str = auth_config()["pbkdf2"]["client_SHA"]
    secure = Security(iterations,SHA)
    
    return (secure.encrypt(EMAIL,PASSWORD,bytes.fromhex(PRIVATE_KEY)))


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