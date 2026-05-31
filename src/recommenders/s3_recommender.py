"""S3 cost optimisation recommendations."""
from __future__ import annotations
from typing import List, Dict


STORAGE_CLASS_SAVINGS = {
    "STANDARD → INTELLIGENT_TIERING": 0.23,
    "STANDARD → STANDARD_IA":         0.46,
    "STANDARD → GLACIER_IR":          0.68,
    "STANDARD → GLACIER":             0.80,
}


def lifecycle_recommendations(buckets_without_policy: List[str]) -> List[Dict]:
    """Suggest lifecycle rules for buckets without them."""
    recs = []
    for bucket in buckets_without_policy:
        recs.append({
            "bucket": bucket,
            "recommendations": [
                {"action": "transition to INTELLIGENT_TIERING after 30 days",  "estimated_saving_pct": 23},
                {"action": "transition to GLACIER_IR after 90 days",           "estimated_saving_pct": 68},
                {"action": "expire incomplete multipart uploads after 7 days",  "estimated_saving_pct": 1},
            ],
        })
    return recs
