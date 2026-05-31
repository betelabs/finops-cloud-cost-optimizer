"""Integration-style tests for AWSCollector using mocked boto3."""
from __future__ import annotations
from unittest.mock import MagicMock, patch
from datetime import datetime
from src.collectors.aws_collector import AWSCollector

BASE_CFG = {
    "region": "us-east-1",
    "thresholds": {"idle_cpu_percent": 5, "idle_cpu_days": 14},
}


def _make_collector():
    with patch("boto3.client") as mock_boto:
        mock_boto.return_value = MagicMock()
        c = AWSCollector(BASE_CFG)
        c.ce  = MagicMock()
        c.ec2 = MagicMock()
        c.rds = MagicMock()
        c.cw  = MagicMock()
    return c


def test_get_total_spend_returns_float():
    c = _make_collector()
    c.ce.get_cost_and_usage.return_value = {
        "ResultsByTime": [{"Total": {"UnblendedCost": {"Amount": "48320.50"}}}]
    }
    total = c.get_total_spend(datetime(2025, 1, 1), datetime(2025, 1, 31))
    assert isinstance(total, float)
    assert total == 48320.50


def test_no_instances_returns_empty_idle():
    c = _make_collector()
    c.ec2.describe_instances.return_value = {"Reservations": []}
    c.rds.describe_db_instances.return_value = {"DBInstances": []}
    c.ec2.describe_volumes.return_value = {"Volumes": []}
    idle = c.get_idle_resources()
    assert idle == []
