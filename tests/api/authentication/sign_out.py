from fastapi.testclient import TestClient
from mindfulguard.__main__ import app

class SignOutApi:
    def __init__(
        self,
        path: str,
    ) -> None:
        self.__client = TestClient(app)
        self.__path: str=  path

    def execute(self, headers: dict[str, str], token: str):
        return self.__client.delete(self.__path+ f"/sign_out/{token}", headers = headers)