from http.client import OK
from io import BytesIO
from fastapi import Request, Response, UploadFile
from fastapi.responses import StreamingResponse
from loguru import logger
from mindfulguard.files.delete import Delete
from mindfulguard.files.download import Download
from mindfulguard.files.upload import Upload


class Files:
    def __init__(self, response: Response) -> None:
        self.__response: Response = response
        logger.debug("Files class initialized with response: {}", response)

    async def upload(
        self,
        token: str,
        safe_id: str,
        request: Request
    ) -> None:
        logger.debug("Upload method called with token: {}, safe_id: {}", token, safe_id)
        obj = Upload()
        await obj.auth(token, safe_id)
        if obj.status_code != OK:
            logger.debug("Authorization failed with status code: {}", obj.status_code)
            self.__response.status_code = obj.status_code
            return

        files = await request.form()
        files_list: list[UploadFile] = [value for key, value in files.multi_items() if key == 'files']  # type: ignore
        logger.debug("Files to upload: {}", [file.filename for file in files_list])
        
        await obj.execute(files_list)
        self.__response.status_code = obj.status_code
        logger.debug("Upload completed with status code: {}", obj.status_code)
        return
    
    async def download(
        self,
        token: str,
        safe_id: str,
        object_name: str
    ) -> (StreamingResponse | None):
        logger.debug("Download method called with token: {}, safe_id: {}, object_name: {}", token, safe_id, object_name)
        obj = Download()
        await obj.execute(token, safe_id, object_name)
        self.__response.status_code = obj.status_code
        if obj.status_code != OK:
            logger.debug("Download failed with status code: {}", obj.status_code)
            return

        logger.debug("Download successful for object_name: {}", obj.name)
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
        logger.debug("Delete method called with token: {}, safe_id: {}, files: {}", token, safe_id, files)
        obj = Delete()
        await obj.execute(token, safe_id, files)
        self.__response.status_code = obj.status_code
        logger.debug("Delete completed with status code: {}", obj.status_code)
        return
