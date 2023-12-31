from http.client import BAD_REQUEST
from mindfulguard.classes.items.base import ItemsBase


class Favorite(ItemsBase):
    def __init__(self) -> None:
        super().__init__()

    async def execute(
        self,
        token: str,
        safe_id: str,
        record_id: str
    ) -> None:
        try:
            self._model_token.token = token
            self._model_record.safe_id = safe_id
            self._model_record.id = record_id
            db = self._pgsql_items.favorite(self._model_token, self._model_record)
            await self._connection.open()
            await db.execute()
            self._status_code = db.status_code
            return
        except ValueError:
            self._status_code = BAD_REQUEST
        finally:
            await self._connection.close()