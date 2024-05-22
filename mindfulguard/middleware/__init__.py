import asyncio
from http.client import BAD_REQUEST, UNAUTHORIZED
from fastapi import Request
from fastapi.responses import JSONResponse
from mindfulguard.classes.audit import Audit
from mindfulguard.classes.database import DataBase
from mindfulguard.classes.middleware.base import MiddlewareBase
from mindfulguard.database.postgresql.data_collection import PostgreSqlDataCollection
from mindfulguard.net.ip import get_client_ip
from loguru import logger


class UpdateTokenInformationMiddleware(MiddlewareBase):
    def __init__(self) -> None:
        super().__init__()

    async def __call__(self, request: Request, call_next):
        logger.debug("Processing request path: {}", request.url.path)
        
        if (
            not request.url.path.startswith("/v1/public")
            and not request.url.path.startswith("/v1/auth/sign_up")
            and not request.url.path.startswith("/v1/auth/sign_in")
        ):
            logger.debug("Request requires authorization.")
            authorization_header = request.headers.get('Authorization')
            device_header = request.headers.get('Device')

            if not authorization_header or not device_header:
                logger.warning("Missing Authorization or Device header.")
                return JSONResponse(
                    status_code=BAD_REQUEST,
                    content=self._http_response.get(BAD_REQUEST).to_json()
                )

            logger.debug("Authorization header: {}, Device header: {}", authorization_header, device_header)
            connection = DataBase().postgresql().connection()

            try:
                self._model_token.token = authorization_header
                self._model_token.device = device_header
                self._model_token.last_ip = get_client_ip(request)

                logger.debug("Opening database connection.")
                await connection.open()

                logger.debug("Updating token information.")
                db = PostgreSqlDataCollection(connection).update_token_information(self._model_token)
                await db.execute()

                if db.status_code == UNAUTHORIZED:
                    logger.warning("Unauthorized access.")
                    return JSONResponse(
                        status_code=UNAUTHORIZED,
                        content=self._http_response.get(UNAUTHORIZED).to_json()
                    )
                
                if not request.url.path.startswith('/v1/auth/sign_out') and not (request.url.path.startswith('/v1/user/settings') and request.method.lower() == 'delete'):
                    logger.debug("Inserting audit log.")
                    asyncio.create_task(Audit(request).insert(authorization_header, device_header))
                    
                logger.debug("Proceeding with the next request handler.")
                return await call_next(request)
            except ValueError as e:
                logger.error("ValueError occurred: {}", e)
                return JSONResponse(
                    status_code=BAD_REQUEST,
                    content=self._http_response.get(BAD_REQUEST).to_json()
                )
            finally:
                logger.debug("Closing database connection.")
                await connection.close()
        else:
            logger.debug("Request path does not require authorization. Proceeding with the next request handler.")
        
        return await call_next(request)
