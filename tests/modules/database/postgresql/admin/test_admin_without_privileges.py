from http.client import FORBIDDEN, OK, UNAUTHORIZED
import pytest
from tests.modules.database.postgresql.admin.classes.get_by_page import DbTestAdminGetByPage
from tests.modules.database.postgresql.admin.classes.search_users import DbTestAdminSearchUsers
from tests.modules.database.postgresql.authentication.classes.db_authentication_sign_in import DbTestsAuthenticationSignIn
from tests.modules.database.postgresql.authentication.classes.db_authentication_sign_up import DbTestsAuthenticationSignUp
from tests.logger import logger

logger()

@pytest.mark.asyncio
async def test_admin_without_privileges():
    sign_up = DbTestsAuthenticationSignUp()

    login: str = 'User8_sbb_--ff--'
    secret_string: str = 'sSshhGUWhAguwv8hcaWDpXirsfdseQ5Cba5YdQuPFO7lOldrM1RZlzwA1rOphJqb'
    secret_code: str = 'KE26VBNRYVHOAUD7YQK5QZ2ONMTL2HKX'
    backup_codes: list[int] = [425234, 424523, 536345, 674522, 321333, 243244]

    assert await sign_up.ok(
        login,
        secret_string,
        secret_code,
        backup_codes
    ) == OK

    sign_in = DbTestsAuthenticationSignIn()
    
    token = 'Bearer bJKkQwx3Dr6a1RGmM7ygsUtdyKoMm42tkMIa1H2LUAyhHIcqLY4Kwwp2MYgXBLoK9W0uBHpkGflaLdWMUt5d9Nr73lAG7LXM3N2JIl69ovKidTNjy48S21YtzwBC8ken'
    assert await sign_in.ok(
        login,
        secret_string,
        token,
        True
    ) == OK

    get_by_page = DbTestAdminGetByPage()
    assert await get_by_page.execute(
        'Bearer Dn8QQDRNpWo3PAbk3GtsDXntoq6AK10uyn2JgTYNJ1unHBF67ZZ4ROsyp5ke4tlph9UnWSV6v0dfowahxiEgjj8BEhLRhUC2utZKLbgjEcXceH9AXnrcWe296ME3t8oD'
    ) == UNAUTHORIZED
    assert await get_by_page.execute(
        token
    ) == FORBIDDEN

    search_user = DbTestAdminSearchUsers()
    assert await search_user.execute(
        'Bearer Dn8QQDRNpWo3PAbk3GtsDXntoq6AK10uyn2JgTYNJ1unHBF67ZZ4ROsyp5ke4tlph9UnWSV6v0dfowahxiEgjj8BEhLRhUC2utZKLbgjEcXceH9AXnrcWe296ME3t8oD',
        '1c9035de-eccd-48d7-8dbc-489a4e636115'
    ) == UNAUTHORIZED
    assert await search_user.execute(
        token,
        '1c9035de-eccd-48d7-8dbc-489a4e636115'
    ) == FORBIDDEN