from http.client import BAD_REQUEST, OK
from typing import Literal
from fastapi import Request
from mindfulguard.classes.authentication.base import AuthenticationBase
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.classes.models.totp_code import ModelTotpCode
from mindfulguard.database.postgresql.authentication.sign_in import PostgreSqlSignIn
from mindfulguard.exceptions.incorrect_parameters import ExceptionIncorrectParameters
from mindfulguard.net.ip import get_client_ip

class SignIn(AuthenticationBase):
    def __init__(self, request: Request) -> None:
        super().__init__(request)
        self.__token: str
        self.__model_totp_code = ModelTotpCode()
    
    @property
    def token(self) -> str:
        return self.__token

    class __ModelTokenExtend(ModelToken):
        def __init__(self):
            super().__init__()
            self.__token: str
            self.__device: str
            self.__last_ip: str
            self.__expiration: int

        @property
        def device(self) -> str:
            return self.__device
        
        @device.setter
        def device(self, value: str) -> None:
            if not self._validation.is_device(value):
                raise ValueError('Invalid value')
            self.__device = value

        @property
        def expiration(self) -> int:
            return self.__expiration
        
        @expiration.setter
        def expiration(self, value: int) -> None:
            MAX_MINUTES: int = 129600
            if 0 > value or value > MAX_MINUTES:
                raise ValueError(f'Invalid value, maximum token expiration time {MAX_MINUTES} minutes')
            self.__expiration: int = value * 60

        @property
        def last_ip(self) -> str:
            return self.__last_ip
        
        @last_ip.setter
        def last_ip(self, value: str) -> None:
            if not self._validation.is_ip(value):
                raise ValueError(f'Invalid ip address {value}')
            self.__last_ip = value

        @property
        def token(self) -> str:
            return self.__token
        
        @token.setter
        def token(self, value: str) -> None:
            if not self._validation.is_token(value):
                raise ValueError('Invalid token value')
            self.__token = str(self._security.hash().sha(value))

    async def execute(
        self,
        login: str,
        secret_string: str,
        device: str,
        expiration: int,
        type: Literal['backup', 'basic'],
        code: str
    ):
        model_token_extend = self.__ModelTokenExtend()
        try:
            if type != 'basic' and type != 'backup':
                raise ValueError(f'Type is not basic or not backup, value: {type}')
            self._model_user.login = login
            self._model_user.secret_string = secret_string
            self.__model_totp_code.totp_code = code
            self.__token = self._security.generate_string(128)
            model_token_extend.token = self.__token
            model_token_extend.device = device
            model_token_extend.last_ip = get_client_ip(self._request)
            model_token_extend.expiration = expiration
            
            db = self._pgsql_auth.sign_in(self._model_user, model_token_extend)
            db_secret_code = db.secret_code()
            await self._connection.open()
            await db_secret_code.execute()
            if db_secret_code.status_code != OK:
                self._status_code = db_secret_code.status_code
                return

            confirm: bool = await self.__confirm(
                db,
                type,
                db_secret_code.secret_code,
                db_secret_code.backup_codes
            )   
            await db.execute(confirm)
            self._status_code = db.status_code
            if db.status_code != OK:
                return

            self._s3.set_bucket_name(self._model_user.login)
            self._s3.bucket().make_bucket()
            self._s3.bucket().make_bucket()
            return
        except ValueError:
            self._status_code = BAD_REQUEST
        except ExceptionIncorrectParameters:
            self._status_code = BAD_REQUEST
        finally:
            await self._connection.close()

    async def __confirm(
            self,
            db: PostgreSqlSignIn,
            type: Literal['backup', 'basic'] ,
            totp_secret_code: str = '',
            backup_codes: list[int] = [],
        ) -> bool:
        if type == 'basic':
            if len(totp_secret_code) == 0:
                raise ExceptionIncorrectParameters('The requested parameter is empty')
            return self._security.totp(totp_secret_code).verify(self.__model_totp_code.totp_code)
        elif type == 'backup':
            icode: int = int(self.__model_totp_code.totp_code)
            if icode in backup_codes:
                backup_codes.remove(icode)
                dbubc = db.update_backup_codes(backup_codes)
                await dbubc.execute()
                if dbubc.status_code == OK:
                    return True
            return False
        raise ExceptionIncorrectParameters(f'Type must have a value of backup or basic, value: {type}')