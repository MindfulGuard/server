from typing import Annotated
from fastapi import APIRouter, Form, Header, Request, Response, UploadFile
from mindfulguard.classes.files import Files


router = APIRouter()

@router.post("/{safe_id}/content")
async def upload_files(
    safe_id: str,
    request:Request,
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
):
    obj = Files(response)

    return await obj.upload(
        token,
        safe_id,
        request
    )

@router.get("/{safe_id}/{file_name}/content")
async def download_file(
    safe_id:str,
    file_name:str,
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
):
    obj = Files(response)
    return await obj.download(
        token,
        safe_id,
        file_name
    )

@router.delete("/{safe_id}/content")
async def delete_files(
    safe_id:str,
    files:Annotated[list[str], Form()],
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
):
    obj = Files(response)
    return await obj.delete(
        token,
        safe_id,
        files
    )