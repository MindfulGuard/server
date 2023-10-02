from mindfulguard.core.configuration import Authentication, Item, ServerConfiguration
from mindfulguard.core.response_status_codes import *

class Get:
    def execute(self):
        return ReadConfigs()

class ReadConfigs():
    def __init__(self):
        self.__server_conf = ServerConfiguration()
        self.__auth_conf = Authentication(self.__server_conf)
        self.__item_conf = Item(self.__server_conf)
    
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
            },
            OK)
    
    def item(self):
        return ({
            "categories":self.__item_conf.categories().get_array(),
            "types":self.__item_conf.types().get_array()
        },OK)