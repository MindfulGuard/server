import pytest
from mindfulguard.core import security
from mindfulguard.core.response_status_codes import *
from mindfulguard.core.security.totp import Totp
from mindfulguard.database.postgresql.authentication import Authentication
from mindfulguard.database.postgresql.items import Item
from mindfulguard.database.postgresql.safe import Safe


async def sign_up():
    auth = Authentication()
    totp = Totp("")
    result_OK:int = await auth.sign_up(
        login="B43bnjknjkbv-fs_",
        secret_string="AtfSfcBfkPMfoncx5PHPfMSkADeSSTzGRcnI4y3CYdII8MfIzLzZZv6OSL7fZqzj",
        reg_ip="127.0.0.1",
        secret_code=totp.generate_secret_code(),
        backup_codes=[53464,75686,423436,765767,98788,234513]
    )

    result_INTERNAL_SERVER_ERROR:int = await auth.sign_up(
        login="8bm&bn34_-bn70893b4n0789b3452n70895b4327n8093b54n27890n3b749580n79035b42n78905b342n7980b3524n798053b42n7980532b4n798035b42n709835b42n790835bn247890n35b789042n7b9085432n709b8534n0978b3542n9078b35427n9803b54254b",
        secret_string="LpaX2UPdsPWAPeZTw5b345b345b435b345b435b34b5345b43333333333333v4234v234v234v234v324v234b234b234b23b433333333333333nnnnnn4655555555555555555555v3544444444444444$#B$#V@#@#V@B$#B#$BVVEFFSFSDTt22Wog2yTQ984xBgHNylbnNRrhw2A7eDrhmc1aJrKi74rP",
        reg_ip="1275.0.0.1",
        secret_code="12345",
        backup_codes=[53475897439859834759843895793845897349857893475893479587348957398454675792657856876578932657893658793465789346578934]
    )

    return (result_OK,result_INTERNAL_SERVER_ERROR)

async def sign_in():
    auth = Authentication()

    result_OK = await auth.sign_in(
        login="B43bnjknjkbv-fs_",
        secret_string="AtfSfcBfkPMfoncx5PHPfMSkADeSSTzGRcnI4y3CYdII8MfIzLzZZv6OSL7fZqzj",
        token="T3h1IcrTxOz5taUZYFFcODSA71b34EeFf2QZ9IEU3t5feVKpvFfZm00Xp5E4hPmq",
        device="None",
        ip="127.0.0.1",
        expiration=60,
        is_verified_code=True
    )
        
    result_NOT_FOUND = await auth.sign_in(
        login="gbm&bng3g_-54b",
        secret_string="Lpaf2UPgdsPWAPeZTwTt22Wog2yTQ984xBgHNylbnNRrhw2A7eDrhmc1aJrKi74rP",
        token=security.generate_512_bit_token_string(),
        device="None",
        ip="127.0.0.1",
        expiration=60,
        is_verified_code=True
    )

    result_INTERNAL_SERVER_ERROR = await auth.sign_in(
        login="8bm&bn70893b4n0789b3452n70895b4327n8093b54n27890n3b749580n79035b42n78905b342n7980b3524n798053b42n7980532b4n798035b42n709835b42n790835bn247890n35b789042n7b9085432n709b8534n0978b3542n9078b35427n9803b54254b-54b",
        secret_string="LpaX2UPdsPWAPeZTw5b345b345b435b345b435b34b5345b43333333333333v4234v234v234v234v324v234b234b234b23b433333333333333nnnnnn4655555555555555555555v3544444444444444AtfSfcBfkPMfoncx5PHPfMSkADeSSTzGRcnI4y3CYdII8MfIzLzZZv6OSL7fZqzj",
        token="LpaX2UPdsPWAPeZTw5b345b345b435b345b435b34b5345b43333333333333v4234v234v234v234v324v234b234b234b23b433333333333333nnnnnn4655555555555555555555v3544444444444444LpaX2UPdsPWAPeZTw5b345b345b435b345b435b34b5345b43333333333333v4234v234v234v234v324v234b234b234b23b433333333333333nnnnnn4655555555555555555555v3544444444444444",
        device="None",
        ip="127.0.0.15",
        expiration=6064565464756756765765756645645645645654,
        is_verified_code=True
    )
    return (result_OK,result_NOT_FOUND,result_INTERNAL_SERVER_ERROR)

