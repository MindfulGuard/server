import hashlib
from http.client import BAD_REQUEST, NOT_FOUND, OK, UNAUTHORIZED
import re
from fastapi.testclient import TestClient
from mindfulguard.__main__ import app
from tests.api.secure.secure import AES_256, PbkdF2HMAC
from tests.api.secure.totp_client import TotpClient
from tests.api.utils import is_list

client = TestClient(app)

AUTH_PATH_V1 = "/v1/auth"

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

LOGIN = "useR123_-"
PASSWORD = "Nnnj43nv3_--v43%>_34"
SALT = "617eb042-3dd3-4ace-b69e-65df5e8db514"

def get_password_rule()->str:
    response_OK = client.get("/v1/public/configuration", headers=without_token)
    return response_OK.json()["authentication"]["password_rule"]

def get_secret_string():
    def validate_password(password:str)->bool:
        return bool(re.compile(get_password_rule()).match(password))

    if validate_password(PASSWORD) == False:
        return hashlib._Hash(data=b"")
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

    response_OK = client.post(AUTH_PATH_V1+ "/sign_up", data=data_ok, headers=without_token)
    response_BAD_REQUEST = client.post(AUTH_PATH_V1+ "/sign_up", data=data_bad_request, headers=without_token)

    return (response_OK,response_BAD_REQUEST)


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

    response_OK_basic = client.post(AUTH_PATH_V1+ f"/sign_in?type={type}", data=data_ok, headers=without_token)
    response_BAD_REQUEST = client.post(AUTH_PATH_V1+ f"/sign_in?type={type}", data=data_bad_request, headers=without_token)
    response_NOT_FOUND= client.post(AUTH_PATH_V1+ f"/sign_in?type={type}", data=data_not_found, headers=without_token)

    return (response_OK_basic,response_BAD_REQUEST,response_NOT_FOUND)

def get_session_tokens(token:str):
    response_OK = client.get(AUTH_PATH_V1+"/sessions", headers=with_token_OK(token))
    response_BAD_REQUEST = client.get(AUTH_PATH_V1+"/sessions", headers=with_token_BAD_REQUEST)
    response_UNAUTHORIZED = client.get(AUTH_PATH_V1+"/sessions", headers=with_token_UNAUTHORIZED)

    return(response_OK,response_BAD_REQUEST,response_UNAUTHORIZED)

def test_authentication():
    password_rule = client.get("/v1/public/configuration", headers=without_token)

    __registration = registration()
    __registration_OK = __registration[0]
    secret_code:str = __registration_OK.json()["secret_code"]
    backup_code:str = str(__registration_OK.json()["backup_codes"][0])
    __registration_BAD_REQUEST = __registration[1]

    totp_client = TotpClient(secret_code)
    __log_in_basic = log_in(totp_client.get(),TYPE_BASIC)
    __log_in_backup = log_in(backup_code,TYPE_BACKUP)
    __log_in_basic_OK = __log_in_basic[0]
    token:str = __log_in_basic_OK.json()["token"]
    __log_in_backup_OK = __log_in_backup[0]
    __log_in_basic_BAD_REQUEST = __log_in_basic[1]
    __log_in_basic_NOT_FOUND = __log_in_basic[2]

    __get_session_tokens = get_session_tokens(token)
    __get_session_tokens_OK = __get_session_tokens[0]
    __get_session_tokens_BAD_REQUEST = __get_session_tokens[1]
    __get_session_tokens_UNAUTHORIZED = __get_session_tokens[2]

    assert password_rule.status_code == OK

    assert __registration_OK.status_code == OK
    assert __registration_BAD_REQUEST.status_code == BAD_REQUEST

    assert __log_in_basic_OK.status_code == OK
    assert __log_in_backup_OK.status_code == OK
    assert __log_in_basic_BAD_REQUEST.status_code == BAD_REQUEST
    assert __log_in_basic_NOT_FOUND.status_code == NOT_FOUND

    assert __get_session_tokens_OK.status_code == OK
    assert is_list(__get_session_tokens_OK.json()["list"]) == True, __get_session_tokens_OK.json()["list"]
    assert __get_session_tokens_BAD_REQUEST.status_code == BAD_REQUEST
    assert __get_session_tokens_UNAUTHORIZED.status_code == UNAUTHORIZED