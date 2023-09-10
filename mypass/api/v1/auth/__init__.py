from typing import Annotated
from fastapi import  APIRouter, Form, Header, Request, Response
from mypass.authentication import Authentication

router = APIRouter()

@router.post("/sign_up")
async def sign_up(email: Annotated[str, Form()],
                  login: Annotated[str, Form()],
                  secret_string:Annotated[str, Form()],
                  request: Request,
                  response:Response
):
    auth = Authentication()
    return await auth.sign_up(email,login,secret_string,request,response)

@router.post("/sign_in")
async def sign_in(
    email: Annotated[str, Form()],
    secret_string:Annotated[str, Form()],
    expiration:Annotated[int, Form()],
    user_agent: Annotated[str, Header()],
    request: Request,response:Response
):
    auth = Authentication()
    return await auth.sign_in(email,secret_string,user_agent,expiration,request,response)

@router.get("/config")
async def get_config_auth(response:Response):
    auth = Authentication()
    return auth.get_config(response)

@router.delete("/sign_out")
async def sign_out(
    id: Annotated[str, Form()],
    user_agent: Annotated[str, Header()],
    request: Request,
    response: Response,
    token: str = Header(default=None, alias="Authorization")
):
    auth = Authentication()
    await auth.update_token_info(token,user_agent,request)
    return await auth.sign_out(token, id, response)

@router.get("/sessions")
async def sessions(
    user_agent: Annotated[str, Header()],
    request: Request,
    response: Response,
    token: str = Header(default=None, alias="Authorization")
):
    auth = Authentication()
    await auth.update_token_info(token,user_agent,request)
    return await auth.get_tokens(token, response)