async def create_safe():
    safe = Safe()
    result_OK = await safe.create(
        token="T3h1IcrTxOz5taUZYFFcODSA71b34EeFf2QZ9IEU3t5feVKpvFfZm00Xp5E4hPmq",
        name="Safe 1",
        description="Hello Safe 1"
    )
    result_UNAUTHORIZED = await safe.create(
        token="g3s1IcrTxOz5tafZYFhcODSA71b34EeFf2QZ9IEU3t5feVKpvFfZm00Xp5E4hPgg",
        name="Safe 1",
        description="Hello Safe 1"
    )
    return (result_OK,result_UNAUTHORIZED)

async def get_safes():
    safe = Safe()
    result_OK = await safe.get(
        token="T3h1IcrTxOz5taUZYFFcODSA71b34EeFf2QZ9IEU3t5feVKpvFfZm00Xp5E4hPmq",
    )
    result_UNAUTHORIZED = await safe.get(
        token="g3s1IcrTxOz5tafZYFhcODSA71b34EeFf2QZ9IEU3t5feVKpvFfZm00Xp5E4hPgg",
    )
    return (result_OK,result_UNAUTHORIZED)

async def update_safe(safe_id:str):
    safe = Safe()
    result_OK = await safe.update(
        token="T3h1IcrTxOz5taUZYFFcODSA71b34EeFf2QZ9IEU3t5feVKpvFfZm00Xp5E4hPmq",
        id=safe_id,
        name="Updated Safe 1",
        description="Hello updated Safe 1"
    )
    result_UNAUTHORIZED = await safe.update(
        token="g3s1IcrTxOz5tafZYFhcODSA71b34EeFf2QZ9IEU3t5feVKpvFfZm00Xp5E4hPgg",
        id="1668cdc1-ce94-4599-81db-67890752a172",
        name="Safe 1",
        description="Hello Safe 1"
    )
    result_INTERNAL_SERVER_ERROR = await safe.update(
        token="T3h1IcrTxOz5taUZYFFcODSA71b34EeFf2QZ9IEU3t5feVKpvFfZm00Xp5E4hPmq",
        id="1668cdc1-ce94-4599-81db-67890752a172",
        name="Safe 1",
        description="Hello Safe 1"
    )
    return (result_OK,result_UNAUTHORIZED,result_INTERNAL_SERVER_ERROR)

async def create_item(safe_id:str):
    print(safe_id)
    item = Item()
    result_OK = await item.create(
        token="T3h1IcrTxOz5taUZYFFcODSA71b34EeFf2QZ9IEU3t5feVKpvFfZm00Xp5E4hPmq",
        safe_id=safe_id,
        title = "Title1",
        item= '{"example1":"example"}',
        notes = "My first item",
        tags= ["tag1","tag2"],
        category="LOGIN"
    )
    result_UNAUTHORIZED = await item.create(
        token="g3s1IcrTxOz5tafZYFhcODSA71b34EeFf2QZ9IEU3t5feVKpvFfZm00Xp5E4hPgg",
        safe_id=safe_id,
        title = "Title1",
        item= '{"example1":"example"}',
        notes = "My first item",
        tags= ["tag1","tag2"],
        category="LOGIN"
    )

    return (result_OK,result_UNAUTHORIZED)

async def get_item():
    item = Item()
    result_OK = await item.get(
        token="T3h1IcrTxOz5taUZYFFcODSA71b34EeFf2QZ9IEU3t5feVKpvFfZm00Xp5E4hPmq",
    )
    result_UNAUTHORIZED = await item.get(
        token="g3s1IcrTxOz5tafZYFhcODSA71b34EeFf2QZ9IEU3t5feVKpvFfZm00Xp5E4hPgg",
    )

    return (result_OK,result_UNAUTHORIZED)    

async def update_item(safe_id:str,item_id:str):
    item = Item()
    result_OK = await item.update(
        token="T3h1IcrTxOz5taUZYFFcODSA71b34EeFf2QZ9IEU3t5feVKpvFfZm00Xp5E4hPmq",
        safe_id=safe_id,
        item_id=item_id,
        title = "Updated Title1",
        item= '{"example1_updated":"example_updated"}',
        notes = "My updated item",
        tags= ["tag1","tag2","tag3"],
    )
    result_UNAUTHORIZED = await item.update(
        token="g3s1IcrTxOz5tafZYFhcODSA71b34EeFf2QZ9IEU3t5feVKpvFfZm00Xp5E4hPgg",
        safe_id=safe_id,
        item_id=item_id,
        title = "Title1",
        item= '{"example1":"example"}',
        notes = "My first item",
        tags= ["tag1","tag2"],
    )

    return (result_OK,result_UNAUTHORIZED) 

