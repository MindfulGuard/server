import tomli

from mypass.core.configuration.nestings.authentication import Public

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
    def get_smtp(self)->str:
        return self.__config.read_configuration(self.__block,'smtp')
    def get_blocked_domains(self)->list[str]:
        return list[str](self.__config.read_configuration(self.__block,'blocked_domains'))
    def get_token_expiration_default(self)->int:
        """N(minutes)"""
        return int(self.__config.read_configuration(self.__block,'token_expiration_default'))
    def public(self):
        return Public(self.__block,self.__config)