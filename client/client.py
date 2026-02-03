#!/bin/python

import sys
import logging
import grpc_client
import datetime
import argparse

from helpers import gen_measures
from client_mock import WeatherStationStubMock

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def get_snapshot(app_client: grpc_client.WeatherStationClient) -> None:
    time_now = datetime.datetime.now()
    response = app_client.GetSnapshot(
        start_time=time_now,
        end_time=time_now + datetime.timedelta(days=1),
        access_token="montreal-python",
    )
    if response.error:
        print(f"Error from server: {response.error.code} - {response.error.details}")
    else:
        print(f"Response from server: {response}")


def get_snapshot_error(app_client: grpc_client.WeatherStationClient) -> None:
    time_now = datetime.datetime.now()
    response = app_client.GetSnapshot(
        start_time=time_now, end_time=time_now, access_token="montreal-python"
    )
    if response.error:
        print(f"Error from server: {response.error.code} - {response.error.details}")


def get_snapshot_wait(app_client: grpc_client.WeatherStationClient) -> None:
    time_now = datetime.datetime.now()
    response = app_client.GetSnapshot(
        start_time=time_now,
        end_time=time_now + datetime.timedelta(days=1),
        access_token="montreal-python",
        wait_for_ready=True,
    )
    if response.error:
        print(f"Error from server: {response.error.code} - {response.error.details}")


def get_snapshot_header(app_client: grpc_client.WeatherStationClient) -> None:
    time_now = datetime.datetime.now()
    response = app_client.GetSnapshot(
        start_time=time_now,
        end_time=time_now + datetime.timedelta(days=1),
        access_token="bad-token",
    )
    if response.error:
        print(f"Error from server: {response.error.code} - {response.error.details}")


def send_measurements(app_client: grpc_client.WeatherStationClient) -> None:
    for r in app_client.SendMeasurements():
        pass


def fill_measurments(app_client: grpc_client.WeatherStationClient) -> None:
    r = app_client.FillMeasurements(gen_measures(10))


def monitor(app_client: grpc_client.WeatherStationClient) -> None:
    for r in app_client.Monitor(gen_measures(10)):
        pass


def health_check(app_client: grpc_client.WeatherStationClient) -> None:
    app_client.HealthCheck()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="WeatherStation Client",
        description="What is the weather today?",
        epilog="Demo done for Montreal Python",
    )
    parser.add_argument(
        "-mode",
        help="Normal or test mode",
        default="normal",
        type=str,
        choices=["normal", "mock"],
    )
    parser.add_argument(
        "action",
        help="What function to run",
        choices=[
            "health_check",
            "simple",
            "wait",
            "header",
            "error",
            "server_stream",
            "client_stream",
            "bi_stream",
        ],
    )
    args = parser.parse_args()
    app_client = grpc_client.WeatherStationClient(host="[::]", port="4242")
    if args.mode == "normal":
        r = app_client.instantiate()
    else:
        r = app_client.instantiate(stub=WeatherStationStubMock)
    if not r:
        logger.critical("Cannot instantiate client")
        sys.exit(1)
    match args.action:
        case "simple":
            get_snapshot(app_client)
        case "wait":
            get_snapshot_wait(app_client)
        case "header":
            get_snapshot_header(app_client)
        case "error":
            get_snapshot_error(app_client)
        case "server_stream":
            send_measurements(app_client)
        case "client_stream":
            fill_measurments(app_client)
        case "bi_stream":
            monitor(app_client)
        case "health_check":
            health_check(app_client)
        case _:
            parser.print_help()

    sys.exit(0)
