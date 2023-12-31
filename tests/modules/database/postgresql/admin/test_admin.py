from http.client import FORBIDDEN, NOT_FOUND, OK, UNAUTHORIZED
import pytest
from mindfulguard.classes.database import DataBase
from tests.modules.database.postgresql.admin.classes.get_by_page import DbTestAdminGetByPage
from tests.modules.database.postgresql.admin.classes.search_users import DbTestAdminSearchUsers
from tests.modules.database.postgresql.admin.classes.update_configuration import DbTestAdminUpdateConfig
from tests.modules.database.postgresql.authentication.classes.db_authentication_sign_in import DbTestsAuthenticationSignIn
from tests.modules.database.postgresql.authentication.classes.db_authentication_sign_up import DbTestsAuthenticationSignUp

async def change_confirmation_period_settings(login: str, is_admin: bool):
    connection = DataBase().postgresql().connection()
    try:
        await connection.open()
        await connection.connection.fetchval('''
        UPDATE u_users
        SET u_admin = $1
        WHERE u_login = $2;
        ''',
        is_admin,
        login
        )
        return True
    finally:
        if connection:
            await connection.close()

@pytest.mark.asyncio
async def test_admin():
    sign_up = DbTestsAuthenticationSignUp()

    login: str = 'User9_sgbb_--ff--'
    secret_string: str = 'sgshhGUhdAguwv8hcaWddXirsfdsgQ5Cha5YdQuPFO7lOldrM1RZlzwA1rOphJqb'
    secret_code: str = 'KE26VBNRYVHOAUD7YQK5QZ2ONMTL2HKX'
    backup_codes: list[int] = [425234, 424523, 536345, 674522, 321333, 243244]

    assert await sign_up.ok(
        login,
        secret_string,
        secret_code,
        backup_codes
    ) == OK

    sign_in = DbTestsAuthenticationSignIn()
    
    token = 'Bearer Ry6KIA8i2qC7gXIBVsM7w7SNuszx7UiZI7l3csACmJI9BWsl4bNmvgQXvsCrn1E6z82ZDwxdyLg3TXW5A916n5ZKLVWk1p7FOllKXOzufR1em1I1db5zN53TrvioJXki'
    assert await sign_in.ok(
        login,
        secret_string,
        token,
        True
    ) == OK
    assert await change_confirmation_period_settings(login, True) == True

    get_by_page = DbTestAdminGetByPage()
    assert await get_by_page.execute(
        token
    ) == OK

    search_user = DbTestAdminSearchUsers()
    assert await search_user.execute(
        token,
        '1c9035de-eccd-48d7-8dbc-489a4e636115'
    ) == NOT_FOUND

    udpate_config = DbTestAdminUpdateConfig()
    assert await udpate_config.execute(
        token,
        'registration',
        'true'
    ) == OK