# AWS Setup Guide

## IAM Policy
Create an IAM policy with these permissions and attach it to the user / role:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ce:GetCostAndUsage",
        "ec2:DescribeInstances",
        "ec2:DescribeVolumes",
        "ec2:DescribeSnapshots",
        "rds:DescribeDBInstances",
        "cloudwatch:GetMetricStatistics",
        "s3:ListBuckets",
        "s3:GetBucketLifecycleConfiguration"
      ],
      "Resource": "*"
    }
  ]
}
```

## Tag your resources
For accurate team-level attribution, tag all resources with:
- `team`        — e.g. `backend`, `data`, `platform`
- `environment` — e.g. `prod`, `staging`, `dev`
- `service`     — e.g. `payments-api`, `ml-training`

Without tags, spend appears under `untagged`.
