from pydantic import BaseModel


class SignInModel(BaseModel):
    email:str
    secret_string:bytes
    login:bytes