import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ActionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACTION_TYPE_UNKNOWN: _ClassVar[ActionType]
    ACTION_TYPE_RESTART: _ClassVar[ActionType]
    ACTION_TYPE_STOP: _ClassVar[ActionType]
    ACTION_TYPE_DELETE: _ClassVar[ActionType]

class WarningMsgType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WARNING_TYPE_UNKNOWN: _ClassVar[WarningMsgType]
    WARNING_TYPE_HOT: _ClassVar[WarningMsgType]
    WARNING_TYPE_HUMIDITY: _ClassVar[WarningMsgType]
    WARNING_TYPE_PRESSURE: _ClassVar[WarningMsgType]
ACTION_TYPE_UNKNOWN: ActionType
ACTION_TYPE_RESTART: ActionType
ACTION_TYPE_STOP: ActionType
ACTION_TYPE_DELETE: ActionType
WARNING_TYPE_UNKNOWN: WarningMsgType
WARNING_TYPE_HOT: WarningMsgType
WARNING_TYPE_HUMIDITY: WarningMsgType
WARNING_TYPE_PRESSURE: WarningMsgType

class Measure(_message.Message):
    __slots__ = ("temp", "humidity", "pressure", "time")
    TEMP_FIELD_NUMBER: _ClassVar[int]
    HUMIDITY_FIELD_NUMBER: _ClassVar[int]
    PRESSURE_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    temp: float
    humidity: int
    pressure: int
    time: _timestamp_pb2.Timestamp
    def __init__(self, temp: _Optional[float] = ..., humidity: _Optional[int] = ..., pressure: _Optional[int] = ..., time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class WarningMsg(_message.Message):
    __slots__ = ("time", "type", "details")
    TIME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    time: _timestamp_pb2.Timestamp
    type: WarningMsgType
    details: _containers.RepeatedCompositeFieldContainer[_any_pb2.Any]
    def __init__(self, time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., type: _Optional[_Union[WarningMsgType, str]] = ..., details: _Optional[_Iterable[_Union[_any_pb2.Any, _Mapping]]] = ...) -> None: ...

class ReportResponse(_message.Message):
    __slots__ = ("measures",)
    MEASURES_FIELD_NUMBER: _ClassVar[int]
    measures: _containers.RepeatedCompositeFieldContainer[Measure]
    def __init__(self, measures: _Optional[_Iterable[_Union[Measure, _Mapping]]] = ...) -> None: ...

class WarningResponse(_message.Message):
    __slots__ = ("warnings",)
    WARNINGS_FIELD_NUMBER: _ClassVar[int]
    warnings: _containers.RepeatedCompositeFieldContainer[WarningMsg]
    def __init__(self, warnings: _Optional[_Iterable[_Union[WarningMsg, _Mapping]]] = ...) -> None: ...

class RequestReport(_message.Message):
    __slots__ = ("start_time", "end_time")
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    def __init__(self, start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class RequestSetConfig(_message.Message):
    __slots__ = ("interval", "time")
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    interval: _duration_pb2.Duration
    time: _timestamp_pb2.Timestamp
    def __init__(self, interval: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ..., time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class RequestAction(_message.Message):
    __slots__ = ("action",)
    ACTION_FIELD_NUMBER: _ClassVar[int]
    action: ActionType
    def __init__(self, action: _Optional[_Union[ActionType, str]] = ...) -> None: ...

class ApiResponse(_message.Message):
    __slots__ = ("code", "msg", "field")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    FIELD_FIELD_NUMBER: _ClassVar[int]
    code: int
    msg: str
    field: str
    def __init__(self, code: _Optional[int] = ..., msg: _Optional[str] = ..., field: _Optional[str] = ...) -> None: ...
