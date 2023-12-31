from http.client import BAD_REQUEST, CONFLICT, INTERNAL_SERVER_ERROR, NOT_FOUND, OK, UNAUTHORIZED
import pytest
from tests.modules.database.postgresql.authentication.classes.db_authentication_sign_in import DbTestsAuthenticationSignIn

from tests.modules.database.postgresql.authentication.classes.db_authentication_sign_up import DbTestsAuthenticationSignUp
from tests.modules.database.postgresql.items.classes.create import DbTestItemCreate
from tests.modules.database.postgresql.items.classes.delete import DbTestItemDelete
from tests.modules.database.postgresql.items.classes.favorite import DbTestItemFavorite
from tests.modules.database.postgresql.items.classes.get import DbTestItemGet
from tests.modules.database.postgresql.items.classes.move import DbTestItemMove
from tests.modules.database.postgresql.items.classes.update import DbTestItemUpdate
from tests.modules.database.postgresql.safe.classes.create import DbTestCreateSafe
from tests.modules.database.postgresql.safe.classes.delete import DbTestDeleteSafe
from tests.modules.database.postgresql.safe.classes.get import DbTestGetSafe


@pytest.mark.asyncio
async def test_items():
    sign_up = DbTestsAuthenticationSignUp()

    assert await sign_up.bad_request(
        '#$V#@)($V*M)(#@)',
        '$V#)@(*M$V)(@#C$@#)',
        '#$VM@)#($V*@#)(C$)',
        [535,353,535,3,53,53,53,53]
    ) == BAD_REQUEST

    login: str = 'User4__-a-ff--'
    secret_string: str = 'qhHgVGUWqq5uwv8ycaWDpXi5yULDeQ5Cba5YdQuPFO7lOldrM1RZlzwA1rOphJqq'
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
    
    token = 'Bearer aCIvFV05t2kpFr5QQ5jrL7lSYftLhs9cMns0hrtJm7M1ACUZRhBrT9dyrFxRil49VVXhGoJSpqf2JD2YEJ75Rejn5gK3kbwQ9jAX1qfhHrHB5XEjRylrsCBZolCuvAOe'
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

    create_safe2 = DbTestCreateSafe()
    assert await create_safe2.execute(
        'Bearer Dn8QQDRNpWo3PAbk3GtsDXntoq6AK10uyn2JgTYNJ1unHBF67ZZ4ROsyp5ke4tlph9UnWSV6v0dfowahxiEgjj8BEhLRhUC2utZKLbgjEcXceH9AXnrcWe296ME3t8oD',
        'Safe',
        'Desc'
    ) == UNAUTHORIZED

    assert await create_safe2.execute(
        token,
        'Vc1mBADya3yHjMkKPKf0CGBLqQk8ZkTdPuOhujAJt9XHB1j0tFAfdTwG8FHrkQ9A9qFIhwCNU3YoKjavd0FPk8dSjaPmX0T0kwIH7979jotSrGj38qBXaB0TIMfRdbp4',
        'Desc mew'
    ) == BAD_REQUEST

    assert await create_safe2.execute(
        token,
        'Safe 2',
        'Description 2'
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

    safe_id1 = get_safes.response.__next__().id
    safe_id2 = get_safes.response.__next__().id

    create_item = DbTestItemCreate()
    assert await create_item.execute(
        'Bearer ST6fwA7PLikqzaag2NExxtaVlbZexvIRm43sFYRshoMclPfNzRU4KPoqOlL2rQ5Motq3fIuXGJ2oaJyGKQSjuSF1j5DRqoP0PtoHog9omkqiYDyk7RHYeSVQbT36q8eA',
        '604e3f5a-1729-4d42-866d-7c732c1602d4',
        'Title',
        {"key":"value"},
        'Notes',
        ["tag1", "tag2"],
        'CATEGORY'
    ) == UNAUTHORIZED
    assert await create_item.execute(
        token,
        'c514786f-76a9-4b83-adc4-b992afe7bcaa',
        'Title',
        {"key":"value"},
        'Notes',
        ["tag1", "tag2"],
        'CATEGORY'
    ) == INTERNAL_SERVER_ERROR
    assert await create_item.execute(
        token,
        safe_id1,
        'Title',
        {"key":"value"},
        'Notes',
        ["tag1", "tag2"],
        'CATEGORY'
    ) == OK
    assert await create_item.execute(
        token,
        safe_id1,
        'Title',
        {"key":"value"},
        'Notes',
        ["tag1", "tag2"],
        'CATEGORY'
    ) == OK
    assert await create_item.execute(
        token,
        safe_id1,
        'Title',
        {"key":"value"},
        'Notes',
        ["tag1", "tag2"],
        'CATEGORY'
    ) == OK
    assert await create_item.execute(
        token,
        safe_id1,
        'Title',
        {"key":"value"},
        'Notes',
        ["tag1", "tag2"],
        'CATEGORY'
    ) == OK
    assert await create_item.execute(
        token,
        safe_id1,
        'Title',
        {"key":"value"},
        'Notes',
        ["tag1", "tag2"],
        'CATEGORY'
    ) == OK
    assert await create_item.execute(
        token,
        safe_id1,
        'Title',
        {"key":"value"},
        'Notes',
        ["tag1", "tag2"],
        'CATEGORY'
    ) == OK
    assert await create_item.execute(
        token,
        safe_id1,
        'Title',
        {"key":"value"},
        'Notes',
        ["tag1", "tag2"],
        'CATEGORY'
    ) == OK

    get_items = DbTestItemGet()
    assert await get_items.execute(
        'Bearer XcjL2XTjMZP7AIxnfngXmDunUpaVoZzTVBk4fJhwFXtliIAXCyDaS1FsVI92IssFBNmzGCizQHEZZy0DfXfE0IwvyB0jVS7tChNliaiqe8ZLcHnsrSwWXIxDGkFNc4ks'
    ) == UNAUTHORIZED
    assert await get_items.execute(token) == OK

    item_id = get_items.response.__next__().id

    update_item = DbTestItemUpdate()
    assert await update_item.execute(
        'Bearer ST6fwA7PLikqzaag2NExxtaVlbZexvIRm43sFYRshoMclPfNzRU4KPoqOlL2rQ5Motq3fIuXGJ2oaJyGKQSjuSF1j5DRqoP0PtoHog9omkqiYDyk7RHYeSVQbT36q8eA',
        '604e3f5a-1729-4d42-866d-7c732c1602d4',
        '604e3f5a-1729-4d42-866d-7c732c1602d4',
        'Title',
        {"key":"value"},
        'Notes',
        ["tag1", "tag2"],
        'CATEGORY'
    ) == UNAUTHORIZED
    assert await update_item.execute(
        token,
        '604e3f5a-1729-4d42-866d-7c732c1602d4',
        '604e3f5a-1729-4d42-866d-7c732c1602d4',
        'Title',
        {"key":"value"},
        'Notes',
        ["tag1", "tag2"],
        'CATEGORY'
    ) == INTERNAL_SERVER_ERROR
    assert await update_item.execute(
        token,
        item_id,
        safe_id1,
        'Title',
        {"key":"value"},
        'Notes',
        ["tag1", "tag2"],
        'CATEGORY'
    ) == OK

    item_move = DbTestItemMove()
    assert await item_move.execute(
        'Bearer 1MlRHQagDdZrfQO8IivZASlg19XANglfB2aasUTDDfYJVQ2faiPq9vUArhr9VgYZWR2F6MYxmAOB1KLVtqGDTza9fT2rpmudSKchH51NT9nebrBI0ZnAdJOQIUAQRwor',
        'c514786f-76a9-4b83-adc4-b992afe7bcaa',
        'b15ba247-aed7-4d2b-aaa2-d24efd87d0c3',
        '447c5223-3c0f-43d0-93a5-7046129f3f80'
    ) == UNAUTHORIZED
    assert await item_move.execute(
        token,
        'c514786f-76a9-4b83-adc4-b992afe7bcaa',
        'b15ba247-aed7-4d2b-aaa2-d24efd87d0c3',
        '447c5223-3c0f-43d0-93a5-7046129f3f80'
    ) == INTERNAL_SERVER_ERROR
    assert await item_move.execute(
        token,
        item_id,
        safe_id1,
        safe_id2
    ) == OK

    safe_delete = DbTestDeleteSafe()
    assert await safe_delete.execute(
        token,
        safe_id1
    )

    item_favorite = DbTestItemFavorite()
    assert await item_favorite.execute(
        'Bearer 1MlRHQagDdZrfQO8IivZASlg19XANglfB2aasUTDDfYJVQ2faiPq9vUArhr9VgYZWR2F6MYxmAOB1KLVtqGDTza9fT2rpmudSKchH51NT9nebrBI0ZnAdJOQIUAQRwor',
        item_id,
        safe_id2
    ) == UNAUTHORIZED
    assert await item_favorite.execute(
        token,
        item_id,
        safe_id2
    ) == OK

    item_delete = DbTestItemDelete()
    assert await item_delete.execute(
        'Bearer 1MlRHQagDdZrfQO8IivZASlg19XANglfB2aasUTDDfYJVQ2faiPq9vUArhr9VgYZWR2F6MYxmAOB1KLVtqGDTza9fT2rpmudSKchH51NT9nebrBI0ZnAdJOQIUAQRwor',
        item_id,
        safe_id2
    ) == UNAUTHORIZED
    assert await item_delete.execute(
        token,
        item_id,
        safe_id2
    ) == OK