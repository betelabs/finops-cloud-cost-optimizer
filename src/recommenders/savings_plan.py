"""Reserved Instance / Savings Plan ROI calculator."""
from __future__ import annotations
from typing import Dict


ON_DEMAND_MONTHLY = {
    "t3.large": 60, "t3.xlarge": 120, "m5.large": 70,
    "m5.xlarge": 140, "r5.large": 90, "r5.xlarge": 180,
}

RI_DISCOUNT_1YR  = 0.38   # ~38 % off 1-year no-upfront
RI_DISCOUNT_3YR  = 0.57   # ~57 % off 3-year no-upfront
SP_DISCOUNT_1YR  = 0.33   # Compute Savings Plan 1-year


def ri_roi(instance_type: str, count: int = 1, term_years: int = 1) -> Dict:
    monthly_od   = ON_DEMAND_MONTHLY.get(instance_type, 100) * count
    discount     = RI_DISCOUNT_1YR if term_years == 1 else RI_DISCOUNT_3YR
    monthly_ri   = monthly_od * (1 - discount)
    monthly_save = monthly_od - monthly_ri
    return {
        "instance_type":      instance_type,
        "count":              count,
        "term_years":         term_years,
        "monthly_on_demand":  round(monthly_od, 2),
        "monthly_reserved":   round(monthly_ri, 2),
        "monthly_saving":     round(monthly_save, 2),
        "annual_saving":      round(monthly_save * 12, 2),
        "total_saving":       round(monthly_save * 12 * term_years, 2),
    }
