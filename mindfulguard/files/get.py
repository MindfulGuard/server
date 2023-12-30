import datetime
from http.client import BAD_REQUEST, OK
from mindfulguard.classes.files.base import FilesBase


class Get(FilesBase):
    def __init__(self) -> None:
        super().__init__()
        self.__response: dict[str, list]

    @property
    def response(self) -> dict[str, list]:
        return self.__response

    async def execute(self, token: str):
        try:
            self._model_token.token = token
            db = self._pgsql_user.get_information(self._model_token)

            await self._connection.open()
            await db.execute()
            if db.status_code != OK:
                self._status_code = db.status_code
                return
            
            response_dict = {"files": []}
            safe_id_set = set()
            self._s3.set_bucket_name(db.response.login)
            object_list = map(
                lambda x: x,
                self._s3.object().get_all_objects(prefix=f"{self._s3.CONTENT_PATH}/"),
            )
            for raw in object_list:
                safe_id = raw.object_name.split('/')[1]
                if safe_id not in safe_id_set:
                    safe_id_set.add(safe_id)
                    file_info = {
                        "safe_id": safe_id,
                        "objects": []
                    }
                    response_dict["files"].append(file_info)

                resp = {
                    "id": raw.object_name.split('/')[-1],
                    "content_path": (raw.object_name).replace(self._s3.CONTENT_PATH, "safe", 1)+"/content",
                    "name": self._s3.object().get_stat(raw.object_name).metadata[f'X-Amz-Meta-{self._s3.object().METADATA_OBJECT_NAME}'], # type: ignore
                    "updated_at": int(datetime.datetime.fromisoformat(str(raw.last_modified)).timestamp()),
                    "size": raw.size
                }
                file_info["objects"].append(resp)

            self.__response = response_dict
            self._status_code = OK
        except ValueError:
            self._status_code = BAD_REQUEST
        finally:
            await self._connection.close()