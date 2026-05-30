# Case Study: Healthcare SaaS — 25% Cloud Cost Reduction in 90 Days

**Baseline:** $48,000/month AWS + Azure | **Team:** 40 engineers | **Timeframe:** 90 days

## Month 1 — Visibility
- Enforced tagging policy (`team`, `env`, `service`) across all resources
- 100% of spend attributed within 2 weeks

## Month 2 — Idle Resource Cleanup
| Action | Saving/mo |
|---|---|
| Terminated 12 idle EC2 (<1% CPU 14d) | $1,440 |
| Rightsized 8 RDS (r5.2xl → r5.lg) | $2,100 |
| Deleted 340 unattached EBS volumes | $680 |
| Removed 3 idle NAT Gateways | $324 |

## Month 3 — Commitment-Based Savings
| Action | Saving/mo |
|---|---|
| 60% EC2 → 1-year Reserved Instances | $3,200 |
| S3 Intelligent-Tiering on cold data | $920 |

## Result: $8,340/month saved = $100K/year (25% reduction)
