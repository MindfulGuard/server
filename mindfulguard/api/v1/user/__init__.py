from typing import Annotated
from fastapi import APIRouter, Form, Header, Query, Request, Response
from mindfulguard.classes.user import User

router = APIRouter()

@router.get("/")
async def get_info(
    response: Response,
    token: str = Header(default=None, alias="Authorization")
):
    user_info = User(response)
    return await user_info.get_information(token)