from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class ResourceCost:
    resource_id: str; resource_type: str; service: str; region: str; cloud: str
    team: Optional[str]; environment: Optional[str]
    daily_cost_usd: float; monthly_cost_usd: float; tags: dict

@dataclass
class IdleResource:
    resource_id: str; resource_type: str; cloud: str; region: str
    avg_cpu_percent: float; avg_network_bytes: float; idle_days: int
    monthly_waste_usd: float; recommendation: str

class BaseCollector(ABC):
    def __init__(self, config: dict): self.config = config
    @abstractmethod
    def get_cost_by_service(self, start: datetime, end: datetime) -> List[ResourceCost]: ...
    @abstractmethod
    def get_idle_resources(self) -> List[IdleResource]: ...
    @abstractmethod
    def get_total_spend(self, start: datetime, end: datetime) -> float: ...
