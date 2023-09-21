from tests.api.settings import *

class TestPublic:
    def get_config(self):
        response = client.get(PUBLIC_PATH_V1+ "/configuration")
        try:
            return (response.json()["authentication"]["password_rule"],response.status_code)
        except KeyError:
            return ("",response.status_code)
    
    def test_config(self):
        assert self.get_config()[1] == 200