import hashlib
from http.client import BAD_REQUEST, OK
from fastapi.testclient import TestClient
from mindfulguard.__main__ import app
from tests.api.secure.secure import AES_256, PbkdF2HMAC

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

def registration():
    secret_string = hashlib.sha256()
    secret_string.update(LOGIN.encode('utf-8'))
    secret_string.update(PASSWORD.encode('utf-8'))
    secret_string.update(SALT.encode('utf-8'))

    data_ok = {
        "login": LOGIN,
        "secret_string": secret_string.hexdigest(),
    }
    data_bad_request = {
        "login": "$v3-4v34v-3-vV_#_V$#",
        "secret_string": "v4234v32b32",
    }

    response_ok = client.post(AUTH_PATH_V1+ "/sign_up", data=data_ok, headers=headers1)
    response_bad_request = client.post(AUTH_PATH_V1+ "/sign_up", data=data_bad_request, headers=headers1)

    return (response_ok,response_bad_request)

def test_authentication():
    __registration = registration()
    __registration_OK = __registration[0]
    __registration_BAD_REQUEST = __registration[1]

    assert __registration_OK.status_code == OK
    assert __registration_BAD_REQUEST.status_code == BAD_REQUEST