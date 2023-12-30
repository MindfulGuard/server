from typing import Annotated
from fastapi import APIRouter, Form, Header, Query, Request, Response
from mindfulguard.classes.user import User

router = APIRouter()

@router.put("/auth/one_time_code")
async def settings_update_one_time_code(
    secret_string:Annotated[str, Form()],
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
    type: str  = Query(min_length=5, max_length=7)
    ):
    user = User(response).settings()
    return await user.update_one_time_codes(
        token,
        secret_string,
        type # type: ignore
    )

@router.put("/auth/secret_string")
async def settings_update_secret_string(
    old_secret_string:Annotated[str, Form()],
    new_secret_string:Annotated[str, Form()],
    code:Annotated[str, Form()],
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
    ):
    user = User(response).settings()
    return await user.update_secret_string(
        token,
        old_secret_string,
        new_secret_string,
        code
    )

@router.delete("/")
async def delete_user(
    secret_string:Annotated[str, Form()],
    code:Annotated[str, Form()],
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
    ):
    user = User(response).settings()
    return await user.delete_account(
        token,
        secret_string,
        code,
    )