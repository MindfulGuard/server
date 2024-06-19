from typing import Generic, TypeVar, Union
import grpc
from loguru import logger
from mindfulguard.classes.grpc.base import BaseGrpc
import mindfulguard.grpc.gen.dynamic_configurations_pb2_grpc as pb2_grpc
import mindfulguard.grpc.gen.dynamic_configurations_pb2 as pb2

T = TypeVar('T', pb2.PutResponse, pb2.GetResponse, pb2.GetListResponse, pb2.DeleteResponse, pb2.DeleteTreeResponse)
class GrpcDynamicConfigurationsMethods(BaseGrpc):
    class __Response(Generic[T]):
        def __init__(self, data: Union[T, None], error: Union[grpc.StatusCode, None]) -> None:
            self.__data: Union[T, None] = data
            self.__error: Union[grpc.StatusCode, None] = error

        @property
        def data(self) -> Union[T, None]:
            return self.__data
        
        @property
        def error(self) -> Union[grpc.StatusCode, None]:
            return self.__error

    def __init__(self) -> None:
        super().__init__()
        self._channel = self._create_channel()

    def _create_channel(self) -> grpc.aio._channel.Channel:
        host = self._configuration.service_dynamic_configurations.host
        logger.info(f"Creating channel to host: {host}")
        return grpc.aio.insecure_channel(host)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        logger.info("Closing channel")
        await self._channel.close()

    async def put(self, key: str, value: bytes) -> __Response[pb2.PutResponse]:
        try:
            logger.info(f"Put request initiated with key: {key} and value: {value}")
            stub = pb2_grpc.DynamicConfigurationsStub(self._channel)
            request = pb2.PutRequest(key=key, value=value)
            response = await stub.Put(request)
            logger.info(f"Put request successful for key: {key}")
            logger.trace("The execution time of the put operation: {} ms. Timestamp: {}.", response.executionTimeMilliseconds, response.timestamp)
            return self.__Response(response, grpc.StatusCode.OK)
        except grpc.RpcError as e:
            logger.error(f"Put request failed for key: {key} with error: {e.code()}") # type: ignore
            return self.__Response(None, e.code()) # type: ignore
            
    async def get(self, key: str) -> __Response[pb2.GetResponse]:
        try:
            logger.info(f"Get request initiated for key: {key}")
            stub = pb2_grpc.DynamicConfigurationsStub(self._channel)
            request = pb2.GetRequest(key=key)
            response = await stub.Get(request)
            logger.info(f"Get request successful for key: {key}")
            logger.trace("The execution time of the put operation: {} ms. Timestamp: {}.", response.executionTimeMilliseconds, response.timestamp)
            return self.__Response(response, grpc.StatusCode.OK)
        except grpc.RpcError as e:
            logger.error(f"Get request failed for key: {key} with error: {e.code()}") # type: ignore
            return self.__Response(None, e.code()) # type: ignore
            
    async def get_list(self, prefix: str) -> __Response[pb2.GetListResponse]:
        try:
            logger.info(f"GetList request initiated with prefix: {prefix}")
            stub = pb2_grpc.DynamicConfigurationsStub(self._channel)
            request = pb2.GetListRequest(prefix=prefix)
            response = await stub.GetList(request)
            logger.info(f"GetList request successful for prefix: {prefix}")
            logger.trace("The execution time of the put operation: {} ms. Timestamp: {}.", response.executionTimeMilliseconds, response.timestamp)
            return self.__Response(response, grpc.StatusCode.OK)
        except grpc.RpcError as e:
            logger.error(f"GetList request failed for prefix: {prefix} with error: {e.code()}") # type: ignore
            return self.__Response(None, e.code()) # type: ignore
            
    async def delete(self, key: str) -> __Response[pb2.DeleteResponse]:
        try:
            logger.info(f"Delete request initiated for key: {key}")
            stub = pb2_grpc.DynamicConfigurationsStub(self._channel)
            request = pb2.DeleteRequest(key=key)
            response = await stub.Delete(request)
            logger.info(f"Delete request successful for key: {key}")
            logger.trace("The execution time of the put operation: {} ms. Timestamp: {}.", response.executionTimeMilliseconds, response.timestamp)
            return self.__Response(response, grpc.StatusCode.OK)
        except grpc.RpcError as e:
            logger.error(f"Delete request failed for key: {key} with error: {e.code()}") # type: ignore
            return self.__Response(None, e.code()) # type: ignore
            
    async def delete_tree(self, prefix: str) -> __Response[pb2.DeleteTreeResponse]:
        try:
            logger.info(f"DeleteTree request initiated for prefix: {prefix}")
            stub = pb2_grpc.DynamicConfigurationsStub(self._channel)
            request = pb2.DeleteTreeRequest(prefix=prefix)
            response = await stub.DeleteTree(request)
            logger.info(f"DeleteTree request successful for prefix: {prefix}")
            logger.trace("The execution time of the put operation: {} ms. Timestamp: {}.", response.executionTimeMilliseconds, response.timestamp)
            return self.__Response(response, grpc.StatusCode.OK)
        except grpc.RpcError as e:
            logger.error(f"DeleteTree request failed for prefix: {prefix} with error: {e.code()}") # type: ignore
            return self.__Response(None, e.code()) # type: ignore
