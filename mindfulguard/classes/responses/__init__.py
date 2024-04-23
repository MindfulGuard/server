from http.client import ACCEPTED, BAD_GATEWAY, BAD_REQUEST, CONFLICT, CONTINUE, CREATED, EXPECTATION_FAILED, FORBIDDEN, FOUND, GATEWAY_TIMEOUT, GONE, HTTP_VERSION_NOT_SUPPORTED, IM_USED, INTERNAL_SERVER_ERROR, LENGTH_REQUIRED, METHOD_NOT_ALLOWED, MOVED_PERMANENTLY, MULTIPLE_CHOICES, NETWORK_AUTHENTICATION_REQUIRED, NO_CONTENT, NON_AUTHORITATIVE_INFORMATION, NOT_ACCEPTABLE, NOT_EXTENDED, NOT_FOUND, NOT_IMPLEMENTED, NOT_MODIFIED, OK, PARTIAL_CONTENT, PAYMENT_REQUIRED, PRECONDITION_FAILED, PRECONDITION_REQUIRED, PROXY_AUTHENTICATION_REQUIRED, REQUEST_HEADER_FIELDS_TOO_LARGE, REQUEST_TIMEOUT, REQUESTED_RANGE_NOT_SATISFIABLE, RESET_CONTENT, SEE_OTHER, SERVICE_UNAVAILABLE, SWITCHING_PROTOCOLS, TEMPORARY_REDIRECT, TOO_MANY_REQUESTS, UNAUTHORIZED, UNSUPPORTED_MEDIA_TYPE, UPGRADE_REQUIRED
from typing import Any

from mindfulguard.exceptions.http import InvalidHttpStatusCode


class EntityResponse:
    def __init__(self) -> None:
        self.__status_code: int
        self.__description: str

    @property
    def status_code(self) -> int:
        return self.__status_code
    
    @status_code.setter
    def status_code(self, value: int) -> None:
        self.__status_code = value

    @property
    def description(self) -> str:
        return self.__description
    
    @description.setter
    def description(self, value: str) -> None:
        self.__description = value

    def to_json(self) -> dict[str, Any]:
        return {
            "status_code": self.__status_code,
            "description": self.__description
        }

