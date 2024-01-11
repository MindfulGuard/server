from typing import Literal
from fastapi.testclient import TestClient
from mindfulguard.__main__ import app

class ItemUpdateApi:
    def __init__(
        self,
        path: str,
    ) -> None:
        self.__client = TestClient(app)
        self.__path: str=  path

    def execute(self, headers: dict[str, str], body: dict[str, str], safe_id: str, item_id: str):
        return self.__client.put(f"{self.__path}/{safe_id}/item/{item_id}", json = body, headers = headers)