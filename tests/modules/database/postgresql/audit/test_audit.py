from http.client import BAD_REQUEST, CONFLICT, INTERNAL_SERVER_ERROR, NOT_FOUND, OK
import pytest

from tests.modules.database.postgresql.audit.classes.db_audit_get import DbTestsAuditGet
from tests.modules.database.postgresql.audit.classes.db_audit_insert import DbTestsAuditInsert
from tests.modules.database.postgresql.authentication.classes.db_authentication_sign_in import DbTestsAuthenticationSignIn
from tests.modules.database.postgresql.authentication.classes.db_authentication_sign_up import DbTestsAuthenticationSignUp
from tests.logger import logger

logger()

@pytest.mark.asyncio
async def test_audit():
    sign_up = DbTestsAuthenticationSignUp()

    assert await sign_up.bad_request(
        '#$V#@)($V*M)(#@)',
        '$V#)@(*M$V)(@#C$@#)',
        '#$VM@)#($V*@#)(C$)',
        [535,353,535,3,53,53,53,53]
    ) == BAD_REQUEST

    login: str = 'User363__--ff--'
    secret_string: str = 'bSHgVGUWhA5uwv8ycaWJpXi5yULDey5Cba5YdQuPFO7lQldrM1RZlzBA1rOphJTT'
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
    
    token = 'Bearer G8W28B90cFiHb0D8hAjKVmxnkVn9dUNXGco7Zj3SRL2xGHYHtiwPE0o7TGsoalh11n4Z6XcspLyz32j4aMH4icpAvAQFKmXKVDWD48PtKiazCHYi0Nkymn50KvnB2GIR'
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
    
    audit_insert = DbTestsAuditInsert()
    await audit_insert.execute(
        token,
        '127.0.0.1',
        audit_insert.model_audit.audit_object.user,
        audit_insert.model_audit.audit_action_type.create,
        'Pytest'
    )

    assert audit_insert.status_code == OK
    assert audit_insert.status_code == OK

    await audit_insert.execute(
        token,
        '127.0.0.1',
        'fvsiuynfiusyniv',
        'bfsverwvrewvrbwebewv',
        'Pytest'
    )

    assert audit_insert.status_code == INTERNAL_SERVER_ERROR

    audit_get = DbTestsAuditGet()
    await audit_get.execute(token)

    assert audit_get.status_code == OK