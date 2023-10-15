import hashlib
from http.client import BAD_REQUEST, NOT_FOUND, OK, UNAUTHORIZED, UNPROCESSABLE_ENTITY
import re

from fastapi.testclient import TestClient

from mindfulguard.__main__ import app
from tests.api.secure.secure import AES_256, PbkdF2HMAC
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

def create_safe(token:str,name:str,description:str):
    data_ok = {
        "name": name,
        "description": description,
    }
    data_bad_request = {
        "name": "0vEzEFk2BGtUcGKUFFXMVp7ESIsZmLw3Ii7VrfbfDsaUMYscnGS5DI9zqveiqBxvL59UQrCAf5KcyxB6k3gW779ckkFVd5v8Km4Fa4yXWMzmTlNbdlfFWF0CstjsaHFll8yNAsPwrd09V05cb1DpFL6QlKiPVuYG8vyd8QQqa06vdNiN2EP5hbwW3SDSDGhL1IrGrzGgShJNcFhgfoZaOdzlBFsr6VKZkl9hwMr668gAvQZ4r1Mqs07sjyZZud2UTg4Y7fMHnJiRva4oOfkE6TjuAUUmTJaQXw66Gjo3b4SAQBa1wEfQysBGnIbnHUiTpMNyiYTLMINYrqohgHYn0QlPqN72PUMDUENspCUHAZthAxONwCyVPAZE5Uzkpec2TXIXJKzFqAJyORECgfO4qqbWIVeQxCA6vERzsLIY08P6GWKUto8qaRZ9COvrFVd0bTmJxp7Xr6nuCY4IbbLhScjW780wpNGcabYKgDoHgMTinozHZ9DVlEvJisqV2OLcuRHvNrTH7x1TtekS3Xl5dGxJOrNsq3zKoRwWCSQhdFlQT7GR8WD7boIJZAaX3ENWOMRlRAIxsk0kAtZZv9r9h7uSVCmhTYczfeJ872HmaYgMLC5OJ8l7s2HTDmVrVUzPOG9g4avPtwzrEeCu9ezBwWXuTvGFDImxlYUcsqcQlqpxmBdaWrY3zdtkaeib",
        "description": "0vEzEFk2BGtUcGKUFFXMVp7ESIsZmLw3Ii7VrfbfDsaUMYscnGS5DI9zqveiqBxvL59UQrCAf5KcyxB6k3gW779ckkFVd5v8Km4Fa4yXWMzmTlNbdlfFWF0CstjsaHFll8yNAsPwrd09V05cb1DpFL6QlKiPVuYG8vyd8QQqa06vdNiN2EP5hbwW3SDSDGhL1IrGrzGgShJNcFhgfoZaOdzlBFsr6VKZkl9hwMr668gAvQZ4r1Mqs07sjyZZud2UTg4Y7fMHnJiRva4oOfkE6TjuAUUmTJaQXw66Gjo3b4SAQBa1wEfQysBGnIbnHUiTpMNyiYTLMINYrqohgHYn0QlPqN72PUMDUENspCUHAZthAxONwCyVPAZE5Uzkpec2TXIXJKzFqAJyORECgfO4qqbWIVeQxCA6vERzsLIY08P6GWKUto8qaRZ9COvrFVd0bTmJxp7Xr6nuCY4IbbLhScjW780wpNGcabYKgDoHgMTinozHZ9DVlEvJisqV2OLcuRHvNrTH7x1TtekS3Xl5dGxJOrNsq3zKoRwWCSQhdFlQT7GR8WD7boIJZAaX3ENWOMRlRAIxsk0kAtZZv9r9h7uSVCmhTYczfeJ872HmaYgMLC5OJ8l7s2HTDmVrVUzPOG9g4avPtwzrEeCu9ezBwWXuTvGFDImxlYUcsqcQlqpxmBdaWrY3zdtkaeib",
    }
    data_unauthorized = {
        "name": "Hello",
        "description": "Hello",
    }

    response_OK = client.post(
        SAFE_AND_ITEM_PATH_V1,
        data=data_ok,
        headers=with_token_OK(token)
    )
    response_BAD_REQUEST = client.post(
        SAFE_AND_ITEM_PATH_V1,
        data=data_bad_request,
        headers=with_token_OK(token)
    )
    response_UNAUTHORIZED = client.post(
        SAFE_AND_ITEM_PATH_V1,
        data=data_unauthorized,
        headers=with_token_UNAUTHORIZED
    )
    return (response_OK,response_BAD_REQUEST,response_UNAUTHORIZED)

