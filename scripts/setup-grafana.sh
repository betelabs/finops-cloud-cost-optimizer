#!/usr/bin/env bash
# Import pre-built Grafana dashboards
# Usage: ./scripts/setup-grafana.sh --grafana-url http://localhost:3000

set -euo pipefail
GRAFANA_URL=${2:-http://localhost:3000}
API_KEY=${GRAFANA_API_KEY:-admin:admin}

echo "Importing FinOps dashboards to Grafana at $GRAFANA_URL"

for dash in dashboards/grafana/*.json; do
  echo "  → importing $dash"
  curl -sf -X POST "$GRAFANA_URL/api/dashboards/import" \
    -H "Content-Type: application/json" \
    -u "$API_KEY" \
    -d "{\"dashboard\": $(cat $dash), \"overwrite\": true}"
  echo
done

echo "Done! Open $GRAFANA_URL to view dashboards."
