from mypass.core.configuration.utils import concatenate_with_dot

"""
!!!Do not import "mypass.core.configuration" module, due to the "circular dependency of modules" error!!!

server_configuration is type(ServerConfiguration)
"""

class Public:
    def __init__(self,root_block:str,server_configuration):
        self.__block:str = concatenate_with_dot(root_block,"public")
        self.__config = server_configuration
    def configuration(self):
        return Configuration(self.__block,self.__config)
    def lengths(self):
        return Lengths(self.__block,self.__config)
    
class Configuration:
    def __init__(self,root_block:str,server_configuration):
        self.__block:str = concatenate_with_dot(root_block,"configuration")
        self.__config = server_configuration
    def get_password_rule(self)->str:
        return self.__config.read_configuration(self.__block,'password_rule')
    def get_iterations(self)->int:
        return int(self.__config.read_configuration(self.__block,'iterations'))
    def get_sha_client(self)->str:
        return self.__config.read_configuration(self.__block,'sha_client')

class Lengths:
    def __init__(self,root_block:str,server_configuration):
        self.__block:str = concatenate_with_dot(root_block,"lengths")
        self.__config = server_configuration
    def get_token_length(self)->int:
        return self.__config.read_configuration(self.__block,'token_length')
    def get_login_length(self)->int:
        return self.__config.read_configuration(self.__block,'login_length')
    def get_secret_string_length(self)->int:
        return self.__config.read_configuration(self.__block,'secret_string_length')