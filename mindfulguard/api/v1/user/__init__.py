from typing import Annotated
from fastapi import APIRouter, Form, Header, Query, Request, Response

from mindfulguard.authentication import Authentication
from mindfulguard.user import User

router = APIRouter()

@router.get("/")
async def get_info(
    user_agent: Annotated[str, Header()],
    request: Request,
    response: Response,
    token: str = Header(default=None, alias="Authorization")
):
    auth = Authentication()
    await auth.update_token_info(token,user_agent,request)
    user_info = User()
    return await user_info.get_info(token, response)