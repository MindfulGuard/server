from fastapi import Response

from mypass.configuration.configuration import Get
from mypass.core.response_status_codes import *


class Configuration:
    def get(self,response:Response):
        config = Get().execute()
        authentication = config.authentication()
        status_code:int = authentication[1]

        response.status_code = status_code
        if status_code == OK:
            return {"authentication":authentication[0]}
        else:
            return {"authentication":None}#INTERNAL_SERVER_ERROR