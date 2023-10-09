from mindfulguard.core.response_status_codes import *
from mindfulguard.core.security.totp import Totp
from mindfulguard.database.postgresql.authentication import Authentication

import pytest

@pytest.mark.asyncio
async def test_sign_up():
    auth = Authentication()
    totp = Totp("")
    result_OK:int = await auth.sign_up(
        login="8bm&bn34_-54b",
        secret_string="LpaX2UPdsPWAPeZTwTt22Wog2yTQ984xBgHNylbnNRrhw2A7eDrhmc1aJrKi74rP",
        reg_ip="127.0.0.1",
        secret_code=totp.generate_secret_code(),
        backup_codes=totp.generate_backup_codes(6)
    )

    result_INTERNAL_SERVER_ERROR:int = await auth.sign_up(
        login="8bm&bn34_-bn70893b4n0789b3452n70895b4327n8093b54n27890n3b749580n79035b42n78905b342n7980b3524n798053b42n7980532b4n798035b42n709835b42n790835bn247890n35b789042n7b9085432n709b8534n0978b3542n9078b35427n9803b54254b",
        secret_string="LpaX2UPdsPWAPeZTw5b345b345b435b345b435b34b5345b43333333333333v4234v234v234v234v324v234b234b234b23b433333333333333nnnnnn4655555555555555555555v3544444444444444$#B$#V@#@#V@B$#B#$BVVEFFSFSDTt22Wog2yTQ984xBgHNylbnNRrhw2A7eDrhmc1aJrKi74rP",
        reg_ip="1275.0.0.1",
        secret_code="12345",
        backup_codes=[53475897439859834759843895793845897349857893475893479587348957398454675792657856876578932657893658793465789346578934]
    )
    result_CONFLICT:int = result_OK

    assert result_OK == OK
    assert result_CONFLICT == CONFLICT
    assert result_INTERNAL_SERVER_ERROR == INTERNAL_SERVER_ERROR