import sys

from pb.generated.sub.sub_demo_pb2 import ReportResponse


def optional_field():
    report = ReportResponse()
    report.measures.add(
        temp=25.0,
        humidity=50,
        pressure=0,
    )
    pb_bin_out = report.SerializeToString()
    new_report = ReportResponse()
    new_report.ParseFromString(pb_bin_out)
    try:
        print(new_report.measures[0].pressure)
        print(new_report.measures[0].HasField("pressure"))
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    sys.exit(optional_field())
