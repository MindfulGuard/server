from http.client import BAD_REQUEST
from mindfulguard.classes.safe.base import SafeBase


class Update(SafeBase):
    def __init__(self) -> None:
        super().__init__()

    async def execute(
        self,
        token: str,
        safe_id: str,
        name: str,
        description: str
    ) -> None:
        try:
            self._model_token.token = token
            self._model_safe.id = safe_id
            self._model_safe.name = name
            self._model_safe.description = description
            db = self._pgsql_safe.update(self._model_token, self._model_safe)
            await self._connection.open()
            await db.execute()
            self._status_code = db.status_code
            return
        except ValueError:
            self._status_code = BAD_REQUEST
        finally:
            await self._connection.close()