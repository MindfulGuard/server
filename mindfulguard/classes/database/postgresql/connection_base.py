from abc import ABC, abstractmethod
import os


class PostgreSqlConnectionBase(ABC):
    def __init__(self):
        self._host: str = os.environ.get('DATABASE_HOST', 'localhost')
        self._port: str = os.environ.get('DATABASE_PORT', '5432')
        self._DATABASE: str = "mindfulguard_production"
        self._user: str = os.environ.get('DATABASE_USER', '')
        self._password: str = os.environ.get('DATABASE_PASSWORD', '')
        self.connection = None

    @abstractmethod
    def open(self) -> None:...

    @abstractmethod
    def close(self) -> None:...