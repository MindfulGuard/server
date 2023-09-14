import tomli

from mypass.core.configuration.nestings.authentication import Totp, Public
from mypass.core.configuration.nestings.safe import Lengths

class ServerConfiguration:
    __PATH_TO_SERVER_CONFIGURATION: str = 'mypass/core/configuration/package/server_configuration.toml'
    def __init__(self):
        with open(self.__PATH_TO_SERVER_CONFIGURATION, "rb") as f:
            self.__cfg = tomli.load(f)
    def read_configuration(self, block: str, key: str) -> str:
        keys = block.split('.')  # Dividing the string into keys
        current = self.__cfg

        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return ""  # If the key is not found, return an empty string

        # Now current contains the value at the specified path
        return current.get(key, "")

class PgSql:
    def __init__(self,server_configuration:ServerConfiguration):
        self.__block:str = 'pgsql'
        self.__config:ServerConfiguration = server_configuration
    def get_host(self)->str:
        return self.__config.read_configuration(self.__block,'host')
    def get_port(self)->str:
        return self.__config.read_configuration(self.__block,'port')
    def get_database(self)->str:
        return self.__config.read_configuration(self.__block,'database')
    def get_user(self)->str:
        return self.__config.read_configuration(self.__block,'user')
    def get_password(self)->str:
        return self.__config.read_configuration(self.__block,'password')

class Authentication:
    def __init__(self,server_configuration:ServerConfiguration):
        self.__block:str = 'authentication'
        self.__config:ServerConfiguration = server_configuration
    def get_registration(self)->bool:
        return bool(self.__config.read_configuration(self.__block,'registration'))
    def get_token_expiration_default(self)->int:
        """N(minutes)"""
        return int(self.__config.read_configuration(self.__block,'token_expiration_default'))
    def public(self):
        return Public(self.__block,self.__config)
    def totp(self):
        return Totp(self.__block,self.__config)

class Safe:
    def __init__(self,server_configuration:ServerConfiguration):
        self.__block:str = 'safe'
        self.__config:ServerConfiguration = server_configuration
    def lengths(self):
        return Lengths(self.__block,self.__config)