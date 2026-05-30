<div align="center">

# 💰 finops-cloud-cost-optimizer

**Automated cloud cost governance — idle resource detection, rightsizing, budget alerts & savings dashboards**  
*Built by [Ashwani Kumar](https://linkedin.com/in/ashwani547) · Head of DevOps · 12+ Years Cloud Experience*

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://python.org)
[![AWS](https://img.shields.io/badge/AWS-Cost%20Explorer-FF9900?logo=amazon-aws&logoColor=white)](https://aws.amazon.com)
[![Azure](https://img.shields.io/badge/Azure-Cost%20Mgmt-0078D4?logo=microsoft-azure&logoColor=white)](https://azure.microsoft.com)
[![GCP](https://img.shields.io/badge/GCP-Billing%20API-4285F4?logo=google-cloud&logoColor=white)](https://cloud.google.com)
[![Grafana](https://img.shields.io/badge/Grafana-Dashboards-F46800?logo=grafana&logoColor=white)](https://grafana.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 🎯 The Problem This Solves

Cloud bills grow silently. Engineering teams ship fast and forget to clean up. Finance teams see the invoice but can't attribute it. The result: **30–40% of cloud spend is wasted** across most organizations.

This tool gives you:
- **Visibility** — who is spending what, on what, in which cloud
- **Detection** — idle resources, oversized instances, forgotten snapshots
- **Action** — automated rightsizing recommendations + one-click Terraform fixes
- **Governance** — budget alerts before the bill arrives, not after

---

## 📊 Real-World Results

> This architecture is based on implementations that delivered measurable savings:

| Metric | Before | After | Improvement |
|---|---|---|---|
| Monthly cloud spend visibility | 0% attributed | 100% by team/service | Full chargeback |
| Idle EC2 instances | ~30 undetected | Auto-flagged in 24h | Eliminated |
| RDS rightsizing | Manual quarterly | Weekly automated scan | 18% DB cost reduction |
| Budget overrun incidents | Discovered on invoice | Alert at 80% threshold | Zero surprises |
| **Total cloud cost reduction** | Baseline | **–25% in 90 days** | **25%+ savings** |

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                      Data Collection Layer                    │
│                                                              │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐   │
│  │  AWS Cost     │  │  Azure Cost   │  │  GCP Billing  │   │
│  │  Explorer API │  │  Mgmt API     │  │  API          │   │
│  └───────┬───────┘  └───────┬───────┘  └───────┬───────┘   │
└──────────┼──────────────────┼──────────────────┼────────────┘
           └──────────────────▼──────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │  Unified Cost      │
                    │  Data Model (JSON) │
                    └─────────┬─────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
   ┌──────▼──────┐   ┌────────▼────────┐  ┌──────▼──────┐
   │  Idle       │   │  Rightsizing    │  │  Budget     │
   │  Detector   │   │  Recommender    │  │  Alert      │
   └──────┬──────┘   └────────┬────────┘  └──────┬──────┘
          └───────────────────▼───────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
   ┌──────▼──────┐   ┌────────▼────────┐  ┌──────▼──────┐
   │  Grafana    │   │  CLI Report     │  │  Slack /    │
   │  Dashboards │   │  (HTML / JSON)  │  │  Email      │
   └─────────────┘   └─────────────────┘  └─────────────┘
```

---

## ⚡ Quick Start

```bash
git clone https://github.com/ashwani547/finops-cloud-cost-optimizer.git
cd finops-cloud-cost-optimizer
pip install -r requirements.txt
cp config/config.example.yaml config/config.yaml
# Fill in your credentials in config.yaml

# Scan for waste (30 seconds)
python -m cli.main scan --cloud aws --days 30

# Generate full HTML report
python -m cli.main report --cloud aws --output reports/this-month.html

# Set up budget alerts
python -m cli.main alerts --cloud aws --threshold 80
```

### Sample CLI Output
```
finops-cloud-cost-optimizer v1.0.0
Scanning AWS | Period: last 30 days
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 Total Spend          $48,320
🚨 Identified Waste     $11,240 (23.3%)
📅 Annual Savings Est.  $134,880

Top Savings Opportunities:
  #1  12x idle EC2 (t3.xl, <1% CPU 14d)   → terminate   $1,440/mo
  #2  8x oversized RDS (r5.2xl → r5.lg)   → rightsize   $2,100/mo
  #3  340 unattached EBS volumes           → delete        $680/mo
  #4  S3 storage class optimization        → lifecycle     $920/mo
  #5  3x NAT Gateway (no traffic 7d)       → remove        $324/mo

Report saved: reports/this-month.html
```

---

## 📁 Repository Structure

```
finops-cloud-cost-optimizer/
│
├── README.md
├── requirements.txt
│
├── config/
│   ├── config.example.yaml            # Template — copy to config.yaml
│   └── thresholds.yaml                # Idle/waste detection thresholds
│
├── src/
│   ├── collectors/
│   │   ├── base_collector.py          # Abstract base class (ResourceCost, IdleResource)
│   │   ├── aws_collector.py           # AWS Cost Explorer + Boto3 + CloudWatch
│   │   ├── azure_collector.py         # Azure Cost Management SDK
│   │   └── gcp_collector.py           # GCP Billing API
│   │
│   ├── analyzers/
│   │   ├── idle_detector.py           # CPU / network / disk idle analysis
│   │   ├── rightsizing.py             # Instance sizing recommendations
│   │   ├── storage_analyzer.py        # Unattached EBS, stale snapshots
│   │   └── network_analyzer.py        # Idle NAT GW, unused Elastic IPs
│   │
│   ├── recommenders/
│   │   ├── ec2_recommender.py         # Terminate / rightsize EC2
│   │   ├── rds_recommender.py         # Rightsize RDS / recommend RIs
│   │   ├── s3_recommender.py          # Lifecycle rules + storage class
│   │   └── savings_plan.py            # Savings Plan vs RI calculator
│   │
│   ├── reporters/
│   │   ├── html_reporter.py           # Styled HTML cost savings report
│   │   ├── pdf_reporter.py            # PDF for finance / leadership
│   │   └── json_reporter.py           # Machine-readable output
│   │
│   └── alerts/
│       ├── budget_alert.py            # Threshold-based budget alerts
│       ├── slack_notifier.py          # Slack webhook integration
│       └── email_notifier.py          # SES / SMTP email alerts
│
├── cli/
│   └── main.py                        # Click-based CLI entrypoint
│
├── lambda/
│   ├── cost_scanner/
│   │   └── handler.py                 # Lambda — weekly automated scan
│   └── budget_enforcer/
│       └── handler.py                 # Lambda — triggered by AWS Budget alert
│
├── terraform/
│   ├── aws/
│   │   ├── main.tf                    # Lambda, EventBridge, AWS Budgets, SNS, S3
│   │   └── variables.tf
│   ├── azure/
│   │   └── main.tf                    # Azure Budget + Action Group
│   └── gcp/
│       └── main.tf                    # GCP Budget alert + Pub/Sub
│
├── dashboards/
│   ├── grafana/
│   │   ├── cost-overview.json         # Multi-cloud cost overview dashboard
│   │   ├── idle-resources.json        # Live idle resource tracker
│   │   ├── team-chargeback.json       # Per-team cost attribution
│   │   └── savings-tracker.json       # Cumulative savings over time
│   └── screenshots/
│       ├── cost-overview.png
│       └── savings-tracker.png
│
├── case-studies/
│   ├── tricog-health-25pct-savings.md # Real case: 25% savings in 90 days
│   └── startup-idle-cleanup.md        # Real case: $1,400/mo eliminated
│
├── reports/examples/
│   └── sample-report.html             # Pre-generated sample output (open in browser)
│
├── tests/
│   ├── unit/
│   │   ├── test_idle_detector.py
│   │   ├── test_rightsizing.py
│   │   └── test_reporters.py
│   └── integration/
│       └── test_aws_collector.py
│
├── scripts/
│   ├── setup-grafana.sh               # Import dashboards into Grafana
│   └── weekly-report-cron.sh          # Cron wrapper for self-hosted setups
│
├── docs/
│   ├── getting-started.md
│   ├── configuration.md
│   ├── aws-setup.md                   # IAM permissions required
│   └── grafana-setup.md
│
└── .github/
    └── workflows/
        ├── ci.yaml                    # Lint + test on every PR
        └── weekly-scan.yaml           # Scheduled weekly cost scan → artifact
```

---

## 🔧 Configuration

```yaml
# config/config.yaml

aws:
  regions: [us-east-1, ap-south-1, eu-west-1]
  account_id: "123456789012"

thresholds:
  idle_cpu_percent: 5          # Flag EC2 with avg CPU < 5% over 14 days
  idle_cpu_days: 14
  unattached_ebs_days: 3       # Flag EBS volumes detached > 3 days
  stale_snapshot_days: 90

budget_alerts:
  monthly_budget_usd: 50000
  alert_at_percent: [50, 80, 95, 100]
  slack_webhook: "https://hooks.slack.com/services/..."
  alert_email: ops@yourcompany.com
```

---

## 📈 Grafana Dashboards

Four pre-built dashboards included — import in one command:

```bash
./scripts/setup-grafana.sh --grafana-url http://localhost:3000
```

| Dashboard | What It Shows |
|---|---|
| **Cost Overview** | Multi-cloud spend, 90-day trend |
| **Idle Resources** | Live idle EC2/RDS tracker with waste estimate |
| **Team Chargeback** | Cost by `team` tag — full accountability |
| **Savings Tracker** | Cumulative $ saved since optimization began |

---

## ⚙️ Automated Weekly Scan (Lambda + EventBridge)

```bash
cd terraform/aws
terraform init && terraform apply
# Lambda fires every Monday 09:00 UTC
# Budget alerts trigger at 50 / 80 / 95 / 100% of monthly budget
# Reports stored in S3 for 90 days
```

---

## 📋 Case Studies

See [`case-studies/`](case-studies/) for documented real-world results:

- **[Tricog Health — 25% reduction in 90 days](case-studies/tricog-health-25pct-savings.md)**  
  $48K/month → $35.9K/month across AWS + Azure

---

## 🤝 Contributing

PRs welcome for: Azure / GCP recommenders, Grafana dashboard improvements,
new idle detection heuristics, test coverage.

---

## 👤 Author

**Ashwani Kumar** · Head of DevOps · CKA Certified  
📧 ashwani.kumar.career@gmail.com · 🔗 [linkedin.com/in/ashwani547](https://linkedin.com/in/ashwani547)

<div align="center"><sub>⭐ Star this repo if it helped you cut cloud costs</sub></div>
