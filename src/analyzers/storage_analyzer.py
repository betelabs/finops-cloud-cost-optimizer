"""Detect storage waste: unattached EBS, stale snapshots, S3 lifecycle gaps."""
from __future__ import annotations
import boto3
from datetime import datetime, timedelta, timezone
from typing import List
from ..collectors.base_collector import IdleResource


class StorageAnalyzer:
    def __init__(self, region: str = "us-east-1"):
        self.ec2 = boto3.client("ec2", region_name=region)
        self.s3  = boto3.client("s3")

    def stale_snapshots(self, days: int = 90) -> List[IdleResource]:
        """Return EBS snapshots older than `days` days."""
        cutoff = datetime.now(tz=timezone.utc) - timedelta(days=days)
        snaps  = self.ec2.describe_snapshots(OwnerIds=["self"])["Snapshots"]
        idle   = []
        for snap in snaps:
            if snap["StartTime"] < cutoff:
                size_gb = snap.get("VolumeSize", 0)
                idle.append(IdleResource(
                    resource_id=snap["SnapshotId"], resource_type="snapshot",
                    cloud="aws", region="global",
                    avg_cpu_percent=0, avg_network_bytes=0,
                    idle_days=(datetime.now(tz=timezone.utc) - snap["StartTime"]).days,
                    monthly_waste_usd=round(size_gb * 0.05, 2),
                    recommendation="delete",
                ))
        return idle

    def s3_lifecycle_candidates(self) -> List[dict]:
        """Return S3 buckets with no lifecycle policy (potential intelligent-tiering candidates)."""
        buckets = self.s3.list_buckets().get("Buckets", [])
        candidates = []
        for b in buckets:
            name = b["Name"]
            try:
                self.s3.get_bucket_lifecycle_configuration(Bucket=name)
            except self.s3.exceptions.ClientError:
                candidates.append({"bucket": name, "recommendation": "add-lifecycle-policy"})
        return candidates
