from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PutRequest(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: bytes
    def __init__(self, key: _Optional[str] = ..., value: _Optional[bytes] = ...) -> None: ...

class PutResponse(_message.Message):
    __slots__ = ("timestamp", "executionTimeMilliseconds")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    EXECUTIONTIMEMILLISECONDS_FIELD_NUMBER: _ClassVar[int]
    timestamp: str
    executionTimeMilliseconds: int
    def __init__(self, timestamp: _Optional[str] = ..., executionTimeMilliseconds: _Optional[int] = ...) -> None: ...

class GetRequest(_message.Message):
    __slots__ = ("key",)
    KEY_FIELD_NUMBER: _ClassVar[int]
    key: str
    def __init__(self, key: _Optional[str] = ...) -> None: ...

class GetResponse(_message.Message):
    __slots__ = ("timestamp", "executionTimeMilliseconds", "value")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    EXECUTIONTIMEMILLISECONDS_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    timestamp: str
    executionTimeMilliseconds: int
    value: bytes
    def __init__(self, timestamp: _Optional[str] = ..., executionTimeMilliseconds: _Optional[int] = ..., value: _Optional[bytes] = ...) -> None: ...

class GetListRequest(_message.Message):
    __slots__ = ("prefix",)
    PREFIX_FIELD_NUMBER: _ClassVar[int]
    prefix: str
    def __init__(self, prefix: _Optional[str] = ...) -> None: ...

class GetListResponse(_message.Message):
    __slots__ = ("timestamp", "executionTimeMilliseconds", "list")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    EXECUTIONTIMEMILLISECONDS_FIELD_NUMBER: _ClassVar[int]
    LIST_FIELD_NUMBER: _ClassVar[int]
    timestamp: str
    executionTimeMilliseconds: int
    list: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, timestamp: _Optional[str] = ..., executionTimeMilliseconds: _Optional[int] = ..., list: _Optional[_Iterable[str]] = ...) -> None: ...

class DeleteRequest(_message.Message):
    __slots__ = ("key",)
    KEY_FIELD_NUMBER: _ClassVar[int]
    key: str
    def __init__(self, key: _Optional[str] = ...) -> None: ...

class DeleteResponse(_message.Message):
    __slots__ = ("timestamp", "executionTimeMilliseconds")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    EXECUTIONTIMEMILLISECONDS_FIELD_NUMBER: _ClassVar[int]
    timestamp: str
    executionTimeMilliseconds: int
    def __init__(self, timestamp: _Optional[str] = ..., executionTimeMilliseconds: _Optional[int] = ...) -> None: ...

class DeleteTreeRequest(_message.Message):
    __slots__ = ("prefix",)
    PREFIX_FIELD_NUMBER: _ClassVar[int]
    prefix: str
    def __init__(self, prefix: _Optional[str] = ...) -> None: ...

class DeleteTreeResponse(_message.Message):
    __slots__ = ("timestamp", "executionTimeMilliseconds", "deleted")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    EXECUTIONTIMEMILLISECONDS_FIELD_NUMBER: _ClassVar[int]
    DELETED_FIELD_NUMBER: _ClassVar[int]
    timestamp: str
    executionTimeMilliseconds: int
    deleted: int
    def __init__(self, timestamp: _Optional[str] = ..., executionTimeMilliseconds: _Optional[int] = ..., deleted: _Optional[int] = ...) -> None: ...
