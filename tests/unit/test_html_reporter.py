"""Unit tests for HTMLReporter."""
import os
import tempfile
from src.reporters.html_reporter import HTMLReporter


SAMPLE_SUMMARY = {
    "total_spend_usd":        48320,
    "total_monthly_waste_usd": 11240,
    "total_annual_waste_usd":  134880,
    "account":                 "123456789012",
    "period":                  "last 30 days",
    "top_offenders": [
        {"id": "i-abc123", "type": "ec2", "cloud": "aws", "region": "us-east-1a",
         "action": "terminate", "waste_usd": 1440},
        {"id": "db-prod01", "type": "rds", "cloud": "aws", "region": "us-east-1a",
         "action": "rightsize", "waste_usd": 2100},
    ],
}


def test_generates_html_file():
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
        path = f.name
    try:
        out = HTMLReporter().generate(SAMPLE_SUMMARY, path)
        assert os.path.exists(out)
        assert os.path.getsize(out) > 500
    finally:
        os.unlink(path)


def test_html_contains_kpi_values():
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w") as f:
        path = f.name
    try:
        HTMLReporter().generate(SAMPLE_SUMMARY, path)
        content = open(path).read()
        assert "48,320" in content
        assert "11,240" in content
        assert "terminate" in content
    finally:
        os.unlink(path)
