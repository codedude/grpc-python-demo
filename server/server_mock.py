import logging
import grpc_testing

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class GRPCServerMock(grpc_testing.Server):
    def invoke_unary_unary(
        self, method_descriptor, invocation_metadata, request, timeout
    ):
        """Invokes an RPC to be serviced by the system under test.

        Args:
          method_descriptor: A descriptor.MethodDescriptor describing a unary-unary
            RPC method.
          invocation_metadata: The RPC's invocation metadata.
          request: The RPC's request.
          timeout: A duration of time in seconds for the RPC or None to
            indicate that the RPC has no time limit.

        Returns:
          A UnaryUnaryServerRpc with which to "play client" for the RPC.
        """
        print(method_descriptor, request)
        pass

    def invoke_unary_stream(
        self, method_descriptor, invocation_metadata, request, timeout
    ):
        """Invokes an RPC to be serviced by the system under test.

        Args:
          method_descriptor: A descriptor.MethodDescriptor describing a unary-stream
            RPC method.
          invocation_metadata: The RPC's invocation metadata.
          request: The RPC's request.
          timeout: A duration of time in seconds for the RPC or None to
            indicate that the RPC has no time limit.

        Returns:
          A UnaryStreamServerRpc with which to "play client" for the RPC.
        """
        pass

    def invoke_stream_unary(self, method_descriptor, invocation_metadata, timeout):
        """Invokes an RPC to be serviced by the system under test.

        Args:
          method_descriptor: A descriptor.MethodDescriptor describing a stream-unary
            RPC method.
          invocation_metadata: The RPC's invocation metadata.
          timeout: A duration of time in seconds for the RPC or None to
            indicate that the RPC has no time limit.

        Returns:
          A StreamUnaryServerRpc with which to "play client" for the RPC.
        """
        pass

    def invoke_stream_stream(self, method_descriptor, invocation_metadata, timeout):
        """Invokes an RPC to be serviced by the system under test.

        Args:
          method_descriptor: A descriptor.MethodDescriptor describing a stream-stream
            RPC method.
          invocation_metadata: The RPC's invocation metadata.
          timeout: A duration of time in seconds for the RPC or None to
            indicate that the RPC has no time limit.

        Returns:
          A StreamStreamServerRpc with which to "play client" for the RPC.
        """
        pass
