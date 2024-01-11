from fastapi.testclient import TestClient
import httpx
from mindfulguard.__main__ import app

class ContentDownloadApi:
    def __init__(
        self,
        path: str,
    ) -> None:
        self.__client = TestClient(app)
        self.__path: str=  path

    def execute(self, headers: dict[str, str], path_to_content: str):
        return self.__client.get(f"{self.__path}/{path_to_content}", headers = headers)