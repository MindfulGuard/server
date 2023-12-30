from http.client import OK
from typing import Any
from mindfulguard.classes.configuration.base import ConfigurationBase


class ConfigurationPublic(ConfigurationBase):
    def __init__(self) -> None:
        super().__init__()
        self.__settings: dict[str, Any] = {}
    
    @property
    def response(self) -> dict[str, Any]:
        return self._response

    @property
    def settings(self) -> dict[str, Any]:
        return self.__settings

    async def execute(self) -> None:
        await self._settings.execute()
        obj = {
            "password_rule": self._settings.response['password_rule'],
            "item_categories": self._settings.response['item_categories'],
            "item_types": self._settings.response['item_types']
        }
        self.__settings = self._settings.response
        self._response = obj
        self._status_code = OK
        return