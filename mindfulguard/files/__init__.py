from io import BytesIO
from unittest import result
from fastapi import Request, Response, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from mindfulguard.core.languages import Language
from mindfulguard.core.languages.responses import Responses
from mindfulguard.core.response_status_codes import BAD_REQUEST, OK, UNAUTHORIZED
from mindfulguard.files.executors.delete import Delete
from mindfulguard.files.executors.download import Download
from mindfulguard.files.executors.get import Get

from mindfulguard.files.executors.put import Put


class Files:
    async def put_files(
            self,
            token:str,
            safe_id:str,
            request:Request,
            response:Response
        ):
        fput = Put(token)
        status_code:int = await fput.auth(safe_id)
        if status_code != OK:
            response.status_code = status_code
            return status_code

        files = await request.form()
        files_list:list[UploadFile] = [value for key, value in files.multi_items() if key == 'files']
        fp = await fput.execute(safe_id,files_list)
        response.status_code = fp
        return fp
    
    async def delete_files(
            self,
            token:str,
            safe_id:str,
            files:list[str],
            response:Response
        ):
        response.status_code = await Delete(token).execute(safe_id,files)
        return
    
    async def download_file(self,token:str,safe_id:str,file_name:str,response:Response):
        download = await Download(token).execute(safe_id,file_name)
        status_code = download[-1]
        response.status_code = status_code
        
        if status_code == OK:
            return StreamingResponse(
                BytesIO(download[0]),
                media_type="application/octet-stream",
                headers={
                    "Content-Disposition": f"attachment; {download[1]}"
                }
            )
        return None