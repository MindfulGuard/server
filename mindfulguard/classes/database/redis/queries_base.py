from abc import ABC, abstractmethod
from typing import Any

from mindfulguard.database.redis.connection import RedisConnection


class RedisQueriesBase(ABC):
    def __init__(self, connection: RedisConnection) -> None:
        self._connection: RedisConnection = connection
        self._status_code: int
        self._response: Any
    
    @abstractmethod
    async def execute(self) -> None:...

    @property
    def status_code(self) -> int:
        return self._status_code