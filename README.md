# aliyun-log-fastpb

[中文文档](README_CN.md) | English

Fast protobuf serialization for Aliyun Log using PyO3 and quick-protobuf.

## Installation

```bash
pip install aliyun-log-fastpb
```

## Quick Start

```python
import aliyun_log_fastpb

# Prepare log data
log_group = {
    "LogItems": [
        {
            "Time": 1234567890,
            "Contents": [
                {"Key": "level", "Value": "INFO"},
                {"Key": "message", "Value": "Application started"}
            ]
        }
    ],
    "LogTags": [
        {"Key": "hostname", "Value": "server-001"}
    ],
    "Topic": "app-logs",
    "Source": "192.168.1.100"
}

# Serialize to protobuf bytes
pb_bytes = aliyun_log_fastpb.serialize_log_group(log_group)
```

For binary data support, use `serialize_log_group_raw`:

```python
log_group_raw = {
    "LogItems": [
        {
            "Time": 1234567890,
            "Contents": [
                {"Key": "data", "Value": b"\x00\x01\x02\xff"}
            ]
        }
    ],
    "LogTags": [],
    "Topic": "binary-logs",
    "Source": ""
}

pb_bytes = aliyun_log_fastpb.serialize_log_group_raw(log_group_raw)
```

For nanosecond precision timestamps, use `TimeNs` field:

```python
log_group = {
    "LogItems": [
        {
            "Time": 1234567890,
            "TimeNs": 123456789,  # Nanosecond precision
            "Contents": [
                {"Key": "event", "Value": "transaction_completed"}
            ]
        }
    ],
    "LogTags": [],
    "Topic": "transactions",
    "Source": ""
}

pb_bytes = aliyun_log_fastpb.serialize_log_group(log_group)
```

## License

MIT License
