from http.client import OK
from typing import Any
from fastapi import Response
from mindfulguard.classes.responses import HttpResponse

class AdminConfiguration:
    def __init__(
        self,
        response: Response,
        responses: HttpResponse,
        admin_class
    ) -> None:
        self.__http_response: HttpResponse = responses
        self.__response: Response = response
        self.__admin_class = admin_class

    async def get(self, token: str) -> dict[str, Any]:
        obj = self.__admin_class.configuration().get()
        await obj.execute(token)
        self.__response.status_code = obj.status_code

        if obj.status_code != OK:
            return self.__http_response.get(obj.status_code).to_json()

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
        return self.__http_response.get(obj.status_code).to_json()