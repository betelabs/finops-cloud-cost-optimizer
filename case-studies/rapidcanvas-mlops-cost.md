# Case Study: RapidCanvas — ML Workload Cost Optimisation

**Company:** RapidCanvas (AI/ML platform for AutoML, Series A)  
**Cloud:** AWS (EKS) + GCP (Vertex AI)  
**Team size:** 25 engineers  
**Baseline monthly spend:** $38,000/month (60% compute, mostly GPU)  
**Industry:** AI/ML SaaS  
**Timeframe:** Oct 2022 – Apr 2023

---

## The Problem

RapidCanvas's cost structure was dominated by compute for ML training and inference.
GPU instances (p3, g4dn) are expensive — but the real problem was **utilisation**:
- GPU instances were being allocated per-experiment, not shared
- Training jobs often ran hours past completion before being noticed
- No visibility into which experiments / customers drove GPU spend
- EKS cluster autoscaler was too aggressive — nodes stayed up 45 min after scale-down

---

## ML-Specific Optimisations

### 1. GPU Instance Right-Scheduling
- Moved batch training from on-demand p3.2xlarge → Spot g4dn.xlarge (66% cheaper for interruptible jobs)
- Added checkpoint logic so interrupted Spot jobs resumed from last checkpoint
- Saving: **$4,800/month**

### 2. Auto-Terminate Idle Training Jobs
- Lambda monitors SageMaker / EC2 GPU instances
- If GPU utilisation < 5% for > 30 minutes, instance is tagged `auto-terminate-candidate`
- Slack alert sent to job owner; auto-terminated after 1 hour with no response
- Saving: **$2,100/month** (eliminated runaway jobs)

### 3. Cluster Autoscaler Tuning
```yaml
# Before
scale-down-delay-after-add: 10m
scale-down-unneeded-time:   10m

# After — nodes retire faster after traffic drops
scale-down-delay-after-add: 3m
scale-down-unneeded-time:   3m
scale-down-utilization-threshold: 0.4
```
Saving: **$1,200/month**

### 4. Inference Endpoint Rightsizing
- 12 inference endpoints on ml.m5.xlarge → ml.m5.large (avg 12% CPU utilisation)
- Saving: **$840/month**

### 5. S3 Model Artifact Cleanup
- 18 months of experiment artifacts in S3 STANDARD (4.2TB)
- Lifecycle policy: models older than 30 days → GLACIER_IR
- Saving: **$630/month**

---

## Results

| Metric | Before | After |
|---|---|---|
| Monthly spend | $38,000 | $27,430 |
| GPU utilisation rate | ~35% | ~72% |
| Runaway training jobs | 8–12/month | 0 (auto-terminated) |
| Cost per experiment | Unknown | Tracked per-customer |

**Total: $10,570/month saved = $126,840/year (27.8% reduction)**

---

*Implemented by Ashwani Kumar, Principal DevOps Engineer, RapidCanvas, Oct 2022 – Apr 2023*