def get_safes_and_items(token:str):
    response_OK = client.get(SAFE_AND_ITEM_PATH_V1+"/all/item", headers=with_token_OK(token))
    response_UNAUTHORIZED = client.get(SAFE_AND_ITEM_PATH_V1+"/all/item", headers=with_token_UNAUTHORIZED)
    return (response_OK,response_UNAUTHORIZED)

def update_safe(token:str,safe_id:str,name:str,description:str):
    data_ok = {
        "name": name,
        "description": description,
    }
    data_bad_request = {
        "name": "0vEzEFk2BGtUcGKUFFXMVp7ESIsZmLw3Ii7VrfbfDsaUMYscnGS5DI9zqveiqBxvL59UQrCAf5KcyxB6k3gW779ckkFVd5v8Km4Fa4yXWMzmTlNbdlfFWF0CstjsaHFll8yNAsPwrd09V05cb1DpFL6QlKiPVuYG8vyd8QQqa06vdNiN2EP5hbwW3SDSDGhL1IrGrzGgShJNcFhgfoZaOdzlBFsr6VKZkl9hwMr668gAvQZ4r1Mqs07sjyZZud2UTg4Y7fMHnJiRva4oOfkE6TjuAUUmTJaQXw66Gjo3b4SAQBa1wEfQysBGnIbnHUiTpMNyiYTLMINYrqohgHYn0QlPqN72PUMDUENspCUHAZthAxONwCyVPAZE5Uzkpec2TXIXJKzFqAJyORECgfO4qqbWIVeQxCA6vERzsLIY08P6GWKUto8qaRZ9COvrFVd0bTmJxp7Xr6nuCY4IbbLhScjW780wpNGcabYKgDoHgMTinozHZ9DVlEvJisqV2OLcuRHvNrTH7x1TtekS3Xl5dGxJOrNsq3zKoRwWCSQhdFlQT7GR8WD7boIJZAaX3ENWOMRlRAIxsk0kAtZZv9r9h7uSVCmhTYczfeJ872HmaYgMLC5OJ8l7s2HTDmVrVUzPOG9g4avPtwzrEeCu9ezBwWXuTvGFDImxlYUcsqcQlqpxmBdaWrY3zdtkaeib",
        "description": "0vEzEFk2BGtUcGKUFFXMVp7ESIsZmLw3Ii7VrfbfDsaUMYscnGS5DI9zqveiqBxvL59UQrCAf5KcyxB6k3gW779ckkFVd5v8Km4Fa4yXWMzmTlNbdlfFWF0CstjsaHFll8yNAsPwrd09V05cb1DpFL6QlKiPVuYG8vyd8QQqa06vdNiN2EP5hbwW3SDSDGhL1IrGrzGgShJNcFhgfoZaOdzlBFsr6VKZkl9hwMr668gAvQZ4r1Mqs07sjyZZud2UTg4Y7fMHnJiRva4oOfkE6TjuAUUmTJaQXw66Gjo3b4SAQBa1wEfQysBGnIbnHUiTpMNyiYTLMINYrqohgHYn0QlPqN72PUMDUENspCUHAZthAxONwCyVPAZE5Uzkpec2TXIXJKzFqAJyORECgfO4qqbWIVeQxCA6vERzsLIY08P6GWKUto8qaRZ9COvrFVd0bTmJxp7Xr6nuCY4IbbLhScjW780wpNGcabYKgDoHgMTinozHZ9DVlEvJisqV2OLcuRHvNrTH7x1TtekS3Xl5dGxJOrNsq3zKoRwWCSQhdFlQT7GR8WD7boIJZAaX3ENWOMRlRAIxsk0kAtZZv9r9h7uSVCmhTYczfeJ872HmaYgMLC5OJ8l7s2HTDmVrVUzPOG9g4avPtwzrEeCu9ezBwWXuTvGFDImxlYUcsqcQlqpxmBdaWrY3zdtkaeib",
    }
    data_unauthorized = {
        "name": "Hello",
        "description": "Hello",
    }

    response_OK = client.put(
        SAFE_AND_ITEM_PATH_V1+f"/{safe_id}",
        data=data_ok,
        headers=with_token_OK(token)
    )
    response_BAD_REQUEST = client.put(
        SAFE_AND_ITEM_PATH_V1+f"/{safe_id}",
        data=data_bad_request,
        headers=with_token_OK(token)
    )
    response_UNAUTHORIZED = client.put(
        SAFE_AND_ITEM_PATH_V1+f"/{safe_id}",
        data=data_unauthorized,
        headers=with_token_UNAUTHORIZED
    )
    return (response_OK,response_BAD_REQUEST,response_UNAUTHORIZED)

