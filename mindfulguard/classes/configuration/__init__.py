from http.client import OK
from fastapi import Response
from mindfulguard.classes.database.redis import Redis
from redis.commands.json.path import Path


class Configuration:
    def __init__(self, response: Response) -> None:
        from mindfulguard.api_configuration.public import ConfigurationPublic
        self.__response: Response = response
        self.__configuration_public = ConfigurationPublic()

    async def public(self):
        await self.__configuration_public.execute()
        
        self.__response.status_code = self.__configuration_public.status_code
        return self.__configuration_public.response