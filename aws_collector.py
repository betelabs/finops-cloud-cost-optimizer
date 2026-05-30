import boto3
from datetime import datetime, timedelta
from typing import List
from .base_collector import BaseCollector, ResourceCost, IdleResource

class AWSCollector(BaseCollector):
    def __init__(self, config: dict):
        super().__init__(config)
        region = config.get("region", "us-east-1")
        self.ce         = boto3.client("ce", region_name="us-east-1")
        self.ec2        = boto3.client("ec2", region_name=region)
        self.cloudwatch = boto3.client("cloudwatch", region_name=region)

    def get_total_spend(self, start: datetime, end: datetime) -> float:
        response = self.ce.get_cost_and_usage(
            TimePeriod={"Start": start.strftime("%Y-%m-%d"), "End": end.strftime("%Y-%m-%d")},
            Granularity="MONTHLY", Metrics=["UnblendedCost"],
        )
        return sum(float(r["Total"]["UnblendedCost"]["Amount"]) for r in response["ResultsByTime"])

    def get_cost_by_service(self, start: datetime, end: datetime) -> List[ResourceCost]:
        response = self.ce.get_cost_and_usage(
            TimePeriod={"Start": start.strftime("%Y-%m-%d"), "End": end.strftime("%Y-%m-%d")},
            Granularity="MONTHLY", Metrics=["UnblendedCost"],
            GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}, {"Type": "TAG", "Key": "team"}],
        )
        resources = []
        for result in response["ResultsByTime"]:
            for group in result.get("Groups", []):
                service = group["Keys"][0]
                team    = group["Keys"][1].replace("team$", "") or "untagged"
                cost    = float(group["Metrics"]["UnblendedCost"]["Amount"])
                resources.append(ResourceCost(
                    resource_id=service, resource_type="service", service=service,
                    region="us-east-1", cloud="aws", team=team, environment=None,
                    daily_cost_usd=cost/30, monthly_cost_usd=cost, tags={"team": team},
                ))
        return resources

    def get_idle_resources(self) -> List[IdleResource]:
        idle = []
        threshold = self.config.get("thresholds", {}).get("idle_cpu_percent", 5)
        idle_days = self.config.get("thresholds", {}).get("idle_cpu_days", 14)
        instances = self.ec2.describe_instances(Filters=[{"Name": "instance-state-name", "Values": ["running"]}])
        for reservation in instances["Reservations"]:
            for instance in reservation["Instances"]:
                iid   = instance["InstanceId"]
                itype = instance["InstanceType"]
                cw    = self.cloudwatch.get_metric_statistics(
                    Namespace="AWS/EC2", MetricName="CPUUtilization",
                    Dimensions=[{"Name": "InstanceId", "Value": iid}],
                    StartTime=datetime.utcnow() - timedelta(days=idle_days),
                    EndTime=datetime.utcnow(), Period=86400, Statistics=["Average"],
                )
                pts = cw.get("Datapoints", [])
                if not pts: continue
                avg_cpu = sum(d["Average"] for d in pts) / len(pts)
                if avg_cpu < threshold:
                    idle.append(IdleResource(
                        resource_id=iid, resource_type="ec2", cloud="aws",
                        region=instance.get("Placement", {}).get("AvailabilityZone", ""),
                        avg_cpu_percent=avg_cpu, avg_network_bytes=0, idle_days=idle_days,
                        monthly_waste_usd=self._ec2_price(itype),
                        recommendation="terminate" if avg_cpu < 1 else "rightsize",
                    ))
        return idle

    def _ec2_price(self, instance_type: str) -> float:
        prices = {"t3.micro": 8.5, "t3.small": 15, "t3.medium": 30, "t3.large": 60,
                  "t3.xlarge": 120, "m5.large": 70, "m5.xlarge": 140, "r5.large": 90}
        return prices.get(instance_type, 100)
