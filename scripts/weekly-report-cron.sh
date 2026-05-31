#!/usr/bin/env bash
# Cron wrapper — add to crontab: 0 9 * * MON /path/to/scripts/weekly-report-cron.sh
set -euo pipefail
cd "$(dirname "$0")/.."
REPORT="reports/weekly-$(date +%Y-%m-%d).html"
python -m cli.main scan  --cloud aws --days 7 --output "${REPORT%.html}.json"
python -m cli.main report --cloud aws --days 7 --output "$REPORT"
echo "Report: $REPORT"
