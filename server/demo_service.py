import time
import logging
import datetime
import grpc
from typing import Generator

import pb.sub.sub_demo_pb2 as pb_sub_demo
import pb.demo_pb2_grpc as pb_demo

from helpers import create_report, gen_measures

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class WeatherStationService(pb_demo.WeatherStationServicer):
    def __init__(self):
        logger.info("Service initialized")

    def GetSnapshot(
        self, request: pb_sub_demo.RequestReport, context: grpc.RpcContext
    ) -> pb_sub_demo.ReportResponse:
        """GetSnapshot, client asks a report to server"""
        authenticated = False
        for key, value in context.invocation_metadata():
            if key == "accesstoken":
                if value != "montreal-python":
                    context.set_code(grpc.StatusCode.UNAUTHENTICATED)
                    context.set_details("bad access token")
                    return None
                else:
                    authenticated = True
        if not authenticated:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details("no access token")
            return None
        if (
            not request.start_time.IsInitialized()
            or not request.end_time.IsInitialized()
        ):
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("start_time and end_time must be set")
            return None
        start_time = request.start_time.ToDatetime(tzinfo=datetime.timezone.utc)
        end_time = request.end_time.ToDatetime(tzinfo=datetime.timezone.utc)
        if (
            start_time >= datetime.datetime.now(datetime.timezone.utc)
            or end_time <= start_time
        ):
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(
                "start_time must be old than now, and different from end_time"
            )
            return None
        reports = create_report(10)
        context.set_code(grpc.StatusCode.OK)
        logger.debug("Report ready to send!")
        return reports

    def SendMeasurements(self, request, context: grpc.RpcContext) -> None:
        """SendMeasurements, server sends live measures to client"""
        for i, measure in enumerate(gen_measures(10)):
            logger.debug(f"Sending measure {i} to client...")
            yield measure
            time.sleep(1)
        context.set_code(grpc.StatusCode.OK)
        logger.debug("All measures sent!")

    def FillMeasurements(
        self, request_iterator, context: grpc.RpcContext
    ) -> pb_sub_demo.ApiResponse:
        """FillMeasurements, client sends missing/new measures to server"""
        for i, measure in enumerate(request_iterator):
            logger.debug(f"Receiving measure {i} from client...")
        context.set_code(grpc.StatusCode.OK)
        logger.debug("All measures received!")
        return pb_sub_demo.ApiResponse(code=0, msg="success")

    def Monitor(self, request_iterator: Generator[pb_sub_demo.Measure], context) -> None:
        """Monitor, client sends live measures, server responds with live warning"""
        logger.debug(f"Start Monitor...")
        for i, measure in enumerate(request_iterator):
            logger.debug(f"Receiving measure {i} from client...")
            if measure.humidity > 6:
                logger.debug("Send warning to client")
                yield pb_sub_demo.WarningResponse(
                    warnings=[
                        pb_sub_demo.WarningMsg(
                            time=datetime.datetime.now(datetime.timezone.utc),
                            type=pb_sub_demo.WARNING_TYPE_HUMIDITY,
                        )
                    ]
                )
        context.set_code(grpc.StatusCode.OK)
        logger.debug("... Monitor ended!")
