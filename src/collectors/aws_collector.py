"""AWS collector — Cost Explorer + Boto3 + CloudWatch."""
from __future__ import annotations
import boto3
from datetime import datetime, timedelta
from typing import List
from .base_collector import BaseCollector, ResourceCost, IdleResource


EC2_PRICES_USD_MONTHLY = {
    "t3.micro": 8.5,  "t3.small": 15,   "t3.medium": 30,
    "t3.large": 60,   "t3.xlarge": 120,  "t3.2xlarge": 240,
    "m5.large": 70,   "m5.xlarge": 140,  "m5.2xlarge": 280,
    "r5.large": 90,   "r5.xlarge": 180,  "r5.2xlarge": 360,
    "c5.large": 62,   "c5.xlarge": 124,
}


class AWSCollector(BaseCollector):
    def __init__(self, config: dict):
        super().__init__(config)
        region = config.get("region", "us-east-1")
        self.ce  = boto3.client("ce",         region_name="us-east-1")
        self.ec2 = boto3.client("ec2",        region_name=region)
        self.rds = boto3.client("rds",        region_name=region)
        self.cw  = boto3.client("cloudwatch", region_name=region)

    # ── spend ───────────────────────────────────────────────────────────
    def get_total_spend(self, start: datetime, end: datetime) -> float:
        resp = self.ce.get_cost_and_usage(
            TimePeriod={"Start": start.strftime("%Y-%m-%d"),
                        "End":   end.strftime("%Y-%m-%d")},
            Granularity="MONTHLY",
            Metrics=["UnblendedCost"],
        )
        return sum(
            float(r["Total"]["UnblendedCost"]["Amount"])
            for r in resp["ResultsByTime"]
        )

    def get_cost_by_service(self, start: datetime, end: datetime) -> List[ResourceCost]:
        resp = self.ce.get_cost_and_usage(
            TimePeriod={"Start": start.strftime("%Y-%m-%d"),
                        "End":   end.strftime("%Y-%m-%d")},
            Granularity="MONTHLY",
            Metrics=["UnblendedCost"],
            GroupBy=[
                {"Type": "DIMENSION", "Key": "SERVICE"},
                {"Type": "TAG",       "Key": "team"},
            ],
        )
        results: List[ResourceCost] = []
        for period in resp["ResultsByTime"]:
            for group in period.get("Groups", []):
                service = group["Keys"][0]
                team    = group["Keys"][1].replace("team$", "") or "untagged"
                cost    = float(group["Metrics"]["UnblendedCost"]["Amount"])
                results.append(ResourceCost(
                    resource_id=service, resource_type="service",
                    service=service, region="multi", cloud="aws",
                    team=team, environment=None,
                    daily_cost_usd=round(cost / 30, 4),
                    monthly_cost_usd=round(cost, 4),
                    tags={"team": team},
                ))
        return results

    # ── idle detection ──────────────────────────────────────────────────
    def get_idle_resources(self) -> List[IdleResource]:
        idle: List[IdleResource] = []
        idle += self._idle_ec2()
        idle += self._idle_rds()
        idle += self._unattached_ebs()
        return idle

    def _idle_ec2(self) -> List[IdleResource]:
        cpu_thresh = self.config.get("thresholds", {}).get("idle_cpu_percent", 5)
        days       = self.config.get("thresholds", {}).get("idle_cpu_days", 14)
        idle: List[IdleResource] = []
        reservations = self.ec2.describe_instances(
            Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
        )["Reservations"]
        for res in reservations:
            for inst in res["Instances"]:
                iid   = inst["InstanceId"]
                itype = inst["InstanceType"]
                pts   = self.cw.get_metric_statistics(
                    Namespace="AWS/EC2", MetricName="CPUUtilization",
                    Dimensions=[{"Name": "InstanceId", "Value": iid}],
                    StartTime=datetime.utcnow() - timedelta(days=days),
                    EndTime=datetime.utcnow(),
                    Period=86400, Statistics=["Average"],
                )["Datapoints"]
                if not pts:
                    continue
                avg_cpu = sum(p["Average"] for p in pts) / len(pts)
                if avg_cpu < cpu_thresh:
                    idle.append(IdleResource(
                        resource_id=iid, resource_type="ec2", cloud="aws",
                        region=inst.get("Placement", {}).get("AvailabilityZone", ""),
                        avg_cpu_percent=round(avg_cpu, 2), avg_network_bytes=0,
                        idle_days=days,
                        monthly_waste_usd=EC2_PRICES_USD_MONTHLY.get(itype, 100),
                        recommendation="terminate" if avg_cpu < 1 else "rightsize",
                    ))
        return idle

    def _idle_rds(self) -> List[IdleResource]:
        idle: List[IdleResource] = []
        instances = self.rds.describe_db_instances()["DBInstances"]
        for db in instances:
            dbid = db["DBInstanceIdentifier"]
            pts  = self.cw.get_metric_statistics(
                Namespace="AWS/RDS", MetricName="DatabaseConnections",
                Dimensions=[{"Name": "DBInstanceIdentifier", "Value": dbid}],
                StartTime=datetime.utcnow() - timedelta(days=7),
                EndTime=datetime.utcnow(),
                Period=86400, Statistics=["Average"],
            )["Datapoints"]
            if not pts:
                continue
            avg_conn = sum(p["Average"] for p in pts) / len(pts)
            if avg_conn < 2:
                idle.append(IdleResource(
                    resource_id=dbid, resource_type="rds", cloud="aws",
                    region=db.get("AvailabilityZone", ""),
                    avg_cpu_percent=0, avg_network_bytes=0, idle_days=7,
                    monthly_waste_usd=self._rds_price(db.get("DBInstanceClass", "")),
                    recommendation="stop",
                ))
        return idle

    def _unattached_ebs(self) -> List[IdleResource]:
        idle: List[IdleResource] = []
        volumes = self.ec2.describe_volumes(
            Filters=[{"Name": "status", "Values": ["available"]}]
        )["Volumes"]
        for vol in volumes:
            size_gb = vol.get("Size", 0)
            cost    = round(size_gb * 0.10, 2)   # gp2 ~$0.10/GB/month
            idle.append(IdleResource(
                resource_id=vol["VolumeId"], resource_type="ebs", cloud="aws",
                region=vol.get("AvailabilityZone", ""),
                avg_cpu_percent=0, avg_network_bytes=0, idle_days=0,
                monthly_waste_usd=cost, recommendation="delete",
            ))
        return idle

    def _rds_price(self, instance_class: str) -> float:
        prices = {
            "db.t3.micro": 15, "db.t3.small": 30, "db.t3.medium": 60,
            "db.r5.large": 175, "db.r5.xlarge": 350, "db.r5.2xlarge": 700,
        }
        return prices.get(instance_class, 200)
