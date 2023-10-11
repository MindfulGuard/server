from mindfulguard import utils
from mindfulguard.core import security
from mindfulguard.core.response_status_codes import *
from mindfulguard.core.security.totp import NUMBER_OF_BACKUP_CODES, Totp
from mindfulguard.database.postgresql import authentication


class SignUp:
    async def execute(self,login:str,secret_string:str,ip:str):
        """
            Returns:
                400 - not valid email\n
                503 - registration is not allowed\n
                200 - registration was successful\n
                409 - the user already exists
        """
        valid = utils.Validation()
        print(valid.validate_secret_string(secret_string),valid.validate_login(login))
        if valid.validate_secret_string(secret_string) == False or valid.validate_login(login)==False:
            return (None,None,BAD_REQUEST)
        totp = Totp("")
        secret_code = totp.generate_secret_code()
        backup_codes = totp.generate_backup_codes(NUMBER_OF_BACKUP_CODES)
        return (secret_code,backup_codes, await authentication.Authentication().sign_up(
            login,
            security.sha256s(secret_string),
            ip,
            secret_code,
            backup_codes
        ))