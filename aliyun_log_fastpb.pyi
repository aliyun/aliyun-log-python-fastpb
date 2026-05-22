"""
Type stubs for aliyun-log-fastpb

Fast protobuf serialization for Aliyun Log using PyO3 and quick-protobuf.
"""

from typing import Any, Dict, List, Optional, Sequence, Tuple, TypedDict, Union

# A compact log entry: (time, [(key, value), ...]) or (time, time_ns, [(key, value), ...]).
# Lists are accepted in place of tuples at every level.
_KvPairStr = Union[Tuple[str, str], List[str]]
_KvPairBytes = Union[Tuple[str, bytes], List[Union[str, bytes]]]
_LogCompactStr = Union[
    Tuple[int, Sequence[_KvPairStr]],
    Tuple[int, int, Sequence[_KvPairStr]],
    List[Any],
]
_LogCompactBytes = Union[
    Tuple[int, Sequence[_KvPairBytes]],
    Tuple[int, int, Sequence[_KvPairBytes]],
    List[Any],
]
_LogTagCompact = Union[Tuple[str, str], List[str]]

def serialize_log_group(log_group_dict: dict) -> bytes:
    """
    Serialize a LogGroup Python dict to protobuf bytes.

    Args:
        log_group_dict: A dict containing LogItems, LogTags, Topic, and Source.
            - LogItems: List of Log entries
            - LogTags: List of LogTag metadata
            - Topic: Topic string (can be empty)
            - Source: Source string (can be empty)

    Returns:
        bytes: The serialized protobuf data.

    Example:
        >>> log_group = {
        ...     "LogItems": [{
        ...         "Time": 1234567890,
        ...         "Contents": [
        ...             {"Key": "level", "Value": "INFO"},
        ...             {"Key": "message", "Value": "Hello World"}
        ...         ]
        ...     }],
        ...     "LogTags": [{"Key": "host", "Value": "server1"}],
        ...     "Topic": "app-logs",
        ...     "Source": "192.168.1.1"
        ... }
        >>> data = serialize_log_group(log_group)
    """
    ...

def deserialize_log_group_list(data: bytes) -> dict:
    """
    Deserialize a LogGroupList protobuf bytes to Python dict.

    Returns:
        dict with "logGroupList" key containing list of LogGroup dicts.
    """
    ...

def serialize_log_group_raw(log_group_dict: dict) -> bytes:
    """
    Serialize a LogGroupRaw Python dict to protobuf bytes.

    This function supports binary data in log content values.

    Args:
        log_group_dict: A dict containing LogItems, LogTags, Topic, and Source.
            - LogItems: List of LogRaw entries (supports binary values)
            - LogTags: List of LogTag metadata
            - Topic: Topic string (can be empty)
            - Source: Source string (can be empty)

    Returns:
        bytes: The serialized protobuf data.

    Example:
        >>> log_group = {
        ...     "LogItems": [{
        ...         "Time": 1234567890,
        ...         "Contents": [
        ...             {"Key": "data", "Value": b"\\x00\\x01\\x02\\xff"}
        ...         ]
        ...     }],
        ...     "LogTags": [],
        ...     "Topic": "",
        ...     "Source": ""
        ... }
        >>> data = serialize_log_group_raw(log_group)
    """
    ...


def serialize_log_group_compact(
    log_items: Sequence[_LogCompactStr],
    topic: Optional[str] = None,
    source: Optional[str] = None,
    log_tags: Optional[Sequence[_LogTagCompact]] = None,
) -> bytes:
    """
    Serialize a LogGroup using a compact tuple/list layout.

    Wire format is byte-identical to ``serialize_log_group``. The compact API
    skips per-content dict allocation and PyDict hashing on the Python side,
    making it ~2x faster for hot-path producers (e.g. logging handlers).

    Args:
        log_items: Sequence of ``(time, contents)`` or ``(time, time_ns, contents)``.
            Each ``contents`` is a sequence of ``(key, value)`` pairs.
            Tuples and lists are interchangeable at every level.
        topic: Optional topic string. None or empty omits the field.
        source: Optional source string. None or empty omits the field.
        log_tags: Optional sequence of ``(key, value)`` tag pairs.

    Returns:
        bytes: The serialized protobuf data.

    Example:
        >>> body = serialize_log_group_compact(
        ...     [(1700000000, [("level", "INFO"), ("message", "Hello")])],
        ...     topic="t", source="s",
        ...     log_tags=[("host", "h1")],
        ... )
    """
    ...


def serialize_log_group_raw_compact(
    log_items: Sequence[_LogCompactBytes],
    topic: Optional[str] = None,
    source: Optional[str] = None,
    log_tags: Optional[Sequence[_LogTagCompact]] = None,
) -> bytes:
    """
    Compact variant of ``serialize_log_group_raw`` — accepts ``bytes`` values
    instead of strings for binary log payloads. Same compact layout as
    ``serialize_log_group_compact``; output is byte-identical to the dict API.
    """
    ...
