from mindfulguard.classes.database.postgresql.connection_base import PostgreSqlConnectionBase
from mindfulguard.database.postgresql.connection import PostgreSqlConnection


class PostgreSql:
    def connection(self) -> PostgreSqlConnection:
        obj: PostgreSqlConnectionBase = PostgreSqlConnection()
        return obj