from http.client import INTERNAL_SERVER_ERROR, OK
from typing import Any
from mindfulguard.classes.configuration.base import ConfigurationBase


class ConfigurationPublic(ConfigurationBase):
    def __init__(self) -> None:
        super().__init__()

    @property
    def response(self) -> Any:
        return self._response

    async def execute(self) -> None:
        try:
            settings: dict[str, Any] = await self._settings.get()
            obj = {
                "password_rule": settings['password_rule'],
                "item_categories": settings['item_categories'],
                "item_types": settings['item_types']
            }

            self._response = obj
            self._status_code = OK
        except KeyError:
            self._status_code = INTERNAL_SERVER_ERROR