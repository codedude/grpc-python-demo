import logging
import grpc_testing
import grpc
import demo_service

from typing import Generator
import pb.sub.sub_demo_pb2 as pb_sub_demo
import pb.demo_pb2 as pb_demo

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class WeatherStationServerMock:
    def __init__(self):
        self._service = pb_demo.DESCRIPTOR.services_by_name["WeatherStation"]
        self._server = grpc_testing.server_from_dictionary(
            {self._service: demo_service.WeatherStationService()},
            grpc_testing.strict_real_time(),
        )

    def GetSnapshot(
        self, request: pb_sub_demo.RequestReport
    ) -> pb_sub_demo.ReportResponse:
        method = self._server.invoke_unary_unary(
            method_descriptor=(self._service.methods_by_name["GetSnapshot"]),
            invocation_metadata=(("accesstoken", "montreal-python"),),
            request=request,
            timeout=1,
        )
        response, metadata, code, details = method.termination()
        if code.value[0] != 0 or len(details) != 0:
            raise RuntimeError(grpc.RpcError({"code": code, "details": details}))
        return response

    def SendMeasurements(self) -> Generator[pb_sub_demo.ReportResponse]:
        method = self._server.invoke_unary_stream(
            method_descriptor=(self._service.methods_by_name["SendMeasurements"]),
            invocation_metadata=(("accesstoken", "montreal-python"),),
            request=None,
            timeout=None,
        )
        while True:
            try:
                r = method.take_response()
            except Exception as e:
                logger.error(e)
                r = None
            if r is None:
                break
            yield r
        metadata, code, details = method.termination()
        if code.value[0] != 0 or len(details) != 0:
            raise RuntimeError(grpc.RpcError({"code": code, "details": details}))
