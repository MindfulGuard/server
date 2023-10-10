from mindfulguard.core.response_status_codes import *
from mindfulguard.core.security.totp import Totp
from mindfulguard.database.postgresql.authentication import Authentication
import mindfulguard.core.security as security

import pytest

async def sign_up():
    auth = Authentication()
    totp = Totp("")
    result_OK:int = await auth.sign_up(
        login="8bm&bn34_-54b",
        secret_string="LpaX2UPdsPWAPeZTwTt22Wog2yTQ984xBgHNylbnNRrhw2A7eDrhmc1aJrKi74rP",
        reg_ip="127.0.0.1",
        secret_code=totp.generate_secret_code(),
        backup_codes=[53464,75686,423436,765767,98788,234513]
    )

    result_INTERNAL_SERVER_ERROR:int = await auth.sign_up(
        login="8bm&bn34_-bn70893b4n0789b3452n70895b4327n8093b54n27890n3b749580n79035b42n78905b342n7980b3524n798053b42n7980532b4n798035b42n709835b42n790835bn247890n35b789042n7b9085432n709b8534n0978b3542n9078b35427n9803b54254b",
        secret_string="LpaX2UPdsPWAPeZTw5b345b345b435b345b435b34b5345b43333333333333v4234v234v234v234v324v234b234b234b23b433333333333333nnnnnn4655555555555555555555v3544444444444444$#B$#V@#@#V@B$#B#$BVVEFFSFSDTt22Wog2yTQ984xBgHNylbnNRrhw2A7eDrhmc1aJrKi74rP",
        reg_ip="1275.0.0.1",
        secret_code="12345",
        backup_codes=[53475897439859834759843895793845897349857893475893479587348957398454675792657856876578932657893658793465789346578934]
    )

    return (result_OK,result_INTERNAL_SERVER_ERROR)

async def sign_in():
    auth = Authentication()

    result_OK = await auth.sign_in(
        login="8bm&bn34_-54b",
        secret_string="LpaX2UPdsPWAPeZTwTt22Wog2yTQ984xBgHNylbnNRrhw2A7eDrhmc1aJrKi74rP",
        token="cknBVpiJ1VFSUTBhhfEsQSq8ehAZkqfQKImprXQQ2KhEhMbgRMLSWb5piJJZBYJm",
        device="None",
        ip="127.0.0.1",
        expiration=60,
        is_verified_code=True
    )
        
    result_NOT_FOUND = await auth.sign_in(
        login="8bm&bng34_-54b",
        secret_string="LpaX2UPddsPWAPeZTwTt22Wog2yTQ984xBgHNylbnNRrhw2A7eDrhmc1aJrKi74rP",
        token=security.generate_512_bit_token_string(),
        device="None",
        ip="127.0.0.1",
        expiration=60,
        is_verified_code=True
    )

    result_INTERNAL_SERVER_ERROR = await auth.sign_in(
        login="8bm&bn70893b4n0789b3452n70895b4327n8093b54n27890n3b749580n79035b42n78905b342n7980b3524n798053b42n7980532b4n798035b42n709835b42n790835bn247890n35b789042n7b9085432n709b8534n0978b3542n9078b35427n9803b54254b-54b",
        secret_string="LpaX2UPdsPWAPeZTw5b345b345b435b345b435b34b5345b43333333333333v4234v234v234v234v324v234b234b234b23b433333333333333nnnnnn4655555555555555555555v3544444444444444LpaX2UPdsPWAPeZTwTt22Wog2yTQ984xBgHNylbnNRrhw2A7eDrhmc1aJrKi74rP",
        token="LpaX2UPdsPWAPeZTw5b345b345b435b345b435b34b5345b43333333333333v4234v234v234v234v324v234b234b234b23b433333333333333nnnnnn4655555555555555555555v3544444444444444LpaX2UPdsPWAPeZTw5b345b345b435b345b435b34b5345b43333333333333v4234v234v234v234v324v234b234b234b23b433333333333333nnnnnn4655555555555555555555v3544444444444444",
        device="None",
        ip="127.0.0.15",
        expiration=6064565464756756765765756645645645645654,
        is_verified_code=True
    )
    return (result_OK,result_NOT_FOUND,result_INTERNAL_SERVER_ERROR)

async def update_token_info():
    auth = Authentication()
    result_OK:int = await auth.update_token_info(
        token="cknBVpiJ1VFSUTBhhfEsQSq8ehAZkqfQKImprXQQ2KhEhMbgRMLSWb5piJJZBYJm",
        device="None",
        ip = "127.0.0.1"
    )
    result_UNAUTHORIZED:int = await auth.update_token_info(
        token="cknBVpiJ1VFSUTBfdfEsQSq8ehAZkqfQKImprXQQ2KhEhMbgRMLSWb5piJJZBYJm",
        device="None",
        ip = "127.0.0.1"
    )

    return (result_OK,result_UNAUTHORIZED)

