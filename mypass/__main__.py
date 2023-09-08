from typing import Annotated
from fastapi import  FastAPI, Form, Header, Request, Response
from mypass.authentication import Authentication
from mypass.settings import *

app = FastAPI(docs_url=None, redoc_url=None)

@app.post(VERSION1+PATH_AUTH+"/sign_up")
async def sign_up(email: Annotated[str, Form()],
                  login: Annotated[str, Form()],
                  secret_string:Annotated[str, Form()],
                  request: Request,
                  response:Response
):
    auth = Authentication()
    return await auth.sign_up(email,login,secret_string,request,response)

@app.post(VERSION1+PATH_AUTH+"/sign_in")
async def sign_in(
    email: Annotated[str, Form()],
    secret_string:Annotated[str, Form()],
    expiration:Annotated[int, Form()],
    user_agent: Annotated[str, Header()],
    request: Request,response:Response
):
    auth = Authentication()
    return await auth.sign_in(email,secret_string,user_agent,expiration,request,response)

@app.get(VERSION1+PATH_AUTH+"/config")
def get_config_auth(response:Response):
    auth = Authentication()
    return auth.get_config(response)

@app.delete(VERSION1 + PATH_AUTH + "/sign_out")
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

@app.get(VERSION1 + PATH_AUTH + "/sessions")
async def sessions(
    user_agent: Annotated[str, Header()],
    request: Request,
    response: Response,
    token: str = Header(default=None, alias="Authorization")
):
    auth = Authentication()
    await auth.update_token_info(token,user_agent,request)
    return await auth.get_tokens(token, response)