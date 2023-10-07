import logging
from mindfulguard.database.postgresql.connection import Connection

async def test_connection():
    flag:bool = False 
    connection = None
    try:
        connection = await Connection().connect()
        value:bool = await connection.fetchval('SELECT TRUE;')
        if value:
            flag = True
        assert flag == True
    except Exception as e:
        logging.error('Exception',e)
    finally:
        if connection:
            await connection.close()