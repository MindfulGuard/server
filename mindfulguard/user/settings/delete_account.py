from http.client import BAD_REQUEST, OK
from mindfulguard.classes.user.base import UserBase


class UserSettingsDeleteAccount(UserBase):
    def __init__(self) -> None:
        super().__init__()

    async def execute(
        self,
        token: str,
        secret_string: str,
        one_time_code: str
    ) -> None:
        try:
            self._model_token.token = token
            self._model_user.secret_string = secret_string
            self._model_totp_code.totp_code = one_time_code

            db_user_info = self._pgsql_user.get_information(self._model_token)
            await self._connection.open()
            await db_user_info.execute()
            self._status_code = db_user_info.status_code
            if db_user_info.status_code != OK:
                print('db_user_info', db_user_info.status_code)
                return

            db = self._pgsql_user.settings().delete_account(
                self._model_token,
                self._model_user
            )
            db_secret_code = db.secret_code()
            await db_secret_code.execute()
            self._status_code = db_secret_code.status_code
            if db_secret_code.status_code != OK:
                print('db_secret_code', db_secret_code.status_code)
                return
            
            confirm = self._security.totp(
                db_secret_code.secret_code
            ).verify(
                self._model_totp_code.totp_code
            )
            print(db_secret_code.secret_code, self._model_totp_code.totp_code)
            print(confirm)
            await db.execute(confirm)
            self._status_code = db.status_code
            if db.status_code != OK:
                print('db', db.status_code)
                return
            
            self._s3.set_bucket_name(db_user_info.response.login)
            self._s3.object().delete_all_objects()
            self._s3.bucket().delete_bucket()
            return
        except ValueError:
            self._status_code = BAD_REQUEST
        finally:
            await self._connection.close()