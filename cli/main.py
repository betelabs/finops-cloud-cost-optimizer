#!/usr/bin/env python3
"""finops-cloud-cost-optimizer — CLI entrypoint."""
from __future__ import annotations
import sys, json, yaml, click
from datetime import datetime, timedelta
from pathlib import Path


def _load_config(path: str) -> dict:
    with open(path) as fh:
        return yaml.safe_load(fh)


@click.group()
@click.version_option("1.0.0")
def cli():
    """💰 finops-cloud-cost-optimizer — Detect cloud waste, slash bills."""


@cli.command()
@click.option("--cloud",   default="aws",  type=click.Choice(["aws","azure","gcp"]))
@click.option("--days",    default=30,     help="Look-back period in days")
@click.option("--config",  default="config/config.yaml", show_default=True)
@click.option("--output",  default="",     help="Optional JSON output path")
def scan(cloud: str, days: int, config: str, output: str):
    """Scan for idle resources and estimate waste."""
    cfg = _load_config(config)
    click.echo(f"\n{'─'*52}")
    click.echo(f"  finops-cloud-cost-optimizer v1.0.0")
    click.echo(f"  Cloud: {cloud.upper()} | Look-back: {days} days")
    click.echo(f"{'─'*52}")

    if cloud == "aws":
        from src.collectors.aws_collector import AWSCollector
        collector = AWSCollector(cfg.get("aws", {}))
    else:
        click.echo(f"⚠  {cloud} collector not yet implemented — PRs welcome!", err=True)
        sys.exit(1)

    from src.analyzers.idle_detector import IdleResourceDetector

    end, start = datetime.utcnow(), datetime.utcnow() - timedelta(days=days)
    total   = collector.get_total_spend(start, end)
    idle    = collector.get_idle_resources()
    summary = IdleResourceDetector(cfg).summarise(idle)
    summary["total_spend_usd"] = total
    summary["period"]          = f"last {days} days"

    click.echo(f"\n💰 Total Spend:          ${total:>12,.2f}")
    click.echo(f"🚨 Identified Waste:     ${summary['total_monthly_waste_usd']:>12,.2f}"
               f"  ({summary['total_monthly_waste_usd']/max(total,1)*100:.1f}%)")
    click.echo(f"📅 Est. Annual Savings:  ${summary['total_annual_waste_usd']:>12,.2f}")
    click.echo(f"🔎 Idle resources found: {summary['total_idle_resources']}")
    click.echo()
    click.echo("Top Savings Opportunities:")
    for i, item in enumerate(summary["top_offenders"][:5], 1):
        click.echo(f"  #{i}  {item['id']:<36} {item['action']:<12} ${item['waste_usd']:>8,.2f}/mo")

    if output:
        from src.reporters.json_reporter import JSONReporter
        JSONReporter().generate(summary, output)
        click.echo(f"\n✅ JSON saved: {output}")


@cli.command()
@click.option("--cloud",   default="aws")
@click.option("--days",    default=30)
@click.option("--output",  default="reports/cost-report.html", show_default=True)
@click.option("--format",  "fmt", default="html", type=click.Choice(["html","json"]))
@click.option("--config",  default="config/config.yaml")
def report(cloud: str, days: int, output: str, fmt: str, config: str):
    """Generate a full cost savings report (HTML or JSON)."""
    cfg = _load_config(config)
    Path(output).parent.mkdir(parents=True, exist_ok=True)

    if cloud == "aws":
        from src.collectors.aws_collector import AWSCollector
        collector = AWSCollector(cfg.get("aws", {}))
    else:
        click.echo(f"⚠  {cloud} not yet supported", err=True); sys.exit(1)

    from src.analyzers.idle_detector import IdleResourceDetector

    end, start = datetime.utcnow(), datetime.utcnow() - timedelta(days=days)
    total   = collector.get_total_spend(start, end)
    idle    = collector.get_idle_resources()
    summary = IdleResourceDetector(cfg).summarise(idle)
    summary.update({
        "total_spend_usd": total,
        "account":         cfg.get("aws", {}).get("account_id", "N/A"),
        "period":          f"last {days} days",
    })

    if fmt == "html":
        from src.reporters.html_reporter import HTMLReporter
        HTMLReporter().generate(summary, output)
    else:
        from src.reporters.json_reporter import JSONReporter
        JSONReporter().generate(summary, output)

    click.echo(f"✅ Report saved: {output}")


@cli.command()
@click.option("--cloud",     default="aws")
@click.option("--threshold", default=80, help="Alert at this % of monthly budget")
@click.option("--config",    default="config/config.yaml")
def alerts(cloud: str, threshold: int, config: str):
    """Show budget alert configuration."""
    cfg = _load_config(config)
    budget = cfg.get("budget_alerts", {}).get("monthly_budget_usd", "N/A")
    click.echo(f"\n⚙  Budget: ${budget:,} | Alert thresholds: 50%, 80%, 95%, 100%")
    click.echo("   To deploy alerts automatically:\n   cd terraform/aws && terraform apply")


if __name__ == "__main__":
    cli()
