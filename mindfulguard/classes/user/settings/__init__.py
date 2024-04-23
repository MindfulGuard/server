from http.client import OK
from typing import Any, Literal
from fastapi import Response
from mindfulguard.classes.responses import HttpResponse

class UserSettings:
    def __init__(self, responses: HttpResponse, response: Response) -> None:
        self.__http_response: HttpResponse = responses
        self.__response: Response = response 

    async def update_one_time_codes(
        self,
        token: str,
        secret_string: str,
        type: Literal['basic', 'backup']
    ) -> dict[str, Any]:
        from mindfulguard.user import User
        obj = User().settings().update_one_time_codes()
        await obj.execute(
            token,
            secret_string,
            type
        )
        self.__response.status_code = obj.status_code

        if obj.status_code != OK:
            return self.__http_response.get(obj.status_code).to_json()

        response: dict[str, Any] = {}
        response['data'] = obj.response
        return response
    
    async def update_secret_string(
        self,
        token: str,
        old_secret_string: str,
        new_secret_string: str,
        one_time_code: str
    ) -> dict[str, Any]:
        from mindfulguard.user import User
        obj = User().settings().update_secret_string()
        await obj.execute(
            token,
            old_secret_string,
            new_secret_string,
            one_time_code
        )
        self.__response.status_code = obj.status_code
        response = self.__http_response.get(obj.status_code).to_json()

        return response
    
    async def delete_account(
        self,
        token: str,
        secret_string: str,
        one_time_code: str
    ) -> dict[str, Any]:
        from mindfulguard.user import User
        obj = User().settings().delete_account()
        await obj.execute(
            token,
            secret_string,
            one_time_code
        )
        self.__response.status_code = obj.status_code
        response = self.__http_response.get(obj.status_code).to_json()

        return response