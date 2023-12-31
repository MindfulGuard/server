from http.client import BAD_REQUEST, UNAUTHORIZED
from fastapi import Request
from fastapi.responses import JSONResponse
from mindfulguard.classes.middleware.base import MiddlewareBase
from mindfulguard.net.ip import get_client_ip


class UpdateTokenInformationMiddleware(MiddlewareBase):
    def __init__(self) -> None:
        super().__init__()

    async def __call__(self, request: Request, call_next):
        if (
            not request.url.path.startswith("/v1/public")
            and not request.url.path.startswith("/v1/auth/sign_up")
            and not request.url.path.startswith("/v1/auth/sign_in")
        ):
            authorization_header = request.headers.get('Authorization')
            device_header = request.headers.get('Device')

            if not authorization_header or not device_header:
                return JSONResponse(
                    status_code = BAD_REQUEST,
                    content = self._responses.default().get(BAD_REQUEST)
                )

            try:
                self._model_token.token = authorization_header
                self._model_token.device = device_header
                self._model_token.last_ip = get_client_ip(request)

                await self._connection.open()
                db = self._pgsql_data_collection.update_token_information(self._model_token)
                await db.execute()
                if db.status_code == UNAUTHORIZED:
                    return JSONResponse(
                        status_code = UNAUTHORIZED,
                        content = self._responses.default().get(UNAUTHORIZED)
                    )
                return await call_next(request)
            except ValueError:
                return JSONResponse(
                    status_code = BAD_REQUEST,
                    content = self._responses.default().get(BAD_REQUEST)
                )
            finally:
                await self._connection.close()

        return await call_next(request)