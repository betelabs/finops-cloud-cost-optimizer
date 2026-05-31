# Grafana Dashboard Setup

## Prerequisites
- Grafana >= 9.x running (local or Cloud)
- Prometheus scraping your Kubernetes cluster
- Kubecost deployed (for cost dashboards)

## Import dashboards

```bash
export GRAFANA_API_KEY="admin:yourpassword"
./scripts/setup-grafana.sh --grafana-url http://localhost:3000
```

## Available dashboards

| File | Description |
|---|---|
| `cost-overview.json`    | Multi-cloud spend, 90-day trend |
| `idle-resources.json`   | Live idle resource tracker |
| `team-chargeback.json`  | Cost by `team` tag |
| `savings-tracker.json`  | Cumulative savings since optimization |
