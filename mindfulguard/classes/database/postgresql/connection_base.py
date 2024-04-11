from abc import ABC, abstractmethod
import os


class PostgreSqlConnectionBase(ABC):
    def __init__(self):
        self._host: str = os.environ.get('POSTGRES_HOST', '')
        self._port: str = os.environ.get('POSTGRES_PORT', '')
        self._database: str = os.environ.get('POSTGRES_DB', '')
        self._user: str = os.environ.get('POSTGRES_USER', '')
        self._password: str = os.environ.get('POSTGRES_PASSWORD', '')
        self.connection = None

    @abstractmethod
    def open(self) -> None:...

    @abstractmethod
    def close(self) -> None:...