class HttpResponse:
    """
    Information source: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
    """
    def __init__(self) -> None:
        self.__entity_response = EntityResponse()
    
    @property
    def continue_(self) -> EntityResponse:
        self.__entity_response.status_code = CONTINUE
        self.__entity_response.description = "Continue"
        return self.__entity_response

    @property
    def switching_protocols(self) -> EntityResponse:
        self.__entity_response.status_code = SWITCHING_PROTOCOLS
        self.__entity_response.description = "Switching Protocols"
        return self.__entity_response
    
    @property
    def ok(self) -> EntityResponse:
        self.__entity_response.status_code = OK
        self.__entity_response.description = "OK"
        return self.__entity_response
    
    @property
    def created(self) -> EntityResponse:
        self.__entity_response.status_code = CREATED
        self.__entity_response.description = "Created"
        return self.__entity_response
    
    @property
    def accepted(self) -> EntityResponse:
        self.__entity_response.status_code = ACCEPTED
        self.__entity_response.description = "Accepted"
        return self.__entity_response
    
    @property
    def non_authoritative_information(self) -> EntityResponse:
        self.__entity_response.status_code = NON_AUTHORITATIVE_INFORMATION
        self.__entity_response.description = "Non-Authoritative Information"
        return self.__entity_response
    
    @property
    def no_content(self) -> EntityResponse:
        self.__entity_response.status_code = NO_CONTENT
        self.__entity_response.description = "No Content"
        return self.__entity_response
    
    @property
    def reset_content(self) -> EntityResponse:
        self.__entity_response.status_code = RESET_CONTENT
        self.__entity_response.description = "Reset Content"
        return self.__entity_response

    @property
    def partial_content(self) -> EntityResponse:
        self.__entity_response.status_code = PARTIAL_CONTENT
        self.__entity_response.description = "Partial Content"
        return self.__entity_response
    
    @property
    def im_used(self) -> EntityResponse:
        self.__entity_response.status_code = IM_USED
        self.__entity_response.description = "IM Used"
        return self.__entity_response
    
    @property
    def multiple_choices(self) -> EntityResponse:
        self.__entity_response.status_code = MULTIPLE_CHOICES
        self.__entity_response.description = "Multiple Choices"
        return self.__entity_response
    
    @property
    def moved_permanently(self) -> EntityResponse:
        self.__entity_response.status_code = MOVED_PERMANENTLY
        self.__entity_response.description = "Moved Permanently"
        return self.__entity_response
    
    @property
    def found(self) -> EntityResponse:
        self.__entity_response.status_code = FOUND
        self.__entity_response.description = "Found"
        return self.__entity_response
    
    @property
    def see_other(self) -> EntityResponse:
        self.__entity_response.status_code = SEE_OTHER
        self.__entity_response.description = "See Other"
        return self.__entity_response
    
    @property
    def not_modified(self) -> EntityResponse:
        self.__entity_response.status_code = NOT_MODIFIED
        self.__entity_response.description = "Not Modified"
        return self.__entity_response

    @property
    def temporary_redirect(self) -> EntityResponse:
        self.__entity_response.status_code = TEMPORARY_REDIRECT
        self.__entity_response.description = "Temporary Redirect"
        return self.__entity_response
    
    @property
    def permanent_redirect(self) -> EntityResponse:
        self.__entity_response.status_code = 308
        self.__entity_response.description = "Permanent Redirect"
        return self.__entity_response
    
    @property
    def bad_request(self) -> EntityResponse:
        self.__entity_response.status_code = BAD_REQUEST
        self.__entity_response.description = "Bad Request"
        return self.__entity_response
    
    @property
    def unauthorized(self) -> EntityResponse:
        self.__entity_response.status_code = UNAUTHORIZED
        self.__entity_response.description = "Unauthorized"
        return self.__entity_response
    
    @property
    def payment_required(self) -> EntityResponse:
        self.__entity_response.status_code = PAYMENT_REQUIRED
        self.__entity_response.description = "Payment Required"
        return self.__entity_response
    
    @property
    def forbidden(self) -> EntityResponse:
        self.__entity_response.status_code = FORBIDDEN
        self.__entity_response.description = "Forbidden"
        return self.__entity_response
    
    @property
    def not_found(self) -> EntityResponse:
        self.__entity_response.status_code = NOT_FOUND
        self.__entity_response.description = "Not Found"
        return self.__entity_response
    
    @property
    def method_not_allowed(self) -> EntityResponse:
        self.__entity_response.status_code = METHOD_NOT_ALLOWED
        self.__entity_response.description = "Method Not Allowed"
        return self.__entity_response
    
    @property
    def not_acceptable(self) -> EntityResponse:
        self.__entity_response.status_code = NOT_ACCEPTABLE
        self.__entity_response.description = "Not Acceptable"
        return self.__entity_response
    
    @property
    def proxy_authentication_required(self) -> EntityResponse:
        self.__entity_response.status_code = PROXY_AUTHENTICATION_REQUIRED
        self.__entity_response.description = "Proxy Authentication Required"
        return self.__entity_response
    
    @property
    def request_timeout(self) -> EntityResponse:
        self.__entity_response.status_code = REQUEST_TIMEOUT
        self.__entity_response.description = "Request Timeout"
        return self.__entity_response
    
    @property
    def conflict(self) -> EntityResponse:
        self.__entity_response.status_code = CONFLICT
        self.__entity_response.description = "Conflict"
        return self.__entity_response
    
    @property
    def gone(self) -> EntityResponse:
        self.__entity_response.status_code = GONE
        self.__entity_response.description = "Gone"
        return self.__entity_response
    
    @property
    def length_required(self) -> EntityResponse:
        self.__entity_response.status_code = LENGTH_REQUIRED
        self.__entity_response.description = "Length Required"
        return self.__entity_response
    
    @property
    def precondition_failed(self) -> EntityResponse:
        self.__entity_response.status_code = PRECONDITION_FAILED
        self.__entity_response.description = "Precondition Failed"
        return self.__entity_response
    
    @property
    def unsupported_media_type(self) -> EntityResponse:
        self.__entity_response.status_code = UNSUPPORTED_MEDIA_TYPE
        self.__entity_response.description = "Unsupported Media Type"
        return self.__entity_response
    
    @property
    def range_not_satisfiable(self) -> EntityResponse:
        self.__entity_response.status_code = REQUESTED_RANGE_NOT_SATISFIABLE
        self.__entity_response.description = "Range Not Satisfiable"
        return self.__entity_response
    
    @property
    def expectation_failed(self) -> EntityResponse:
        self.__entity_response.status_code = EXPECTATION_FAILED
        self.__entity_response.description = "Expectation Failed"
        return self.__entity_response
    
    @property
    def upgrade_required(self) -> EntityResponse:
        self.__entity_response.status_code = UPGRADE_REQUIRED
        self.__entity_response.description = "Upgrade Required"
        return self.__entity_response
    
    @property
    def precondition_required(self) -> EntityResponse:
        self.__entity_response.status_code = PRECONDITION_REQUIRED
        self.__entity_response.description = "Precondition Required"
        return self.__entity_response
    
    @property
    def too_many_requests(self) -> EntityResponse:
        self.__entity_response.status_code = TOO_MANY_REQUESTS
        self.__entity_response.description = "Too Many Requests"
        return self.__entity_response
    
    @property
    def request_header_fields_too_large(self) -> EntityResponse:
        self.__entity_response.status_code = REQUEST_HEADER_FIELDS_TOO_LARGE
        self.__entity_response.description = "Request Header Fields Too Large"
        return self.__entity_response
    
    @property
    def internal_server_error(self) -> EntityResponse:
        self.__entity_response.status_code = INTERNAL_SERVER_ERROR
        self.__entity_response.description = "Internal Server Error"
        return self.__entity_response
    
    @property
    def not_implemented(self) -> EntityResponse:
        self.__entity_response.status_code = NOT_IMPLEMENTED
        self.__entity_response.description = "Not Implemented"
        return self.__entity_response
    
    @property
    def bad_gateway(self) -> EntityResponse:
        self.__entity_response.status_code = BAD_GATEWAY
        self.__entity_response.description = "Bad Gateway"
        return self.__entity_response
    
    @property
    def service_unavailable(self) -> EntityResponse:
        self.__entity_response.status_code = SERVICE_UNAVAILABLE
        self.__entity_response.description = "Service Unavailable"
        return self.__entity_response
    
    @property
    def gateway_timeout(self) -> EntityResponse:
        self.__entity_response.status_code = GATEWAY_TIMEOUT
        self.__entity_response.description = "Gateway Timeout"
        return self.__entity_response
    
    @property
    def http_version_not_supported(self) -> EntityResponse:
        self.__entity_response.status_code = HTTP_VERSION_NOT_SUPPORTED
        self.__entity_response.description = "HTTP Version Not Supported"
        return self.__entity_response
    
    @property
    def not_extended(self) -> EntityResponse:
        self.__entity_response.status_code = NOT_EXTENDED
        self.__entity_response.description = "Not Extended"
        return self.__entity_response
    
    @property
    def network_authentication_required(self) -> EntityResponse:
        self.__entity_response.status_code = NETWORK_AUTHENTICATION_REQUIRED
        self.__entity_response.description = "Network Authentication Required"
        return self.__entity_response
    
    def get(self, status_code: int) -> EntityResponse:
        if status_code == CONTINUE:
            return self.continue_
        elif status_code == SWITCHING_PROTOCOLS:
            return self.switching_protocols
        elif status_code == OK:
            return self.ok
        elif status_code == CREATED:
            return self.created
        elif status_code == NON_AUTHORITATIVE_INFORMATION:
            return self.non_authoritative_information
        elif status_code == NO_CONTENT:
            return self.no_content
        elif status_code == RESET_CONTENT:
            return self.reset_content
        elif status_code == PARTIAL_CONTENT:
            return self.partial_content
        elif status_code == IM_USED:
            return self.im_used
        elif status_code == MULTIPLE_CHOICES:
            return self.multiple_choices
        elif status_code == MOVED_PERMANENTLY:
            return self.moved_permanently
        elif status_code == FOUND:
            return self.found
        elif status_code == SEE_OTHER:
            return self.see_other
        elif status_code == NOT_MODIFIED:
            return self.not_modified
        elif status_code == TEMPORARY_REDIRECT:
            return self.temporary_redirect
        elif status_code == 308:
            return self.permanent_redirect
        elif status_code == BAD_REQUEST:
            return self.bad_request
        elif status_code == UNAUTHORIZED:
            return self.unauthorized
        elif status_code == PAYMENT_REQUIRED:
            return self.payment_required
        elif status_code == FORBIDDEN:
            return self.forbidden
        elif status_code == NOT_FOUND:
            return self.not_found
        elif status_code == METHOD_NOT_ALLOWED:
            return self.method_not_allowed
        elif status_code == NOT_ACCEPTABLE:
            return self.not_acceptable
        elif status_code == PROXY_AUTHENTICATION_REQUIRED:
            return self.proxy_authentication_required
        elif status_code == REQUEST_TIMEOUT:
            return self.request_timeout
        elif status_code == CONFLICT:
            return self.conflict
        elif status_code == GONE:
            return self.gone
        elif status_code == LENGTH_REQUIRED:
            return self.length_required
        elif status_code == PRECONDITION_FAILED:
            return self.precondition_failed
        elif status_code == UNSUPPORTED_MEDIA_TYPE:
            return self.unsupported_media_type
        elif status_code == EXPECTATION_FAILED:
            return self.expectation_failed
        elif status_code == UPGRADE_REQUIRED:
            return self.upgrade_required
        elif status_code == PRECONDITION_REQUIRED:
            return self.precondition_required
        elif status_code == TOO_MANY_REQUESTS:
            return self.too_many_requests
        elif status_code == REQUEST_HEADER_FIELDS_TOO_LARGE:
            return self.request_header_fields_too_large
        elif status_code == INTERNAL_SERVER_ERROR:
            return self.internal_server_error
        elif status_code == NOT_IMPLEMENTED:
            return self.not_implemented
        elif status_code == BAD_GATEWAY:
            return self.bad_gateway
        elif status_code == SERVICE_UNAVAILABLE:
            return self.service_unavailable
        elif status_code == GATEWAY_TIMEOUT:
            return self.gateway_timeout
        elif status_code == HTTP_VERSION_NOT_SUPPORTED:
            return self.http_version_not_supported
        elif status_code == NOT_EXTENDED:
            return self.not_extended
        elif status_code == NETWORK_AUTHENTICATION_REQUIRED:
            return self.network_authentication_required
        else:
            raise InvalidHttpStatusCode()