async def get_secret_code():
    auth = Authentication()
    result_OK = await auth.get_secret_code(
        login = "8bm&bn34_-54b",
        secret_string= "LpaX2UPdsPWAPeZTwTt22Wog2yTQ984xBgHNylbnNRrhw2A7eDrhmc1aJrKi74rP"
    )
    result_UNAUTHORIZED = await auth.get_secret_code(
        login = "8b5m&bng34_-54b",
        secret_string= "jpag2UPddsPWAPeZTwTt22Wog2yTQ984xBgHNylbnNRrhw2A7eDrhmc1aJrKi74rP"
    )

    return (result_OK,result_UNAUTHORIZED)

async def update_reserve_codes(new_backup_codes:list[int]):
    auth = Authentication()
    result_OK:int = await auth.update_reserve_codes(
        login="8bm&bn34_-54b",
        secret_string="LpaX2UPdsPWAPeZTwTt22Wog2yTQ984xBgHNylbnNRrhw2A7eDrhmc1aJrKi74rP",
        reserve_codes=new_backup_codes
    )

    result_NOT_FOUND:int = await auth.update_reserve_codes(
        login="fbh&bngh4_-5gfdb",
        secret_string="jpaX2UPddsPWAPeZTwTt22Wog2yTQ984xBgHNylbnNRrhw2A7eDrhmc1aJrKi74rP",
        reserve_codes=new_backup_codes
    )
    return (result_OK,result_NOT_FOUND)

async def get_tokens():
    auth = Authentication()
    result_OK = await auth.get_tokens(
        token="cknBVpiJ1VFSUTBhhfEsQSq8ehAZkqfQKImprXQQ2KhEhMbgRMLSWb5piJJZBYJm"
    )
    result_UNAUTHORIZED = await auth.get_tokens(
        token="cknBVpiJ1VFjfTBhhfEsnSq8ehAckqfQKImprXQQ2KhEhMbgRMLSWb5piJJZBYJm"
    )
    return (result_OK,result_UNAUTHORIZED)

async def sign_out(token_id:str):
    auth = Authentication()
    result_OK = await auth.sign_out(
        token="cknBVpiJ1VFSUTBhhfEsQSq8ehAZkqfQKImprXQQ2KhEhMbgRMLSWb5piJJZBYJm",
        token_id = token_id
    )

    result_NOT_FOUND = await auth.sign_out(
        token="cknBVpiJ1VFSUTBhhfEsQSq8ehAZkqfQKImprXQQ2KhEhMbgRMLSWb5piJJZBYJm",
        token_id = "8be9ff5d-20dc-4479-b215-b6ebf316ecdf"
    )

    return (result_OK,result_NOT_FOUND)

@pytest.mark.asyncio
async def test_authentication():
    __sign_up = await sign_up()
    __sign_up_OK = __sign_up[0]
    __sign_up_INTERNAL_SERVER_ERROR = __sign_up[1]

    __sign_in = await sign_in()
    __sign_in_OK = __sign_in[0]
    __sign_in_NOT_FOUND = __sign_in[1]
    __sign_in_INTERNAL_SERVER_ERROR = __sign_in[2]

    __update_token_info = await update_token_info()
    __update_token_info_OK = __update_token_info[0]
    __update_token_info_UNAUTHORIZED = __update_token_info[1]

    __get_secret_code = await get_secret_code()
    __get_secret_code_OK = __get_secret_code[0]
    __get_secret_code_UNAUTHORIZED = __get_secret_code[1]
    

    
    assert __sign_up_OK == OK
    assert __sign_up_OK == OK
    assert __sign_up_INTERNAL_SERVER_ERROR == INTERNAL_SERVER_ERROR

    assert __sign_in_OK == OK
    assert __sign_in_NOT_FOUND == NOT_FOUND
    assert __sign_in_INTERNAL_SERVER_ERROR == INTERNAL_SERVER_ERROR
    
    assert __update_token_info_OK == OK
    assert __update_token_info_UNAUTHORIZED == UNAUTHORIZED

    assert __get_secret_code_OK[1] == OK
    assert __get_secret_code_UNAUTHORIZED[1] == UNAUTHORIZED

    backup_codes:list[int] = __get_secret_code_OK[0][0]['backup_codes']

    assert 53464 in backup_codes 
    assert 434768 not in backup_codes
    
    if 53464 in backup_codes:
        backup_codes.remove(53464)

    __update_reserve_codes = await update_reserve_codes(backup_codes)
    __update_reserve_codes_OK = __update_reserve_codes[0]
    __update_reserve_codes_NOT_FOUND = __update_reserve_codes[1]

    assert __update_reserve_codes_OK == OK
    assert __update_reserve_codes_NOT_FOUND == NOT_FOUND

    __get_tokens = await get_tokens()
    __get_tokens_OK = __get_tokens[0]
    __get_tokens_UNAUTHORIZED = __get_tokens[1]

    __sign_out = await sign_out(
        token_id=__get_tokens_OK[0][0]['id']
    )

    assert __get_tokens_OK[1] == OK
    assert __get_tokens_UNAUTHORIZED[1] == UNAUTHORIZED

    __sign_out_OK:int = __sign_out[0]

    assert __sign_out_OK == OK