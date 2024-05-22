import json
from typing import Any
from loguru import logger
from mindfulguard.classes.database import DataBase
from mindfulguard.database.postgresql.settings import PostgreSqlSettings


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
            logger.info("Opening database connection...")
            await self.__connection.open()
            logger.info("Database connection opened successfully.")
            logger.info("Executing PostgreSQL settings...")
            await self.__pgsql_settings.execute()
            logger.info("PostgreSQL settings executed successfully.")
            self.__response = self.__pgsql_settings.response
            logger.debug("Converting response values to correct types...")
            for key, value in self.__pgsql_settings.response.items():
                self.__response[key] = self.__converting_from_string_to_correct_type(value)
            logger.info("Response values converted successfully.")
            return
        finally:
            logger.info("Closing database connection...")
            await self.__connection.close()
            logger.info("Database connection closed.")

    def __converting_from_string_to_correct_type(self, value: str) -> Any:
        if isinstance(value, str):
            try:
                return json.loads(value)
            except (json.JSONDecodeError, ValueError) as e:
                logger.warning("Error converting string to JSON: {}", e)
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
                logger.warning('Invalid boolean value')
                raise ValueError('Invalid boolean value')
        elif isinstance(value, (list, dict)):
            try:
                return json.loads(value)
            except (json.JSONDecodeError, ValueError) as e:
                logger.warning("Error converting string to JSON: {}", e)
                return value
        else:
            logger.error('Unknown Type, type: {}', type(value))
            raise Exception(f'Unknown Type, type: {type(value)}')
