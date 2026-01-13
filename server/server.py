import logging
import sys

import hello_service
import grpc_server

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)


def start_server(host: str, port: str) -> int:
    server = grpc_server.GRPCServer(host, port)
    ret = server.config(hello_service.HelloService())
    if not ret:
        return 1

    ret = server.start()
    if not ret:
        return 1

    server.stop()

    return 0


if __name__ == '__main__':
    sys.exit(start_server(host="0.0.0.0", port="8042"))
