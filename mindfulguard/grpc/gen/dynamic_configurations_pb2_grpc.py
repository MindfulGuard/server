# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

# Fixed import!
import mindfulguard.grpc.gen.dynamic_configurations_pb2 as dynamic__configurations__pb2

GRPC_GENERATED_VERSION = '1.64.1'
GRPC_VERSION = grpc.__version__
EXPECTED_ERROR_RELEASE = '1.65.0'
SCHEDULED_RELEASE_DATE = 'June 25, 2024'
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    warnings.warn(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in dynamic_configurations_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class DynamicConfigurationsStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Put = channel.unary_unary(
                '/dynamic_configurations.DynamicConfigurations/Put',
                request_serializer=dynamic__configurations__pb2.PutRequest.SerializeToString,
                response_deserializer=dynamic__configurations__pb2.PutResponse.FromString,
                _registered_method=True)
        self.Get = channel.unary_unary(
                '/dynamic_configurations.DynamicConfigurations/Get',
                request_serializer=dynamic__configurations__pb2.GetRequest.SerializeToString,
                response_deserializer=dynamic__configurations__pb2.GetResponse.FromString,
                _registered_method=True)
        self.GetList = channel.unary_unary(
                '/dynamic_configurations.DynamicConfigurations/GetList',
                request_serializer=dynamic__configurations__pb2.GetListRequest.SerializeToString,
                response_deserializer=dynamic__configurations__pb2.GetListResponse.FromString,
                _registered_method=True)
        self.Delete = channel.unary_unary(
                '/dynamic_configurations.DynamicConfigurations/Delete',
                request_serializer=dynamic__configurations__pb2.DeleteRequest.SerializeToString,
                response_deserializer=dynamic__configurations__pb2.DeleteResponse.FromString,
                _registered_method=True)
        self.DeleteTree = channel.unary_unary(
                '/dynamic_configurations.DynamicConfigurations/DeleteTree',
                request_serializer=dynamic__configurations__pb2.DeleteTreeRequest.SerializeToString,
                response_deserializer=dynamic__configurations__pb2.DeleteTreeResponse.FromString,
                _registered_method=True)


class DynamicConfigurationsServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Put(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Get(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetList(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Delete(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteTree(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DynamicConfigurationsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Put': grpc.unary_unary_rpc_method_handler(
                    servicer.Put,
                    request_deserializer=dynamic__configurations__pb2.PutRequest.FromString,
                    response_serializer=dynamic__configurations__pb2.PutResponse.SerializeToString,
            ),
            'Get': grpc.unary_unary_rpc_method_handler(
                    servicer.Get,
                    request_deserializer=dynamic__configurations__pb2.GetRequest.FromString,
                    response_serializer=dynamic__configurations__pb2.GetResponse.SerializeToString,
            ),
            'GetList': grpc.unary_unary_rpc_method_handler(
                    servicer.GetList,
                    request_deserializer=dynamic__configurations__pb2.GetListRequest.FromString,
                    response_serializer=dynamic__configurations__pb2.GetListResponse.SerializeToString,
            ),
            'Delete': grpc.unary_unary_rpc_method_handler(
                    servicer.Delete,
                    request_deserializer=dynamic__configurations__pb2.DeleteRequest.FromString,
                    response_serializer=dynamic__configurations__pb2.DeleteResponse.SerializeToString,
            ),
            'DeleteTree': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteTree,
                    request_deserializer=dynamic__configurations__pb2.DeleteTreeRequest.FromString,
                    response_serializer=dynamic__configurations__pb2.DeleteTreeResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'dynamic_configurations.DynamicConfigurations', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('dynamic_configurations.DynamicConfigurations', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class DynamicConfigurations(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Put(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/dynamic_configurations.DynamicConfigurations/Put',
            dynamic__configurations__pb2.PutRequest.SerializeToString,
            dynamic__configurations__pb2.PutResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/dynamic_configurations.DynamicConfigurations/Get',
            dynamic__configurations__pb2.GetRequest.SerializeToString,
            dynamic__configurations__pb2.GetResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetList(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/dynamic_configurations.DynamicConfigurations/GetList',
            dynamic__configurations__pb2.GetListRequest.SerializeToString,
            dynamic__configurations__pb2.GetListResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Delete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/dynamic_configurations.DynamicConfigurations/Delete',
            dynamic__configurations__pb2.DeleteRequest.SerializeToString,
            dynamic__configurations__pb2.DeleteResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DeleteTree(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/dynamic_configurations.DynamicConfigurations/DeleteTree',
            dynamic__configurations__pb2.DeleteTreeRequest.SerializeToString,
            dynamic__configurations__pb2.DeleteTreeResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
