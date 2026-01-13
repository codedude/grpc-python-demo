import json
import logging

import grpc
import pb.hello_pb2 as pb2
import pb.hello_pb2_grpc as pb2_grpc

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)


class HelloService(pb2_grpc.HelloServicer):
    def __init__(self):
        logger.info("HelloService initialized")

    def _error(self, context: grpc.RpcContext, code: int, msg: str) -> None:
        context.set_code(code)
        context.set_details(msg)
        return None

    def SayHello(self, request, context):
        logger.info("Call to HelloService:SayHello")
        return pb2.HelloResponse(message=f"Hello, {request.name}!")
