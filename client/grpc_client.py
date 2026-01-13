import logging
from types import SimpleNamespace
from typing import Any

import grpc
import pb.hello_pb2 as pb2
import pb.hello_pb2_grpc as pb2_grpc
from google.protobuf.json_format import MessageToDict

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)


class HelloClient(object):
    """
    Client for gRPC functionality
    """

    NO_ERROR_MSG = SimpleNamespace(**{"code": grpc.StatusCode.OK, "details": ""})

    def __init__(self, host: str, port: str) -> None:
        """
        Initialise internal data
        Dont throw exception.
        """
        self._host = host
        self._port = port
        self._stub = None

    def instantiate(self) -> bool:
        """
        :rtype: bool
        :return: True if success, False on error
        """
        try:
            channel = grpc.insecure_channel(f"{self._host}:{self._port}")
            self._stub = pb2_grpc.HelloStub(channel)
        except Exception as e:
            logger.error(f"HelloClient:instantiate(): {e}")
            return False
        return True

    def _request(self, func_msg: Any, func_stub: Any, **kwargs: Any) -> Any:
        """
        Encapsulate the grpc call, so it can format error response correctly
        """
        request = func_msg(**kwargs)
        try:
            response = func_stub(request)
        except grpc.RpcError as e:
            return SimpleNamespace(
                **{
                    "error": SimpleNamespace(
                        **{"code": e.code(), "details": e.details()}
                    )
                }
            )
        response_as_dict = MessageToDict(
            response,
            preserving_proto_field_name=True,
            use_integers_for_enums=False,
            always_print_fields_with_no_presence=True,
        )
        data = SimpleNamespace(**response_as_dict)
        data.__setattr__("error", self.NO_ERROR_MSG)
        return data

    def say_hello(self, name: str):
        return self._request(pb2.HelloRequest, self._stub.SayHello, name=name)


if __name__ == "__main__":
    import sys

    client = HelloClient(host="0.0.0.0", port="8042")
    ret = client.instantiate()
    if not ret:
        sys.exit(1)
    sys.exit(0)
