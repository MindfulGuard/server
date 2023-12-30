import json
from typing import Any
from mindfulguard.classes.database import DataBase
from mindfulguard.database.postgresql.settings import PostgreSqlSettings
from mindfulguard.exceptions.unknown_type import ExceptionUnknownType
import ast


class Settings:
    def __init__(self) -> None:
        self.__response: dict[str, Any] = {}
        self.__connection = DataBase().postgresql().connection()
        self.__pgsql_settings = PostgreSqlSettings(self.__connection)

    @property
    def response(self) -> dict[str, Any]:
        return self.__response

    async def execute(self) -> None:
        try:
            await self.__connection.open()
            await self.__pgsql_settings.execute()
            self.__response = self.__pgsql_settings.response
            for key, value in self.__pgsql_settings.response.items():
                self.__response[key] = self.__converting_from_string_to_correct_type(value)
            return
        finally:
            await self.__connection.close()

    def __converting_from_string_to_correct_type(self, value: str) -> Any:
        if isinstance(value, str):
            try:
                return json.loads(value)
            except (json.JSONDecodeError, ValueError):
                return value
        elif isinstance(value, int):
            return int(value)
        elif isinstance(value, float):
            return float(value)
        elif isinstance(value, bool):
            if value.lower() == 'true':
                return True
            elif value.lower() == 'false':
                return False
            else:
                raise ValueError('Invalid boolean value')
        elif isinstance(value, list):
            try:
                return json.loads(value)
            except (json.JSONDecodeError, ValueError):
                return value
        elif isinstance(value, dict):
            try:
                return json.loads(value)
            except (json.JSONDecodeError, ValueError):
                return value
        else:
            raise Exception(f'Unknown Type, type: {type(value)}')