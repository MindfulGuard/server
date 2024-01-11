from typing import Any
from fastapi.testclient import TestClient
from mindfulguard.__main__ import app

class UserDeleteApi:
    def __init__(
        self,
        path: str,
    ) -> None:
        self.__client = TestClient(app)
        self.__path: str=  path

    def execute(self, headers: dict[str, str], body: dict[str, Any]):
        return self.__client.request("DELETE", self.__path + "/settings", data = body, headers = headers)