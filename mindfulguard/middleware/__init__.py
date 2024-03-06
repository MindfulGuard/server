import asyncio
from http.client import BAD_REQUEST, UNAUTHORIZED
from fastapi import Request
from fastapi.responses import JSONResponse
from mindfulguard.classes.audit import Audit
from mindfulguard.classes.database import DataBase
from mindfulguard.classes.middleware.base import MiddlewareBase
from mindfulguard.database.postgresql.data_collection import PostgreSqlDataCollection
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
            
            connection = DataBase().postgresql().connection()

            try:
                self._model_token.token = authorization_header
                self._model_token.device = device_header
                self._model_token.last_ip = get_client_ip(request)

                await connection.open()
                db = PostgreSqlDataCollection(connection).update_token_information(self._model_token)
                await db.execute()
                if db.status_code == UNAUTHORIZED:
                    return JSONResponse(
                        status_code = UNAUTHORIZED,
                        content = self._responses.default().get(UNAUTHORIZED)
                    )
                
                if not request.url.path.startswith('/v1/auth/sign_out') and not (request.url.path.startswith('/v1/user/settings') and request.method.lower() == 'delete'):
                    asyncio.create_task(Audit(request).insert(authorization_header, device_header))
                    
                return await call_next(request)
            except ValueError:
                return JSONResponse(
                    status_code = BAD_REQUEST,
                    content = self._responses.default().get(BAD_REQUEST)
                )
            finally:
                await connection.close()

        return await call_next(request)