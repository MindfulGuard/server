from mindfulguard.core.response_status_codes import *
from mindfulguard.database.postgresql.connection import Connection
import asyncpg

class Settings:
    async def get(self):
        connection = None
        try:
            connection = await Connection().connect()
            values = await connection.fetch('''
            SELECT st_id, st_key, st_value
            FROM st_settings
            ''')

            settings_dict = {}
            for row in values:
                key, value = row['st_key'], row['st_value']
                settings_dict[key] = value
            return (settings_dict,OK)
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            return ({}, INTERNAL_SERVER_ERROR)
        finally:
            if connection:
                await connection.close()