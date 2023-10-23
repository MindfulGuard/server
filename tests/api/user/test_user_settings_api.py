import hashlib
from http.client import BAD_REQUEST, INTERNAL_SERVER_ERROR, NOT_FOUND, OK, UNAUTHORIZED
import re
from fastapi.testclient import TestClient
from mindfulguard.__main__ import app
from tests.api.secure.totp_client import TotpClient
from tests.api.utils import is_list

client = TestClient(app)

AUTH_PATH_V1 = "/v1/auth"
USER_SETTINGS_PATH_V1 = "/v1/user/settings"

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

LOGIN = "Helfsv_--43"
PASSWORD = "**()V#)0mv34m08924v83092mv?b3454/gfd"
SALT = "a8f9fe9f-1342-4459-bf08-418e1c14bd13"

def get_password_rule()->str:
    response_OK = client.get("/v1/public/configuration", headers=without_token)
    rule = response_OK.json()["password_rule"]
    rule = rule.replace("\\", "\\")
    rule = rule.replace("//", "/")
    return rule

def get_secret_string(password:str)->str:
    def validate_password(password:str)->bool:
        return bool(re.compile(get_password_rule()).match(password))

    if validate_password(password) == False:
        return ""
    secret_string = hashlib.sha256()
    secret_string.update(LOGIN.encode('utf-8'))
    secret_string.update(password.encode('utf-8'))
    secret_string.update(SALT.encode('utf-8'))
    return secret_string.hexdigest()

def registration():
    secret_string:str = get_secret_string(PASSWORD)

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
    secret_string:str = get_secret_string(PASSWORD)
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

NEW_SECRET_STRING = get_secret_string("$*0Mvm809vm83m84<V#vv-dsaf")
def update_secret_string(token:str,code:str):
    old_secret_string:str = get_secret_string(PASSWORD)
    new_secret_string:str = NEW_SECRET_STRING

    data_ok = {
        "login":LOGIN,
        "old_secret_string": old_secret_string,
        "new_secret_string": new_secret_string,
        "code":code
    }
    data_bad_request = {
        "login":"&*$9nvn9v432",
        "old_secret_string": "12343",
        "new_secret_string": "5345345",
        "code":"65784f3"
    }
    data_internal_server_error = {
        "login":LOGIN,
        "old_secret_string": old_secret_string,
        "new_secret_string": new_secret_string,
        "code":"739458"
    }

    response_OK_basic = client.put(USER_SETTINGS_PATH_V1+"/auth/secret_string", data=data_ok, headers=with_token_OK(token))
    response_BAD_REQUEST = client.put(USER_SETTINGS_PATH_V1+"/auth/secret_string", data=data_bad_request, headers=with_token_BAD_REQUEST)
    response_UNAUTHORIZED= client.put(USER_SETTINGS_PATH_V1+"/auth/secret_string", data=data_ok, headers=with_token_UNAUTHORIZED)
    response_INTERNAL_SERVER_ERROR = client.put(USER_SETTINGS_PATH_V1+"/auth/secret_string", data=data_internal_server_error, headers=with_token_OK(token))
    return (
        response_OK_basic,
        response_BAD_REQUEST,
        response_UNAUTHORIZED,
        response_INTERNAL_SERVER_ERROR
    )

def update_one_time_codes(token:str):
    secret_string:str = get_secret_string(PASSWORD)
    data_ok = {
        "secret_string": secret_string,
    }
    data_bad_request = {
        "secret_string": "123",
    }
    data_internal_server_error = {
        "secret_string": "9l6rryeUVcXvO67Gax9zrZERJCgAzISyYe1Jf0Ue9w0VTSweVFnK6d3VANm0G0oq",
    }

    response_OK_basic = client.put(USER_SETTINGS_PATH_V1+"/auth/one_time_code?type=basic", data=data_ok, headers=with_token_OK(token))
    response_OK_backup = client.put(USER_SETTINGS_PATH_V1+"/auth/one_time_code?type=backup", data=data_ok, headers=with_token_OK(token))
    response_BAD_REQUEST = client.put(USER_SETTINGS_PATH_V1+"/auth/one_time_code?type=basic", data=data_bad_request, headers=with_token_BAD_REQUEST)
    response_UNAUTHORIZED= client.put(USER_SETTINGS_PATH_V1+"/auth/one_time_code?type=basic", data=data_ok, headers=with_token_UNAUTHORIZED)
    response_INTERNAL_SERVER_ERROR = client.put(USER_SETTINGS_PATH_V1+"/auth/one_time_code?type=basic", data=data_internal_server_error, headers=with_token_OK(token))
    return (
        response_OK_basic,
        response_OK_backup,
        response_BAD_REQUEST,
        response_UNAUTHORIZED,
        response_INTERNAL_SERVER_ERROR,
        True if type(response_OK_basic.json()['data'])==str else False,
        True if type(response_OK_backup.json()['data'])==list else False
    )

