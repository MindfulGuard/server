from http.client import BAD_REQUEST, NOT_FOUND, OK
from loguru import logger
from mindfulguard.classes.user.base import UserBase


class UserSettingsUpdateSecretString(UserBase):
    def __init__(self) -> None:
        super().__init__()
        from mindfulguard.user.settings.model_user_extend import ModelUserExtend
        self.__model_user_extend = ModelUserExtend()
    
    async def execute(
        self,
        token: str,
        old_secret_string: str,
        new_secret_string: str,
        one_time_code: str
        ) -> None:
        try:
            logger.info("Executing UserSettingsUpdateSecretString...")
            self._model_token.token = token
            self._model_totp_code.totp_code = one_time_code
            self.__model_user_extend.old_secret_string = old_secret_string
            self.__model_user_extend.new_secret_string = new_secret_string
            if (
                self.__model_user_extend.old_secret_string ==
                self.__model_user_extend.new_secret_string
            ):
                logger.warning("Old and new secret strings are the same.")
                self._status_code = BAD_REQUEST
                return    
            
            logger.info("Updating secret string in settings...")
            db = self._pgsql_user.settings().udpate_secret_string(
                self.__model_user_extend,
                self._model_token
            )
            db_secret_code = db.secret_code()
            await self._connection.open()
            await db_secret_code.execute()

            if db_secret_code.status_code != OK:
                logger.error("Failed to update secret string.")
                self._status_code = db_secret_code.status_code
                return
            
            logger.info("Verifying TOTP...")
            if not self.__confirm(
                self._model_totp_code.totp_code,
                db_secret_code.secret_code
            ):
                logger.warning("TOTP verification failed.")
                self._status_code = NOT_FOUND
                return
            logger.info("TOTP verification successful.")
            await db.execute()

            self._status_code = db.status_code
            logger.info("Secret string updated successfully.")
            return
        except ValueError as e:
            logger.error(f"ValueError occurred: {e}")
            self._status_code = BAD_REQUEST
        finally:
            logger.info("Closing database connection...")
            await self._connection.close()
            logger.info("Database connection closed.")
    
    def __confirm(self, code: str, secret_code: str) -> bool:
        totp = self._security.totp(secret_code)
        return totp.verify(code)
