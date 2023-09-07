import tomli


class ServerConfiguration:
    __PATH_TO_SERVER_CONFIGURATION: str = 'mypass/core/configuration/package/server_configuration.toml'

    def read_configuration(self, key: str, value: str) -> str:
        with open(self.__PATH_TO_SERVER_CONFIGURATION, "rb") as f:
            cfg = tomli.load(f)
        return cfg[key][value]

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
    def get_iterations(self)->int:
        return int(self.__config.read_configuration(self.__block,'iterations'))
    def get_sha_client(self)->str:
        return self.__config.read_configuration(self.__block,'sha_client')

class Validation:
    def __init__(self,server_configuration:ServerConfiguration):
        self.__block:str = 'validation'
        self.__config:ServerConfiguration = server_configuration
    def get_login_length(self)->int:
        return int(self.__config.read_configuration(self.__block,'login_length'))
    def get_password_length(self)->int:
        return int(self.__config.read_configuration(self.__block,'password_length'))