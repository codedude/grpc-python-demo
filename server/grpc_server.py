import logging
import threading
from concurrent import futures
import time
import grpc
from grpc_health.v1 import health
from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc

import pb.generated.demo_pb2_grpc as pb2_grpc

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

MAX_MESSAGE_LENGTH = 1024 * 1024 * 16  # 16Mo


def _check_health(health_servicer: health.HealthServicer, service: str):
    counter = 1
    while True:
        if counter % 3 == 0:
            health_servicer.set(service, health_pb2.HealthCheckResponse.NOT_SERVING)
        else:
            health_servicer.set(service, health_pb2.HealthCheckResponse.SERVING)
        counter += 1
        time.sleep(1)


def _configure_health_server(server: grpc.Server):
    health_servicer = health.HealthServicer(
        experimental_non_blocking=True,
        experimental_thread_pool=futures.ThreadPoolExecutor(max_workers=2),
    )
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)

    # Use a daemon thread to monitor health of your service
    toggle_health_status_thread = threading.Thread(
        target=_check_health,
        args=(health_servicer, "demo.WeatherStation"),
        daemon=True,
    )
    toggle_health_status_thread.start()
    return health_servicer


class GRPCServer:
    """
    Simple wrapper around grpc
    """

    def __init__(self, host: str, port: str) -> None:
        self._host: str = host
        self._port: str = port
        self._server: grpc.Server = None
        self._health_servicer: health.HealthServicer = None

    def config(self, service: pb2_grpc.WeatherStationServicer) -> bool:
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
            pb2_grpc.add_WeatherStationServicer_to_server(service, self._server)
        except Exception as e:
            logger.error(f"Cannot add servicer to the server: {e}")
            return False
        try:
            self._health_servicer = _configure_health_server(self._server)
        except Exception as e:
            logger.error(f"Cannot add health servicer to the server: {e}")
            return False
        return True

    def start(self) -> bool:
        """
        Start the server, blocks until terminated.
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
        self._health_servicer.enter_graceful_shutdown()
        if self._server is None:
            logger.debug(
                "Calling GRPCServer:stop() when server is not running, no effect"
            )
            return
        try:
            event = self._server.stop(grace=1)
            event.wait(timeout=3)
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
