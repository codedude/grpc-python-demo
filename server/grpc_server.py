import logging
from concurrent import futures
from grpc_health.v1 import health

import grpc

import pb.demo_pb2_grpc as pb_demo
from server import demo_service

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

MAX_MESSAGE_LENGTH = 1024 * 1024 * 16  # 16Mo


class GRPCServer:
    """
    Simple wrapper around grpc
    """

    def __init__(self, host: str, port: str) -> None:
        self._host: str = host
        self._port: str = port

    def config(self) -> bool:
        try:
            self._server = grpc.server(
                futures.ThreadPoolExecutor(max_workers=8),
                options=[
                    ("grpc.max_send_message_length", MAX_MESSAGE_LENGTH),
                    ("grpc.max_receive_message_length", MAX_MESSAGE_LENGTH),
                    ("grpc.keepalive_time_ms", 20000),
                    ("grpc.keepalive_timeout_ms", 10000),
                    ("grpc.http2.min_ping_interval_without_data_ms", 5000),
                    ("grpc.max_connection_idle_ms", 10000),
                    ("grpc.max_connection_age_ms", 30000),
                    ("grpc.max_connection_age_grace_ms", 5000),
                    ("grpc.http2.max_pings_without_data", 5),
                    ("grpc.keepalive_permit_without_calls", 1),
                ],
            )
            self._server.add_insecure_port(f"{self._host}:{self._port}")
        except grpc.RpcError as e:
            logger.error(f"Cannot create the server: {e}")
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
            return False
        logger.info("GRPC server has terminated")
        return True

    def stop(self, from_del=False) -> None:
        """
        Gracefuylly stop the server
        """
        self._health_servicer.enter_graceful_shutdown()
        if self._server is None:
            if not from_del:
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
        self.stop(from_del=True)


class WeatherStationServer(GRPCServer):
    def __init__(self, host: str, port: str):
        super().__init__(host, port)
        self._server: grpc.Server = None
        self._health_servicer: health.HealthServicer = None

    def add_weather_station_service(
        self, service: pb_demo.WeatherStationServicer
    ) -> bool:
        try:
            pb_demo.add_WeatherStationServicer_to_server(service, self._server)
        except Exception as e:
            logger.error(f"Cannot add servicer to the server: {e}")
            return False
        return True

    def add_health_check_service(self) -> bool:
        try:
            self._health_servicer = demo_service.configure_health_server(self._server)
        except Exception as e:
            logger.error(f"Cannot add health servicer to the server: {e}")
            return False
        return True
