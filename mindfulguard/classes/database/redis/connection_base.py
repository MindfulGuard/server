from abc import ABC
import os
from typing import Any


class RedisConnectionBase(ABC):
    def __init__(self):
        self._host: str = os.environ.get('REDIS_HOST', 'localhost')
        self._port: int = int(os.environ.get('REDIS_PORT', '6379'))
        self._username: str = os.environ.get('REDIS_USERNAME', '')
        self._password: str = os.environ.get('REDIS_PASSWORD', '')
        self._ld: int = int(os.environ.get('REDIS_LD', '0'))
        self.connection = Any