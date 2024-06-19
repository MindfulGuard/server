from http.client import CONFLICT, INTERNAL_SERVER_ERROR, NOT_FOUND, OK, SERVICE_UNAVAILABLE
import asyncpg
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.code import ModelCode
from mindfulguard.classes.models.user import ModelUser
from mindfulguard.database.postgresql.connection import PostgreSqlConnection
from loguru import logger
import time

class PostgreSqlSignUp(PostgreSqlQueriesBase):
    """
    Requested values for ModelUser:
        ModelUser().login,
        ModelUser().secret_string,
        ModelUser().reg_ip,
        ModelUser().confirm

    Requested values for ModelCode:
        ModelCode().secret_code,
        ModelCode().backup_codes
    """
    def __init__(self, connection: PostgreSqlConnection, model_user: ModelUser, model_code: ModelCode) -> None:
        super().__init__(connection)
        self.__model_user: ModelUser = model_user
        self.__model_code: ModelCode = model_code
    
    async def execute(self, registration_allowed: bool) -> None:
        start_time = time.time()
        logger.debug("Executing SQL query to sign up user...")

        try:
            value: int = await self._connection.connection.fetchval('''
            SELECT sign_up($1, $2, $3, $4, $5, $6, $7)
            ''',
            self.__model_user.login,
            self.__model_user.secret_string,
            self.__model_user.reg_ip,
            self.__model_user.confirm,
            self.__model_code.secret_code,
            self.__model_code.backup_codes,
            registration_allowed
            )

            if value == 0 or value == 1 or value == 2:
                self._status_code = OK
                logger.debug("User signed up successfully.")
            elif value == -1:
                self._status_code = CONFLICT
                logger.warning("Conflict occurred during user sign up.")
            elif value == -2 or value == -3 or value == -4:
                self._status_code = NOT_FOUND
                logger.warning("Required data not found during user sign up.")
            elif value == -5:
                self._status_code = SERVICE_UNAVAILABLE
                logger.warning("Service unavailable during user sign up.")
            else:
                self._status_code = INTERNAL_SERVER_ERROR
                logger.error("Internal server error occurred during user sign up.")

        except asyncpg.exceptions.DataError:
            self._status_code = INTERNAL_SERVER_ERROR
            logger.exception("Data error occurred during user sign up.")
        except asyncpg.exceptions.UniqueViolationError:
            self._status_code = CONFLICT
            logger.warning("Unique violation occurred during user sign up.")
        finally:
            end_time = time.time()
            execution_time = end_time - start_time
            logger.trace("Sign up execution time: {} seconds", execution_time)
            logger.debug("Execution of sign up query completed.")
