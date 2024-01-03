from http.client import BAD_REQUEST, OK
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
            if db.status_code == OK:
                for i in self._redis.client().connection.scan_iter(
                    f'{self._model_token.token}:{self._redis.PATH_SAFE_ALL_ITEM}'
                ):
                    self._redis.client().connection.delete(i)
            self._status_code = db.status_code
            return
        except ValueError:
            self._status_code = BAD_REQUEST
        finally:
            await self._connection.close()