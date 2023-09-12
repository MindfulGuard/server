"""
from fastapi.testclient import TestClient
from mypass.__main__ import app
from tests.api.test_auth import sign_in

client_safe = TestClient(app)

SAFE_PATH_V1 = "/v1/safe"

def test_create():
    data = {
        "name": "safe1",
        "description": "hello its my 1 safe",
    }
    headers = {
        'Authorization': 'Bearer ' + sign_in(),
        'User-Agent': 'python/win',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Real-IP': '192.168.1.1'
    }
    response = client_safe.post(SAFE_PATH_V1 + "/create", data=data, headers=headers)
    assert response.status_code == 200, sign_in()
"""