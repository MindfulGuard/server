from abc import ABC, abstractmethod
import grpc
from mindfulguard.grpc.config import GrpcConfiguration

class BaseGrpc(ABC):
    def __init__(self) -> None:
        self._configuration = GrpcConfiguration()

    @abstractmethod
    def _create_channel(self) -> grpc.aio._channel.Channel:...

    @abstractmethod
    async def __aenter__(self) -> None:...

    @abstractmethod
    async def __aexit__(self, exc_type, exc, tb) -> None:...
