from http.client import BAD_REQUEST, OK
from typing import Any
from mindfulguard.classes.safe.base import SafeBase
from mindfulguard.validation import Validation
from loguru import logger

class Get(SafeBase):
    def __init__(self) -> None:
        super().__init__()
        self.__response: list[dict[str, Any]] = []
        self.__validation = Validation()

    @property
    def response(self) -> list[dict[str, Any]]:
        return self.__response

    async def execute(self, token: str) -> None:
        logger.debug("Executing 'execute' method to get safes for token: {}", token)
        try:
            self._model_token.token = token
            db = self._pgsql_safe.get(self._model_token)
            await self._connection.open()
            await db.execute()

            if db.status_code != OK:
                self._status_code = db.status_code
                logger.debug("Failed to get safes for token: {}. Status code: {}", token, db.status_code)
                return

            for i in db.response:
                if not self.__validation.is_uuid(i.id):
                    self.__response = []
                    self._status_code = OK
                    logger.debug("Safes not found for token: {}", token)
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
            logger.debug("Safes fetched successfully for token: {}", token)
            return
        except ValueError as e:
            self._status_code = BAD_REQUEST
            logger.error("ValueError occurred: {}", e)
        finally:
            await self._connection.close()
            logger.debug("Database connection closed.")
