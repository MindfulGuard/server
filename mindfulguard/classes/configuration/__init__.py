from fastapi import Response


class Configuration:
    def __init__(self, response: Response) -> None:
        from mindfulguard.configuration.public import ConfigurationPublic
        self.__response: Response = response
        self.__configuration_public = ConfigurationPublic()

    async def public(self):
        await self.__configuration_public.execute()
        self.__response.status_code = self.__configuration_public.status_code
        return self.__configuration_public.response