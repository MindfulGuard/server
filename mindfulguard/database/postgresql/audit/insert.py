from http.client import INTERNAL_SERVER_ERROR, OK, UNAUTHORIZED
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.audit import ModelAudit
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.connection import PostgreSqlConnection

class PostgreSqlAuditInsert(PostgreSqlQueriesBase):
    def __init__(
        self,
        connection: PostgreSqlConnection,
        model_token: ModelToken,
        model_audit: ModelAudit
    ) -> None:
        super().__init__(connection)
        self.__model_token: ModelToken = model_token
        self.__model_audit: ModelAudit = model_audit
    
    async def execute(self) -> None:
        await self._connection.connection.fetch('''
        CALL create_audit_item($1, $2, $3, $4, $5)
        ''',
        self.__model_token.token,
        self.__model_audit.ip,
        self.__model_audit.object,
        self.__model_audit.action,
        self.__model_audit.device
        )