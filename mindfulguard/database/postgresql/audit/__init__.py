from mindfulguard.classes.models.audit import ModelAudit
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.audit.get import PostgreSqlAuditGet
from mindfulguard.database.postgresql.audit.insert import PostgreSqlAuditInsert
from mindfulguard.database.postgresql.connection import PostgreSqlConnection

class PostgreSqlAudit:
    def __init__(self, connection: PostgreSqlConnection):
        self.__connection: PostgreSqlConnection = connection

    def insert(self, model_token: ModelToken, model_audit: ModelAudit) -> PostgreSqlAuditInsert:
        """
        Requested values for ModelToken:
            ModelToken().token

        Requested values for ModelCode:
            ModelAudit().ip,
            ModelAudit().object,
            ModelAudit().action,
            ModelAudit().device
        """
        return PostgreSqlAuditInsert(self.__connection, model_token, model_audit)
    

    def get(self, model_token: ModelToken):
        """
        Requested values for ModelToken:
            ModelToken().token
        """
        return PostgreSqlAuditGet(self.__connection, model_token)