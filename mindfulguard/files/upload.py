from http.client import BAD_REQUEST, INTERNAL_SERVER_ERROR, OK
from typing import Any

from fastapi import UploadFile
from mindfulguard.classes.files.base import FilesBase
from mindfulguard.database.postgresql.safe import PostgreSqlSafe

class Upload(FilesBase):
    def __init__(self) -> None:
        super().__init__()
        self.__safe = PostgreSqlSafe(self._connection)

    async def auth(self, token: str, safe_id: str) -> None:
        try:
            self._model_token.token = token
            self._model_safe.id = safe_id
            db = self.__safe.safe_exist(self._model_token, self._model_safe)
            await self._connection.open()
            await db.execute()
            self._status_code = db.status_code
        except ValueError:
            self._status_code = BAD_REQUEST
        finally:
            await self._connection.close()

    def __free_disk_space(self, settings: dict[str, Any], file_size: int) -> bool:
        space_per_user: int = settings['disk_space_per_user']
        if self._s3.bucket().get_size + file_size > space_per_user:
            return False
        return True

    async def execute(
        self,
        files: list[UploadFile]
    ) -> None:
        try:
            db_info = self._pgsql_user.get_information(self._model_token)
            await self._connection.open()
            await db_info.execute()
            if db_info.status_code != OK:
                self._status_code = db_info.status_code
                return

            self._s3.set_bucket_name(db_info.response.login)
            await self._settings.execute()
            fds: bool = self.__free_disk_space(
                self._settings.response,
                sum([file.size for file in files]) # type: ignore
            )
            if fds == False:
                self._status_code = INTERNAL_SERVER_ERROR
                return

            upload_objs = await self._s3.object().put_objects(
                [file for file in files],
                prefix_object_name_=f"{self._s3.CONTENT_PATH}/{self._model_safe.id}/"
            )
            if not upload_objs:
                self._status_code = INTERNAL_SERVER_ERROR
                return
            self._status_code = OK
            return
        except ValueError:
            self._status_code = BAD_REQUEST
        finally:
            await self._connection.close()