from http.client import INTERNAL_SERVER_ERROR, OK

import asyncpg
from mindfulguard.classes.database import DataBase
from mindfulguard.classes.models.audit import ModelAudit
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.audit import PostgreSqlAudit


class DbTestsAuditGet:
    def __init__(self) -> None:
        self.__status_code: int
        self.__connection = DataBase().postgresql().connection()
        self.__pgsql_audit  = PostgreSqlAudit(self.__connection)
        self.__model_token: ModelToken = ModelToken()

    @property
    def status_code(self) -> int:
        return self.__status_code

    async def execute(
        self,
        token: str,
    ) -> None:
        try:
            self.__model_token.token = token
            
            await self.__connection.open()
            db = self.__pgsql_audit.get(self.__model_token)
            await db.execute(2, 1)

            response_list: list[ModelAudit] = []

            for i in db.response:
                response_list.append(i)

            if len(response_list) > 0:
                self.__status_code = OK
                return
            else:
                self.__status_code = INTERNAL_SERVER_ERROR
                return
        finally:
            await self.__connection.close()