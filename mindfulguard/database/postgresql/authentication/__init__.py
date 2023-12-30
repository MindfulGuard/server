from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.code import ModelCode
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.classes.models.user import ModelUser
from mindfulguard.database.postgresql.authentication.is_auth import PostgreSqlIsAuth
from mindfulguard.database.postgresql.authentication.is_auth_admin import PostgreSqlIsAuthAdmin
from mindfulguard.database.postgresql.authentication.sign_in import PostgreSqlSignIn
from mindfulguard.database.postgresql.authentication.sign_out import PostgreSqlSignOut
from mindfulguard.database.postgresql.connection import PostgreSqlConnection
from mindfulguard.database.postgresql.authentication.sign_up import PostgreSqlSignUp

class PostgreSqlAuthentication:
    def __init__(self, connection: PostgreSqlConnection):
        self.__connection: PostgreSqlConnection = connection

    def sign_up(self, model_user: ModelUser, model_code: ModelCode) -> PostgreSqlSignUp:
        """
        Requested values for ModelUser:
            ModelUser().login,
            ModelUser().secret_string,
            ModelUser().reg_ip,
            ModelUser().confirm

        Requested values for ModelCode:
            ModelCode().secret_code,
            ModelCode().backup_codes
        """
        obj: PostgreSqlQueriesBase = PostgreSqlSignUp(
            self.__connection,
            model_user,
            model_code
        )
        return obj
    
    def sign_in(self, model_user: ModelUser, model_token: ModelToken) -> PostgreSqlSignIn:
        """
        Params:
            ModelUser().login,
            ModelUser().secret_string,
            ModelToken().token,
            ModelToken().device,
            ModelToken().last_ip,
            ModelToken().expiration,
        """
        obj: PostgreSqlQueriesBase = PostgreSqlSignIn(self.__connection, model_user, model_token)
        return obj
    
    def sign_out(self, model_token: ModelToken) -> PostgreSqlSignOut:
        """
        Params:
            ModelToken().id,
            ModelToken().token
        """
        obj: PostgreSqlQueriesBase =  PostgreSqlSignOut(self.__connection, model_token)
        return obj
    
    def is_auth(self, model_token: ModelToken) -> PostgreSqlIsAuth:
        obj: PostgreSqlQueriesBase = PostgreSqlIsAuth(self.__connection, model_token)
        return obj
    
    def is_auth_admin(self, model_token: ModelToken) -> PostgreSqlIsAuthAdmin:
        """
        Params:
            ModelToken().token
        """
        obj: PostgreSqlQueriesBase = PostgreSqlIsAuthAdmin(
            self.__connection,
            model_token
        )
        return obj