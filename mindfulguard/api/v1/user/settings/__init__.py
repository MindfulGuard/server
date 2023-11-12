from typing import Annotated
from fastapi import APIRouter, Form, Header, Query, Request, Response

from mindfulguard.authentication import Authentication
from mindfulguard.user import User

router = APIRouter()

@router.put("/auth/one_time_code")
async def settings_update_one_time_code(
    secret_string:Annotated[str, Form()],
    device: Annotated[str, Header()],
    request: Request,
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
    type:str  = Query(min_length=5, max_length=7)
    ):
    auth = Authentication()
    user = User()
    await auth.update_token_info(token,device,request)
    return await user.settings_one_time_codes(token,secret_string,type,response)

@router.put("/auth/secret_string")
async def settings_update_secret_string(
    login:Annotated[str, Form()],
    old_secret_string:Annotated[str, Form()],
    new_secret_string:Annotated[str, Form()],
    code:Annotated[str, Form()],
    device: Annotated[str, Header()],
    request: Request,
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
    ):
    auth = Authentication()
    user = User()
    await auth.update_token_info(token,device,request)
    return await user.settings_secret_string(
        token,
        login,
        old_secret_string,
        new_secret_string,
        code,
        response
    )

@router.delete("/")
async def delete_user(
    login:Annotated[str, Form()],
    secret_string:Annotated[str, Form()],
    code:Annotated[str, Form()],
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
    ):
    user = User()
    return await user.delete_user(
        token,
        login,
        secret_string,
        code,
        response
    )