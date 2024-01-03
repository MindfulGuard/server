from abc import ABC, abstractmethod
from typing import Any
from mindfulguard.settings import Settings


class ConfigurationBase(ABC):
    def __init__(self) -> None:
        self._status_code: int
        self._settings = Settings()
        self._response: dict[str, Any] = {}

    @abstractmethod
    async def execute(self) -> None:...

    @property
    def status_code(self) -> int:
        return self._status_code