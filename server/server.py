#!/bin/python

import logging
import sys
import signal

import demo_service
import grpc_server

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


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
