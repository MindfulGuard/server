from typing import Annotated
from fastapi import APIRouter, Form, Header, Request, Response

from mypass.authentication import Authentication
from mypass.safe import Safe


router = APIRouter()

@router.post("/create")
async def create_safe(
    name:Annotated[str, Form()], 
    description:Annotated[str, Form()],
    user_agent: Annotated[str, Header()],
    request: Request,
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
    ):
    auth = Authentication()
    safe = Safe()
    await auth.update_token_info(token,user_agent,request)
    return await safe.create(token,name,description,response)

@router.get("/get")
async def get_safe(
    user_agent: Annotated[str, Header()],
    request: Request,
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
    ):
    auth = Authentication()
    safe = Safe()
    await auth.update_token_info(token,user_agent,request)
    return await safe.get(token,response)

@router.put("/udpate")
async def update_safe(
    id:Annotated[str, Form()],
    name:Annotated[str, Form()],
    description:Annotated[str, Form()],
    user_agent: Annotated[str, Header()],
    request: Request,
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
    ):
    auth = Authentication()
    safe = Safe()
    await auth.update_token_info(token,user_agent,request)
    return await safe.update(token,id,name,description,response)