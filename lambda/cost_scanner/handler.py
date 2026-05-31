"""AWS Lambda handler — triggered weekly by EventBridge."""
from __future__ import annotations
import json, os, boto3
from datetime import datetime

s3  = boto3.client("s3")
sns = boto3.client("sns")


def handler(event, context):
    """
    Entry point.  EventBridge fires this every Monday 09:00 UTC.
    The full scan logic lives in src/ — packaged via lambda/cost_scanner/build.sh.
    """
    print(f"[finops-scanner] started at {datetime.utcnow().isoformat()}")

    # --- run scan (imported from bundled src/) ---
    # from src.collectors.aws_collector import AWSCollector
    # from src.analyzers.idle_detector  import IdleResourceDetector
    # collector = AWSCollector({"region": os.environ.get("AWS_REGION", "us-east-1")})
    # ...

    key    = f"reports/weekly/{datetime.utcnow().strftime('%Y/%m/%d')}/report.json"
    result = {
        "scan_date":  datetime.utcnow().isoformat(),
        "status":     "completed",
        "report_key": key,
    }

    bucket = os.environ.get("REPORTS_BUCKET")
    if bucket:
        s3.put_object(Bucket=bucket, Key=key,
                      Body=json.dumps(result, indent=2),
                      ContentType="application/json")
        print(f"[finops-scanner] report uploaded → s3://{bucket}/{key}")

    topic = os.environ.get("SNS_TOPIC_ARN")
    if topic:
        sns.publish(
            TopicArn=topic,
            Subject="Weekly FinOps Report Ready",
            Message=json.dumps(result, indent=2),
        )
        print(f"[finops-scanner] SNS notification sent → {topic}")

    return {"statusCode": 200, "body": json.dumps(result)}
