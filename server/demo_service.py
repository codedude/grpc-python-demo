import time
import logging
import datetime
import grpc
from typing import Generator

import pb.generated.sub.sub_demo_pb2 as pb2_sub
import pb.generated.demo_pb2_grpc as pb2_grpc

from helpers import generate_reports, yield_measures

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class WeatherStationService(pb2_grpc.WeatherStationServicer):
    def __init__(self):
        logger.info("Service initialized")

    def GetSnapshot(self, request: pb2_sub.RequestReport, context: grpc.RpcContext):
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
        reports = generate_reports(10)
        context.set_code(grpc.StatusCode.OK)
        return reports

    def SendMeasurements(self, request, context):
        """SendMeasurements, server sends live measures to client"""
        for measure in yield_measures(10):
            yield measure
            time.sleep(1)
        context.set_code(grpc.StatusCode.OK)

    def FillMeasurements(self, request_iterator, context):
        """FillMeasurements, client sends missing/new measures to server"""
        for measure in request_iterator:
            logger.info(measure)
        context.set_code(grpc.StatusCode.OK)
        return pb2_sub.ApiResponse(code=0, msg="success")

    def Monitor(self, request_iterator: Generator[pb2_sub.Measure], context):
        """Monitor, client sends live measures, server responds with live warning"""
        for measure in request_iterator:
            if measure.humidity > 6:
                yield pb2_sub.WarningResponse(
                    warnings=[
                        pb2_sub.WarningMsg(
                            time=datetime.datetime.now(datetime.timezone.utc),
                            type=pb2_sub.WARNING_TYPE_HUMIDITY,
                        )
                    ]
                )
        context.set_code(grpc.StatusCode.OK)
