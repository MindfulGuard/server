from fastapi import Response

from mindfulguard.configuration.configuration import Get
from mindfulguard.core.languages import Language
from mindfulguard.core.languages.responses import Responses
from mindfulguard.core.response_status_codes import *


class Configuration:
    def __init__(self):
        self.__lang = Language()
        self.__json_responses = Responses(self.__lang)

    def get(self,response:Response):
        config = Get().execute()
        authentication = config.authentication()
        item =config.item()
        status_code:int = authentication[1]

        response.status_code = status_code
        if status_code == OK:
            return {"authentication":authentication[0], "item":item[0]}
        else:
            return self.__json_responses.server_error()#INTERNAL_SERVER_ERROR