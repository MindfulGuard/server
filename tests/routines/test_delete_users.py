from http.client import NOT_FOUND, OK
import time
import pytest
from mindfulguard.classes.database import DataBase
from tests.modules.database.postgresql.authentication.classes.db_authentication_sign_in import DbTestsAuthenticationSignIn
from tests.modules.database.postgresql.authentication.classes.db_authentication_sign_up import DbTestsAuthenticationSignUp


async def change_confirmation_period_settings(time: str):
    connection = DataBase().postgresql().connection()
    try:
        await connection.open()
        await connection.connection.fetchval('''
        UPDATE st_settings
        SET st_value = $1
        WHERE st_id = '24775562-22d7-4f71-873b-2503ff1135fd';
        ''',
        time
        )
        return True
    finally:
        if connection:
            await connection.close()

@pytest.mark.asyncio
async def test_routines_delete_users():
    assert await change_confirmation_period_settings('20')

    sign_up = DbTestsAuthenticationSignUp()

    login: str = 'User6_sftgv_--ff--'
    secret_string: str = 'ssHhtvUWhg5unv8ycaWDpXiryULDeQ5Cba5YdQuPFO7lOldrM1RZlzwA1rOphJqh'
    secret_code: str = 'KE26VBNRYVHOAUD7YQK5QZ2ONMTL2HKX'
    backup_codes: list[int] = [425234, 424523, 536345, 674522, 321333, 243244]

    assert await sign_up.ok(
        login,
        secret_string,
        secret_code,
        backup_codes,
        confirm=False
    ) == OK

    time.sleep(120)

    sign_in = DbTestsAuthenticationSignIn()
    
    token = 'Bearer KzBY2qoURydaqn8C4WXfDZEFN0mIoTERtnBFlZB6oq4jnukSPqCQPj0zugORZvxLhImS7vikKNdXMwAkG9vMNid5MlImkGCN6mL0Xp2DG1LxHm2eyfa4YqtJMWw3lCK3'
    assert await sign_in.ok(
        login,
        secret_string,
        token,
        True
    ) == NOT_FOUND
    assert await change_confirmation_period_settings('604800')