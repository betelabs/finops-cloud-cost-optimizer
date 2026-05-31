# Case Study: Coredge Inc — Multi-Cloud FinOps Governance at Scale

**Company:** Coredge Inc (Enterprise cloud-native infrastructure, Bangalore)  
**Cloud:** AWS + Azure + GCP (all three simultaneously)  
**Team size:** 80+ engineers across 6 product squads  
**Baseline monthly spend:** $95,000/month across 3 clouds  
**Industry:** Cloud infrastructure / platform engineering  
**Timeframe:** Sep 2025 – ongoing

---

## The Problem

Coredge operated workloads across AWS, Azure, and GCP for different clients.
With 6 squads and 3 clouds, cost visibility was near-zero:
- Each cloud had a separate billing dashboard with no unified view
- Chargeback to clients was manual, monthly, and error-prone
- No governance: one team accidentally left 40 vCPUs running in Azure for 3 weeks
- Cloud cost was the #2 topic in every board meeting

---

## Solution Architecture

We extended this tool to collect from all 3 clouds into a unified data model,
then built dashboards that showed:
- **Per-cloud spend** side by side (AWS vs Azure vs GCP)
- **Per-client chargeback** — costs attributed to client project tags
- **Anomaly detection** — spend > 20% above 7-day rolling average triggers a Slack alert

### Multi-Cloud Collection Pipeline

```
AWS Cost Explorer ─┐
Azure Cost Mgmt   ─┼─→ Unified Cost Model ─→ Grafana Dashboards
GCP Billing API   ─┘         │
                              └─→ Weekly PDF report → Finance team
```

---

## Key Findings (First 30 Days)

| Finding | Cloud | Monthly Waste |
|---|---|---|
| 8 idle VMs (avg 2% CPU, 21 days) | Azure | $2,240 |
| 15 idle EC2 instances | AWS | $1,800 |
| 60TB cold data in hot storage class | GCP Cloud Storage | $3,600 |
| Orphaned load balancers (no targets) | AWS | $540 |
| Premium SSD attached to stopped VMs | Azure | $380 |
| Idle GKE node pools (0 pods, 5 days) | GCP | $920 |
| **Total identified waste** | | **$9,480/month** |

---

## Governance Framework Implemented

### 1. Mandatory Tagging Policy (enforced via IaC)
```yaml
required_tags:
  - client       # client project this resource belongs to
  - team         # squad owning the resource
  - environment  # prod | staging | dev
  - cost_center  # finance charge code
```

Resources failing tagging validation are **blocked at deploy time** (OPA policy).

### 2. Budget Guardrails Per Client
Each client project gets an AWS/Azure/GCP budget. At 80%:
- Slack alert to the squad lead
- Ticket auto-created in Jira
- Report emailed to account manager

At 100%: escalation to CTO.

### 3. Weekly Finance Report
Automated PDF emailed to finance every Monday:
- Total spend by cloud
- Total spend by client (chargeback ready)
- Top 5 anomalies
- Savings realised this month

---

## Results (First Quarter)

| Metric | Before | After |
|---|---|---|
| Monthly multi-cloud spend | $95,000 | $74,200 |
| Cost attribution | ~30% | 100% |
| Client chargeback accuracy | Manual ±15% | Automated ±2% |
| Budget surprises | Bi-monthly | Zero |
| Anomaly detection | None | < 24h detection |

**Total: $20,800/month saved = $249,600/year (21.9% reduction)**

---

## What Made the Difference

The unified data model was the key unlock. Once all 3 clouds' spend was in the same
schema, building cross-cloud dashboards and alerts was straightforward. Previously,
engineers were switching between 3 different billing UIs and reconciling numbers in
spreadsheets. Now it's one Grafana dashboard, one weekly report, one source of truth.

---

*Implemented by Ashwani Kumar, Head of DevOps, Coredge Inc, Sep 2025 – present*
