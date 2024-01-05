from http.client import BAD_REQUEST, OK
from mindfulguard.classes.safe.base import SafeBase


class Delete(SafeBase):
    def __init__(self) -> None:
        super().__init__()
    
    async def execute(
        self,
        token: str,
        safe_id: str,
    ) -> None:
        try:
            self._model_token.token = token
            self._model_safe.id = safe_id
            db = self._pgsql_safe.delete(self._model_token, self._model_safe)
            await self._connection.open()
            await db.execute()
            self._status_code = db.status_code
            if db.status_code == OK:
                db_user_info = self._pgsql_user.get_information(self._model_token)
                await db_user_info.execute()
                self._s3.set_bucket_name(db_user_info.response.login)
                object_list = [obj.object_name for obj in self._s3.object().get_all_objects(f'{self._s3.CONTENT_PATH}/{safe_id}/')]
                self._s3.object().delete_objects(object_list) # type: ignore
                for i in self._redis.client().connection.scan_iter(
                    f'{self._model_token.token}:{self._redis.PATH_SAFE_ALL_ITEM}'
                ):
                    self._redis.client().connection.delete(i)
            return
        except ValueError:
            self._status_code = BAD_REQUEST
        finally:
            await self._connection.close()