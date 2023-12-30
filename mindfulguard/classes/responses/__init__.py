from typing import Any
from mindfulguard.languages.default_responses import DefaultResponses
from mindfulguard.languages.messages import Messages


class Responses:
    def __init__(self):
        self.__message: Messages = Messages()
    
    def custom(self) -> Messages:
        return self.__message
    
    def default(
            self,
            ok: dict[str, Any] = {},
            bad_request: dict[str, Any] = {},
            unauthorized: dict[str, Any] = {},
            not_found: dict[str, Any] = {},
            forbidden: dict[str, Any] = {},
            service_is_not_available: dict[str, Any] = {},
            internal_server_error: dict[str, Any] = {}
        ):
        return DefaultResponses(
            self.__message,
            ok,
            bad_request,
            unauthorized,
            not_found,
            forbidden,
            service_is_not_available,
            internal_server_error
        )