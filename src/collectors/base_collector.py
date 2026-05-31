"""Abstract base classes for all cloud cost collectors."""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class ResourceCost:
    resource_id: str
    resource_type: str          # ec2 | rds | s3 | ebs | nat_gw | vm | gcs …
    service: str
    region: str
    cloud: str                  # aws | azure | gcp
    team: Optional[str]
    environment: Optional[str]
    daily_cost_usd: float
    monthly_cost_usd: float
    tags: dict = field(default_factory=dict)


@dataclass
class IdleResource:
    resource_id: str
    resource_type: str
    cloud: str
    region: str
    avg_cpu_percent: float
    avg_network_bytes: float
    idle_days: int
    monthly_waste_usd: float
    recommendation: str         # terminate | rightsize | stop | delete | lifecycle


class BaseCollector(ABC):
    def __init__(self, config: dict):
        self.config = config

    @abstractmethod
    def get_total_spend(self, start: datetime, end: datetime) -> float:
        """Return total USD spend for the period."""

    @abstractmethod
    def get_cost_by_service(self, start: datetime, end: datetime) -> List[ResourceCost]:
        """Return cost breakdown by service for the given period."""

    @abstractmethod
    def get_idle_resources(self) -> List[IdleResource]:
        """Return list of idle / underutilised resources."""
