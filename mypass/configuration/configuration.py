from mypass.core.configuration import Authentication, ServerConfiguration
from mypass.core.response_status_codes import *


class Get:
    def execute(self):
        return ReadConfigs()

class ReadConfigs():
    def __init__(self):
        self.__server_conf = ServerConfiguration()
        self.__auth_conf = Authentication(self.__server_conf)
    
    def authentication(self):
        return ({
            "pbkdf2":{
            "SHA":self.__auth_conf.public().configuration().pbkdf2().get_sha(),
            "iterations":self.__auth_conf.public().configuration().pbkdf2().get_iterations()
            },
            "aes256":{
                "mode":self.__auth_conf.public().configuration().get_aes_mode()
            },
            "password_rule":self.__auth_conf.public().configuration().get_password_rule()
            },OK)