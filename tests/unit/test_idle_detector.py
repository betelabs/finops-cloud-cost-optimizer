"""Unit tests for IdleResourceDetector."""
import pytest
from src.analyzers.idle_detector import IdleResourceDetector
from src.collectors.base_collector import IdleResource


@pytest.fixture
def cfg():
    return {"thresholds": {"idle_cpu_percent": 5}}


@pytest.fixture
def resources():
    return [
        IdleResource("i-aaa111", "ec2", "aws", "us-east-1a", 0.4, 0, 14, 120.0, "terminate"),
        IdleResource("i-bbb222", "ec2", "aws", "us-east-1b", 3.2, 0, 14,  70.0, "rightsize"),
        IdleResource("vol-ccc",  "ebs", "aws", "us-east-1a", 0.0, 0, 10,   8.5, "delete"),
        IdleResource("db-ddd",   "rds", "aws", "us-east-1a", 0.0, 0,  7, 175.0, "stop"),
    ]


def test_total_waste(cfg, resources):
    s = IdleResourceDetector(cfg).summarise(resources)
    assert s["total_monthly_waste_usd"] == pytest.approx(373.5)


def test_annual_projection(cfg, resources):
    s = IdleResourceDetector(cfg).summarise(resources)
    assert s["total_annual_waste_usd"] == pytest.approx(373.5 * 12)


def test_top_offenders_sorted(cfg, resources):
    s = IdleResourceDetector(cfg).summarise(resources)
    offenders = s["top_offenders"]
    for i in range(len(offenders) - 1):
        assert offenders[i]["waste_usd"] >= offenders[i+1]["waste_usd"]


def test_by_type_breakdown(cfg, resources):
    s = IdleResourceDetector(cfg).summarise(resources)
    assert "ec2" in s["by_type"]
    assert "ebs" in s["by_type"]
    assert "rds" in s["by_type"]
    assert s["by_type"]["ec2"]["count"] == 2


def test_empty_resources(cfg):
    s = IdleResourceDetector(cfg).summarise([])
    assert s["total_idle_resources"] == 0
    assert s["total_monthly_waste_usd"] == 0.0
    assert s["top_offenders"] == []
