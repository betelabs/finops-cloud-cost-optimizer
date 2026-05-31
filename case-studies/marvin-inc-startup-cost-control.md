# Case Study: Marvin Inc — Startup Cost Control from Day 1

**Company:** Marvin Inc (AI-powered home improvement platform, Series A startup)  
**Cloud:** AWS  
**Team size:** 18 engineers (small, fast-moving)  
**Baseline monthly spend:** $22,000/month  
**Stage:** Post-product-market fit, scaling phase  
**Timeframe:** Dec 2024 – Mar 2025

---

## The Problem

Marvin was 6 months post-Series A. The team was shipping fast — 3–4 deploys a day —
and cloud spend was growing 12% month-over-month. The founding team wanted FinOps
discipline from the start, not a firefighting exercise 18 months later.

Key concerns:
- No cost attribution per feature team (ML, backend, infra)
- Dev/staging environments running 24/7 at near-prod spec
- ML training jobs left running after experiments completed
- No budget alerts — costs discovered only on monthly invoice

---

## What We Built

Using this tool's framework, we implemented a lightweight FinOps system in 2 sprints:

### Sprint 1: Tagging + Alerting
- Enforced `team`, `env`, `project` tags via OPA/SCPs — PRs blocked if resources
  are created without mandatory tags
- AWS Budgets configured at 50%, 80%, 95%, 100% with Slack alerts
- GitHub Actions weekly scan added to CI/CD pipeline (zero extra infra)

### Sprint 2: Environment Scheduling + Rightsizing
- Lambda-based auto-scheduler: dev/staging EC2 and RDS **stopped at 7pm, started at 8am**
  (weekdays only) via EventBridge
- ML training EC2 (p3.2xlarge) tagged with `auto-terminate=true` —
  Lambda terminates instances idle > 2 hours
- EBS volume audit: found 120 volumes unattached > 3 days ($480/mo waste)

---

## Results by Month

### Month 1 (Dec 2024)
- Tagging + budget alerts live
- Discovered $3,200/mo untagged spend — attributed to ML team experiments
- EBS cleanup: $480 saved
- **Month saving: $480**

### Month 2 (Jan 2025)
- Dev/staging schedule active: 16 on-demand EC2 off 13h/day, weekends off
- Saving: 13h × 2/24 = ~54% uptime → ~$1,850/mo EC2 reduction
- ML auto-terminate: 6 runaway training jobs caught → $1,100/mo saved
- **Month saving: $2,950**

### Month 3 (Feb 2025)
- Rightsized 4 over-provisioned RDS (db.r5.xlarge → db.r5.large) → $700/mo
- 3 m5.2xlarge API servers (avg 8% CPU) → m5.xlarge → $420/mo
- Spot Instances for batch jobs (image processing pipeline) → $640/mo
- **Month saving: $1,760**

---

## 90-Day Summary

| Metric | Before | After |
|---|---|---|
| Monthly spend | $22,000 | $16,810 |
| Cost attribution | 0% | 100% by team |
| Budget surprises | Monthly | Never |
| ML runaway jobs | 6+ undetected/month | Auto-terminated |
| Dev env waste | $1,850/mo | ~$0 (scheduled) |

**Total: $5,190/month saved = $62,280/year (23.6% reduction)**

---

## Lessons for Startups

1. **Start tagging on day 1.** Retrofitting tags across 200+ resources is painful.
2. **Auto-schedule non-prod environments.** Dev/staging don't need to run nights and weekends.
3. **Alert before the invoice.** Set budgets at 80%, not 100%.
4. **ML teams need guardrails.** Training jobs left running are the fastest way to spike a bill.
5. **Weekly scans > monthly reviews.** Catch waste in days, not after the invoice.

---

*Implemented by Ashwani Kumar, Head of DevOps, Marvin Inc, Dec 2024 – Mar 2025*
