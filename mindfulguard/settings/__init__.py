from http.client import BAD_REQUEST, NOT_FOUND, OK
import json
from typing import Any
import grpc
from google.protobuf.internal import containers
from redis.commands.json.path import Path
from loguru import logger
from mindfulguard.classes.database.redis import Redis
from mindfulguard.classes.settings.base import BaseSettings
from mindfulguard.grpc.client.dynamic_configurations.methods import GrpcDynamicConfigurationsMethods

class Settings(BaseSettings):
    def __init__(self) -> None:
        super().__init__()
        self.__redis = Redis()
        self.__CACHE_NAME: str = f'{self.__redis.CACHE_NAME_SETTINGS}:v1'
        self.__CACHE_TTL: int = 180 # 3 minute

    async def get(self) -> dict[str, Any]:
        logger.info("Entering get method. Class Settings()")
        response: dict[str, Any] = {}

        try:
            cached_response: dict[str, Any] = self.__redis.client().connection.json().get(self.__CACHE_NAME)  # type: ignore
            if cached_response:
                return cached_response

            async with GrpcDynamicConfigurationsMethods() as client:
                keys_list_request = await client.get_list(self.SETTINGS_PATH_V1)
                logger.debug("keys_list_request: {}", keys_list_request)

                if keys_list_request.error != grpc.StatusCode.OK or not keys_list_request.data:
                    logger.error("Failed to get list with error: {} and no data.", keys_list_request.error)
                    return response

                keys_list_data: containers.RepeatedScalarFieldContainer[str] = keys_list_request.data.list  # type: ignore
                logger.debug("keys_list_data: {}", keys_list_data)

                for key in keys_list_data:
                    logger.debug("Processing key: {}", key)
                    result = await client.get(key)
                    logger.debug("Received result from gRPC client: {}", result)

                    if result.error != grpc.StatusCode.OK or not result.data:
                        logger.error("gRPC call failed with error: {} and no data returned for key: {}", result.error, key)
                        continue

                    data: str = result.data.value.decode('utf-8')  # type: ignore
                    logger.debug("Decoded data from gRPC response: {}", data)

                    response[key.replace(self.SETTINGS_PATH_V1, '')] = self.__convert_from_string_to_correct_type(data)
                    logger.debug("Converted data to correct type and updated response: {}", response)
        except grpc.RpcError as e:
            logger.error("gRPC error occurred in get method: {}", e)
        except AttributeError as e:
            logger.error("Unexpected exception occurred in get method: {}", e)
        finally:
            logger.info("Exiting get method.")

        try:
            self.__redis.client().connection.json().set(
                self.__CACHE_NAME,
                Path.root_path(),
                response
            )
            self.__redis.client().connection.expire(self.__CACHE_NAME, self.__CACHE_TTL)
        except Exception as e:
            logger.error("Failed to set cache in Redis: {}", e)

        return response

    async def update(self, key: str, value: str) -> int:
        logger.info("Initializing settings update...")
        try:
            get_list_response: dict[str, Any] = await self.get()
            get_list: list[str] = list(get_list_response.keys())
            logger.debug("Current settings keys: %s", get_list)
            
            if key not in get_list:
                logger.warning("Key not found: %s", key)
                return NOT_FOUND

            async with GrpcDynamicConfigurationsMethods() as client:
                logger.info("Updating settings in the dynamic configurations service...")
                put_result = await client.put(self.SETTINGS_PATH_V1 + key, value.encode('utf-8'))

                if put_result.error == grpc.StatusCode.OK and put_result.data is not None:
                    logger.info("Settings update successful. Clearing cache...")
                    for i in self.__redis.client().connection.scan_iter(self.__CACHE_NAME):
                        self.__redis.client().connection.delete(i)
                    logger.info("Cache cleared for key: %s", self.__CACHE_NAME)

                    get_list_response = await self.get()
                    get_list = list(get_list_response.keys())
                    logger.debug("Updated settings keys: %s", get_list)

                    if key not in get_list:
                        logger.warning("Key not found after update: %s", key)
                        return NOT_FOUND
                    else:
                        self.__redis.client().connection.json().set(
                            self.__CACHE_NAME,
                            Path.root_path(),
                            get_list_response
                        )
                        self.__redis.client().connection.expire(self.__CACHE_NAME, self.__CACHE_TTL)
                        logger.info("Cache updated and TTL set for key: %s", self.__CACHE_NAME)

                    return OK
                else:
                    logger.error("Settings update failed with error: %s", put_result.error)
                    return BAD_REQUEST
        except grpc.RpcError as e:
            logger.error("gRPC error occurred during update: %s", e)
            return BAD_REQUEST
        except AttributeError as e:
            logger.error("Unexpected error occurred during update: %s", e)
            return BAD_REQUEST
        except Exception as e:
            logger.error("Unhandled exception occurred: %s", e)
            return BAD_REQUEST

    def __convert_from_string_to_correct_type(self, value: str) -> Any:
        logger.debug("Converting value from string to correct type: {}", value)
        if isinstance(value, str):
            try:
                converted_value = json.loads(value)
                logger.debug("Successfully converted string to JSON: {}", converted_value)
                return converted_value
            except (json.JSONDecodeError, ValueError) as e:
                logger.warning("Error converting string to JSON: {}", e)
                return value
        elif isinstance(value, int):
            logger.debug("Value is an integer: {}", value)
            return int(value)
        elif isinstance(value, float):
            logger.debug("Value is a float: {}", value)
            return float(value)
        elif isinstance(value, bool):
            logger.debug("Value is a boolean: {}", value)
            if value.lower() == 'true':
                return True
            elif value.lower() == 'false':
                return False
            else:
                logger.warning('Invalid boolean value')
                raise ValueError('Invalid boolean value')
        elif isinstance(value, (list, dict)):
            try:
                converted_value = json.loads(value)
                logger.debug("Successfully converted string to JSON: {}", converted_value)
                return converted_value
            except (json.JSONDecodeError, ValueError) as e:
                logger.warning("Error converting string to JSON: {}", e)
                return value
        else:
            logger.error('Unknown Type, type: {}', type(value))
            raise AttributeError(f'Unknown Type, type: {type(value)}')
