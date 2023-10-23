from fastapi import Response

from mindfulguard.configuration.configuration import Get
from mindfulguard.core.languages import Language
from mindfulguard.core.languages.responses import Responses
from mindfulguard.core.response_status_codes import *


class Configuration:
    def __init__(self):
        self.__lang = Language()
        self.__json_responses = Responses(self.__lang)

    async def get(self,response:Response):
        config = Get().execute()
        authentication = await config.authentication()
        item = await config.item()
        status_code:int = authentication[1]

        response.status_code = status_code
        if status_code == OK:
            return {
                "password_rule":authentication[0],
                "item_categories":item[0],
                "item_types":item[1]
            }
        else:
            return self.__json_responses.server_error()#INTERNAL_SERVER_ERROR