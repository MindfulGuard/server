from mindfulguard.authentication.executors.sign_in import TYPE_BASIC, TYPE_BACKUP
from mindfulguard.core.response_status_codes import BAD_REQUEST, INTERNAL_SERVER_ERROR
from mindfulguard.core.security.totp import NUMBER_OF_BACKUP_CODES, Totp
from mindfulguard.database.postgresql.user.settings import Settings

class OneTimeCodes:
    def __init__(self):
        self.__totp = Totp("")

    async def update(self,token:str,secret_string:str,type:str):
        settings = Settings()

        if type == TYPE_BASIC:
            secret_code:str = self.__generate_secret_code()
            return (
                secret_code,
                await settings.update_one_time_codes(
                    token,
                    secret_string,
                    secret_code
                )
            )
        elif type == TYPE_BACKUP:
            backup_codes:list[int] = self.__generate_backup_codes()
            return (
                backup_codes,
                await settings.update_one_time_codes(
                    token,
                    secret_string,
                    backup_codes
                )
            )
        else:
            return ("",BAD_REQUEST)

    def __generate_secret_code(self):
        return self.__totp.generate_secret_code()

    def __generate_backup_codes(self):
        return self.__totp.generate_backup_codes(NUMBER_OF_BACKUP_CODES)