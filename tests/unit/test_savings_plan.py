"""Unit tests for RI/Savings Plan ROI calculator."""
import pytest
from src.recommenders.savings_plan import ri_roi


def test_ri_1yr_saves_money():
    result = ri_roi("m5.large", count=1, term_years=1)
    assert result["monthly_saving"] > 0
    assert result["annual_saving"] == pytest.approx(result["monthly_saving"] * 12)


def test_ri_3yr_saves_more_than_1yr():
    r1 = ri_roi("m5.xlarge", count=1, term_years=1)
    r3 = ri_roi("m5.xlarge", count=1, term_years=3)
    assert r3["monthly_saving"] > r1["monthly_saving"]


def test_ri_scales_with_count():
    r1 = ri_roi("t3.large", count=1)
    r5 = ri_roi("t3.large", count=5)
    assert r5["monthly_saving"] == pytest.approx(r1["monthly_saving"] * 5)


def test_unknown_instance_uses_default():
    result = ri_roi("p4d.24xlarge", count=1)
    assert result["monthly_saving"] > 0
