from typing import List, Dict
from ..collectors.base_collector import IdleResource

class IdleResourceDetector:
    def __init__(self, config: dict):
        self.cpu_threshold = config.get("thresholds", {}).get("idle_cpu_percent", 5)

    def summarise(self, idle_resources: List[IdleResource]) -> Dict:
        total_waste = sum(r.monthly_waste_usd for r in idle_resources)
        by_type = {}
        for r in idle_resources:
            by_type.setdefault(r.resource_type, []).append(r)
        return {
            "total_idle_resources": len(idle_resources),
            "total_monthly_waste_usd": round(total_waste, 2),
            "total_annual_waste_usd": round(total_waste * 12, 2),
            "by_type": {
                rt: {"count": len(rs), "monthly_waste_usd": round(sum(r.monthly_waste_usd for r in rs), 2)}
                for rt, rs in by_type.items()
            },
            "top_offenders": sorted(
                [{"id": r.resource_id, "type": r.resource_type,
                  "waste_usd": r.monthly_waste_usd, "action": r.recommendation}
                 for r in idle_resources],
                key=lambda x: x["waste_usd"], reverse=True
            )[:10],
        }
