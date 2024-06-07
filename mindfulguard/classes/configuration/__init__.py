from http.client import OK
from fastapi import Response
from mindfulguard.classes.database.redis import Redis
from redis.commands.json.path import Path


class Configuration:
    def __init__(self, response: Response) -> None:
        from mindfulguard.api_configuration.public import ConfigurationPublic
        self.__response: Response = response
        self.__configuration_public = ConfigurationPublic()
        self.__redis = Redis()
        self.__cache_name: str = f'{self.__redis.CACHE_NAME_SETTINGS}:public'

    async def public(self):
        response_cache = self.__redis.client().connection.json().get(self.__cache_name) # type: ignore
        if response_cache:
            self.__response.status_code = OK
            return response_cache

        await self.__configuration_public.execute()
        self.__response.status_code = self.__configuration_public.status_code
        self.__redis.client().connection.json().set(
            self.__cache_name,
            Path.root_path(),
            self.__configuration_public.response
        )
        self.__redis.client().connection.expire(self.__cache_name, 3600)
        return self.__configuration_public.response