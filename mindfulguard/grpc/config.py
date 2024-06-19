import os
from loguru import logger

class ServiceDynamicConfigurations:
    def __init__(self, host: str) -> None:
        self.__host: str = host

    @property
    def host(self) -> str:
        return self.__host

class GrpcConfiguration:
    @property
    def service_dynamic_configurations(self) -> ServiceDynamicConfigurations:
        host: str = os.environ.get('SERVICE_DYNAMIC_CONFIGURATIONS_HOST', '')

        logger.debug("Host grpc server: {}. Service: 'dynamic_configurations'.", host)

        return ServiceDynamicConfigurations(host)
    
