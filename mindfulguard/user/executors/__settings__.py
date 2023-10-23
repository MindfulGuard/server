from mindfulguard.authentication.executors import get_authorization_token
from mindfulguard.core.response_status_codes import BAD_REQUEST
from mindfulguard.user.executors.settings.delete_user import Delete
from mindfulguard.user.executors.settings.one_time_codes import OneTimeCodes
from mindfulguard.user.executors.settings.update_secret_string import SecretString
from mindfulguard.utils import Validation
from tests.api.secure.secure import sha256s


class UserSettings:
    async def one_time_codes(self,token:str,secret_string:str,type:str):
        one_time_codes = OneTimeCodes()
        validation = Validation()
        tokenf:str = get_authorization_token(token)
        
        if (
            validation.validate_token(tokenf) == False
            or validation.validate_secret_string(secret_string) == False
            ):
            return ("",BAD_REQUEST)
        return await one_time_codes.update(
            sha256s(tokenf),
            sha256s(secret_string),
            type
        )
    async def secret_string_(
            self,
            token:str,
            login:str,
            old_secret_string:str,
            new_secret_string:str,
            code:str
        ):
        one_time_codes = SecretString()
        validation = Validation()
        tokenf:str = get_authorization_token(token)
        
        if (
            validation.validate_token(tokenf) == False
            or validation.validate_login(login) == False
            or validation.validate_secret_string(old_secret_string) == False
            or validation.validate_secret_string(new_secret_string) == False
            or old_secret_string == new_secret_string
            or validation.validate_TOTP_code(code) == False
            ):
            return (BAD_REQUEST)
        return await one_time_codes.update(
            sha256s(tokenf),
            login,
            sha256s(old_secret_string),
            sha256s(new_secret_string),
            code
        )
    
    async def delete_user(
            self,
            token:str,
            login:str,
            secret_string:str,
            code:str
        ):
        validation = Validation()
        tokenf:str = get_authorization_token(token)

        if (
            validation.validate_token(tokenf) == False
            or validation.validate_login(login) == False
            or validation.validate_secret_string(secret_string) == False
            or validation.validate_TOTP_code(code) == False
        ):
            return BAD_REQUEST
        
        delet_user = Delete()
        return await delet_user.execute(
            sha256s(tokenf),
            login,
            sha256s(secret_string),
            code
        )