def create_item(token:str,safe_id:str):
    header_with_token_OK = {
        'User-Agent': 'python:3.10/windows',
        'Content-Type': 'application/json',
        'X-Real-IP': '127.0.0.1',
        'Authorization': 'Bearer '+token
    }

    header_with_token_UNAUTHORIZED = {
        'User-Agent': 'python:3.10/windows',
        'Content-Type': 'application/json',
        'X-Real-IP': '127.0.0.1',
        'Authorization': 'Bearer xqdwu8tPKvnFBPZiQzGanMZ2UM8b8ALJVikZ6iTNK0RdxehS4AUiYy9sgP7Ys7OULF6FsJekTB5XARFzOTolTgR8WTJqw85AhylCS3WxWA6Gr7D5zeHM7VmWT2KpbPzO'
    }

    data_ok = {
        "title":"Title",
        "category":"LOGIN",
        "notes":"There should be notes here",
        "tags":["the values in the tags must be of the string type","tag2"],
        "sections":[
            {
            "section":"INIT",
            "fields":[
                {
                "type":"STRING",
                "label":"login",
                "value":"user1"
                },
                {
                "type":"PASSWORD",
                "label":"password",
                "value":"12345"
                }
            ]
            },
            {
            "section":"Other sections",
            "fields":[
                {
                "type":"URL",
                "label":"title",
                "value":"https://example.com"
                },
                {
                "type":"EMAIL",
                "label":"email",
                "value":"user@example.com"
                }
            ]
            }
        ]
    }

    data_unprocessable_content = {
        "title":"Title",
        "category":"NOT_LOGIN",
        "notes":"There should be notes here",
        "tags":["the values in the tags must be of the string type","tag2"],
        "sections":[
            {
            "section":"INI",
            "fields":[
                {
                "type":"STRING",
                "label":"login",
                "value":"user1"
                },
                {
                "type":"PASSWORD",
                "label":"password",
                "value":"12345"
                }
            ]
            },
            {
            "section":"Other sections",
            "fields":[
                {
                "type":"URL",
                "label":"title",
                "value":"https://example.com"
                },
                {
                "type":"EMAIL",
                "label":"email",
                "value":"user@example.com"
                }
            ]
            }
        ]
    }

    response_OK = client.post(
        SAFE_AND_ITEM_PATH_V1+f"/{safe_id}/item",
        json=data_ok,
        headers=header_with_token_OK
    )
    response_UNPROCESSABLE_CONTENT = client.post(
        SAFE_AND_ITEM_PATH_V1+f"/{safe_id}/item",
        json=data_unprocessable_content,
        headers=header_with_token_OK
    )
    response_UNAUTHORIZED = client.post(
        SAFE_AND_ITEM_PATH_V1+f"/{safe_id}/item",
        json=data_ok,
        headers=header_with_token_UNAUTHORIZED
    )
    return (response_OK,response_UNPROCESSABLE_CONTENT,response_UNAUTHORIZED)

def encrypt_string(password:str,salt:str,text:str):
    private_key = PbkdF2HMAC().encrypt(
        password=password,
        salt=salt.encode('utf-8')
    )
    aes256 = AES_256()
    cipher:str = aes256.encrypt(private_key,text)
    return cipher

