#!/bin/python

import grpc
import sys
import grpc_client

if __name__ == '__main__':
    app_client = grpc_client.HelloClient(host="127.0.0.1", port="8042")
    if not app_client.instantiate():
        print("Cannot instantiate grpc client, abort")
        sys.exit(1)
    response = app_client.say_hello("Bobby")
    if response.error.code != grpc.StatusCode.OK:
        print(f"Error from server: {response.error.code} - {response.error.details}")
        sys.exit(1)
    print(f"Response from server: {response.message}")
    sys.exit(0)
