# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import qwdata_pb2 as qwdata__pb2


class MarketDataServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SayHello = channel.unary_unary(
                '/qwdata.MarketDataService/SayHello',
                request_serializer=qwdata__pb2.HelloRequest.SerializeToString,
                response_deserializer=qwdata__pb2.HelloReply.FromString,
                )
        self.Auth = channel.unary_unary(
                '/qwdata.MarketDataService/Auth',
                request_serializer=qwdata__pb2.AuthRequest.SerializeToString,
                response_deserializer=qwdata__pb2.AuthResponse.FromString,
                )
        self.FetchData = channel.unary_stream(
                '/qwdata.MarketDataService/FetchData',
                request_serializer=qwdata__pb2.FetchDataRequest.SerializeToString,
                response_deserializer=qwdata__pb2.FetchDataResponse.FromString,
                )


class MarketDataServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SayHello(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Auth(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def FetchData(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MarketDataServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SayHello': grpc.unary_unary_rpc_method_handler(
                    servicer.SayHello,
                    request_deserializer=qwdata__pb2.HelloRequest.FromString,
                    response_serializer=qwdata__pb2.HelloReply.SerializeToString,
            ),
            'Auth': grpc.unary_unary_rpc_method_handler(
                    servicer.Auth,
                    request_deserializer=qwdata__pb2.AuthRequest.FromString,
                    response_serializer=qwdata__pb2.AuthResponse.SerializeToString,
            ),
            'FetchData': grpc.unary_stream_rpc_method_handler(
                    servicer.FetchData,
                    request_deserializer=qwdata__pb2.FetchDataRequest.FromString,
                    response_serializer=qwdata__pb2.FetchDataResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'qwdata.MarketDataService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class MarketDataService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SayHello(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/qwdata.MarketDataService/SayHello',
            qwdata__pb2.HelloRequest.SerializeToString,
            qwdata__pb2.HelloReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Auth(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/qwdata.MarketDataService/Auth',
            qwdata__pb2.AuthRequest.SerializeToString,
            qwdata__pb2.AuthResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def FetchData(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/qwdata.MarketDataService/FetchData',
            qwdata__pb2.FetchDataRequest.SerializeToString,
            qwdata__pb2.FetchDataResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
