import sys

from pb.sub.sub_demo_pb2 import ReportResponse


def optional_field():
    print("With pressure defined:")
    report_pressure = ReportResponse()
    report_pressure.measures.add(
        temp=25.0,
        humidity=50,
        pressure=1,
    )
    pb_bin_out = report_pressure.SerializeToString()
    new_report_pressure = ReportResponse()
    new_report_pressure.ParseFromString(pb_bin_out)
    print("Pressure value:", new_report_pressure.measures[0].pressure)
    try:
        print(
            "Pressure is defined", new_report_pressure.measures[0].HasField("pressure")
        )
    except ValueError:
        print("Cannot check pressure presence")

    print("\nWithout pressure defined:")
    report = ReportResponse()
    report.measures.add(
        temp=25.0,
        humidity=50,
    )
    pb_bin_out = report.SerializeToString()
    new_report = ReportResponse()
    new_report.ParseFromString(pb_bin_out)
    print("Pressure value:", new_report.measures[0].pressure)
    try:
        print("Pressure is defined", new_report.measures[0].HasField("pressure"))
    except ValueError as e:
        print("Cannot check pressure presence")


if __name__ == "__main__":
    sys.exit(optional_field())