def decrypt_string(private_key:bytes,cipher_text:str):
    try:
        aes256 = AES_256()
        decrypt_text:str = aes256.decrypt(
            private_key=private_key,
            ciphertext=cipher_text
        )
        return decrypt_text
    except Exception as e:
        print(f"Error during decryption: {e}")
        return ""

def test_encrypt_decrypt_string():
    text = "Hello world"
    cipher:str = encrypt_string(
        password=PASSWORD1,
        salt=SALT1,
        text=text
    )

    private_key:bytes = PbkdF2HMAC().encrypt(
        password=PASSWORD1,
        salt=SALT1.encode('utf-8')
    )

    decrypt_text = decrypt_string(
        private_key=private_key,
        cipher_text=cipher
    )

    assert cipher!="",cipher
    assert private_key!=b"",private_key
    assert decrypt_text==text,decrypt_text

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

    NAME1 = "Safe 1"
    DESCRIPTION1 = "Description 1" 
    __create_safe = create_safe(
        token=token1,
        name=NAME1,
        description=encrypt_string(PASSWORD1,SALT1,DESCRIPTION1)
    )
    __create_safe_OK = __create_safe[0]
    __create_safe_BAD_REQUEST = __create_safe[1]
    __create_safe_UNAUTHORIZED = __create_safe[2]

    __get_safes_and_items = get_safes_and_items(token=token1)
    __get_safes_and_items_OK = __get_safes_and_items[0]
    cipher_description = __get_safes_and_items_OK.json()['safes'][0]['description']
    safe_id:str = __get_safes_and_items_OK.json()['safes'][0]['id']
    __get_safes_and_items_UNAUTHORIZED = __get_safes_and_items[1]

    UPDATED_NAME1 = "Updated "+NAME1
    UPDATED_DESCRIPTION1 = "Updated "+DESCRIPTION1
    __update_safe = update_safe(
        token=token1,
        safe_id=safe_id,
        name=UPDATED_NAME1,
        description=encrypt_string(PASSWORD1,SALT1,UPDATED_DESCRIPTION1)
    )

    private_key:bytes = PbkdF2HMAC().encrypt(
        password=PASSWORD1,
        salt=SALT1.encode('utf-8')
    )
    decrypt_description = decrypt_string(
        private_key=private_key,
        cipher_text=cipher_description
    )

    __update_safe_OK = __update_safe[0]
    __update_safe_BAD_REQUEST = __update_safe[1]
    __update_safe_UNAUTHORIZED = __update_safe[2]

    __create_item = create_item(
        token=token1,
        safe_id=safe_id
    )
    __create_item_OK = __create_item[0]
    __create_item_UNPROCESSABLE_CONTENT = __create_item[1]
    __create_item_UNAUTHORIZED = __create_item[2]

    assert __registration1_OK.status_code == OK
    assert ____registration1_BAD_REQUEST.status_code == BAD_REQUEST

    assert __log_in1_OK.status_code == OK
    assert __log_in1_BAD_REQUEST.status_code == BAD_REQUEST
    assert __log_in1_NOT_FOUND.status_code == NOT_FOUND

    assert __create_safe_OK.status_code == OK
    assert __create_safe_BAD_REQUEST.status_code == BAD_REQUEST
    assert __create_safe_UNAUTHORIZED.status_code == UNAUTHORIZED

    assert __get_safes_and_items_OK.status_code == OK
    assert __get_safes_and_items_UNAUTHORIZED.status_code == UNAUTHORIZED

    assert decrypt_description != '',decrypt_description
    assert decrypt_description == DESCRIPTION1,decrypt_description

    assert __update_safe_OK.status_code == OK
    assert __update_safe_BAD_REQUEST.status_code == BAD_REQUEST
    assert __update_safe_UNAUTHORIZED.status_code == UNAUTHORIZED

    assert __create_item_OK.status_code == OK,__create_item_OK
    assert __create_item_UNPROCESSABLE_CONTENT.status_code == UNPROCESSABLE_ENTITY
    assert __create_item_UNAUTHORIZED.status_code == UNAUTHORIZED