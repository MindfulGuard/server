from http.client import BAD_REQUEST, OK
from typing import Any
from loguru import logger
from mindfulguard.classes.user.base import UserBase


class UserInformation(UserBase):
    def __init__(self) -> None:
        super().__init__()
        self.__tokens: list[dict[str, Any]] = []

    @property
    def login(self) -> str:
        return self._model_user.login
    
    @property
    def reg_ip(self) -> str:
        return self._model_user.reg_ip

    @property
    def created_at(self) -> int:
        return self._model_user.created_at
    
    @property
    def tokens(self) -> list[dict[str, Any]]:
        return self.__tokens

    async def execute(self, token: str) -> None:
        try:
            logger.info("Executing UserInformation...")
            self._model_token.token = token

            logger.debug("Getting user information from PostgreSQL...")
            db_get_info = self._pgsql_user.get_information(self._model_token)
            await self._connection.open()
            await db_get_info.execute()
            self._status_code = db_get_info._status_code
            if self._status_code != OK:
                logger.debug("Failed to get user information from PostgreSQL.")
                return

            logger.debug("Getting user tokens from PostgreSQL...")
            db_get_tokens = self._pgsql_user.get_tokens(self._model_token)
            await db_get_tokens.execute()
            if db_get_tokens.status_code != OK:
                self._status_code = db_get_tokens.status_code
                logger.debug("Failed to get user tokens from PostgreSQL.")
                return
            
            logger.debug("Setting user information...")
            self._model_user.login = db_get_info.response.login
            self._model_user.reg_ip = db_get_info.response.reg_ip
            self._model_user.created_at = db_get_info.response.created_at

            logger.trace("Processing user tokens...")
            for i, token_record in enumerate(db_get_tokens.response, start=1):
                value_dict = {
                    'id': token_record.id,
                    'short_hash': token_record.hashed_token_shortened,
                    'created_at': token_record.created_at,
                    'updated_at': token_record.updated_at,
                    'device': token_record.device,
                    'last_ip': token_record.last_ip,
                    'expiration': token_record.expiration
                }
                self.__tokens.append(value_dict)
                logger.debug("Token record {}: {}", i, value_dict)

            self._status_code = OK
            logger.info("User information retrieval completed successfully.")
            return
        except ValueError as e:
            logger.error("ValueError occurred: {}", e)
            self._status_code = BAD_REQUEST
        finally:
            logger.debug("Closing database connection...")
            await self._connection.close()
            logger.debug("Database connection closed.")
