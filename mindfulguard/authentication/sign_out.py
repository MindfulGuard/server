from http.client import BAD_REQUEST
from fastapi import Request
from mindfulguard.classes.authentication.base import AuthenticationBase


class SignOut(AuthenticationBase):
    def __init__(self, request: Request) -> None:
        super().__init__(request)

    async def execute(self, token: str, token_id: str) -> None:
        try:
            self._model_token.token = token
            self._model_token.id = token_id
            db = self._pgsql_auth.sign_out(self._model_token)
            await self._connection.open()
            await db.execute()
            self._status_code = db.status_code
            return
        except ValueError:
            self._status_code = BAD_REQUEST
        finally:
            await self._connection.close()