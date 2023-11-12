from typing import Annotated
from fastapi import APIRouter, Form, Header, Request, Response

from mindfulguard.authentication import Authentication
from mindfulguard.safe import Safe


router = APIRouter()

@router.post("/")
async def create_safe(
    name:Annotated[str, Form()], 
    description:Annotated[str, Form()],
    device: Annotated[str, Header()],
    request: Request,
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
    ):
    auth = Authentication()
    safe = Safe()
    await auth.update_token_info(token,device,request)
    return await safe.create(token,name,description,response)

@router.put("/{id}")
async def update_safe(
    id,
    name:Annotated[str, Form()],
    description:Annotated[str, Form()],
    device: Annotated[str, Header()],
    request: Request,
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
    ):
    auth = Authentication()
    safe = Safe()
    await auth.update_token_info(token,device,request)
    return await safe.update(token,id,name,description,response)

@router.delete("/{id}")
async def delete_safe(
    id,
    device: Annotated[str, Header()],
    request: Request,
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
    ):
    auth = Authentication()
    safe = Safe()
    await auth.update_token_info(token,device,request)
    return await safe.delete(token,id,response)