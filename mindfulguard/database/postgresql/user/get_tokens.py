from http.client import OK, UNAUTHORIZED
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.classes.models.user import ModelUser
from mindfulguard.database.postgresql.authentication.is_auth import PostgreSqlIsAuth
from mindfulguard.database.postgresql.connection import PostgreSqlConnection


class PostgreSqlUserGetTokens(PostgreSqlQueriesBase):
    def __init__(self, connection: PostgreSqlConnection, model_token: ModelToken) -> None:
        super().__init__(connection)
        self.__pgsql_is_auth = PostgreSqlIsAuth(self._connection, model_token)
        self._model_token: ModelToken = model_token

    class _ModelTokenExtend(ModelToken):
        def __init__(self):
            super().__init__()
            self.__id: str
            self.__created_at: int
            self.__updated_at: int
            self.__device: str
            self.__last_ip: str
            self.__expiration: int

        @property
        def id(self) -> str:
            return self.__id
        
        @id.setter
        def id(self, value: str) -> None:
            if not self._validation.is_uuid(value):
                raise ValueError('The value is not a uuid')
            self.__id = value

        @property
        def created_at(self) -> int:
            return self.__created_at
        
        @created_at.setter
        def created_at(self, value: int) -> None:
            self.__created_at = value
        
        @property
        def updated_at(self) -> int:
            return self.__updated_at
        
        @updated_at.setter
        def updated_at(self, value: int) -> None:
            self.__updated_at = value

        @property
        def device(self) -> str:
            return self.__device
        
        @device.setter
        def device(self, value: str) -> None:
            if not self._validation.is_device(value):
                raise ValueError('Invalid value')
            self.__device = value

        @property
        def last_ip(self) -> str:
            return self.__last_ip
        
        @last_ip.setter
        def last_ip(self, value: str) -> None:
            if not self._validation.is_ip(value):
                raise ValueError(f'Invalid ip address {value}')
            self.__last_ip = value

        @property
        def expiration(self) -> int:
            return self.__expiration
        
        @expiration.setter
        def expiration(self, value: int) -> None:
            self.__expiration = value


    class __Iterator:
        def __init__(self, pgsql_response: list):
            self.__pgsql_response: list = pgsql_response
            self.__model_token_extend = PostgreSqlUserGetTokens._ModelTokenExtend()
            self.__i: int = 0

        def __iter__(self):
            return self
        
        def __next__(self):
            if self.__i < len(self.__pgsql_response):
                self.__model_token_extend.id = self.__pgsql_response[self.__i]['t_id']
                self.__model_token_extend.created_at = self.__pgsql_response[self.__i]['t_created_at']
                self.__model_token_extend.updated_at = self.__pgsql_response[self.__i]['t_updated_at']
                self.__model_token_extend.device = self.__pgsql_response[self.__i]['t_device']
                self.__model_token_extend.last_ip = self.__pgsql_response[self.__i]['t_last_ip']
                self.__model_token_extend.expiration = self.__pgsql_response[self.__i]['t_expiration']
                self.__i += 1
                return self.__model_token_extend
            else:
                raise StopIteration
    
    @property
    def response(self) -> __Iterator:
        return self._response

    async def execute(self) -> None:
        await self.__pgsql_is_auth.execute()
        if self.__pgsql_is_auth.status_code == UNAUTHORIZED:
            self._status_code = self.__pgsql_is_auth.status_code
            return

        values = await self._connection.connection.fetch('''
        SELECT t_id, t_created_at, t_updated_at, t_device, t_last_ip, t_expiration
        FROM t_tokens
        WHERE t_u_id IN (
            SELECT t_u_id
            FROM t_tokens
            WHERE t_token = $1 AND active_token($1) = TRUE
        );
        ''',
        self._model_token.token
        )
        self._response = self.__Iterator(values)
        self._status_code = OK
        return