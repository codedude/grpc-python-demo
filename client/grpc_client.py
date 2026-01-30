import logging
from typing import Generator
import datetime
import time
import grpc
import json
from google.protobuf import empty_pb2
from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc

import pb.sub.sub_demo_pb2 as pb_sub_demo
import pb.demo_pb2_grpc as pb_demo

import helpers

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

service_config_json = json.dumps(
    {
        "methodConfig": [
            {
                # To apply retry to all methods, put [{}] in the "name" field
                "name": [{"service": "demo.WeatherStation", "method": "GetSnapshot"}],
                "retryPolicy": {
                    "maxAttempts": 5,
                    "initialBackoff": "0.1s",
                    "maxBackoff": "1s",
                    "backoffMultiplier": 2,
                    "retryableStatusCodes": ["UNAVAILABLE"],
                },
            }
        ]
    }
)


class WeatherStationClient(object):
    def __init__(self, host: str, port: str) -> None:
        self._host = host
        self._port = port
        self._stub = None
        self._health_stub = None

    def instantiate(self, stub=pb_demo.WeatherStationStub) -> bool:
        if not issubclass(stub, pb_demo.WeatherStationStub):
            return False
        try:
            channel = grpc.insecure_channel(
                target=f"{self._host}:{self._port}",
                options=(
                    ("grpc.keepalive_time_ms", 8000),
                    ("grpc.keepalive_timeout_ms", 5000),
                    ("grpc.http2.max_pings_without_data", 5),
                    ("grpc.keepalive_permit_without_calls", 1),
                    ("grpc.enable_retries", 1),
                    ("grpc.service_config", service_config_json),
                ),
            )
            self._stub = stub(channel)
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
                request=pb_sub_demo.RequestReport(
                    start_time=start_time, end_time=end_time
                ),
                wait_for_ready=wait_for_ready,
                metadata=(("accesstoken", access_token),),
            )
        except grpc.RpcError as e:
            return helpers.error_response(e)
        logger.debug("Report received from server!")
        print(type(response))
        return helpers.success_response(response)

    def SendMeasurements(self) -> Generator[helpers.ApiResponse]:
        try:
            responses = self._stub.SendMeasurements(request=empty_pb2.Empty())
            for i, measure in enumerate(responses):
                logger.debug(f"Received measure {i} from server")
                yield helpers.success_response(measure)
        except grpc.RpcError as e:
            yield helpers.error_response(e)
        logger.debug("All measures received!")

    def FillMeasurements(
        self, measures: Generator[pb_sub_demo.Measure]
    ) -> helpers.ApiResponse:
        logger.debug("Send measures to server...")
        try:
            response = self._stub.FillMeasurements(measures)
        except grpc.RpcError as e:
            return helpers.error_response(e)
        logger.debug("Done!")
        return helpers.success_response(response)

    def Monitor(
        self, measures: Generator[pb_sub_demo.Measure]
    ) -> Generator[helpers.ApiResponse]:
        logger.debug("Start Monitor...")
        try:
            for i, response in enumerate(self._stub.Monitor(measures)):
                logger.debug("Received warning from server")
                yield helpers.success_response(response)
        except grpc.RpcError as e:
            yield helpers.error_response(e)
        logger.debug("Monitor ended!")

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
            logger.debug("Server is serving")
        elif resp.status == health_pb2.HealthCheckResponse.NOT_SERVING:
            logger.debug("Server stopped serving")
        else:
            logger.debug(resp)
