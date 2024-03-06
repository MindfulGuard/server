from http.client import INTERNAL_SERVER_ERROR, OK

import asyncpg
from mindfulguard.classes.database import DataBase
from mindfulguard.classes.models.audit import ModelAudit
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.audit import PostgreSqlAudit


class DbTestsAuditInsert:
    def __init__(self) -> None:
        self.__status_code: int
        self.__connection = DataBase().postgresql().connection()
        self.__pgsql_audit  = PostgreSqlAudit(self.__connection)
        self.__model_token: ModelToken = ModelToken()
        self.__model_audit = ModelAudit()

    @property
    def model_audit(self) -> ModelAudit:
        return ModelAudit()

    @property
    def status_code(self) -> int:
        return self.__status_code

    async def execute(
        self,
        token: str,
        ip: str,
        object: str,
        action: str,
        device: str
    ) -> None:
        try:
            self.__model_token.token = token
            self.__model_audit.ip = ip
            self.__model_audit.object = object
            self.__model_audit.action = action
            self.__model_audit.device = device
            
            await self.__connection.open()
            await self.__pgsql_audit.insert(self.__model_token, self.__model_audit).execute()
            self.__status_code = OK
            return
        except asyncpg.exceptions.InvalidTextRepresentationError:
            self.__status_code = INTERNAL_SERVER_ERROR
        finally:
            await self.__connection.close()