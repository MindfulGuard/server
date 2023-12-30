from http.client import BAD_REQUEST, OK
from typing import Any
from mindfulguard.classes.safe.base import SafeBase
from mindfulguard.validation import Validation


class Get(SafeBase):
    def __init__(self) -> None:
        super().__init__()
        self.__response: list[dict[str, Any]] = []
        self.__validation = Validation()

    @property
    def response(self) -> list[dict[str, Any]]:
        return self.__response

    async def execute(self, token: str) -> None:
        try:
            self._model_token.token = token
            db = self._pgsql_safe.get(self._model_token)
            await self._connection.open()
            await db.execute()

            if db.status_code != OK:
                self._status_code = db.status_code
                return

            for i in db.response:
                if not self.__validation.is_uuid(i.id):
                    self.__response = []
                    self._status_code = OK
                    return
                values = {
                    'id': i.id,
                    'name': i.name,
                    'description': i.description,
                    'created_at': i.created_at,
                    'updated_at': i.updated_at,
                    'count_items': i.count_items
                }
                self.__response.append(values)
            self._status_code = db.status_code
            return
        except ValueError:
            self._status_code = BAD_REQUEST
        finally:
            await self._connection.close()