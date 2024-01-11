from http.client import OK
from fastapi.testclient import TestClient
from mindfulguard.__main__ import app
from tests.api.paths import PUBLIC_PATH_V1


def test_get_configuration_api():
    client = TestClient(app)
    assert client.get(PUBLIC_PATH_V1+"/configuration").status_code == OK