from typing import Annotated, Any, Optional
from fastapi import APIRouter, Form, Header, Query, Request, Response
from mindfulguard.admin import Admin

from mindfulguard.authentication import Authentication

router = APIRouter()

@router.get("/users/all")
async def get_info(
    user_agent: Annotated[str, Header()],
    request: Request,
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
    page:int  = Query()
):
    auth = Authentication()
    await auth.update_token_info(token,user_agent,request)
    admin = Admin()
    return await admin.get_users(token, page, response)

@router.get("/users/search")
async def search(
    value: Annotated[str, Form()],
    user_agent: Annotated[str, Header()],
    request: Request,
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
    by:str  = Query(),
):
    auth = Authentication()
    await auth.update_token_info(token,user_agent,request)
    admin = Admin()
    return await admin.search_users(token, by, value, response)

@router.get("/settings")
async def get_settings(
    user_agent: Annotated[str, Header()],
    request: Request,
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
):
    auth = Authentication()
    await auth.update_token_info(token,user_agent,request)
    admin = Admin()
    return await admin.get_settings(token, response)


@router.put("/settings")
async def update_settings(
    value:Annotated[Optional[str], Form()],
    user_agent: Annotated[str, Header()],
    request: Request,
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
    key:str  = Query(),
):
    auth = Authentication()
    await auth.update_token_info(token,user_agent,request)
    admin = Admin()
    return await admin.update_settings(token,key,value, response)

@router.post("/users")
async def create_user(
    login: Annotated[str, Form()],
    secret_string:Annotated[str, Form()],
    user_agent: Annotated[str, Header()],
    request: Request,
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
):
    auth = Authentication()
    await auth.update_token_info(token,user_agent,request)
    admin = Admin()
    return await admin.create_user(
        token,
        login,
        secret_string,
        request,
        response
    )

@router.delete("/users")
async def delete_user(
    user_agent: Annotated[str, Header()],
    request: Request,
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
    id = Query(),
):
    auth = Authentication()
    await auth.update_token_info(token,user_agent,request)
    admin = Admin()
    return await admin.delete_user(token, id, response)