async def set_favorite_item(safe_id:str,item_id:str):
    item = Item()
    result_OK = await item.set_favorite(
        token="T3h1IcrTxOz5taUZYFFcODSA71b34EeFf2QZ9IEU3t5feVKpvFfZm00Xp5E4hPmq",
        safe_id=safe_id,
        item_id=item_id,
    )
    result_UNAUTHORIZED = await item.set_favorite(
        token="g3s1IcrTxOz5tafZYFhcODSA71b34EeFf2QZ9IEU3t5feVKpvFfZm00Xp5E4hPgg",
        safe_id=safe_id,
        item_id=item_id,
    )

    return (result_OK,result_UNAUTHORIZED) 

@pytest.mark.asyncio
async def test_authentication():
    __sign_up = await sign_up()
    __sign_up_OK = __sign_up[0]
    __sign_up_INTERNAL_SERVER_ERROR = __sign_up[1]

    __sign_in = await sign_in()
    __sign_in_OK = __sign_in[0]
    __sign_in_NOT_FOUND = __sign_in[1]
    __sign_in_INTERNAL_SERVER_ERROR = __sign_in[2]

    assert __sign_up_OK == OK
    assert __sign_up_OK == OK
    assert __sign_up_INTERNAL_SERVER_ERROR == INTERNAL_SERVER_ERROR

    assert __sign_in_OK == OK
    assert __sign_in_NOT_FOUND == NOT_FOUND
    assert __sign_in_INTERNAL_SERVER_ERROR == INTERNAL_SERVER_ERROR

@pytest.mark.asyncio
async def test_safe_item():
    __create_safe = await create_safe()
    __create_safe_OK = __create_safe[0]
    __create_safe_UNAUTHORIZED = __create_safe[1]

    __get_safes = await get_safes()
    __get_safes_OK = __get_safes[0]
    __get_safes_UNAUTHORIZED = __get_safes[1]
    get_safe_id = __get_safes_OK[0][0]['id']

    __update_safe = await update_safe(get_safe_id)
    __update_safe_OK = __update_safe[0]
    __update_safe_UNAUTHORIZED = __update_safe[1]
    __update_safe_INTERNAL_SERVER_ERROR = __update_safe[2]

    __create_item = await create_item(get_safe_id)
    __create_item_OK = __create_item[0]
    __create_item_UNAUTHORIZED = __create_item[1]

    __get_item = await get_item()
    __get_item_OK = __get_item[0]
    __get_item_UNAUTHORIZED = __get_item[1]
    get_item_id = __get_item_OK[0][0]['items'][0]['id']

    __update_item = await update_item(get_safe_id,get_item_id)
    __update_item_OK =  __update_item[0]
    __update_item_UNAUTHORIZED = __update_item[1]

    __set_favorite_item = await set_favorite_item(get_safe_id,get_item_id)
    __set_favorite_item_OK = __set_favorite_item[0]
    __set_favorite_item_UNAUTHORIZED = __set_favorite_item[1]

    assert __create_safe_OK == OK
    assert __create_safe_UNAUTHORIZED == UNAUTHORIZED

    assert __get_safes_OK[1] == OK
    assert __get_safes_UNAUTHORIZED[1] == UNAUTHORIZED

    assert __update_safe_OK == OK
    assert __update_safe_UNAUTHORIZED == UNAUTHORIZED
    assert __update_safe_INTERNAL_SERVER_ERROR == INTERNAL_SERVER_ERROR

    assert __create_item_OK == OK
    assert __create_item_UNAUTHORIZED == UNAUTHORIZED

    assert __get_item_OK[3] == OK
    assert __get_item_UNAUTHORIZED[3] == UNAUTHORIZED

    assert __update_item_OK == OK
    assert __update_item_UNAUTHORIZED == UNAUTHORIZED

    assert __set_favorite_item_OK == OK
    assert __set_favorite_item_UNAUTHORIZED == UNAUTHORIZED 