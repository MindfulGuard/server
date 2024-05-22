from http.client import BAD_REQUEST, OK
from loguru import logger
from mindfulguard.classes.admin.base import AdminBase
from mindfulguard.database.postgresql.admin import PostgreSqlAdmin


class AdminUsersDeleteUser(AdminBase):
    def __init__(self) -> None:
        super().__init__()
        self._pgsql_admin = PostgreSqlAdmin(self._connection)

    async def execute(
        self,
        token: str,
        user_id: str
    ) -> None:
        try:
            logger.info("Executing 'AdminUsersDeleteUser' for user with ID: {}", user_id)
            self._model_token.token = token
            self._model_user.id = user_id
            
            await self._connection.open()
            logger.debug("Connection opened successfully.")
            
            user_info = self._pgsql_admin.search_users(self._model_token, self._model_user)
            await user_info.execute('id')
            self._status_code = user_info.status_code
            
            if user_info.status_code != OK:
                logger.error("Failed to fetch user information from database. Status Code: {}", self._status_code)
                return
            
            logger.info("User information fetched successfully.")
            
            db_delete = self._pgsql_admin.delete_user(self._model_token, self._model_user)
            await db_delete.execute()
            self._status_code = db_delete.status_code
            
            if db_delete.status_code != OK:
                logger.error("Failed to delete user from database. Status Code: {}", self._status_code)
                return
            
            logger.info("User deleted successfully from database.")
            
            self._s3.set_bucket_name(user_info.response.login)
            self._s3.object().delete_all_objects()
            self._s3.bucket().delete_bucket()
            
            logger.info("User's S3 bucket and objects deleted successfully.")
            return
        except ValueError as e:
            logger.error("An error occurred: {}", e)
            self._status_code = BAD_REQUEST
        finally:
            await self._connection.close()
            logger.debug("Connection closed.")
