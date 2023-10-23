import pytest
import mindfulguard.core.security as security
from mindfulguard.core.security.totp import NUMBER_OF_BACKUP_CODES, Totp

from mindfulguard.database.postgresql.authentication import Authentication
from mindfulguard.core.response_status_codes import *
from mindfulguard.database.postgresql.user.settings import Settings

LOGIN = "JFDfsKn34v3__--432"
SECRET_STRING = "KQFfkumq94czKXsG6XIRmXBzMNo8it8CiTUlAIDS0CmAMnNOQ9nA3Ag9KNovJa5u"
TOKEN = "xanBqvSaxHYDzEdbvLgq1kUgBHPts7tzPKhM7GE7FipiVMYrIztCUOColNvhCjs57gCy258j42eQ7CF2AhsV0KHEGdMfzeaul4E3GkOT4VJQUNLhfUj0TocVYCqXDRPU"

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

async def update_one_time_codes_():
    totp = Totp("")
    settings = Settings()
    result_OK_basic = await settings.update_one_time_codes(
        token=TOKEN,
        secret_string=SECRET_STRING,
        data = totp.generate_secret_code()
    )
    result_OK_backup = await settings.update_one_time_codes(
        token=TOKEN,
        secret_string=SECRET_STRING,
        data = totp.generate_backup_codes(NUMBER_OF_BACKUP_CODES)
    )
    result_UNAUTHORIZED = await settings.update_one_time_codes(
        token="2b7n024b7n30n3472b05897n809b5347n089b342",
        secret_string=SECRET_STRING,
        data = totp.generate_backup_codes(NUMBER_OF_BACKUP_CODES)
    )
    result_INTERNAL_SERVER_ERROR = await settings.update_one_time_codes(
        token=TOKEN,
        secret_string="8v35248m543v28-m34b2-8m03b54-8fsd",
        data = totp.generate_secret_code()
    )
    return (result_OK_basic,result_OK_backup,result_UNAUTHORIZED,result_INTERNAL_SERVER_ERROR)

NEW_SECRET_STRING = "579834758934"

async def update_secret_string():
    settings = Settings()
    result_OK = await settings.update_secret_string(
        token=TOKEN,
        old_secret_string = SECRET_STRING,
        new_secret_string = NEW_SECRET_STRING
    )
    result_UNAUTHORIZED = await settings.update_secret_string(
        token="73547085437805",
        old_secret_string = SECRET_STRING,
        new_secret_string = "534543"
    )
    result_INTERNAL_SERVER_ERROR = await settings.update_secret_string(
        token=TOKEN,
        old_secret_string = "5834954",
        new_secret_string = "534543645"
    )
    return (result_OK,result_UNAUTHORIZED,result_INTERNAL_SERVER_ERROR)

async def delete_user():
    settings = Settings()
    result_OK = await settings.delete_user(
        token=TOKEN,
        secret_string=NEW_SECRET_STRING,
        code_confirm=True
    )
    result_UNAUTHORIZED = await settings.delete_user(
        token="73547085437805",
        secret_string=NEW_SECRET_STRING,
        code_confirm=True
    )
    result_INTERNAL_SERVER_ERROR = await settings.delete_user(
        token=TOKEN,
        secret_string="12343",
        code_confirm=False
    )
    return (result_OK,result_UNAUTHORIZED,result_INTERNAL_SERVER_ERROR)

@pytest.mark.asyncio
async def test_user_settings():
    __sign_up = await sign_up()
    __sign_up_OK = __sign_up[0]
    __sign_up_INTERNAL_SERVER_ERROR = __sign_up[1]

    __sign_in = await sign_in()
    __sign_in_OK = __sign_in[0]
    __sign_in_NOT_FOUND = __sign_in[1]
    __sign_in_INTERNAL_SERVER_ERROR = __sign_in[2]

    __update_one_time_codes = await update_one_time_codes_()
    update_one_time_codes_OK_basic = __update_one_time_codes[0]
    update_one_time_codes_OK_backup = __update_one_time_codes[1]
    update_one_time_codes_UNAUTHORIZED = __update_one_time_codes[2]
    update_one_time_codes_INTERNAL_SERVER_ERROR = __update_one_time_codes[3]

    __update_secret_string = await update_secret_string()
    __update_secret_string_OK = __update_secret_string[0]
    __update_secret_string_UNAUTHORIZED = __update_secret_string[1]
    __update_secret_string_INTERNAL_SERVER_ERROR = __update_secret_string[2]

    __delete_user = await delete_user()
    __delete_user_OK = __delete_user[0]
    __delete_user_UNAUTHORIZED = __delete_user[1]
    __delete_user_INTERNAL_SERVER_ERROR = __delete_user[2]

    assert __sign_up_OK == OK
    assert __sign_up_OK == OK
    assert __sign_up_INTERNAL_SERVER_ERROR == INTERNAL_SERVER_ERROR

    assert __sign_in_OK == OK
    assert __sign_in_NOT_FOUND == NOT_FOUND
    assert __sign_in_INTERNAL_SERVER_ERROR == INTERNAL_SERVER_ERROR

    assert update_one_time_codes_OK_basic == OK
    assert update_one_time_codes_OK_backup == OK
    assert update_one_time_codes_UNAUTHORIZED == UNAUTHORIZED
    assert update_one_time_codes_INTERNAL_SERVER_ERROR == INTERNAL_SERVER_ERROR

    assert __update_secret_string_OK == OK
    assert __update_secret_string_UNAUTHORIZED == UNAUTHORIZED
    assert __update_secret_string_INTERNAL_SERVER_ERROR == INTERNAL_SERVER_ERROR

    assert __delete_user_OK == OK, __delete_user_OK
    #assert __delete_user_UNAUTHORIZED == UNAUTHORIZED
    #assert __delete_user_INTERNAL_SERVER_ERROR == INTERNAL_SERVER_ERROR