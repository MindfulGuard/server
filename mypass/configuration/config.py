import configparser
from typing import Any


class Configuration:
    _PATH_TO_SERVER_CONFIGURATION: str = 'mypass/configuration/server_configuration.ini'

    def server_configuration(self, key: str, value: str) -> str:
        cfg = configparser.ConfigParser()
        cfg.read(self._PATH_TO_SERVER_CONFIGURATION)
        return cfg.get(key, value)