from http.client import BAD_REQUEST, CONFLICT, NOT_FOUND, OK, UNAUTHORIZED
import pytest
from mindfulguard.classes.database import DataBase
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.data_collection import PostgreSqlDataCollection
from tests.modules.database.postgresql.authentication.classes.db_authentication_sign_in import DbTestsAuthenticationSignIn
from tests.modules.database.postgresql.authentication.classes.db_authentication_sign_up import DbTestsAuthenticationSignUp
from tests.logger import logger

logger()

class DbTestDataCollection:
    def __init__(self) -> None:
        self.__connection = DataBase().postgresql().connection()
        self.__pgsql_data_collection: PostgreSqlDataCollection  = PostgreSqlDataCollection(self.__connection)
        self.__model_token: ModelToken = ModelToken()

    async def ok(
        self,
        token: str,
        device: str = 'Python client 0.0.0/Windows',
        last_ip: str = '127.0.0.1'
    ) -> int:
        try:
            self.__model_token.token = token
            self.__model_token.device = device
            self.__model_token.last_ip = last_ip
            db = self.__pgsql_data_collection.update_token_information(self.__model_token)
            await self.__connection.open()
            await db.execute()
            return db.status_code
        finally:
            await self.__connection.close()


@pytest.mark.asyncio
async def test_data_collection():
    sign_up = DbTestsAuthenticationSignUp()

    assert await sign_up.bad_request(
        '#$V#@)($V*M)(#@)',
        '$V#)@(*M$V)(@#C$@#)',
        '#$VM@)#($V*@#)(C$)',
        [535,353,535,3,53,53,53,53]
    ) == BAD_REQUEST

    login: str = 'User2__----'
    secret_string: str = 'gSHlVGUWBA5uwv8ycjWDpXi5yULDeQ5Cba5YdQuPFO7lOldrM1RZlzwA1rOphJqf'
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
    
    token = 'Bearer KGp3UQlkndTvGUfMXw9FcqbmKPnjgGdfY1Os75qn7bLCJqXvyODEi6F7OwzrxWKT4X5Mv23pr4JaET8pZqFNlLd4WRWsdNq1WxKNkJKlh0MF5AYOzSx8Ad6qzPWK9DtO'
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

    data_collection = DbTestDataCollection()

    assert await data_collection.ok(
        'Bearer ww46UpED3Nj7g4iwVRwcIHOV04iE2pw20isgRU83bFHzInjbn5irTKJiEqHJ1kgSkdwFurRK4ui6duHIsnnwjjSZgKuipwWj6lOPOHC1WvwwcQdjqAmT4iDYkFiJ0HTn'
    ) == UNAUTHORIZED

    assert await data_collection.ok(
        token
    ) == OK