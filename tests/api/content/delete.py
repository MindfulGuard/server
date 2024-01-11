from typing import Any
from fastapi.testclient import TestClient
from mindfulguard.__main__ import app

class ContentDeleteApi:
    def __init__(
        self,
        path: str,
    ) -> None:
        self.__client = TestClient(app)
        self.__path: str=  path

    def execute(self, headers: dict[str, str], body: dict[str, Any], path_to_content: str):
        return self.__client.request('DELETE', f"{self.__path}/{path_to_content}", data = body,  headers = headers)