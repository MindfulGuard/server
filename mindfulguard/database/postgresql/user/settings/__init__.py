from mindfulguard.classes.models.code import ModelCode
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.classes.models.user import ModelUser
from mindfulguard.database.postgresql.connection import PostgreSqlConnection
from mindfulguard.database.postgresql.user.settings.delete_account import PostgreSqlUserSettingsDeleteAccount
from mindfulguard.database.postgresql.user.settings.update_one_times_code import PostgreSqlUserSettingsUpdateOneTimeCode
from mindfulguard.database.postgresql.user.settings.update_secret_string import PostgreSqlUserSettingsUpdateSecretString
from mindfulguard.user.settings.model_user_extend import ModelUserExtend

class PostgreSqlUserSettings:
    def __init__(
        self,
        connection: PostgreSqlConnection,
    ) -> None:
        self.__connection: PostgreSqlConnection = connection

    def update_one_time_code(
        self,
        model_user: ModelUser,
        model_token: ModelToken,
        model_code: ModelCode
    ) -> PostgreSqlUserSettingsUpdateOneTimeCode:
        """
        Pararms:
            ModelToken().token,
            ModelUser().secret_string,
            ModelCode().secret_code for totp || ModelCode().backup_codes for backup codes
        """
        return PostgreSqlUserSettingsUpdateOneTimeCode(
            self.__connection,
            model_token,
            model_user,
            model_code
        )
    
    def udpate_secret_string(
        self,
        model_user_extend: ModelUserExtend,
        model_token: ModelToken
    ) -> PostgreSqlUserSettingsUpdateSecretString:
        """
        Pararms:
            ModelToken().token,
            ModelUserExtend().old_secret_string,
            ModelUserExtend().new_secret_string,
        """
        return PostgreSqlUserSettingsUpdateSecretString(
            self.__connection,
            model_token,
            model_user_extend
        )
    
    def delete_account(
        self,
        model_token: ModelToken,
        model_user: ModelUser
    ) -> PostgreSqlUserSettingsDeleteAccount:
        """
        Params:
            ModelToken().token,
            ModelUser().secret_string
        """
        return PostgreSqlUserSettingsDeleteAccount(
            self.__connection,
            model_token,
            model_user
        )