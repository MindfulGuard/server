from http.client import OK
from io import BytesIO
from typing import Any
from fastapi import Request, Response, UploadFile
from fastapi.responses import StreamingResponse
from mindfulguard.files.delete import Delete
from mindfulguard.files.download import Download

from mindfulguard.files.upload import Upload


class Files:
    def __init__(self, response: Response) -> None:
        self.__response: Response = response

    async def upload(
        self,
        token: str,
        safe_id: str,
        request: Request
    ) -> None:
        obj = Upload()
        await obj.auth(token, safe_id)
        if obj.status_code != OK:
            self.__response.status_code = obj.status_code
            return

        files = await request.form()
        files_list: list[UploadFile] = [value for key, value in files.multi_items() if key == 'files'] # type: ignore
        await obj.execute(
            files_list
        )
        self.__response.status_code = obj.status_code
        return
    
    async def download(
        self,
        token: str,
        safe_id: str,
        object_name: str
    ) -> (StreamingResponse | None):
        obj = Download()
        await obj.execute(
            token,
            safe_id,
            object_name
        )
        self.__response.status_code = obj.status_code
        if obj.status_code != OK:
            return

        return StreamingResponse(
                BytesIO(obj.data),
                media_type="application/octet-stream",
                headers={
                    "Content-Disposition": f"attachment; filename={obj.name}"
                }
        )
    
    async def delete(
        self,
        token: str,
        safe_id: str,
        files: list[str]
    ) -> None:
        obj = Delete()
        await obj.execute(
            token,
            safe_id,
            files
        )
        self.__response.status_code = obj.status_code
        return