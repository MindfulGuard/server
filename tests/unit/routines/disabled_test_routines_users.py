import time
import pytest

import mindfulguard.core.security as security
from mindfulguard.core.security.totp import Totp
from mindfulguard.database.postgresql.authentication import Authentication
from mindfulguard.core.response_status_codes import *
from mindfulguard.database.postgresql.connection import Connection

LOGIN = "34v432v423843__-432"
SECRET_STRING = "v543v435vbcvmbq53454354356XIRmXBzMNo8it8CiTUlAIDS0CmAM53vvvnA3Ag9KNovJa5u"
TOKEN = "6LtUgYnU9iD8XlfbW26uISgstSIRsj6k1GYVVGmDUkjzoTPemjTOFdO6PhIdKOYXTZRL12Mf6iRm9TlysfwuJzwqv8SauW1jN3TxFOSsWLDpsttITPpneaLtwm4ckfM5"

async def sign_up():
    auth = Authentication()
    totp = Totp("")
    result_OK:int = await auth.sign_up(
        login=LOGIN,
        secret_string=SECRET_STRING,
        reg_ip="127.0.0.1",
        confirm=False,
        secret_code=totp.generate_secret_code(),
        backup_codes=[53464,75686,423436,765767,98788,234513]
    )

    result_INTERNAL_SERVER_ERROR:int = await auth.sign_up(
        login="8bm&bn34_-bn70893b4n0789b3452n70895b4327n8093b54n27890n3b749580n79035b42n78905b342n7980b3524n798053b42n7980532b4n798035b42n709835b42n790835bn247890n35b789042n7b9085432n709b8534n0978b3542n9078b35427n9803b54254b",
        secret_string="LpaX2UPdsPWAPeZTw5b345b345b435b345b435b34b5345b43333333333333v4234v234v234v234v324v234b234b234b23b433333333333333nnnnnn4655555555555555555555v3544444444444444$#B$#V@#@#V@B$#B#$BVVEFFSFSDTt22Wog2yTQ984xBgHNylbnNRrhw2A7eDrhmc1aJrKi74rP",
        reg_ip="1275.0.0.1",
        confirm=False,
        secret_code="12345",
        backup_codes=[53475897439859834759843895793845897349857893475893479587348957398454675792657856876578932657893658793465789346578934]
    )

    return (result_OK,result_INTERNAL_SERVER_ERROR)

async def sign_in():
    auth = Authentication()

    result_OK = await auth.sign_in(
        login=LOGIN,
        secret_string=SECRET_STRING,
        token=TOKEN,
        device="None",
        ip="127.0.0.1",
        expiration=50,
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

async def change_confirmation_period_settings():
    connection = None
    try:
        connection = await Connection().connect()
        await connection.fetchval('''
        UPDATE st_settings
        SET st_value = 40
        WHERE st_id = '24775562-22d7-4f71-873b-2503ff1135fd';
        ''')
        return 0
    except Exception as e:
        print(e)
    finally:
        if connection:
            await connection.close()

@pytest.mark.asyncio
async def test_routines_users():
    __sign_up = await sign_up()
    __sign_up_OK = __sign_up[0]
    __sign_up_INTERNAL_SERVER_ERROR = __sign_up[1]

    assert await change_confirmation_period_settings() == 0

    assert __sign_up_OK == OK
    assert __sign_up_OK == OK
    assert __sign_up_INTERNAL_SERVER_ERROR == INTERNAL_SERVER_ERROR

    time.sleep(110)


    __sign_in = await sign_in()
    __sign_in_OK = __sign_in[0]
    assert __sign_in_OK == NOT_FOUND