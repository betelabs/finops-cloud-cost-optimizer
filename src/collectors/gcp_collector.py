"""GCP Billing API collector (stub — extend with google-cloud-billing)."""
from __future__ import annotations
from datetime import datetime
from typing import List
from .base_collector import BaseCollector, ResourceCost, IdleResource


class GCPCollector(BaseCollector):
    """
    Requires: pip install google-cloud-billing google-cloud-monitoring
    Auth:     gcloud auth application-default login
    """

    def __init__(self, config: dict):
        super().__init__(config)
        self.project_id      = config.get("project_id", "")
        self.billing_account = config.get("billing_account", "")

    def get_total_spend(self, start: datetime, end: datetime) -> float:
        # TODO: BigQuery billing export query
        raise NotImplementedError("GCP total spend — see docs/gcp-setup.md")

    def get_cost_by_service(self, start: datetime, end: datetime) -> List[ResourceCost]:
        raise NotImplementedError("GCP cost by service — see docs/gcp-setup.md")

    def get_idle_resources(self) -> List[IdleResource]:
        raise NotImplementedError("GCP idle resources — see docs/gcp-setup.md")
