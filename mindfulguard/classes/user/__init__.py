from http.client import OK
from typing import Any
from fastapi import Response
from mindfulguard.classes.responses import Responses
from mindfulguard.classes.user.settings import UserSettings

class User:
    def __init__(self, response: Response) -> None:
        self.__responses = Responses()
        self.__response: Response = response

    async def get_information(self, token: str) -> dict[str, Any]:
        from mindfulguard.user import User as UserClass
        obj = UserClass().information()
        await obj.execute(token)
        
        self.__response.status_code = obj.status_code
        if obj.status_code != OK:
            return self.__responses.default().get(obj.status_code)
        
        response: dict[str, Any] = {
            "tokens": obj.tokens,
            "count_tokens": len(obj.tokens),
            "information": {
                "username": obj.login,
                "created_at": obj.created_at,
                "ip": obj.reg_ip
            }
        }
        return response
    
    def settings(self) -> UserSettings:
        return UserSettings(self.__responses, self.__response)