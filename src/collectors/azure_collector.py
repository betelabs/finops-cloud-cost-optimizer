"""Azure Cost Management SDK collector (stub — extend with azure-mgmt-costmanagement)."""
from __future__ import annotations
from datetime import datetime
from typing import List
from .base_collector import BaseCollector, ResourceCost, IdleResource


class AzureCollector(BaseCollector):
    """
    Requires: pip install azure-mgmt-costmanagement azure-identity
    Auth:     az login  or  set AZURE_CLIENT_ID / AZURE_CLIENT_SECRET / AZURE_TENANT_ID
    """

    def __init__(self, config: dict):
        super().__init__(config)
        self.subscription_id = config.get("subscription_id", "")
        self._client = None   # lazy-init so tests don't need Azure creds

    def _get_client(self):
        if self._client is None:
            from azure.identity import DefaultAzureCredential
            from azure.mgmt.costmanagement import CostManagementClient
            self._client = CostManagementClient(
                credential=DefaultAzureCredential(),
                subscription_id=self.subscription_id,
            )
        return self._client

    def get_total_spend(self, start: datetime, end: datetime) -> float:
        # TODO: implement via self._get_client().query.usage(...)
        raise NotImplementedError("Azure total spend — see docs/azure-setup.md")

    def get_cost_by_service(self, start: datetime, end: datetime) -> List[ResourceCost]:
        raise NotImplementedError("Azure cost by service — see docs/azure-setup.md")

    def get_idle_resources(self) -> List[IdleResource]:
        raise NotImplementedError("Azure idle resources — see docs/azure-setup.md")
