"""EC2 rightsizing recommendations based on CloudWatch CPU metrics."""
from __future__ import annotations
import boto3
from datetime import datetime, timedelta
from typing import List, Dict


DOWNSIZE_MAP = {
    "t3.2xlarge": "t3.xlarge", "t3.xlarge": "t3.large", "t3.large": "t3.medium",
    "m5.2xlarge": "m5.xlarge", "m5.xlarge": "m5.large",
    "r5.2xlarge": "r5.xlarge", "r5.xlarge": "r5.large",
    "c5.2xlarge": "c5.xlarge", "c5.xlarge": "c5.large",
}

EC2_PRICES = {
    "t3.medium": 30, "t3.large": 60,  "t3.xlarge": 120, "t3.2xlarge": 240,
    "m5.large":  70, "m5.xlarge": 140, "m5.2xlarge": 280,
    "r5.large":  90, "r5.xlarge": 180, "r5.2xlarge": 360,
    "c5.large":  62, "c5.xlarge": 124, "c5.2xlarge": 248,
}


class EC2RightsizingRecommender:
    def __init__(self, region: str = "us-east-1"):
        self.ec2 = boto3.client("ec2",        region_name=region)
        self.cw  = boto3.client("cloudwatch", region_name=region)

    def analyse(self, cpu_high_threshold: float = 40.0, days: int = 14) -> List[Dict]:
        """Return instances where avg CPU < threshold and a smaller type exists."""
        recommendations = []
        reservations = self.ec2.describe_instances(
            Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
        )["Reservations"]

        for res in reservations:
            for inst in res["Instances"]:
                iid   = inst["InstanceId"]
                itype = inst["InstanceType"]
                if itype not in DOWNSIZE_MAP:
                    continue

                pts = self.cw.get_metric_statistics(
                    Namespace="AWS/EC2", MetricName="CPUUtilization",
                    Dimensions=[{"Name": "InstanceId", "Value": iid}],
                    StartTime=datetime.utcnow() - timedelta(days=days),
                    EndTime=datetime.utcnow(),
                    Period=86400, Statistics=["Average", "Maximum"],
                )["Datapoints"]

                if not pts:
                    continue

                avg_cpu = sum(p["Average"] for p in pts) / len(pts)
                max_cpu = max(p["Maximum"] for p in pts)

                if avg_cpu < cpu_high_threshold and max_cpu < 80:
                    target = DOWNSIZE_MAP[itype]
                    saving = EC2_PRICES.get(itype, 0) - EC2_PRICES.get(target, 0)
                    recommendations.append({
                        "instance_id":    iid,
                        "current_type":   itype,
                        "recommended":    target,
                        "avg_cpu_pct":    round(avg_cpu, 1),
                        "max_cpu_pct":    round(max_cpu, 1),
                        "monthly_saving": saving,
                    })

        return sorted(recommendations, key=lambda x: x["monthly_saving"], reverse=True)
