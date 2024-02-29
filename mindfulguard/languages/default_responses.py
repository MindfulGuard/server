from http.client import BAD_REQUEST, CONFLICT, FORBIDDEN, INTERNAL_SERVER_ERROR, NOT_FOUND, OK, SERVICE_UNAVAILABLE, UNAUTHORIZED
from typing import Any
from mindfulguard.exceptions.incorrect_parameters import ExceptionIncorrectParameters
from mindfulguard.languages.messages import Messages

class DefaultResponses:
    def __init__(
        self,
        message: Messages,
        ok: dict[str, Any] = {},
        bad_request: dict[str, Any] = {},
        unauthorized: dict[str, Any] = {},
        not_found: dict[str, Any] = {},
        forbidden: dict[str, Any] = {},
        conflict: dict[str, Any] = {},
        service_is_not_available: dict[str, Any] = {},
        internal_server_error: dict[str, Any] = {}
    ) -> None:
        self.__message: Messages = message
        self.__ok: dict[str, Any] = ok
        self.__bad_request: dict[str, Any] = bad_request
        self.__not_found: dict[str, Any] = not_found
        self.__forbidden: dict[str, Any] = forbidden
        self.__conflict: dict[str, Any] = conflict
        self.__unauthorized: dict[str, Any] = unauthorized
        self.__service_is_not_available: dict[str, Any] = service_is_not_available
        self.__internal_server_error: dict[str, Any] = internal_server_error

    def get(self, status_code: int) -> dict[str, Any]:
        if status_code == OK:
            return self.__check_if_custom(self.__message.get("successfully"), self.__ok)
        elif status_code == BAD_REQUEST:
            return self.__check_if_custom(self.__message.get("data_not_valid"), self.__bad_request)
        elif status_code == UNAUTHORIZED:
            return self.__check_if_custom(self.__message.get("unauthorized"), self.__unauthorized)
        elif status_code == NOT_FOUND:
            return self.__check_if_custom(self.__message.get("not_found"), self.__not_found)
        elif status_code == FORBIDDEN:
            return self.__check_if_custom(self.__message.get("access_denied"), self.__forbidden)
        elif status_code == CONFLICT:
            return self.__check_if_custom(self.__message.get("conflict"), self.__conflict)
        elif status_code == SERVICE_UNAVAILABLE:
            return self.__check_if_custom(self.__message.get("service_is_not_available"), self.__service_is_not_available)
        elif status_code == INTERNAL_SERVER_ERROR:
            return self.__check_if_custom(self.__message.get("server_error"), self.__internal_server_error)
        else:
            raise ExceptionIncorrectParameters(f'Unknown Parameter: {status_code}')

    def __check_if_custom(
            self,
            message: dict[str, Any],
            custom_message: dict[str, Any]
        ) -> dict[str, dict[str, Any]]:
        if len(custom_message) == 0:
            return {"msg": message}
        return {"msg": custom_message}