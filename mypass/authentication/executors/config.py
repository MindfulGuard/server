from mypass.core.configuration import Authentication, ServerConfiguration
from mypass.core.response_status_codes import OK


class Config:
    def execute(self):
        return PrivateConfigs()

class PrivateConfigs():
    def pbkdf2(self):
        server_conf = ServerConfiguration()
        auth_conf = Authentication(server_conf)
        return ({
            "client_SHA":auth_conf.get_sha_client(),
            "iterations":auth_conf.get_iterations()
        },OK)