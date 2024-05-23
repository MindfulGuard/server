import pytest
from mindfulguard.classes.database import DataBase
from tests.logger import logger

logger()

@pytest.mark.asyncio
async def test_postgresql_connection():
    connection = DataBase().postgresql().connection()
    try:
        await connection.open()
        value: bool = await connection.connection.fetchval('SELECT TRUE;')
        assert value == True, value
    finally:
        await connection.close()