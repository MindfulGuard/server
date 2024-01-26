from http.client import CONFLICT, OK
from typing import Literal
from fastapi import Request, Response
from mindfulguard.authentication.sign_out import SignOut
from mindfulguard.authentication.sign_in import SignIn
from mindfulguard.authentication.sign_up import SignUp
from mindfulguard.classes.responses import Responses


class Authentication:
    def __init__(self, response: Response, request: Request) -> None:
        self.__responses = Responses()
        self.__response = response
        self.__request = request

    async def sign_up(self, login: str, secret_string: str, confirm: bool = False):
        obj = SignUp(self.__request)
        await obj.execute(login, secret_string, confirm)
        self.__response.status_code = obj.status_code
        
        response = self.__responses.default(
            ok = self.__responses.custom().registration_was_successful,
            service_is_not_available = self.__responses.custom().registration_not_allowed,
            conflict = self.__responses.custom().user_already_exists
        ).get(obj.status_code)

        if obj.status_code != OK:
            if obj.status_code == CONFLICT:
                response['secret_code'] = None
                response['backup_codes'] = None
                return response
            else:
                return response

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
        response = self.__responses.default(
            ok = self.__responses.custom().successful_login,
            not_found= self.__responses.custom().user_not_found
        ).get(obj.status_code)

        if obj.status_code != OK:
            return response
        
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
        response = self.__responses.default(
            ok = self.__responses.custom().session_token_has_been_deleted,
            not_found= self.__responses.custom().failed_to_delete_token
        ).get(obj.status_code)
        return response