from typing import Annotated
from fastapi import  APIRouter, Form, Header, Query, Request, Response
from mindfulguard.authentication import Authentication

router = APIRouter()

@router.post("/sign_up")
async def sign_up(login: Annotated[str, Form()],
                  secret_string:Annotated[str, Form()],
                  request: Request,
                  response:Response
):
    auth = Authentication()
    return await auth.sign_up(login,secret_string,request,response)

@router.post("/sign_in")
async def sign_in(
    login: Annotated[str, Form()],
    secret_string:Annotated[str, Form()],
    code:Annotated[str, Form()],
    expiration:Annotated[int, Form()],
    user_agent: Annotated[str, Header()],
    request: Request,
    response:Response,
    type:str  = Query(min_length=5, max_length=7)
):
    auth = Authentication()
    return await auth.sign_in(login,secret_string,code,type,user_agent,expiration,request,response)

@router.delete("/sign_out/{id}")
async def sign_out(
    id:str,
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