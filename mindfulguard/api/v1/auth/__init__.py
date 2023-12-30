from typing import Annotated, Literal
from fastapi import  APIRouter, Form, Header, Query, Request, Response
from mindfulguard.classes.authentication import Authentication

router = APIRouter()

@router.post("/sign_up")
async def sign_up(
    login: Annotated[str, Form()],
    secret_string:Annotated[str, Form()],
    request: Request,
    response:Response
):
    auth = Authentication(response, request)
    return await auth.sign_up(login,secret_string)

@router.post("/sign_in")
async def sign_in(
    login: Annotated[str, Form()],
    secret_string: Annotated[str, Form()],
    code: Annotated[str, Form()],
    expiration: Annotated[int, Form()],
    device: Annotated[str, Header()],
    request: Request,
    response: Response,
    type: str = Query(min_length=5, max_length=7)
):
    auth = Authentication(response, request)
    return await auth.sign_in(login, secret_string, device, expiration, type, code) # type: ignore

@router.delete("/sign_out/{id}")
async def sign_out(
    id: str,
    request: Request,
    response: Response,
    token: str = Header(default=None, alias="Authorization")
):
    auth = Authentication(response, request)
    return await auth.sign_out(token, id)