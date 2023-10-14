import hashlib
from http.client import BAD_REQUEST, OK
from fastapi.testclient import TestClient
from mindfulguard.__main__ import app
from tests.api.secure.secure import AES_256, PbkdF2HMAC
from tests.api.secure.totp_client import TotpClient

client = TestClient(app)

AUTH_PATH_V1 = "/v1/auth"

headers1 = {
    'User-Agent': 'python:3.10/windows',
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Real-IP': '127.0.0.1'
}

LOGIN = "useR123_-"
PASSWORD = "Nnnj43nv3_--v43%>_34"
SALT = "617eb042-3dd3-4ace-b69e-65df5e8db514"

def get_secret_string():
    secret_string = hashlib.sha256()
    secret_string.update(LOGIN.encode('utf-8'))
    secret_string.update(PASSWORD.encode('utf-8'))
    secret_string.update(SALT.encode('utf-8'))
    return secret_string
 
def registration():
    secret_string:str = get_secret_string().hexdigest()

    data_ok = {
        "login": LOGIN,
        "secret_string": secret_string,
    }
    data_bad_request = {
        "login": "$v3-4v34v-3-vV_#_V$#",
        "secret_string": "v4234v32b32",
    }

    response_ok = client.post(AUTH_PATH_V1+ "/sign_up", data=data_ok, headers=headers1)
    response_bad_request = client.post(AUTH_PATH_V1+ "/sign_up", data=data_bad_request, headers=headers1)

    return (response_ok,response_bad_request)


"""
These constants are used to tell the function which type of confirmation code to use.
"""
TYPE_BASIC = "basic"
TYPE_BACKUP = "backup"
def log_in(code:str,type:str):
    secret_string:str = get_secret_string().hexdigest()
    data_ok = {
        "login": LOGIN,
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

    response_ok_basic = client.post(AUTH_PATH_V1+ f"/sign_in?type={type}", data=data_ok, headers=headers1)
    response_bad_request = client.post(AUTH_PATH_V1+ f"/sign_in?type={type}", data=data_bad_request, headers=headers1)

    return (response_ok_basic,response_bad_request)

def test_authentication():
    __registration = registration()
    __registration_OK = __registration[0]
    secret_code:str = __registration_OK.json()["secret_code"]
    backup_code:str = str(__registration_OK.json()["backup_codes"][0])
    __registration_BAD_REQUEST = __registration[1]

    totp_client = TotpClient(secret_code)
    __log_in_basic = log_in(totp_client.get(),TYPE_BASIC)
    __log_in_backup = log_in(backup_code,TYPE_BACKUP)
    __log_in_basic_OK = __log_in_basic[0]
    __log_in_backup_OK = __log_in_backup[0]
    __log_in_basic_bad_request = __log_in_basic[1]

    assert __registration_OK.status_code == OK
    assert __registration_BAD_REQUEST.status_code == BAD_REQUEST

    assert __log_in_basic_OK.status_code == OK
    assert __log_in_backup_OK.status_code == OK
    assert __log_in_basic_bad_request.status_code == BAD_REQUEST