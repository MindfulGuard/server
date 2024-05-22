from http.client import OK
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.audit import ModelAudit
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.connection import PostgreSqlConnection
from loguru import logger
import time

class PostgreSqlAuditGet(PostgreSqlQueriesBase):
    def __init__(
        self,
        connection: PostgreSqlConnection,
        model_token: ModelToken,
    ) -> None:
        super().__init__(connection)
        self.__model_token: ModelToken = model_token

    def count(self):
        return PostgreSqlAuditGetCount(self._connection, self.__model_token)

    class __Iterator:
        def __init__(self, pgsql_response: list) -> None:
            self.__pgsql_response: list = pgsql_response
            self.__model_audit = ModelAudit()
            self.__i: int = 0

        def __iter__(self):
            return self
        
        def __next__(self):
            if self.__i < len(self.__pgsql_response):
                self.__model_audit.id = self.__pgsql_response[self.__i]['a_id']
                self.__model_audit.created_at = self.__pgsql_response[self.__i]['a_created_at']
                self.__model_audit.ip = self.__pgsql_response[self.__i]['a_ip']
                self.__model_audit.object = self.__pgsql_response[self.__i]['a_object']
                self.__model_audit.action = self.__pgsql_response[self.__i]['a_action']
                self.__model_audit.device = self.__pgsql_response[self.__i]['a_device']

                self.__i += 1
                return self.__model_audit
            else:
                raise StopIteration

    @property
    def response(self) -> __Iterator:
        return self._response

    async def execute(self, limit: int, offset: int) -> None:
        start_time = time.time()
        logger.debug("Executing SQL query to get audit logs...")

        try:
            values = await self._connection.connection.fetch('''
            select a_id, a_created_at , a_ip, a_object, a_action, a_device
            from a_audit
            where a_u_id = (select t_u_id from t_tokens where t_token = $1)
            order by a_created_at desc
            limit $2 OFFSET $3;
            ''',
            self.__model_token.token,
            limit,
            offset
            )
    
            self._response = self.__Iterator(values)
            self._status_code = OK
        finally:
            end_time = time.time()
            execution_time = end_time - start_time
            logger.trace("Audit logs retrieval execution time: {} seconds", execution_time)
            
            logger.debug("Audit logs retrieval execution completed.")
            return
    
class PostgreSqlAuditGetCount(PostgreSqlQueriesBase):
    def __init__(self, connection: PostgreSqlConnection, model_token: ModelToken) -> None:
        super().__init__(connection)
        self.__count: int
        self.__model_token: ModelToken = model_token

    @property
    def count(self) -> int:
        return self.__count
    
    async def execute(self) -> None:
        logger.debug("Executing SQL query to get count of audit logs...")

        try:
            value: int = await self._connection.connection.fetchval('''
            SELECT count(*) FROM a_audit where a_u_id = (select t_u_id from t_tokens where t_token = $1);
            ''',
            self.__model_token.token
            )
            if value is None:
                self.__count = 0
            else:
                self.__count = value
        finally:
            logger.debug("Count of audit logs retrieved successfully.")
            return
