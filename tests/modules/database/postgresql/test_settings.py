from http.client import OK

import pytest
from mindfulguard.classes.database import DataBase
from mindfulguard.database.postgresql.settings import PostgreSqlSettings
from tests.logger import logger

logger()

@pytest.mark.asyncio
async def test_settings():
    connection = DataBase().postgresql().connection()
    pgsql_settings = PostgreSqlSettings(connection)
    try:
        await connection.open()
        await pgsql_settings.execute()
        assert pgsql_settings.status_code == OK
    finally:
        await connection.close()