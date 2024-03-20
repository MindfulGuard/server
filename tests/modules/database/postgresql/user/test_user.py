from http.client import BAD_REQUEST, CONFLICT, INTERNAL_SERVER_ERROR, NOT_FOUND, OK, UNAUTHORIZED
import pytest
from tests.modules.database.postgresql.authentication.classes.db_authentication_sign_in import DbTestsAuthenticationSignIn
from tests.modules.database.postgresql.authentication.classes.db_authentication_sign_up import DbTestsAuthenticationSignUp

from tests.modules.database.postgresql.user.classes.get_information import DbTestUserInformationGet
from tests.modules.database.postgresql.user.classes.get_tokens import DbTestUserGetTokens
from tests.modules.database.postgresql.user.classes.settings import DbTestUserSettingsDeleteAccount, DbTestUserSettingsUpdateOneTimeCode, DbTestUserSettingsUpdateSecretString


@pytest.mark.asyncio
async def test_user():
    sign_up = DbTestsAuthenticationSignUp()

    assert await sign_up.bad_request(
        '#$V#@)($V*M)(#@)',
        '$V#)@(*M$V)(@#C$@#)',
        '#$VM@)#($V*@#)(C$)',
        [535,353,535,3,53,53,53,53]
    ) == BAD_REQUEST

    login: str = 'User5_s_--ff--'
    secret_string: str = 'sSHhhGUWhA5uwv8ycaWDpXiryULDeQ5Cba5YdQuPFO7lOldrM1RZlzwA1rOphJqq'
    secret_code: str = 'KE26VBNRYVHOAUD7YQK5QZ2ONMTL2HKX'
    backup_codes: list[int] = [425234, 424523, 536345, 674522, 321333, 243244]

    assert await sign_up.bad_request(
        '#$V#@)($V*M)(#@)',
        '$V#)@(*M$V)(@#C$@#)',
        '#$VM@)#($V*@#)(C$)',
        [535,353,535,3,53,53,53,53]
    ) == BAD_REQUEST

    assert await sign_up.ok(
        login,
        secret_string,
        secret_code,
        backup_codes
    ) == OK

    assert await sign_up.ok(
        login,
        secret_string,
        secret_code,
        backup_codes
    ) == OK

    sign_in = DbTestsAuthenticationSignIn()
    assert await sign_in.bad_request(
        '#$V#@)($V*M)(#@)',
        '$V#)@(*M$V)(@#C$@#)',
        '#$VM@)#($V*@#)(C$)',
        False
    ) == BAD_REQUEST
    
    token = 'Bearer PxZR0U4qWjDFXeGWQFPWmnzFLJksWlWd1bg6VExfWIMynj6QaHwnZO654JqDoFyWvAoxXfYFvm15mDf9M7PtrgQIWH3LJDnIkMgXQ2fwyhhkWrrw5E3s1JdnzSCdJN9U'
    assert await sign_in.ok(
        login,
        secret_string,
        token,
        True
    ) == OK

    assert await sign_in.ok(
        login,
        secret_string,
        token,
        False
    ) == NOT_FOUND

    assert await sign_up.ok(
        login,
        secret_string,
        secret_code,
        backup_codes
    ) == CONFLICT

    get_user_info = DbTestUserInformationGet()
    assert await get_user_info.execute(
        'Bearer Dn8QQDRNpWo3PAbk3GtsDXntoq6AK10uyn2JgTYNJ1unHBF67ZZ4ROsyp5ke4tlph9UnWSV6v0dfowahxiEgjj8BEhLRhUC2utZKLbgjEcXceH9AXnrcWe296ME3t8oD'
    ) == UNAUTHORIZED
    assert await get_user_info.execute(
        token
    ) == OK

    get_tokens = DbTestUserGetTokens()
    assert await get_tokens.execute(
        'Bearer Dn8QQDRNpWo3PAbk3GtsDXntoq6AK10uyn2JgTYNJ1unHBF67ZZ4ROsyp5ke4tlph9UnWSV6v0dfowahxiEgjj8BEhLRhUC2utZKLbgjEcXceH9AXnrcWe296ME3t8oD'
    ) == UNAUTHORIZED
    assert await get_tokens.execute(
        token
    ) == OK
    
    update_one_time_code = DbTestUserSettingsUpdateOneTimeCode()
    assert await update_one_time_code.execute(
        'Bearer Dn8QQDRNpWo3PAbk3GtsDXntoq6AK10uyn2JgTYNJ1unHBF67ZZ4ROsyp5ke4tlph9UnWSV6v0dfowahxiEgjj8BEhLRhUC2utZKLbgjEcXceH9AXnrcWe296ME3t8oD',
        sign_in.token_hashed,
        'FE16YYNRYVHOAUD7YQK5QZ2ONMTL2HKH',
    ) == UNAUTHORIZED
    assert await update_one_time_code.execute(
        token,
        'r0lXK4ymjrVajWghAyDrvOdIJGUIZeQKGZLSoD4yfj2O7lUOjQ3qVXA9EhDzoaAK',
        'FE16YYNRYVHOAUD7YQK5QZ2ONMTL2HKH',
    ) == INTERNAL_SERVER_ERROR
    assert await update_one_time_code.execute(
        token,
        secret_string,
        'FE16YYNRYVHOAUD7YQK5QZ2ONMTL2HKH',
    ) == OK

    update_secret_string = DbTestUserSettingsUpdateSecretString()
    new_secret_string = 'FsfgLNXqn6jZ48zbYf30ntfbjeHE5jQmxw2G5AeZ40wVc6EsWV85Q3fyQEoZlioQ'
    assert await update_secret_string.execute(
        'Bearer Dn8QQDRNpWo3PAbk3GtsDXntoq6AK10uyn2JgTYNJ1unHBF67ZZ4ROsyp5ke4tlph9UnWSV6v0dfowahxiEgjj8BEhLRhUC2utZKLbgjEcXceH9AXnrcWe296ME3t8oD',
        secret_string,
        new_secret_string
    ) == UNAUTHORIZED
    assert await update_secret_string.execute(
        token,
        secret_string,
        new_secret_string
    ) == OK

    delete_account = DbTestUserSettingsDeleteAccount()
    assert await delete_account.execute(
        'Bearer Dn8QQDRNpWo3PAbk3GtsDXntoq6AK10uyn2JgTYNJ1unHBF67ZZ4ROsyp5ke4tlph9UnWSV6v0dfowahxiEgjj8BEhLRhUC2utZKLbgjEcXceH9AXnrcWe296ME3t8oD',
        new_secret_string
    ) == UNAUTHORIZED

    assert await sign_in.ok(
        login,
        new_secret_string,
        token,
        True
    ) == OK

    assert await delete_account.execute(
        token,
        'IIm8jyVPcU8EsMPT4Ma33HW12LgOws5mwJTgmgr9Zj2hXIDRfX6KqfjbM1jUkgqD'
    ) == INTERNAL_SERVER_ERROR
    assert await delete_account.execute(
        token,
        new_secret_string
    ) == OK