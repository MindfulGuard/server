from http.client import BAD_REQUEST, CONFLICT, NOT_FOUND, OK, UNAUTHORIZED, UNPROCESSABLE_ENTITY
from mindfulguard.classes.security import Security
from routines.sucure.secret_string import get_secret_string
from tests.api.authentication.sign_in import SignInApi
from tests.api.authentication.sign_out import SignOutApi
from tests.api.authentication.sign_up import SignUpApi
from tests.api.paths import AUTH_PATH_V1, USER_PATH_V1
from tests.api.headers import *
from tests.api.user.get_information import UserGetInformationApi

def test_authentication_api():
    LOGIN = "User1"
    PASSWORD = "Jnnnj#43n434njkvkjnlzNV^%"
    SALT = "617eb042-3dd3-4ace-b69e-65df5e8db514"
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

    user_info = UserGetInformationApi(USER_PATH_V1)
    assert user_info.execute(with_token_BAD_REQUEST).status_code == BAD_REQUEST
    assert user_info.execute(with_token_UNAUTHORIZED).status_code == UNAUTHORIZED


    user_info_response = user_info.execute(with_token_OK(token))
    assert user_info_response.status_code == OK
    user_information = user_info_response.json()

    sign_out = SignOutApi(AUTH_PATH_V1)
    assert sign_out.execute(with_token_UNAUTHORIZED, '10da53de-7e41-4659-94b3-0666dd49164d').status_code == UNAUTHORIZED
    assert sign_out.execute(with_token_OK(token), '10da53de-7e41-4659-94b3-0666dd49164d').status_code == NOT_FOUND
    assert sign_out.execute(with_token_OK(token), 'v40239m8v409238m409c234v23').status_code == BAD_REQUEST

    token_id = user_information['tokens'][0]['id']
    assert sign_out.execute(with_token_OK(token), token_id).status_code == OK
    assert sign_out.execute(with_token_OK(token), token_id).status_code == NOT_FOUND
    token_id = user_information['tokens'][1]['id']
    assert sign_out.execute(with_token_OK(token), token_id).status_code == OK
    assert sign_out.execute(with_token_OK(token), token_id).status_code == UNAUTHORIZED