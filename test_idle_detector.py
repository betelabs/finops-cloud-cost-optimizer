import pytest
from src.analyzers.idle_detector import IdleResourceDetector
from src.collectors.base_collector import IdleResource

@pytest.fixture
def config(): return {"thresholds": {"idle_cpu_percent": 5}}

@pytest.fixture
def resources():
    return [
        IdleResource("i-abc123", "ec2", "aws", "us-east-1", 0.5, 0, 14, 120.0, "terminate"),
        IdleResource("i-def456", "ec2", "aws", "us-east-1", 3.2, 0, 14,  70.0, "rightsize"),
        IdleResource("vol-xyz",  "ebs", "aws", "us-east-1", 0.0, 0, 30,   8.5, "delete"),
    ]

def test_total_waste(config, resources):
    s = IdleResourceDetector(config).summarise(resources)
    assert s["total_monthly_waste_usd"] == pytest.approx(198.5)

def test_annual_projection(config, resources):
    s = IdleResourceDetector(config).summarise(resources)
    assert s["total_annual_waste_usd"] == pytest.approx(198.5 * 12)

def test_top_offenders_sorted(config, resources):
    s = IdleResourceDetector(config).summarise(resources)
    offs = s["top_offenders"]
    assert offs[0]["waste_usd"] >= offs[1]["waste_usd"]

def test_empty(config):
    s = IdleResourceDetector(config).summarise([])
    assert s["total_idle_resources"] == 0
