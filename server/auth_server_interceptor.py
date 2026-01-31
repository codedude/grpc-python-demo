"""Interceptor that ensures a specific header is present."""

import grpc
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def _unary_unary_rpc_terminator(code, details):
    def terminate(ignored_request, context):
        context.abort(code, details)

    return grpc.unary_unary_rpc_method_handler(terminate)


class RequestHeaderValidatorInterceptor(grpc.ServerInterceptor):
    def __init__(self, header, value, code, details):
        self._header = header
        self._value = value
        self._terminator = _unary_unary_rpc_terminator(code, details)

    def intercept_service(self, continuation, handler_call_details):
        if (
            (
                self._header,
                self._value,
            )
            in handler_call_details.invocation_metadata
            or handler_call_details.method
            in ["/grpc.health.v1.Health/Check", "/grpc.health.v1.Health/Watch"]
        ):
            return continuation(handler_call_details)
        else:
            return self._terminator
