from fastapi import  Request, Response
from mypass.authentication import Authentication

from mypass.core.models import SignInModel
from mypass.performers.authentication import Auth
from mypass.settings import *


@app.get(VERSION1+PATH_AUTH+"/sign_up")
async def sign_up(body:SignInModel,request: Request,response:Response):
    auth = Authentication()
    return await auth.sign_up(body,request,response)