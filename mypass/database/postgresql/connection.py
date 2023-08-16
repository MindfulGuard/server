import asyncpg

from mypass.core.configuration import *


class Connection:
    async def connect(self):
        config = ServerConfiguration()
        db = PgSql(config)
        return await asyncpg.connect(database=db.get_database(),
                                     user=db.get_user(),
                                     password=db.get_password(),
                                     host=db.get_host(),
                                     port=db.get_port())