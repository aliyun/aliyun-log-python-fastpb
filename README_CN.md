# aliyun-log-fastpb

[![Test](https://github.com/aliyun/aliyun-log-python-fastpb/actions/workflows/test.yml/badge.svg)](https://github.com/aliyun/aliyun-log-python-fastpb/actions/workflows/test.yml) [![PyPI - Version](https://img.shields.io/pypi/v/aliyun-log-fastpb)](https://pypi.python.org/pypi/aliyun-log-fastpb) [![versions](https://img.shields.io/pypi/pyversions/aliyun-log-fastpb.svg)](https://github.com/aliyun/aliyun-log-python-fastpb) [![PyPI - License](https://img.shields.io/pypi/l/aliyun-log-fastpb)](https://github.com/aliyun/aliyun-log-python-fastpb/blob/main/LICENSE)

[English](README.md) | 中文文档

基于 PyO3 和 quick-protobuf 的阿里云日志高性能 protobuf 序列化库。

## 安装

```bash
pip install aliyun-log-fastpb
```

## 快速开始

```python
import aliyun_log_fastpb

# 准备日志数据
log_group = {
    "LogItems": [
        {
            "Time": 1234567890,
            "Contents": [
                {"Key": "level", "Value": "INFO"},
                {"Key": "message", "Value": "应用程序已启动"}
            ]
        }
    ],
    "LogTags": [
        {"Key": "hostname", "Value": "server-001"}
    ],
    "Topic": "app-logs",
    "Source": "192.168.1.100"
}

# 序列化为 protobuf 字节
pb_bytes = aliyun_log_fastpb.serialize_log_group(log_group)
```

支持二进制数据，使用 `serialize_log_group_raw`：

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

支持纳秒精度时间戳，使用 `TimeNs` 字段：

```python
log_group = {
    "LogItems": [
        {
            "Time": 1234567890,
            "TimeNs": 123456789,  # 纳秒精度
            "Contents": [
                {"Key": "event", "Value": "交易完成"}
            ]
        }
    ],
    "LogTags": [],
    "Topic": "transactions",
    "Source": ""
}

pb_bytes = aliyun_log_fastpb.serialize_log_group(log_group)
```

## 许可证

MIT License
