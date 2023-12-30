from http.client import BAD_REQUEST, OK
from mindfulguard.admin.users import AdminUsers
from mindfulguard.classes.admin.base import AdminBase
from mindfulguard.classes.s3 import S3
from mindfulguard.database.postgresql.admin import PostgreSqlAdmin
from mindfulguard.database.postgresql.authentication import PostgreSqlAuthentication
from mindfulguard.database.postgresql.user import PostgreSqlUser


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
            self._model_token.token = token
            self._model_user.id = user_id
            
            await self._connection.open()
            user_info = self._pgsql_admin.search_users(self._model_token, self._model_user)
            await user_info.execute('id')
            self._status_code = user_info.status_code
            if user_info.status_code != OK:
                print('User info', user_info.status_code)
                return
            
            db_delete = self._pgsql_admin.delete_user(self._model_token, self._model_user)
            await db_delete.execute()
            self._status_code = db_delete.status_code
            if db_delete.status_code != OK:
                print('Db_delete', db_delete.status_code)
                return

            print(user_info.response.login)
            self._s3.set_bucket_name(user_info.response.login)
            self._s3.object().delete_all_objects()
            self._s3.bucket().delete_bucket()
            return
        except ValueError as e:
            print(e)
            self._status_code = BAD_REQUEST
        finally:
            await self._connection.close()
