from http.client import BAD_REQUEST, CONFLICT, NOT_FOUND, OK, UNAUTHORIZED
import pytest
from tests.modules.database.postgresql.authentication.classes.db_authentication_sign_in import DbTestsAuthenticationSignIn

from tests.modules.database.postgresql.authentication.classes.db_authentication_sign_up import DbTestsAuthenticationSignUp
from tests.modules.database.postgresql.safe.classes.create import DbTestCreateSafe
from tests.modules.database.postgresql.safe.classes.delete import DbTestDeleteSafe
from tests.modules.database.postgresql.safe.classes.get import DbTestGetSafe
from tests.modules.database.postgresql.safe.classes.update import DbTestUpdateSafe
from tests.logger import logger

logger()

@pytest.mark.asyncio
async def test_safe():
    sign_up = DbTestsAuthenticationSignUp()

    assert await sign_up.bad_request(
        '#$V#@)($V*M)(#@)',
        '$V#)@(*M$V)(@#C$@#)',
        '#$VM@)#($V*@#)(C$)',
        [535,353,535,3,53,53,53,53]
    ) == BAD_REQUEST

    login: str = 'User3__--ff--'
    secret_string: str = 'mSHgVGUWhA5uwv8ycaWDpXi5yULDeQ5Cba5YdQuPFO7lOldrM1RZlzwA1rOphJqq'
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

    create_safe = DbTestCreateSafe()
    assert await create_safe.execute(
        'Bearer Dn8QQDRNpWo3PAbk3GtsDXntoq6AK10uyn2JgTYNJ1unHBF67ZZ4ROsyp5ke4tlph9UnWSV6v0dfowahxiEgjj8BEhLRhUC2utZKLbgjEcXceH9AXnrcWe296ME3t8oD',
        'Safe',
        'Desc'
    ) == UNAUTHORIZED

    assert await create_safe.execute(
        token,
        'Vc1mBADya3yHjMkKPKf0CGBLqQk8ZkTdPuOhujAJt9XHB1j0tFAfdTwG8FHrkQ9A9qFIhwCNU3YoKjavd0FPk8dSjaPmX0T0kwIH7979jotSrGj38qBXaB0TIMfRdbp4',
        'Desc mew'
    ) == BAD_REQUEST

    assert await create_safe.execute(
        token,
        'Safe 1',
        'Description 1'
    ) == OK

    get_safes = DbTestGetSafe()
    assert await get_safes.execute(
        'Bearer v2v432v4'
    ) == BAD_REQUEST
    assert await get_safes.execute(
        'Bearer SuOv40zYakOmWQl1sK8r1brPMdT97nMLcbCPpAdhoMHgx6ZKMlqu1VpgsIVH51c9pKHFgnCjVYOrmZ7iEt1hRnZixohhT7ZuXFCygMtm3NmANHFDH4pDui8hqal5SkQO'
    ) == UNAUTHORIZED
    assert await get_safes.execute(
        token
    ) == OK
    safe_id = get_safes.response.__next__().id
    
    update_safe = DbTestUpdateSafe()
    assert await update_safe.execute(
        'Bearer v2v432v4',
        '4v23432c4234v32',
        'Safe',
        'Desc'
    ) == BAD_REQUEST
    assert await update_safe.execute(
        'Bearer SuOv40zYakOmWQl1sK8r1brPMdT97nMLcbCPpAdhoMHgx6ZKMlqu1VpgsIVH51c9pKHFgnCjVYOrmZ7iEt1hRnZixohhT7ZuXFCygMtm3NmANHFDH4pDui8hqal5SkQO',
        '56340c1e-bad4-4731-b119-36bed7170418',
        'Safe 1',
        'Description'
    ) == UNAUTHORIZED
    assert await update_safe.execute(
        token,
        safe_id,
        'Updated Safe 1',
        'Updated Description 1'
    ) == OK

    delete_safe = DbTestDeleteSafe()
    assert await delete_safe.execute(
        token,
        '4v23432c4234v32'
    ) == BAD_REQUEST
    assert await delete_safe.execute(
        'Bearer SuOv40zYakOmWQl1sK8r1brPMdT97nMLcbCPpAdhoMHgx6ZKMlqu1VpgsIVH51c9pKHFgnCjVYOrmZ7iEt1hRnZixohhT7ZuXFCygMtm3NmANHFDH4pDui8hqal5SkQO',
        '604e3f5a-1729-4d42-866d-7c732c1602d4'
    ) == UNAUTHORIZED
    assert await delete_safe.execute(
        token,
        '604e3f5a-1729-4d42-866d-7c732c1602d4'
    ) == NOT_FOUND
    assert await delete_safe.execute(
        token,
        safe_id
    ) == OK