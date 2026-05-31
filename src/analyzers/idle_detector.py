"""Aggregate and rank idle resources across all clouds."""
from __future__ import annotations
from typing import List, Dict
from ..collectors.base_collector import IdleResource


class IdleResourceDetector:
    def __init__(self, config: dict):
        self.config = config

    def summarise(self, resources: List[IdleResource]) -> Dict:
        total_waste = sum(r.monthly_waste_usd for r in resources)
        by_type: Dict[str, List[IdleResource]] = {}
        for r in resources:
            by_type.setdefault(r.resource_type, []).append(r)

        return {
            "total_idle_resources": len(resources),
            "total_monthly_waste_usd": round(total_waste, 2),
            "total_annual_waste_usd":  round(total_waste * 12, 2),
            "by_type": {
                rt: {
                    "count": len(rs),
                    "monthly_waste_usd": round(sum(r.monthly_waste_usd for r in rs), 2),
                }
                for rt, rs in by_type.items()
            },
            "top_offenders": sorted(
                [
                    {
                        "id":        r.resource_id,
                        "type":      r.resource_type,
                        "cloud":     r.cloud,
                        "region":    r.region,
                        "action":    r.recommendation,
                        "waste_usd": round(r.monthly_waste_usd, 2),
                    }
                    for r in resources
                ],
                key=lambda x: x["waste_usd"],
                reverse=True,
            )[:10],
        }
