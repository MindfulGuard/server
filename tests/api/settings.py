from fastapi.testclient import TestClient

from mindfulguard.__main__ import app

client = TestClient(app)

AUTH_PATH_V1 = "/v1/auth"
SAFE_PATH_V1 = "/v1/safe"
PUBLIC_PATH_V1 = "/v1/public"

def get_headers(token:str):
    headers = {
        'Authorization': 'Bearer ' + token,
        'User-Agent': 'python/win',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Real-IP': '192.168.1.1'
    }
    return headers