"""AWS Lambda — triggered by AWS Budgets SNS notification."""
from __future__ import annotations
import json, os, requests
from datetime import datetime


def handler(event, context):
    """Parse AWS Budget alert and forward to Slack."""
    for record in event.get("Records", []):
        message = json.loads(record.get("Sns", {}).get("Message", "{}"))
        budget  = message.get("budgetName", "unknown")
        actual  = message.get("costFilters", {})
        pct     = message.get("notificationThreshold", 0)

        print(f"Budget alert: {budget} at {pct}% | {datetime.utcnow().isoformat()}")

        webhook = os.environ.get("SLACK_WEBHOOK")
        if webhook:
            requests.post(webhook, json={
                "text": f":money_with_wings: *Budget Alert* — `{budget}` reached *{pct}%* of monthly limit"
            }, timeout=10)

    return {"statusCode": 200}
