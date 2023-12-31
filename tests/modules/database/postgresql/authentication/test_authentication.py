from http.client import BAD_REQUEST, CONFLICT, NOT_FOUND, OK
import pytest
from tests.modules.database.postgresql.authentication.classes.db_authentication_sign_in import DbTestsAuthenticationSignIn
from tests.modules.database.postgresql.authentication.classes.db_authentication_sign_out import DbTestsAuthenticationSignOut
from tests.modules.database.postgresql.authentication.classes.db_authentication_sign_up import DbTestsAuthenticationSignUp
from tests.modules.database.postgresql.authentication.classes.db_user_info import DbTestUserInfo



@pytest.mark.asyncio
async def test_authentication():
    sign_up = DbTestsAuthenticationSignUp()

    assert await sign_up.bad_request(
        '#$V#@)($V*M)(#@)',
        '$V#)@(*M$V)(@#C$@#)',
        '#$VM@)#($V*@#)(C$)',
        [535,353,535,3,53,53,53,53]
    ) == BAD_REQUEST

    login: str = 'User1__----'
    secret_string: str = 'mSHlVGUWBA5uwv8ycjWDpXi5yULDeQ5Cba5YdQuPFO7lOldrM1RZlzwA1rOphJqq'
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
    
    token = 'Bearer tOwatNxMYgXQZShhM8YRVozV8PX5kD8LzqBpc2XhQC5De9RjJmrskRRf9N5OU2GLWbfKeifqLWKKLmYyVuwocQGx1RHlqMcCWqAZKDHQO1td56XtIDEHJ5txxk3X7vlm'
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

    user_info = DbTestUserInfo()
    iter  = await user_info.get(token)
    token_id = iter.__next__().id

    sign_out = DbTestsAuthenticationSignOut()
    
    assert await sign_out.bad_request(
        token,
        '403829480392v8v04m923'
    ) == BAD_REQUEST

    assert await sign_out.bad_request(
        token,
        'fa1f3289-4559-443a-b819-ca53f71fa268'
    ) == NOT_FOUND

    assert await sign_out.bad_request(
        token,
        token_id
    ) == OK