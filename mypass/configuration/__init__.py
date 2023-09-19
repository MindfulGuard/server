from fastapi import Response

from mypass.configuration.configuration import Get
from mypass.core.languages import Language
from mypass.core.languages.responses import Responses
from mypass.core.response_status_codes import *


class Configuration:
    def __init__(self):
        self.__lang = Language()
        self.__json_responses = Responses(self.__lang)

    def get(self,response:Response):
        config = Get().execute()
        authentication = config.authentication()
        status_code:int = authentication[1]

        response.status_code = status_code
        if status_code == OK:
            return {"authentication":authentication[0]}
        else:
            return self.__json_responses.server_error()#INTERNAL_SERVER_ERROR