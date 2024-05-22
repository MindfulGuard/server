from http.client import OK
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.classes.models.user import ModelUser
from mindfulguard.database.postgresql.authentication import PostgreSqlAuthentication
from mindfulguard.database.postgresql.connection import PostgreSqlConnection
from loguru import logger
import time

class PostgreSqlAdminGetUsers(PostgreSqlQueriesBase):
    def __init__(self, connection: PostgreSqlConnection, model_token: ModelToken) -> None:
        super().__init__(connection)
        self.__auth_is_auth_admin = PostgreSqlAuthentication(self._connection)
        self.__model_token = model_token
    
    def count_users(self):
        return PostgreSqlAdminGetCountUsers(self._connection)

    class __Iterator:
        def __init__(self, pgsql_response: list):
            self.__pgsql_response: list = pgsql_response
            self.__model_user = ModelUser()
            self.__i: int = 0

        def __iter__(self):
            return self

        def __next__(self):
            if self.__i < len(self.__pgsql_response):
                self.__model_user.id = self.__pgsql_response[self.__i]['u_id']
                self.__model_user.login = self.__pgsql_response[self.__i]['u_login']
                self.__model_user.reg_ip = self.__pgsql_response[self.__i]['u_reg_ip']
                self.__model_user.confirm = self.__pgsql_response[self.__i]['u_confirm']
                self.__model_user.created_at = self.__pgsql_response[self.__i]['u_created_at']
                self.__i += 1
                return self.__model_user
            else:
                raise StopIteration

    @property
    def response(self) -> __Iterator:
        return self._response

    async def execute(self, limit: int, offset: int) -> None:
        start_time = time.time()
        logger.debug("Executing SQL query to get admin users...")
        
        try:
            is_auth = self.__auth_is_auth_admin.is_auth_admin(self.__model_token)
            await is_auth.execute()

            if is_auth.status_code != OK:
                self._status_code = is_auth.status_code
                logger.error("Admin user retrieval failed due to authentication failure.")
                return
            
            values = await self._connection.connection.fetch('''
            SELECT u_id, u_login, u_reg_ip, u_confirm, u_created_at
            FROM u_users
            ORDER BY u_id
            LIMIT $1 OFFSET $2;
            ''',
            limit,
            offset
            )

            self._response = self.__Iterator(values)
            self._status_code = OK
        finally:
            end_time = time.time()
            execution_time = end_time - start_time
            logger.trace("Admin user retrieval execution time: {} seconds", execution_time)
            
            logger.debug("Admin user retrieval execution completed.")
            return
    
class PostgreSqlAdminGetCountUsers(PostgreSqlQueriesBase):
    def __init__(self, connection: PostgreSqlConnection) -> None:
        super().__init__(connection)
        self.__count: int

    @property
    def count(self) -> int:
        return self.__count
    
    async def execute(self) -> None:
        logger.debug("Executing SQL query to get count of admin users...")
        
        try:
            value: int = await self._connection.connection.fetchval('''
            SELECT count(*) FROM u_users;
            ''')
            
            if value is None:
                self.__count = 0
            else:
                self.__count = value
        finally:
            logger.debug("Count of admin users retrieved successfully.")
            return
