from http.client import OK, UNAUTHORIZED
import time
import pytest
from tests.modules.database.postgresql.authentication.classes.db_authentication_sign_in import DbTestsAuthenticationSignIn
from tests.modules.database.postgresql.authentication.classes.db_authentication_sign_up import DbTestsAuthenticationSignUp
from tests.modules.database.postgresql.safe.classes.create import DbTestCreateSafe


@pytest.mark.asyncio
async def test_routines_delete_token():
    sign_up = DbTestsAuthenticationSignUp()

    login: str = 'User7v_sv_--ff--'
    secret_string: str = 'qsHhtvhghA5unvjycaWDdXiryULDeQ5Cba5YdQuPFO7lOldrM1RZlzwA1rOphJqq'
    secret_code: str = 'KE26VBNRYVHOAUD7YQK5QZ2ONMTL2HKX'
    backup_codes: list[int] = [425234, 424523, 536345, 674522, 321333, 243244]

    assert await sign_up.ok(
        login,
        secret_string,
        secret_code,
        backup_codes
    ) == OK

    sign_in = DbTestsAuthenticationSignIn()
    token = 'Bearer EbEUm0VlRJjjVK6WsHVQBvZn0XruZtNsIWLnNNTVCEvRs7ndMWX9Ml6MjrWGsYeQRJdOK4e5yYaa7YXVdXNXDwdEZibImDb5pBEdPVlCVgS9J8o9oupnUyZddGz2Kx9S'
    assert await sign_in.ok(
        login,
        secret_string,
        token,
        True,
        expiration=1
    ) == OK

    time.sleep(90)

    create_safe = DbTestCreateSafe()

    assert await create_safe.execute(
        token,
        'Safe 1',
        'Description 1'
    ) == UNAUTHORIZED