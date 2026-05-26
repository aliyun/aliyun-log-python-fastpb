# -*- coding: utf-8 -*-
"""Tests for the compact (tuple-based) serialization API.

The compact API skips per-content dict allocation and PyDict hashing on the
Python side, in exchange for tuple/list inputs:

    serialize_log_group_compact(
        [(time, [(key, value), ...]), ...],
        topic=..., source=..., log_tags=[(k, v), ...],
    )

Wire format must be byte-for-byte identical to the dict-based API. These tests
exercise the equivalence and the edge cases (empty optionals, time_ns variant,
unicode, raw-bytes variant).
"""

import pytest

import aliyun_log_fastpb as fpb

try:
    from . import logs_pb2
except (ImportError, ValueError):
    import logs_pb2

LogGroup = logs_pb2.LogGroup


pytestmark = pytest.mark.skipif(
    not hasattr(fpb, 'serialize_log_group_compact'),
    reason='compact API not built into this fastpb version',
)


def test_compact_matches_dict_minimal():
    items_dict = [{
        "Time": 1700000000,
        "Contents": [{"Key": "k", "Value": "v"}],
    }]
    items_tup = [(1700000000, [("k", "v")])]

    a = fpb.serialize_log_group({"LogItems": items_dict})
    b = fpb.serialize_log_group_compact(items_tup)
    assert a == b

    parsed = LogGroup()
    parsed.ParseFromString(b)
    assert len(parsed.logs) == 1
    assert parsed.logs[0].time == 1700000000
    assert parsed.logs[0].contents[0].key == "k"
    assert parsed.logs[0].contents[0].value == "v"


def test_compact_matches_dict_full():
    items_dict = [
        {"Time": 1700000001, "Contents": [
            {"Key": "message", "Value": "hello"},
            {"Key": "level", "Value": "INFO"},
        ]},
        {"Time": 1700000002, "Contents": [
            {"Key": "message", "Value": "bye"},
        ]},
    ]
    items_tup = [
        (1700000001, [("message", "hello"), ("level", "INFO")]),
        (1700000002, [("message", "bye")]),
    ]
    log_tags_dict = [{"Key": "host", "Value": "h1"}, {"Key": "env", "Value": "prod"}]
    log_tags_tup = [("host", "h1"), ("env", "prod")]

    a = fpb.serialize_log_group({
        "LogItems": items_dict, "Topic": "t", "Source": "s",
        "LogTags": log_tags_dict,
    })
    b = fpb.serialize_log_group_compact(
        items_tup, topic="t", source="s", log_tags=log_tags_tup,
    )
    assert a == b


def test_compact_with_time_ns():
    items_dict = [{
        "Time": 1700000000,
        "TimeNs": 12345,
        "Contents": [{"Key": "k", "Value": "v"}],
    }]
    items_tup = [(1700000000, 12345, [("k", "v")])]

    a = fpb.serialize_log_group({"LogItems": items_dict})
    b = fpb.serialize_log_group_compact(items_tup)
    assert a == b


def test_compact_unicode():
    items_dict = [{
        "Time": 1700000000,
        "Contents": [{"Key": "msg", "Value": "你好世界 🌍"}],
    }]
    items_tup = [(1700000000, [("msg", "你好世界 🌍")])]

    a = fpb.serialize_log_group({"LogItems": items_dict})
    b = fpb.serialize_log_group_compact(items_tup)
    assert a == b
    parsed = LogGroup()
    parsed.ParseFromString(b)
    assert parsed.logs[0].contents[0].value == "你好世界 🌍"


def test_compact_empty_log_items():
    a = fpb.serialize_log_group({"LogItems": [], "Topic": "t"})
    b = fpb.serialize_log_group_compact([], topic="t")
    assert a == b


def test_compact_lists_accepted_as_well_as_tuples():
    items_tuples = [(1700000000, [("k", "v")])]
    items_lists = [[1700000000, [["k", "v"]]]]
    a = fpb.serialize_log_group_compact(items_tuples)
    b = fpb.serialize_log_group_compact(items_lists)
    assert a == b


def test_compact_rejects_wrong_arity():
    # Bare value where a tuple is expected.
    with pytest.raises((TypeError, ValueError)):
        fpb.serialize_log_group_compact([(1700000000,)])  # missing contents
    with pytest.raises((TypeError, ValueError)):
        fpb.serialize_log_group_compact([(1700000000, [("k", "v", "extra")])])


def test_compact_raw_matches_dict_raw():
    raw = getattr(fpb, 'serialize_log_group_raw_compact', None)
    if raw is None:
        pytest.skip('raw compact variant not built')
    items_dict = [{
        "Time": 1700000000,
        "Contents": [{"Key": "k", "Value": b"binary"}],
    }]
    items_tup = [(1700000000, [("k", b"binary")])]

    a = fpb.serialize_log_group_raw({"LogItems": items_dict})
    b = raw(items_tup)
    assert a == b
