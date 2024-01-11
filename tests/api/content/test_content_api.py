from http.client import BAD_REQUEST, CONFLICT, INTERNAL_SERVER_ERROR, NOT_FOUND, OK, UNAUTHORIZED, UNPROCESSABLE_ENTITY
from io import BufferedReader
import os
from mindfulguard.classes.security import Security
from routines.sucure.secret_string import get_secret_string
from tests.api.authentication.sign_in import SignInApi
from tests.api.authentication.sign_up import SignUpApi
from tests.api.content.delete import ContentDeleteApi
from tests.api.content.download import ContentDownloadApi
from tests.api.content.upload import ContentUploadApi
from tests.api.paths import AUTH_PATH_V1, SAFE_PATH_V1, USER_PATH_V1
from tests.api.headers import *
from tests.api.safe.create import SafeCreateApi
from tests.api.safe.delete import SafeDeleteApi
from tests.api.safe.get import SafeGetApi
from tests.api.safe.udpate import SafeUpdateApi
from tests.api.user.delete import UserDeleteApi

PATH_TO_FILES = 'tests/api/content/temp_files'
PATH_TO_DOWNLOAD_FILES = 'tests/api/content/temp_download_files'
FILE_NAMES: list[str] = ["/400MiB1.bin", "/400MiB2.bin", "/400MiB3.bin"]

def generate_files(file_names: list[str], directory: str, size_in_mb: int):
    for file_name in file_names:
        file_path = os.path.join(directory, file_name.lstrip("/"))
        generate_binary_file(file_path, size_in_mb)
    
    return True

def generate_binary_file(file_path: str, size_in_mb: int):
    size_in_bytes = size_in_mb * 1024 * 1024  # Convert MB to bytes
    with open(file_path, "wb") as f:
        f.write(os.urandom(size_in_bytes))

def test_content_api():
    assert generate_files(FILE_NAMES, PATH_TO_FILES, 400) ==  True

    LOGIN = "User_2242"
    PASSWORD = "GSnaG#43n4v4njkvksnGzNS^%"
    SALT = "95ec3185-7d8e-460f-b88a-ea1c1354505e"
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

    safe_get = SafeGetApi(SAFE_PATH_V1)
    safe_get_response = safe_get.execute(with_token_OK(token))
    assert safe_get_response.status_code == OK

    safe_and_items_and_files_information = safe_get_response.json()
    
    safe_update = SafeUpdateApi(SAFE_PATH_V1)
    assert safe_update.execute(with_token_OK(token), safe_body, '4v20394v8023b4m823084v032').status_code == BAD_REQUEST
    assert safe_update.execute(with_token_OK(token), safe_body, 'ad8f33db-0042-42ca-9b36-b33357c01d96').status_code == INTERNAL_SERVER_ERROR
    safe_id: str = safe_and_items_and_files_information['safes'][0]['id']
    assert safe_update.execute(with_token_OK(token), safe_body, safe_id).status_code == OK

    content_upload = ContentUploadApi(SAFE_PATH_V1)

    for i in range(0, len(FILE_NAMES) -1):
        content_file: dict[str, BufferedReader] = {'files': open(f'{PATH_TO_FILES}/{FILE_NAMES[i]}', 'rb')}
        assert content_upload.execute(
            with_token_OK(token, 'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW'),
            content_file,
            safe_id
        ).status_code == OK

    for i in range(len(FILE_NAMES) + 1, len(FILE_NAMES)):
        content_file: dict[str, BufferedReader] = {'files': open(f'{PATH_TO_FILES}/{FILE_NAMES[i]}', 'rb')}
        assert content_upload.execute(
            with_token_OK(token, 'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW'),
            content_file,
            safe_id
        ).status_code == INTERNAL_SERVER_ERROR

    download_file = ContentDownloadApi('/v1')
    assert download_file.execute(
        with_token_OK(token),
        '/safe/b0f73d92-fcd1-4f48-9b87-1b5cf48c9e64/bc55c2f4-cf54-4427-857d-2793e68c76e3/content'
    ).status_code == NOT_FOUND

    file_get = SafeGetApi(SAFE_PATH_V1)
    file_get_response = file_get.execute(with_token_OK(token))
    assert file_get_response.status_code == OK
    safe_and_items_and_files_information = file_get_response.json()
    file_id = safe_and_items_and_files_information['files'][0]['objects'][0]['id']

    download_file_reponse =  download_file.execute(with_token_OK(token), file_id)
    assert download_file_reponse.status_code == OK, safe_and_items_and_files_information
            
    file_delete = ContentDeleteApi(SAFE_PATH_V1)
    file_data = {
        'files': file_id
    }
    assert file_delete.execute(with_token_OK(token), file_data, f'{safe_id}/content').status_code == OK

    safe_delete = SafeDeleteApi(SAFE_PATH_V1)
    assert safe_delete.execute(with_token_OK(token), safe_id).status_code == OK

    file_get = SafeGetApi(SAFE_PATH_V1)
    file_get_response = file_get.execute(with_token_OK(token))
    assert file_get_response.status_code == OK
    safe_and_items_and_files_information = file_get_response.json()
    files_list: list = safe_and_items_and_files_information['files']
    assert len(files_list) == 0, files_list

    safe_body = {
        "name": "Safe 2",
        "description": "Description 2"
    }
    assert safe_create.execute(with_token_OK(token), safe_body).status_code == OK
    
    safe_get = SafeGetApi(SAFE_PATH_V1)
    safe_get_response = safe_get.execute(with_token_OK(token))
    assert safe_get_response.status_code == OK
    safe_and_items_and_files_information = safe_get_response.json()
    safe_id: str = safe_and_items_and_files_information['safes'][0]['id']

    content_file: dict[str, BufferedReader] = {'files': open(f'{PATH_TO_FILES}/{FILE_NAMES[0]}', 'rb')}
    assert content_upload.execute(
        with_token_OK(token, 'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW'),
        content_file,
        safe_id
    ).status_code == OK

    user_delete = UserDeleteApi(USER_PATH_V1)
    body = {
        'secret_string': 'G11QFvku8HQGVecdKFHOzNPABo1G6qKgBhcMan2OBLTQjkhhz22lYtO9Xo2HNNhT',
        'code': totp.get()
    }
    assert user_delete.execute(with_token_OK(token), body).status_code == UNAUTHORIZED
    body = {
        'secret_string': secret_string,
        'code': '123456'
    }
    assert user_delete.execute(with_token_OK(token), body).status_code == INTERNAL_SERVER_ERROR
    body = {
        'secret_string': secret_string,
        'code': totp.get()
    }
    assert user_delete.execute(with_token_OK(token), body).status_code == OK

    sign_up = SignUpApi(AUTH_PATH_V1)
    sign_up_body_ok = {
        "login": LOGIN,
        "secret_string": secret_string,
    }

    sign_up_response = sign_up.execute(without_token, sign_up_body_ok)
    assert sign_up_response.status_code == OK
    secret_code: str = sign_up_response.json()['secret_code']

    sign_in = SignInApi(AUTH_PATH_V1)
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

    file_get = SafeGetApi(SAFE_PATH_V1)
    file_get_response = file_get.execute(with_token_OK(token))
    assert file_get_response.status_code == OK
    safe_and_items_and_files_information = file_get_response.json()
    files_list: list = safe_and_items_and_files_information['files']
    assert len(files_list) == 0, files_list