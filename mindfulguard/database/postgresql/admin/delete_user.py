from http.client import INTERNAL_SERVER_ERROR, OK, UNAUTHORIZED
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.classes.models.user import ModelUser
from mindfulguard.database.postgresql.authentication import PostgreSqlAuthentication
from mindfulguard.database.postgresql.connection import PostgreSqlConnection
from loguru import logger
import time

class PostgreSqlAdminDeletUser(PostgreSqlQueriesBase):
    def __init__(
        self,
        connection: PostgreSqlConnection,
        model_token: ModelToken,
        model_user: ModelUser
    ) -> None:
        super().__init__(connection)
        self.__auth_is_auth_admin = PostgreSqlAuthentication(self._connection)
        self.__model_token: ModelToken = model_token
        self.__model_user: ModelUser = model_user

    async def execute(self) -> None:
        start_time = time.time()
        logger.debug("Executing SQL query for admin user deletion...")
        
        try:
            is_auth = self.__auth_is_auth_admin.is_auth_admin(self.__model_token)
            await is_auth.execute()

            if is_auth.status_code != OK:
                self._status_code = is_auth.status_code
                logger.error("Admin user deletion failed due to authentication failure.")
                return
            
            value: int = await self._connection.connection.fetchval('''
            SELECT delete_user($1);
            ''',
            self.__model_user.id
            )
            
            if value == 0:
                self._status_code = OK
                logger.debug("Admin user deleted successfully.")
            elif value == -1:
                self._status_code = UNAUTHORIZED
                logger.warning("Unauthorized access for admin user deletion.")
            elif value == -2:
                self._status_code = INTERNAL_SERVER_ERROR
                logger.error("Internal server error occurred while deleting admin user.")
            else:
                self._status_code = INTERNAL_SERVER_ERROR
                logger.error("Unknown error occurred while deleting admin user.")
        finally:
            end_time = time.time()
            execution_time = end_time - start_time
            logger.trace("Admin user deletion execution time: {} seconds", execution_time)
            
            logger.debug("Admin user deletion execution completed.")
            return
