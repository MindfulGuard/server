from typing import Annotated
from fastapi import Form
from pydantic import BaseModel


class SignInModel(BaseModel):
    email:Annotated[str, Form()]
    secret_string:Annotated[bytes, Form()]
    login:Annotated[str, Form()]