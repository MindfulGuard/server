import hashlib
from http.client import BAD_REQUEST, NOT_FOUND, OK
import re

from fastapi.testclient import TestClient

from mindfulguard.__main__ import app
from tests.api.secure.totp_client import TotpClient


client = TestClient(app)

AUTH_PATH_V1 = "/v1/auth"
SAFE_AND_ITEM_PATH_V1 = "v1/safe"

without_token = {
    'User-Agent': 'python:3.10/windows',
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Real-IP': '127.0.0.1'
}

def with_token_OK(token:str)-> dict[str, str]:
    with_token_OK = {
        'User-Agent': 'python:3.10/windows',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Real-IP': '127.0.0.1',
        'Authorization': 'Bearer '+token
    }
    return with_token_OK

with_token_BAD_REQUEST = {
    'User-Agent': 'python:3.10/windows',
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Real-IP': '127.0.0.1',
    'Authorization': '54385vn9384'
}

with_token_UNAUTHORIZED = {
    'User-Agent': 'python:3.10/windows',
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Real-IP': '127.0.0.1',
    'Authorization': 'Bearer xqdwu8tPKvnFBPZiQzGanMZ2UM8b8ALJVikZ6iTNK0RdxehS4AUiYy9sgP7Ys7OULF6FsJekTB5XARFzOTolTgR8WTJqw85AhylCS3WxWA6Gr7D5zeHM7VmWT2KpbPzO'
}

LOGIN1 = "UFnvjknn_-23"
PASSWORD1 = "#j98j(VJ(BNJNNKVJNvnx"
SALT1 = "167f8252-5bfc-4cce-b2d0-41c22406c50d"

def get_password_rule()->str:
    response_OK = client.get("/v1/public/configuration", headers=without_token)
    rule = response_OK.json()["authentication"]["password_rule"]
    rule = rule.replace("\\", "\\")
    rule = rule.replace("//", "/")
    return rule

def get_secret_string(login:str,password:str,salt:str)->str:
    def validate_password(password:str)->bool:
        return bool(re.compile(get_password_rule()).match(password))

    if validate_password(password) == False:
        return ""
    secret_string = hashlib.sha256()
    secret_string.update(login.encode('utf-8'))
    secret_string.update(password.encode('utf-8'))
    secret_string.update(salt.encode('utf-8'))
    return secret_string.hexdigest()

def registration(login:str,password:str,salt:str):
    secret_string:str = get_secret_string(login,password,salt)

    data_ok = {
        "login": login,
        "secret_string": secret_string,
    }
    data_bad_request = {
        "login": "$v3-4v34v-3-vV_#_V$#",
        "secret_string": "v4234v32b32",
    }

    response_OK = client.post(AUTH_PATH_V1+ "/sign_up", data=data_ok, headers=without_token)
    response_BAD_REQUEST = client.post(AUTH_PATH_V1+ "/sign_up", data=data_bad_request, headers=without_token)

    return (response_OK,response_BAD_REQUEST)


"""
These constants are used to tell the function which type of confirmation code to use.
"""
TYPE_BASIC = "basic"
def log_in(login:str,password:str,salt:str,code:str,type:str):
    secret_string:str = get_secret_string(login,password,salt)
    data_ok = {
        "login": login,
        "secret_string": secret_string,
        "code": code,
        "expiration": 60 #minutes
    }
    data_bad_request = {
        "login": "*8vn3vn487*&NV$N&#*V*NV",
        "secret_string": "123",
        "code": "12",
        "expiration": 534534 #minutes
    }
    data_not_found = {
        "login": "Hel_-o",
        "secret_string": "9l6rryeUVcXvO67Gax9zrZERJCgAzISyYe1Jf0Ue9w0VTSweVFnK6d3VANm0G0oq",
        "code": "573856",
        "expiration": 100 #minutes
    }

    response_OK_basic = client.post(AUTH_PATH_V1+ f"/sign_in?type={type}", data=data_ok, headers=without_token)
    response_BAD_REQUEST = client.post(AUTH_PATH_V1+ f"/sign_in?type={type}", data=data_bad_request, headers=without_token)
    response_NOT_FOUND= client.post(AUTH_PATH_V1+ f"/sign_in?type={type}", data=data_not_found, headers=without_token)

    return (response_OK_basic,response_BAD_REQUEST,response_NOT_FOUND)


def test_safe_and_items():
    __registration1 = registration(LOGIN1,PASSWORD1,SALT1)
    __registration1_OK = __registration1[0]
    secret_code1:str = __registration1_OK.json()["secret_code"]
    ____registration1_BAD_REQUEST = __registration1[1]
    
    totp_client1 = TotpClient(secret_code1)
    __log_in1 = log_in(LOGIN1,PASSWORD1,SALT1,totp_client1.get(),TYPE_BASIC)
    __log_in1_OK = __log_in1[0]
    token1:str = __log_in1_OK.json()["token"]
    __log_in1_BAD_REQUEST = __log_in1[1]
    __log_in1_NOT_FOUND = __log_in1[2]

    assert __registration1_OK.status_code == OK
    assert ____registration1_BAD_REQUEST.status_code == BAD_REQUEST

    assert __log_in1_OK.status_code == OK
    assert __log_in1_BAD_REQUEST.status_code == BAD_REQUEST
    assert __log_in1_NOT_FOUND.status_code == NOT_FOUND