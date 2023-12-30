from http.client import INTERNAL_SERVER_ERROR, OK
import asyncpg
from routines.pgsql.connection import Connection

class Sql:
    async def get_settings(self):
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
            return (settings_dict, OK)
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            return ({}, INTERNAL_SERVER_ERROR)
        finally:
            if connection:
                await connection.close()
    
    async def delete_tokens(self):
        connection = None
        try:
            connection = await Connection().connect()
            await connection.fetch('''
            DELETE FROM t_tokens
            WHERE EXTRACT(EPOCH FROM current_timestamp)::bigint > t_expiration;
            ''')
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            return ({}, INTERNAL_SERVER_ERROR)
        finally:
            if connection:
                await connection.close()

    async def delete_users(self, expiration: int):
        connection = None
        try:
            connection = await Connection().connect()
            await connection.fetch('''
            WITH deleted_users AS (
                DELETE FROM u_users
                WHERE EXTRACT(EPOCH FROM current_timestamp)::bigint > u_created_at + $1 AND u_confirm = FALSE
                RETURNING u_id
            )
            DELETE FROM c_codes
            WHERE c_codes.c_u_id IN (SELECT u_id FROM deleted_users);
            ''',
            expiration
        )
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            return ({}, INTERNAL_SERVER_ERROR)
        finally:
            if connection:
                await connection.close()