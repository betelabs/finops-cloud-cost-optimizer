"""Send cost alerts to a Slack webhook."""
from __future__ import annotations
import json, requests
from typing import Dict


class SlackNotifier:
    def __init__(self, webhook_url: str):
        self.webhook = webhook_url

    def send(self, summary: Dict) -> bool:
        waste   = summary.get("total_monthly_waste_usd", 0)
        annual  = summary.get("total_annual_waste_usd", 0)
        n_idle  = summary.get("total_idle_resources", 0)
        top     = summary.get("top_offenders", [])[:3]

        lines = [f"> *{o['id']}* — `{o['action']}` → *${o['waste_usd']:,.0f}/mo*" for o in top]
        body = {
            "blocks": [
                {"type": "header", "text": {"type": "plain_text", "text": "💰 FinOps Weekly Scan"}},
                {"type": "section", "text": {"type": "mrkdwn", "text": (
                    f"*Identified waste:* ${waste:,.0f}/mo  |  *Annual savings est:* ${annual:,.0f}  |  *Idle resources:* {n_idle}"
                )}},
                {"type": "section", "text": {"type": "mrkdwn", "text": "*Top offenders:*\n" + "\n".join(lines)}},
            ]
        }
        r = requests.post(self.webhook, data=json.dumps(body),
                          headers={"Content-Type": "application/json"}, timeout=10)
        return r.status_code == 200

    def send_budget_alert(self, percent_used: float, budget_usd: float) -> bool:
        body = {"text": (
            f":rotating_light: *Budget Alert* — {percent_used:.0f}% of monthly budget used\n"
            f"Budget: ${budget_usd:,.0f} | Used: ${budget_usd * percent_used / 100:,.0f}"
        )}
        r = requests.post(self.webhook, data=json.dumps(body),
                          headers={"Content-Type": "application/json"}, timeout=10)
        return r.status_code == 200
