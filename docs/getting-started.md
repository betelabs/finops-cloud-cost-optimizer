# Getting Started

## 1 — Clone & install
```bash
git clone https://github.com/ashwani547/finops-cloud-cost-optimizer.git
cd finops-cloud-cost-optimizer
pip install -r requirements.txt
```

## 2 — Configure
```bash
cp config/config.example.yaml config/config.yaml
# Fill in your AWS account ID, region, budget, Slack webhook
```

## 3 — AWS permissions needed
The IAM user / role running scans needs:
- `ce:GetCostAndUsage`
- `ec2:DescribeInstances`, `ec2:DescribeVolumes`, `ec2:DescribeSnapshots`
- `rds:DescribeDBInstances`
- `cloudwatch:GetMetricStatistics`

## 4 — Run your first scan
```bash
python -m cli.main scan --cloud aws --days 30
```

## 5 — Automate (optional)
```bash
cd terraform/aws
cp terraform.tfvars.example terraform.tfvars   # fill in values
terraform init && terraform apply
# Lambda fires every Monday 09:00 UTC automatically
```
