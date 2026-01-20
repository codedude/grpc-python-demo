import logging
from typing import Generator
import datetime
import time
import grpc
from google.protobuf import empty_pb2
from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc

import helpers
import pb.generated.sub.sub_demo_pb2 as sub_pb2
import pb.generated.demo_pb2_grpc as pb2_grpc

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class WeatherStationClient(object):
    def __init__(self, host: str, port: str) -> None:
        self._host = host
        self._port = port
        self._stub = None
        self._health_stub = None

    def instantiate(self) -> bool:
        try:
            channel = grpc.insecure_channel(
                target=f"{self._host}:{self._port}",
                options=(
                    ("grpc.keepalive_time_ms", 8000),
                    ("grpc.keepalive_timeout_ms", 5000),
                    ("grpc.http2.max_pings_without_data", 5),
                    ("grpc.keepalive_permit_without_calls", 1),
                ),
            )
            self._stub = pb2_grpc.WeatherStationStub(channel)
            self._health_stub = health_pb2_grpc.HealthStub(channel)
        except Exception as e:
            logger.error(f"instantiate(): {e}")
            return False
        logger.info("Client is ready")
        return True

    def GetSnapshot(
        self,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        access_token: str,
        wait_for_ready=None,
    ) -> helpers.ApiResponse:
        try:
            response = self._stub.GetSnapshot(
                request=sub_pb2.RequestReport(start_time=start_time, end_time=end_time),
                wait_for_ready=wait_for_ready,
                metadata=(("accesstoken", access_token),),
            )
        except grpc.RpcError as e:
            return helpers.error_response(e)
        return helpers.success_response(response)

    def SendMeasurements(self) -> Generator[helpers.ApiResponse]:
        try:
            responses = self._stub.SendMeasurements(request=empty_pb2.Empty())
            for measure in responses:
                yield helpers.success_response(measure)
        except grpc.RpcError as e:
            yield helpers.error_response(e)

    def FillMeasurements(
        self, measures: Generator[sub_pb2.Measure]
    ) -> helpers.ApiResponse:
        try:
            response = self._stub.FillMeasurements(measures)
        except grpc.RpcError as e:
            return helpers.error_response(e)
        return helpers.success_response(response)

    def Monitor(
        self, measures: Generator[sub_pb2.Measure]
    ) -> Generator[helpers.ApiResponse]:
        try:
            for response in self._stub.Monitor(measures):
                yield helpers.success_response(response)
        except grpc.RpcError as e:
            yield helpers.error_response(e)

    def HealthCheck(self):
        for _ in range(10):
            time.sleep(1)
            try:
                self._health_check_call(self._health_stub)
            except Exception as e:
                logger.error(e)
                continue

    def _health_check_call(self, stub: health_pb2_grpc.HealthStub):
        request = health_pb2.HealthCheckRequest(service="demo.WeatherStation")
        resp = stub.Check(request)
        if resp.status == health_pb2.HealthCheckResponse.SERVING:
            logger.debug("server is serving")
        elif resp.status == health_pb2.HealthCheckResponse.NOT_SERVING:
            logger.debug("server stopped serving")
        else:
            logger.debug(resp)
