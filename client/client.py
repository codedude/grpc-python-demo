#!/bin/python

import grpc
import sys
import logging
import grpc_client
import datetime
import time
import argparse

from helpers import yield_measures

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
    else:
        print(f"Response from server: {response}")


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
    else:
        print(f"Response from server: {response}")


def get_snapshot_header(app_client: grpc_client.WeatherStationClient) -> None:
    time_now = datetime.datetime.now()
    response = app_client.GetSnapshot(
        start_time=time_now,
        end_time=time_now + datetime.timedelta(days=1),
        access_token="bad-token",
    )
    if response.error:
        print(f"Error from server: {response.error.code} - {response.error.details}")
    else:
        print(f"Response from server: {response}")


def send_measurements(app_client: grpc_client.WeatherStationClient) -> None:
    for r in app_client.SendMeasurements():
        print(f"Response from server: {r}")


def fill_measurments(app_client: grpc_client.WeatherStationClient) -> None:
    r = app_client.FillMeasurements(yield_measures(10))
    print(f"Response from server: {r}")


def monitor(app_client: grpc_client.WeatherStationClient) -> None:
    for r in app_client.Monitor(yield_measures(10)):
        print(f"Response from server: {r}")
        time.sleep(1)


def health_check(app_client: grpc_client.WeatherStationClient) -> None:
    app_client.HealthCheck()


if __name__ == "__main__":
    app_client = grpc_client.WeatherStationClient(host="127.0.0.1", port="4242")
    if not app_client.instantiate():
        logger.critical("Cannot instantiate client")
        sys.exit(1)
    parser = argparse.ArgumentParser(
        prog="WeatherStation Client",
        description="What is the weather today?",
        epilog="Demo done for Montreal Python",
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
