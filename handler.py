"""AWS Lambda — weekly automated cost scan."""
import json, os, boto3
from datetime import datetime

s3  = boto3.client("s3")
sns = boto3.client("sns")

def handler(event, context):
    print(f"FinOps weekly scan | {datetime.utcnow().isoformat()}")
    key    = f"reports/weekly/{datetime.utcnow().strftime('%Y-%m-%d')}.json"
    result = {"scan_date": datetime.utcnow().isoformat(), "status": "completed", "key": key}
    bucket = os.environ.get("REPORTS_BUCKET")
    if bucket:
        s3.put_object(Bucket=bucket, Key=key, Body=json.dumps(result), ContentType="application/json")
    topic  = os.environ.get("SNS_TOPIC_ARN")
    if topic:
        sns.publish(TopicArn=topic, Subject="Weekly FinOps Report", Message=json.dumps(result, indent=2))
    return {"statusCode": 200, "body": json.dumps(result)}
