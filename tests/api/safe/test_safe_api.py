from http.client import BAD_REQUEST, CONFLICT, INTERNAL_SERVER_ERROR, NOT_FOUND, OK, UNAUTHORIZED, UNPROCESSABLE_ENTITY
from mindfulguard.classes.security import Security
from routines.sucure.secret_string import get_secret_string
from tests.api.authentication.sign_in import SignInApi
from tests.api.authentication.sign_up import SignUpApi
from tests.api.paths import AUTH_PATH_V1, SAFE_PATH_V1
from tests.api.headers import *
from tests.api.safe.create import SafeCreateApi
from tests.api.safe.delete import SafeDeleteApi
from tests.api.safe.get import SafeGetApi
from tests.api.safe.udpate import SafeUpdateApi
from tests.logger import logger

logger()

def test_safe_api():
    LOGIN = "User_22"
    PASSWORD = "Ggnnj#43n4v4njkvksnlzNV^%"
    SALT = "a908b798-6c6e-49e4-aebd-262d7c503ce4"
    secret_string: str = get_secret_string(LOGIN, PASSWORD, SALT)

    sign_up = SignUpApi(AUTH_PATH_V1)
    sign_up_body_ok = {
        "login": LOGIN,
        "secret_string": secret_string,
    }
    sign_up_body_bad_request = {
        "login": "$v3-4v34v-3-vV_#_V$#",
        "secret_string": "v4234v32b32",
    }

    assert sign_up.execute(without_token, sign_up_body_bad_request).status_code == BAD_REQUEST

    assert sign_up.execute(without_token, sign_up_body_ok).status_code == OK

    sign_up_response = sign_up.execute(without_token, sign_up_body_ok)
    assert sign_up_response.status_code == OK
    secret_code: str = sign_up_response.json()['secret_code']
    backup_codes: list[int] = sign_up_response.json()['backup_codes']

    sign_in = SignInApi(AUTH_PATH_V1)
    sign_in_body_bad_request = {
        "login": LOGIN,
        "secret_string": secret_string,
        "code": "123456",
        "expiration": 534534 #minutes
    }
    assert sign_in.execute(without_token, sign_in_body_bad_request, 'basic').status_code == BAD_REQUEST
    sign_in_body_bad_request = {
        "login": LOGIN,
        "secret_string": secret_string,
        "code": "123456789",
        "expiration": 60 #minutes
    }
    assert sign_in.execute(without_token, sign_in_body_bad_request, 'basic').status_code == BAD_REQUEST
    sign_in_body_ok = {
        "login": LOGIN,
        "secret_string": secret_string,
        "code": str(backup_codes[0]),
        "expiration": 60 #minutes
    }
    assert sign_in.execute(without_token, sign_in_body_ok, 'None').status_code == UNPROCESSABLE_ENTITY
    assert sign_in.execute(without_token, sign_in_body_ok, 'backup').status_code == OK
    assert sign_in.execute(without_token, sign_in_body_ok, 'backup').status_code == NOT_FOUND
    totp = Security().totp("WjGoa4joB7vFsFRXx7mJd2reCn4YVQNL")
    sign_in_body_ok = {
        "login": LOGIN,
        "secret_string": secret_string,
        "code": totp.get(),
        "expiration": 60 #minutes
    }
    assert sign_in.execute(without_token, sign_in_body_ok, 'basic').status_code == NOT_FOUND
    totp = Security().totp(secret_code)
    sign_in_body_ok = {
        "login": LOGIN,
        "secret_string": secret_string,
        "code": totp.get(),
        "expiration": 60 #minutes
    }
    sign_in_response = sign_in.execute(without_token, sign_in_body_ok, 'basic')
    assert sign_in_response.status_code == OK
    token: str = sign_in_response.json()['token']

    assert sign_up.execute(without_token, sign_up_body_ok).status_code == CONFLICT

    safe_create = SafeCreateApi(SAFE_PATH_V1)
    safe_body = {
        "name": "75WaTMAdrJf5h87UZ6LqixHkYELYqt9jyzpQxSEeXUIaj3o9oEe99tLuK23i5mhxuJ1PqT1pfFjuB6M5lxOk0nT2y8iZjPFZ6yectPS1x2rY7IoRnwGnVzjDyywDVECw",
        "description": "Description 1"
    }
    assert safe_create.execute(with_token_OK(token), safe_body).status_code == BAD_REQUEST
    safe_body = {
        "name": "Safe 1",
        "description": "Description 1"
    }
    assert safe_create.execute(with_token_OK(token), safe_body).status_code == OK
    assert safe_create.execute(with_token_OK(token), safe_body).status_code == OK

    safe_get = SafeGetApi(SAFE_PATH_V1)
    safe_get_response = safe_get.execute(with_token_OK(token))
    assert safe_get_response.status_code == OK

    safe_and_items_and_files_information = safe_get_response.json()
    
    safe_update = SafeUpdateApi(SAFE_PATH_V1)
    assert safe_update.execute(with_token_OK(token), safe_body, '4v20394v8023b4m823084v032').status_code == BAD_REQUEST
    assert safe_update.execute(with_token_OK(token), safe_body, 'ad8f33db-0042-42ca-9b36-b33357c01d96').status_code == INTERNAL_SERVER_ERROR
    safe_id = safe_and_items_and_files_information['safes'][0]['id']
    assert safe_update.execute(with_token_OK(token), safe_body, safe_id).status_code == OK
    
    safe_delete = SafeDeleteApi(SAFE_PATH_V1)
    #assert safe_delete.execute(with_token_OK(token), '4v20394v8023b4m823084v032').status_code == BAD_REQUEST
    #assert safe_delete.execute(with_token_OK(token), 'ad8f33db-0042-42ca-9b36-b33357c01d96').status_code == NOT_FOUND
    assert safe_delete.execute(with_token_OK(token), safe_id).status_code == OK
