import logging
from concurrent import futures

import grpc
import pb.hello_pb2_grpc as pb2_grpc

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

MAX_MESSAGE_LENGTH = 1024 * 1024 * 20  # 20Mo


class GRPCServer:
    """
    Simple wrapper around grpc
    """

    def __init__(self, host: str, port: str) -> None:
        """
        Initialise internal data
        Dont throw exception.
        """
        self._host: str = host
        self._port: str = port
        self._server: grpc.Server = None

    def config(self, service: pb2_grpc.HelloServicer) -> bool:
        """
        :params HelloServicer: Concrete implementation of HelloServicer
        :rtype: bool
        :return: True if success, False on error
        """
        try:
            self._server = grpc.server(
                futures.ThreadPoolExecutor(max_workers=8),
                options=[
                    ("grpc.max_send_message_length", MAX_MESSAGE_LENGTH),
                    ("grpc.max_receive_message_length", MAX_MESSAGE_LENGTH),
                ],
            )
            self._server.add_insecure_port(f"{self._host}:{self._port}")
        except grpc.RpcError as e:
            logger.error(f"Cannot create the server: {e}")
            return False

        try:
            pb2_grpc.add_HelloServicer_to_server(service, self._server)
        except Exception as e:
            logger.error(f"Cannot add ApiServicer to the server: {e}")
            return False

        return True

    def start(self) -> bool:
        """
        Start the server, blocks until terminated.

        :return Return True if success, False on error
        """
        try:
            self._server.start()
        except grpc.RpcError as e:
            logger.error(f"GRPC server cannot start: {e}")
            return False
        logger.info(f"GRPC server started, listenning on port {self._port}")
        try:
            self._server.wait_for_termination()
        except grpc.RpcError as e:
            logger.error(f"GRPC server has terminated with an error: {e}")
            # Ignore it
            return True
        logger.info("GRPC server has terminated")
        return True

    def stop(self) -> None:
        """
        Gracefuylly stop the server
        """
        if self._server is None:
            logger.warning("Calling GRPCServer:stop() before start(), no effect")
            return
        try:
            self._server.stop(grace=0)
        except grpc.RpcError as e:
            logger.error(f"Cannot properly stop GRPCServer, ignoring: {e}")
            return
        finally:
            self._server = None
        logger.info("GRPC server stopped")

    def __del__(self) -> None:
        """
        Ensure connection is properly shutdown.
        """
        self.stop()
