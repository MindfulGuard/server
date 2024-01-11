from typing import Literal
from fastapi.testclient import TestClient
from mindfulguard.__main__ import app

class SignInApi:
    def __init__(
        self,
        path: str,
    ) -> None:
        self.__client = TestClient(app)
        self.__path: str=  path

    def execute(self, headers: dict[str, str], body: dict[str, str], type: Literal['basic', 'backup', 'None']):
        if type == 'basic':
            return self.__client.post(self.__path+ "/sign_in?type=basic", data = body, headers = headers)
        elif type == 'backup':
            return self.__client.post(self.__path+ "/sign_in?type=backup", data = body, headers = headers)
        else:
            return self.__client.post(self.__path+ f"/sign_in?type={type}", data = body, headers = headers)