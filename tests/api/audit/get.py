from fastapi.testclient import TestClient
from mindfulguard.__main__ import app

class AuditGetApi:
    def __init__(
        self,
        path: str,
    ) -> None:
        self.__client = TestClient(app)
        self.__path: str=  path

    def execute(self, headers: dict[str, str]):
        return self.__client.get(f"{self.__path}/audit?page=1", headers = headers)