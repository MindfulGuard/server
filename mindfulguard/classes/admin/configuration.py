from http.client import OK
from typing import Any
from fastapi import Response
from mindfulguard.classes.responses import Responses

class AdminConfiguration:
    def __init__(
        self,
        response: Response,
        responses: Responses,
        admin_class
    ) -> None:
        self.__responses: Responses = responses
        self.__response: Response = response
        self.__admin_class = admin_class

    async def get(self, token: str) -> dict[str, Any]:
        obj = self.__admin_class.configuration().get()
        await obj.execute(token)
        self.__response.status_code = obj.status_code

        if obj.status_code != OK:
            return self.__responses.default().get(obj.status_code)

        return obj.response
    
    async def update(
        self,
        token: str,
        key: str,
        value: str
    ) -> dict[str, Any]:
        obj = self.__admin_class.configuration().update()
        await obj.execute(
            token,
            key,
            value
        )
        self.__response.status_code = obj.status_code
        return self.__responses.default(
            ok = {
            
            },
            internal_server_error = self.__responses.custom().get("failed_to_update_settings")
        ).get(obj.status_code)