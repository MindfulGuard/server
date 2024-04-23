from http.client import OK
from typing import Any, Literal
from fastapi import Request, Response
from mindfulguard.authentication.sign_out import SignOut
from mindfulguard.authentication.sign_in import SignIn
from mindfulguard.authentication.sign_up import SignUp
from mindfulguard.classes.responses import HttpResponse


class Authentication:
    def __init__(self, response: Response, request: Request) -> None:
        self.__http_response = HttpResponse()
        self.__response = response
        self.__request = request

    async def sign_up(self, login: str, secret_string: str, confirm: bool = False):
        obj = SignUp(self.__request)
        await obj.execute(login, secret_string, confirm)
        self.__response.status_code = obj.status_code
        
        response: dict[str, Any] = {}

        if obj.status_code != OK:
            return self.__http_response.get(obj.status_code).to_json()

        response['secret_code'] = obj.secret_code
        response['backup_codes'] = obj.backup_codes
        return response

    async def sign_in(
        self,
        login: str,
        secret_string: str,
        device: str,
        expiration: int,
        type: Literal['backup', 'basic'],
        code: str
    ):
        obj = SignIn(self.__request)
        await obj.execute(login, secret_string, device, expiration, type, code)
        self.__response.status_code = obj.status_code
        response: dict[str, str] = {}

        if obj.status_code != OK:
            return self.__http_response.get(obj.status_code).to_json()
        
        response['token'] = obj.token
        return response
    
    async def sign_out(
        self,
        token: str,
        token_id: str
    ):
        obj = SignOut(self.__request)
        await obj.execute(token, token_id)
        self.__response.status_code = obj.status_code

        response = self.__http_response.get(obj.status_code).to_json()
        return response