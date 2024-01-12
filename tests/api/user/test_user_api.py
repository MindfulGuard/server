from tests.api.paths import USER_PATH_V1
from tests.api.user.delete import UserDeleteApi
from tests.api.user.get_information import UserGetInformationApi
from http.client import BAD_REQUEST, CONFLICT, INTERNAL_SERVER_ERROR, NOT_FOUND, OK, UNAUTHORIZED, UNPROCESSABLE_ENTITY
from mindfulguard.classes.security import Security
from routines.sucure.secret_string import get_secret_string
from tests.api.authentication.sign_in import SignInApi
from tests.api.authentication.sign_up import SignUpApi
from tests.api.paths import AUTH_PATH_V1
from tests.api.headers import *
from tests.api.user.udpate_secret_code_and_backup_codes import UserUpdateSecretCodeAdnBackupCodesApi
from tests.api.user.update_secret_string import UserUpdateSecretStringApi

def test_user_api():
    LOGIN = "User_222"
    PASSWORD = "HgADj#43n4v4njkvksnlzNV^%"
    SALT = "ecadd7b8-8167-476a-af5e-b626d095987f"
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

    user_information = UserGetInformationApi(USER_PATH_V1)
    assert user_information.execute(with_token_OK(token)).status_code == OK
    
    update_secret_code = UserUpdateSecretCodeAdnBackupCodesApi(USER_PATH_V1)
    body = {
        "secret_string": 'aX7pDfUTAMQvQU3tOPs7IJ8pYaczHjilEo9cQ4r2DOrSTx6aVYqpYOMQatScCdfR'
    }
    assert update_secret_code.execute(
        with_token_OK(token),
        body,
        'None'
    ).status_code == UNPROCESSABLE_ENTITY
    assert update_secret_code.execute(
        with_token_OK(token),
        body,
        'basic'
    ).status_code == INTERNAL_SERVER_ERROR
    assert update_secret_code.execute(
        with_token_OK(token),
        body,
        'backup'
    ).status_code == INTERNAL_SERVER_ERROR
    body = {
        "secret_string": secret_string
    }
    update_secret_code_request = update_secret_code.execute(
        with_token_OK(token),
        body,
        'basic'
    )
    assert update_secret_code_request.status_code == OK
    secret_code = update_secret_code_request.json()['data']
    update_secret_code_request = update_secret_code.execute(
        with_token_OK(token),
        body,
        'backup'
    )
    assert update_secret_code_request.status_code == OK
    backup_codes = update_secret_code_request.json()['data']

    sign_in_body_ok = {
        "login": LOGIN,
        "secret_string": secret_string,
        "code": backup_codes[0],
        "expiration": 60 #minutes
    }
    assert sign_in.execute(without_token, sign_in_body_ok, 'backup').status_code == OK

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

    update_secret_string = UserUpdateSecretStringApi(USER_PATH_V1)
    body = {
        "old_secret_string": secret_string,
        "new_secret_string": secret_string,
        "code": totp.get()
    }
    assert update_secret_string.execute(with_token_OK(token), body).status_code == BAD_REQUEST
    PASSWORD = "$*)(#@B*M0948m09v4324v238m90vVV)"
    new_secret_string = get_secret_string(LOGIN, PASSWORD, SALT)
    body = {
        "old_secret_string": secret_string,
        "new_secret_string": new_secret_string,
        "code": '123456'
    }
    assert update_secret_string.execute(with_token_OK(token), body).status_code == NOT_FOUND
    body = {
        "old_secret_string": secret_string,
        "new_secret_string": new_secret_string,
        "code": totp.get()
    }
    assert update_secret_string.execute(with_token_OK(token), body).status_code == OK
    assert update_secret_string.execute(with_token_OK(token), body).status_code == UNAUTHORIZED

    sign_in_body_ok = {
        "login": LOGIN,
        "secret_string": new_secret_string,
        "code": totp.get(),
        "expiration": 60 #minutes
    }
    sign_in_response = sign_in.execute(without_token, sign_in_body_ok, 'basic')
    assert sign_in_response.status_code == OK

    delete_user = UserDeleteApi(USER_PATH_V1)
    body = {
        "secret_string": new_secret_string,
        "code": '123456'
    }
    assert delete_user.execute(with_token_OK(token), body).status_code == INTERNAL_SERVER_ERROR
    body = {
        "secret_string": 'wiwq3Jcos8KWBVHsNttahNXIvice1AstAiNCjVMLQYvWO0oeqzmfkpmVZFwNyXqp',
        "code": totp.get()
    }
    assert delete_user.execute(with_token_OK(token), body).status_code == UNAUTHORIZED
    body = {
        "secret_string": new_secret_string,
        "code": totp.get()
    }
    assert delete_user.execute(with_token_OK(token), body).status_code == OK