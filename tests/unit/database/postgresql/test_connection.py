from mindfulguard.core.response_status_codes import OK
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
    assert result_OK == OK