def delete_user(token:str,code:str):
    data_ok = {
        "login": LOGIN,
        "secret_string": NEW_SECRET_STRING,
        "code": code,
    }
    data_bad_request = {
        "login": "*8vn3vn487*&NV$N&#*V*NV",
        "secret_string": "123",
        "code": "12",
    }
    data_internal_server_error = {
        "login": "Hel_-o",
        "secret_string": "9l6rryeUVcXvO67Gax9zrZERJCgAzISyYe1Jf0Ue9w0VTSweVFnK6d3VANm0G0oq",
        "code": "573856",
    }

    response_OK_basic = client.request(url=USER_SETTINGS_PATH_V1, method="DELETE", data=data_ok, headers=with_token_OK(token))
    response_UNAUTHORIZED = client.request(url=USER_SETTINGS_PATH_V1, method="DELETE", data=data_bad_request, headers=without_token)
    response_INTERNAL_SERVER_ERROR= client.request(url=USER_SETTINGS_PATH_V1, method="DELETE", data=data_internal_server_error, headers=with_token_OK(token))

    return (response_OK_basic,response_UNAUTHORIZED,response_INTERNAL_SERVER_ERROR)

def test_secret_string():
    assert get_secret_string(PASSWORD) != "", get_password_rule()

def test_user_settings():
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

    __update_one_time_codes = update_one_time_codes(token)
    __update_one_time_codes_OK_basic = __update_one_time_codes[0]
    new_secret_string = __update_one_time_codes_OK_basic.json()['data']
    __update_one_time_codes_OK_backup = __update_one_time_codes[1]
    __update_one_time_codes_BAD_REQUEST = __update_one_time_codes[2]
    __update_one_time_codes_UNAUTHORIZED = __update_one_time_codes[3]
    __update_one_time_codes_INTERNAL_SERVER_ERROR = __update_one_time_codes[4]
    __update_one_time_codes_OK_basic_is_str = __update_one_time_codes[5]
    __update_one_time_codes_OK_backup_is_list = __update_one_time_codes[6]

    new_totp_client = TotpClient(new_secret_string)
    __update_secret_string = update_secret_string(token,new_totp_client.get())
    __update_secret_string_OK = __update_secret_string[0]
    __update_secret_string_BAD_REQUEST = __update_secret_string[1]
    __update_secret_string_INTERNAL_SERVER_ERROR = __update_secret_string[3]

    __delete_user = delete_user(token,new_totp_client.get())
    __delete_user_OK = __delete_user[0]
    __delete_user_BAD_REQUEST = __delete_user[1]
    __delete_user_INTERNAL_SERVER_ERROR = __delete_user[2]

    assert password_rule.status_code == OK

    assert __registration_OK.status_code == OK
    assert __registration_BAD_REQUEST.status_code == BAD_REQUEST

    assert __log_in_basic_OK.status_code == OK
    assert __log_in_backup_OK.status_code == OK
    assert __log_in_basic_BAD_REQUEST.status_code == BAD_REQUEST
    assert __log_in_basic_NOT_FOUND.status_code == NOT_FOUND

    assert __update_one_time_codes_OK_basic.status_code == OK
    assert __update_one_time_codes_OK_backup.status_code == OK
    assert __update_one_time_codes_BAD_REQUEST.status_code == BAD_REQUEST
    assert __update_one_time_codes_UNAUTHORIZED.status_code == UNAUTHORIZED
    assert __update_one_time_codes_INTERNAL_SERVER_ERROR.status_code == INTERNAL_SERVER_ERROR
    assert __update_one_time_codes_OK_basic_is_str == True
    assert __update_one_time_codes_OK_backup_is_list == True

    assert __update_secret_string_BAD_REQUEST.status_code == BAD_REQUEST
    assert __update_secret_string_OK.status_code == OK

    assert __delete_user_OK.status_code == OK
    #assert __delete_user_BAD_REQUEST.status_code == BAD_REQUEST
    #assert __delete_user_INTERNAL_SERVER_ERROR.status_code == INTERNAL_SERVER_ERROR