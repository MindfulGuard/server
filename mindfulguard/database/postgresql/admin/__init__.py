from mindfulguard.classes.models.settings import ModelSettings
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.classes.models.user import ModelUser
from mindfulguard.database.postgresql.admin.configuration_update import PostgreSqlAdminConfigurationUpdate
from mindfulguard.database.postgresql.admin.delet_user import PostgreSqlAdminDeletUser
from mindfulguard.database.postgresql.admin.get_users import PostgreSqlAdminGetUsers
from mindfulguard.database.postgresql.admin.search_users import PostgreSqlAdminSearchUsers
from mindfulguard.database.postgresql.connection import PostgreSqlConnection


class PostgreSqlAdmin:
    def __init__(self, connection: PostgreSqlConnection):
        self.__connection: PostgreSqlConnection = connection

    def get_users(self, model_token: ModelToken) -> PostgreSqlAdminGetUsers:
        """
        Params:
            ModelToken().token
        Return:
            __Iterator().ModelUser() returns everything except ModelUser().secret_string and ModelUser().admin
        """
        return PostgreSqlAdminGetUsers(
            self.__connection,
            model_token
        )
    
    def search_users(
        self,
        model_token: ModelToken,
        model_user: ModelUser
    ) -> PostgreSqlAdminSearchUsers:
        """
        Params:
            ModelToken().token,
            ModelUser().id || ModelUser().login
        Return:
            ModelUser() returns everything except ModelUser().secret_string and ModelUser().admin
        """
        return PostgreSqlAdminSearchUsers(
            self.__connection,
            model_token,
            model_user
        )
    
    def update_configuration(
        self,
        model_token: ModelToken,
        model_settings: ModelSettings
    ) -> PostgreSqlAdminConfigurationUpdate:
        """
        Params:
            ModelToken().token,
            ModelSettings().key,
            ModelSettings().value
        """
        return PostgreSqlAdminConfigurationUpdate(
            self.__connection,
            model_token,
            model_settings
        )
    
    def delete_user(
        self,
        model_token: ModelToken,
        model_user: ModelUser
    ) -> PostgreSqlAdminDeletUser:
        """
        Params:
            ModelToken().token,
            ModelUser().id
        """
        return PostgreSqlAdminDeletUser(
            self.__connection,
            model_token,
            model_user
        )