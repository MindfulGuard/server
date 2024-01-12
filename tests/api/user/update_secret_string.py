from typing import Literal, Any
from fastapi.testclient import TestClient
from mindfulguard.__main__ import app

class UserUpdateSecretStringApi:
    def __init__(
        self,
        path: str,
    ) -> None:
        self.__client = TestClient(app)
        self.__path: str=  path

    def execute(
        self, 
        headers: dict[str, str],
        body: dict[str, Any]
    ):
        return self.__client.put(
            f"{self.__path}/settings/auth/secret_string",
            headers = headers,
            data = body
        )