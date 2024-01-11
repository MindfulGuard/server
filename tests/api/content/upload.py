from typing import Literal
from fastapi.testclient import TestClient
import httpx
from mindfulguard.__main__ import app

class ContentUploadApi:
    def __init__(
        self,
        path: str,
    ) -> None:
        self.__client = TestClient(app)
        self.__path: str=  path

    def execute(self, headers: dict[str, str], file: httpx._types.RequestFiles, safe_id: str):
        return self.__client.post(f"{self.__path}/{safe_id}/content", files = file, headers = headers)