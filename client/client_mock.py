import grpc
import time
import logging
from typing import Generator

import pb.demo_pb2_grpc as pb_demo
import pb.sub.sub_demo_pb2 as pb_sub_demo
import helpers

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class WeatherStationStubMock(pb_demo.WeatherStationStub):
    def __init__(self, channel):
        self.GetSnapshot = self._GetSnapshot
        self.SendMeasurements = self._SendMeasurements
        self.FillMeasurements = self._FillMeasurements
        self.Monitor = self._Monitor

    def _GetSnapshot(self, request: grpc.Message, **params) -> helpers.ApiResponse:
        server_data = helpers.create_report(10)
        return pb_sub_demo.ReportResponse(measures=server_data.measures)

    def _SendMeasurements(
        self, request: grpc.Message, **params
    ) -> Generator[grpc.Message]:
        for measure in helpers.gen_measures(10):
            yield measure
            time.sleep(1)

    def _FillMeasurements(
        self, request: Generator[grpc.Message], **params
    ) -> grpc.Message:
        return pb_sub_demo.ApiResponse()

    def _Monitor(
        self, request: Generator[grpc.Message], **params
    ) -> Generator[grpc.Message]:
        i = 0
        for measure in helpers.gen_measures(10):
            # generate a warning every 3 measure received
            if i % 3 == 0:
                yield pb_sub_demo.WarningResponse()
            time.sleep(1)
            i += 1
