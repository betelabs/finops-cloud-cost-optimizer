# Case Study: Tricog Health — 25% Cloud Cost Reduction in 90 Days

**Company:** Tricog Health India Pvt. Ltd. (AI-powered cardiac diagnostics SaaS)  
**Cloud:** AWS (primary) + Azure  
**Team size:** 40 engineers across product, data, and platform  
**Baseline monthly spend:** ₹40L (~$48,000 USD/month)  
**Industry:** Healthcare — HIPAA-adjacent, uptime-critical  
**Timeframe:** Jan 2024 – Mar 2024

---

## The Problem

Tricog's cloud bill had grown 35% YoY with no clear attribution. Finance flagged a ₹6L/month
spike in Q4 2023. The engineering team had no idea which service or team was responsible.
Healthcare workloads ran 24/7 with strict uptime SLAs, making blind cost cuts risky.

---

## Month 1 — Visibility: You Can't Optimise What You Can't See

**Action:** Deployed this tool's collectors across all AWS regions. Enforced mandatory tagging:
`team`, `env` (prod/staging/dev), `service`, and `data-classification`.

**Findings:**
- 45% of compute spend was **untagged** — impossible to attribute before tagging policy
- 3 staging environments running 24/7 identical to prod (no auto-shutdown)
- $4,200/mo in data transfer costs caused by mis-routed cross-AZ traffic

**Result:** 100% of spend attributed within 10 days.

---

## Month 2 — Idle Resource Cleanup

The scanner identified the following within the first automated run:

| Resource | Count | Finding | Action | Monthly Saving |
|---|---|---|---|---|
| EC2 (t3.xlarge) | 12 | Avg CPU < 1% for 14 days | Terminated | $1,440 |
| RDS (db.r5.2xlarge) | 8 | < 2 avg connections for 7 days | Rightsized to db.r5.large | $2,100 |
| Unattached EBS volumes | 340 | Detached > 3 days | Deleted | $680 |
| NAT Gateways | 3 | < 1MB traffic for 7 days | Removed | $324 |
| Stale snapshots | 180 | Older than 90 days | Deleted | $270 |
| S3 (no lifecycle) | 14 buckets | 6TB cold data in STANDARD | Added lifecycle → GLACIER_IR | $920 |

**Month 2 total savings: $5,734/month**

---

## Month 3 — Commitment-Based Savings

With steady-state workloads now visible and right-sized, it was safe to commit:

| Action | Scope | Monthly Saving |
|---|---|---|
| 1-year Reserved Instances | 60% of prod EC2 fleet | $3,200 |
| Compute Savings Plan | Remaining on-demand | $800 |
| RDS Reserved | 4 prod databases | $640 |

**Month 3 total savings: $4,640/month**

---

## Cross-AZ Traffic Fix (Bonus)

Tracing revealed microservices calling across Availability Zones unnecessarily.
Pinning services to the same AZ in staging saved an additional **$840/month** in data transfer fees.

---

## 90-Day Summary

| Metric | Before | After |
|---|---|---|
| Monthly cloud spend | $48,000 | $35,900 |
| Cost attribution | 0% | 100% |
| Idle resources detected | Unknown | Auto-flagged weekly |
| Budget surprises | Monthly on invoice | Never (alerts at 80%) |
| MTTR for cost anomalies | Days | < 4 hours (Slack alert) |

**Total savings: $12,100/month = $145,200/year (25.2% reduction)**

> *"We went from having no idea where our cloud budget was going to having full team-level  
> chargeback and zero-surprise invoices. The ROI on building this tooling was immediate."*

---

*Implemented by Ashwani Kumar, Head of DevOps, Tricog Health India Pvt. Ltd., Jan–Mar 2024*
