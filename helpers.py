import datetime
import grpc
from types import SimpleNamespace
from typing import List, Generator, Dict, Optional, Protocol
from google.protobuf.json_format import MessageToDict
from google.protobuf.message import Message

from pb.generated.sub.sub_demo_pb2 import ReportResponse, Measure


class ApiError(Protocol):
    code: int
    name: str
    details: Optional[str]


class ApiResponse(Protocol):
    error: Optional[ApiError]
    response: Optional[Dict]


def error_response(e: grpc.RpcError) -> ApiResponse:
    code = e.code()
    return SimpleNamespace(
        **{
            "error": SimpleNamespace(
                **{
                    "code": code.value[0],
                    "name": code.value[1],
                    "details": e.details(),
                }
            ),
            "response": None,
        }
    )


def success_response(response: Message) -> ApiResponse:
    return SimpleNamespace(
        **{
            "response": MessageToDict(
                response,
                preserving_proto_field_name=True,
                use_integers_for_enums=False,
                always_print_fields_with_no_presence=True,
            ),
            "error": None,
        }
    )


def generate_reports(n: int = 100) -> List[ReportResponse]:
    if n < 0 or n > 1000:
        raise RuntimeError(f"Cannot generate {n} reports")
    report = ReportResponse()
    for i in range(n):
        report.measures.add(
            temp=float("{:.2f}".format(i / 3.0 + 0.42)),
            humidity=i,
            pressure=950 + i,
            time=datetime.datetime.now(datetime.timezone.utc)
            - datetime.timedelta(hours=i),
        )
    return report


def yield_measures(n: int = 100) -> Generator[Measure]:
    if n < 0 or n > 1000:
        raise RuntimeError(f"Cannot generate {n} measures")
    for i in range(n):
        yield Measure(
            temp=float("{:.2f}".format(i / 3.0 + 0.42)),
            humidity=i,
            pressure=950 + i,
            time=datetime.datetime.now(datetime.timezone.utc)
            - datetime.timedelta(hours=i),
        )
