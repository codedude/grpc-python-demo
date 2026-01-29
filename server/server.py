#!/bin/python

import logging
import sys
import signal

import demo_service
import grpc_server

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def start_server(host: str, port: str) -> int:
    server = grpc_server.GRPCServer(host, port)
    if not server.config(demo_service.WeatherStationService()):
        return 1
    signal.signal(signal.SIGINT, lambda s, f: server.stop())
    ret = server.start()
    if not ret:
        return 1
    server.stop()
    return 0


if __name__ == "__main__":
    sys.exit(start_server(host="[::]", port="4242"))
