from typing import Annotated
from fastapi import APIRouter, Form, Header, Request, Response, UploadFile
from mindfulguard.authentication import Authentication
from mindfulguard.files import Files


router = APIRouter()

@router.post("/{safe_id}/content")
async def upload_files(
    safe_id: str,
    request:Request,
    response: Response,
    device: Annotated[str, Header()],
    token: str = Header(default=None, alias="Authorization"),
):
    auth = Authentication()
    obj = Files()
    
    await auth.update_token_info(token, device, request)

    return await obj.put_files(
        token,
        safe_id,
        request,
        response
    )

@router.get("/{safe_id}/{file_name}/content")
async def download_file(
    safe_id:str,
    file_name:str,
    request:Request,
    response: Response,
    device: Annotated[str, Header()],
    token:str = Header(default=None, alias="Authorization"),
):
    auth = Authentication()
    obj = Files()
    
    await auth.update_token_info(token, device, request)

    return await obj.download_file(
        token,
        safe_id,
        file_name,
        response
    )

@router.delete("/{safe_id}/content")
async def delete_files(
    safe_id:str,
    files:Annotated[list[str], Form()],
    request:Request,
    response: Response,
    device: Annotated[str, Header()],
    token:str = Header(default=None, alias="Authorization"),
):
    auth = Authentication()
    obj = Files()
    
    await auth.update_token_info(token, device, request)

    return await obj.delete_files(
        token,
        safe_id,
        files,
        response
    )