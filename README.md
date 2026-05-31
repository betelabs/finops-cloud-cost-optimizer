<div align="center">

# 💰 finops-cloud-cost-optimizer

**Automated cloud cost governance — idle resource detection, rightsizing, budget alerts & savings dashboards**

*Built by [Ashwani Kumar](https://linkedin.com/in/ashwani547) · Head of DevOps · CKA Certified · 12+ years cloud experience*

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![AWS](https://img.shields.io/badge/AWS-Cost%20Explorer-FF9900?logo=amazon-aws&logoColor=white)](https://aws.amazon.com)
[![Azure](https://img.shields.io/badge/Azure-Cost%20Mgmt-0078D4?logo=microsoft-azure&logoColor=white)](https://azure.microsoft.com)
[![GCP](https://img.shields.io/badge/GCP-Billing%20API-4285F4?logo=google-cloud&logoColor=white)](https://cloud.google.com)
[![Grafana](https://img.shields.io/badge/Grafana-Dashboards-F46800?logo=grafana&logoColor=white)](https://grafana.com)
[![Terraform](https://img.shields.io/badge/Terraform-1.7-7B42BC?logo=terraform&logoColor=white)](https://terraform.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/betelabs/finops-cloud-cost-optimizer/actions/workflows/ci.yaml/badge.svg)](https://github.com/betelabs/finops-cloud-cost-optimizer/actions)

</div>

---

## 🎯 What This Solves

Cloud bills grow silently. Teams ship fast and forget to clean up. Finance sees the invoice
but can't attribute it. The result: **30–40% of cloud spend is waste** in most organisations.

This tool gives you:

| Problem | This Tool's Answer |
|---|---|
| No idea where the money goes | Multi-cloud collector + team-level attribution |
| Idle EC2, RDS, EBS piling up | Automated weekly idle resource scanner |
| Oversized instances | CloudWatch-based rightsizing recommendations |
| Budget shocks on invoice day | AWS/Azure/GCP budget alerts at 50/80/95/100% |
| Manual monthly reviews | HTML/JSON reports + Slack digest, auto-generated |
| No audit trail | S3-backed report history, 90-day retention |

---

## 📊 Proven Results Across Real Deployments

> See [`case-studies/`](case-studies/) for full write-ups with methodology and numbers.

| Organisation | Cloud | Baseline | Saved/mo | Saving % | Time |
|---|---|---|---|---|---|
| [Tricog Health](case-studies/tricog-health-25pct-savings.md) | AWS + Azure | $48K | $12,100 | 25% | 90 days |
| [Marvin](case-studies/marvin-inc-startup-cost-control.md) | AWS | $22K | $5,190 | 24% | 90 days |
| [Coredge Inc](case-studies/coredge-multicloud-governance.md) | AWS+Azure+GCP | $95K | $20,800 | 22% | 60 days |
| [RapidCanvas](case-studies/rapidcanvas-mlops-cost.md) | AWS + GCP | $38K | $10,570 | 28% | 90 days |

---

## 🏗️ Architecture

```
┌───────────────────────────────────────────────────────────────┐
│                     Data Collection Layer                      │
│                                                               │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────────┐  │
│  │ AWS Cost     │   │ Azure Cost   │   │ GCP Billing API  │  │
│  │ Explorer +   │   │ Mgmt SDK     │   │ + BigQuery       │  │
│  │ CloudWatch   │   │              │   │   export         │  │
│  └──────┬───────┘   └──────┬───────┘   └────────┬─────────┘  │
└─────────┼──────────────────┼────────────────────┼────────────┘
          └──────────────────▼────────────────────┘
                             │
                   ┌─────────▼──────────┐
                   │  Unified Cost Model │
                   │  (dataclasses)      │
                   └─────────┬──────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
  ┌──────▼──────┐   ┌────────▼────────┐  ┌──────▼──────┐
  │  Idle        │   │  Rightsizing    │  │  Budget     │
  │  Detector    │   │  Recommender    │  │  Alert      │
  │  (EC2/RDS/   │   │  (CloudWatch    │  │  Engine     │
  │   EBS/NAT)   │   │   CPU/Memory)   │  │             │
  └──────┬───────┘   └────────┬────────┘  └──────┬──────┘
         └───────────────────┬┘───────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
  ┌──────▼──────┐   ┌────────▼────────┐  ┌──────▼──────┐
  │  Grafana    │   │  HTML / JSON    │  │  Slack &    │
  │  Dashboards │   │  Reports        │  │  Email      │
  └─────────────┘   └─────────────────┘  └─────────────┘
```

---

## ⚡ Quick Start (< 5 minutes)

### Prerequisites
```bash
python >= 3.11
aws configure   # AWS CLI with Cost Explorer + EC2 + CloudWatch access
```

### Install
```bash
git clone https://github.com/betelabs/finops-cloud-cost-optimizer.git
cd finops-cloud-cost-optimizer
pip install -r requirements.txt
cp config/config.example.yaml config/config.yaml
# Edit config.yaml: add your AWS account ID, budget, Slack webhook
```

### Run your first scan
```bash
python -m cli.main scan --cloud aws --days 30
```

### Sample output
```
────────────────────────────────────────────────────
  finops-cloud-cost-optimizer v1.0.0
  Cloud: AWS | Look-back: 30 days
────────────────────────────────────────────────────

💰 Total Spend:          $48,320.00
🚨 Identified Waste:     $11,240.00  (23.3%)
📅 Est. Annual Savings:  $134,880.00
🔎 Idle resources found: 47

Top Savings Opportunities:
  #1  i-0abc123def456789   terminate      $1,440.00/mo
  #2  db-prod-reporting    stop           $2,100.00/mo
  #3  vol-0123456789abcdef delete             $68.00/mo
  #4  i-0def987654321abc   rightsize        $120.00/mo
  #5  snap-0a1b2c3d4e5f6   delete             $27.00/mo
```

### Generate HTML report
```bash
python -m cli.main report --cloud aws --output reports/this-month.html
# Open reports/this-month.html in browser — shareable with finance/leadership
```

---

## 📁 Repository Structure

```
finops-cloud-cost-optimizer/
│
├── README.md
├── requirements.txt
├── requirements-dev.txt
│
├── config/
│   ├── config.example.yaml        # Copy to config.yaml and fill in values
│   └── thresholds.yaml            # Detection sensitivity per resource type
│
├── src/
│   ├── collectors/
│   │   ├── base_collector.py      # ResourceCost + IdleResource dataclasses; abstract base
│   │   ├── aws_collector.py       # AWS: Cost Explorer + Boto3 + CloudWatch (fully implemented)
│   │   ├── azure_collector.py     # Azure: Cost Mgmt SDK stub (ready to extend)
│   │   └── gcp_collector.py       # GCP: Billing API stub (ready to extend)
│   │
│   ├── analyzers/
│   │   ├── idle_detector.py       # Aggregate idle resources; rank by waste; produce summary
│   │   ├── rightsizing.py         # EC2 rightsizing via CloudWatch CPU/memory data
│   │   └── storage_analyzer.py    # Stale EBS snapshots; S3 buckets without lifecycle
│   │
│   ├── recommenders/
│   │   ├── savings_plan.py        # RI / Savings Plan ROI calculator
│   │   └── s3_recommender.py      # S3 lifecycle rule suggestions
│   │
│   ├── reporters/
│   │   ├── html_reporter.py       # Styled HTML report with KPI cards + offenders table
│   │   ├── json_reporter.py       # Machine-readable JSON output
│   │   └── pdf_reporter.py        # PDF wrapper via weasyprint
│   │
│   └── alerts/
│       ├── slack_notifier.py      # Slack Block Kit alert + budget notifications
│       └── email_notifier.py      # SMTP / SES email alerts
│
├── cli/
│   └── main.py                    # Click CLI: scan | report | alerts
│
├── lambda/
│   ├── cost_scanner/
│   │   └── handler.py             # Lambda handler — weekly automated scan
│   └── budget_enforcer/
│       └── handler.py             # Lambda — triggered by AWS Budgets SNS notification
│
├── terraform/
│   ├── aws/
│   │   ├── main.tf                # Lambda, EventBridge schedule, AWS Budgets, SNS, S3
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── azure/
│   │   └── main.tf                # Azure Budget + Action Group
│   └── gcp/
│       └── main.tf                # GCP Budget + Pub/Sub
│
├── dashboards/
│   └── grafana/                   # Pre-built Grafana dashboard JSON files
│       ├── cost-overview.json
│       ├── idle-resources.json
│       ├── team-chargeback.json
│       └── savings-tracker.json
│
├── case-studies/                  # Documented real-world savings with methodology
│   ├── tricog-health-25pct-savings.md       # $12,100/mo saved in 90 days
│   ├── marvin-inc-startup-cost-control.md   # $5,190/mo saved, startup FinOps from scratch
│   ├── coredge-multicloud-governance.md     # $20,800/mo across AWS+Azure+GCP
│   └── rapidcanvas-mlops-cost.md            # 28% reduction on ML GPU workloads
│
├── reports/
│   └── examples/                  # Pre-generated sample report (open in browser)
│
├── tests/
│   ├── unit/
│   │   ├── test_idle_detector.py  # 5 unit tests — summarise, sorting, edge cases
│   │   ├── test_savings_plan.py   # RI ROI calculator tests
│   │   └── test_html_reporter.py  # HTML report generation tests
│   └── integration/
│       └── test_aws_collector_mock.py  # Mocked boto3 integration tests
│
├── docs/
│   ├── getting-started.md
│   ├── aws-setup.md               # IAM permissions required
│   └── grafana-setup.md
│
├── scripts/
│   ├── setup-grafana.sh           # Import dashboards into Grafana
│   └── weekly-report-cron.sh      # Cron wrapper for self-hosted
│
└── .github/
    └── workflows/
        ├── ci.yaml                # Lint + test on every PR (Python 3.11 + 3.12)
        ├── weekly-scan.yaml       # Scheduled Monday 09:00 UTC scan → artifact
        └── terraform-plan.yaml    # Auto-comment Terraform plan on PRs
```

---

## 🔧 Configuration

```yaml
# config/config.yaml (copy from config.example.yaml)

aws:
  regions: [us-east-1, ap-south-1, eu-west-1]
  account_id: "123456789012"

thresholds:
  idle_cpu_percent: 5       # EC2 flagged if avg CPU < 5% over 14 days
  idle_cpu_days: 14
  unattached_ebs_days: 3    # EBS volumes detached > 3 days
  stale_snapshot_days: 90

budget_alerts:
  monthly_budget_usd: 50000
  alert_at_percent: [50, 80, 95, 100]
  slack_webhook: "https://hooks.slack.com/services/..."
  alert_email: ops@yourcompany.com
```

---

## 📈 Grafana Dashboards

Import 4 pre-built dashboards in one command:
```bash
./scripts/setup-grafana.sh --grafana-url http://localhost:3000
```

| Dashboard | What It Shows |
|---|---|
| Cost Overview | Multi-cloud spend, 90-day trend, top services |
| Idle Resources | Live idle EC2/RDS/EBS tracker with monthly waste |
| Team Chargeback | Spend attributed to each `team` tag |
| Savings Tracker | Cumulative $ saved since optimization started |

---

## ⚙️ Automated Weekly Scan (Lambda + EventBridge)

Deploy the Terraform module for zero-touch weekly automation:

```bash
cd terraform/aws
terraform init
terraform apply -var="account_id=123456789012" \
                -var="alert_email=ops@yourcompany.com" \
                -var="monthly_budget_usd=50000"
```

This provisions:
- **Lambda** — runs full scan every Monday 09:00 UTC
- **AWS Budgets** — alerts at 50 / 80 / 95 / 100% of monthly budget
- **SNS + email** — instant notification when thresholds crossed
- **S3** — report archive, 90-day retention

Manual trigger any time:
```bash
aws lambda invoke --function-name finops-optimizer-cost-scanner output.json
```

---

## 🧪 Running Tests

```bash
pip install -r requirements-dev.txt
pytest tests/unit/ -v --cov=src --cov-report=term-missing
```

```
tests/unit/test_idle_detector.py      ✅ 5 passed
tests/unit/test_savings_plan.py       ✅ 4 passed
tests/unit/test_html_reporter.py      ✅ 2 passed
tests/integration/test_aws_*.py       ✅ 2 passed
```

---

## 📋 Case Studies

Real results from real deployments — not synthetic benchmarks:

| Write-up | Summary |
|---|---|
| [Tricog Health — 25% in 90 days](case-studies/tricog-health-25pct-savings.md) | Healthcare SaaS, full methodology, $145K annual savings |
| [Marvin — Startup](case-studies/marvin-inc-startup-cost-control.md) | Series A startup, dev-env scheduling, ML guardrails |
| [Coredge — Multi-cloud Governance](case-studies/coredge-multicloud-governance.md) | 3-cloud unified view, client chargeback, $250K/yr |
| [RapidCanvas — ML Cost Optimisation](case-studies/rapidcanvas-mlops-cost.md) | GPU spot instances, auto-terminate, 28% reduction |

---

## 🤝 Contributing

PRs welcome. High-value contributions:
- Azure and GCP collector implementations
- Additional Grafana dashboards (export as JSON + PR)
- New idle detection heuristics
- Test coverage improvements

---
## 👤 Author

<p align="left">
  <a href="https://github.com/betelabs" target="_blank">
    <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white"/>
  </a>

  <a href="https://linkedin.com/in/ashwani547" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-Ashwani%20Kumar-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white"/>
  </a>

  <a href="mailto:hello@betelabs.com">
    <img src="https://img.shields.io/badge/Email-Contact-D14836?style=for-the-badge&logo=gmail&logoColor=white"/>
  </a>
</p>

### Ashwani Kumar
Head of DevOps • Kubernetes Engineer • Cloud Native Enthusiast

---

<div align="center">
  <sub>
    ⭐ If this project helped you cut your cloud cost, consider starring the repository to support the project.
  </sub>
</div>
