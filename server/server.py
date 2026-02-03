#!/bin/python

import logging
import sys
import signal
import datetime

import demo_service
import grpc_server
import server_mock
import pb.sub.sub_demo_pb2 as pb_sub_demo

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


# def start_server(host: str, port: str) -> int:
#     server = server_mock.WeatherStationServerMock()
#     time_now = datetime.datetime.now()
#     r = server.GetSnapshot(
#         pb_sub_demo.RequestReport(
#             start_time=time_now, end_time=time_now + datetime.timedelta(days=1)
#         )
#     )
#     try:
#         for r in server.SendMeasurements():
#             print(r)
#     except Exception as e:
#         logger.error(e)
#     return 0


def start_server(host: str, port: str) -> int:
    server = grpc_server.WeatherStationServer(host, port)
    if not server.config():
        return 1
    if not server.add_weather_station_service(demo_service.WeatherStationService()):
        return 1
    if not server.add_health_check_service():
        return 1
    signal.signal(signal.SIGINT, lambda s, f: server.stop())
    if not server.start():
        return 1
    server.stop()
    return 0


if __name__ == "__main__":
    sys.exit(start_server(host="[::]", port="4242"))
