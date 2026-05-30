#!/usr/bin/env python3
"""FinOps Cloud Cost Optimizer CLI."""

import click, yaml
from datetime import datetime, timedelta
from src.collectors.aws_collector import AWSCollector
from src.analyzers.idle_detector import IdleResourceDetector
from src.reporters.html_reporter import HTMLReporter

def load_config(path): 
    with open(path) as f: return yaml.safe_load(f)

@click.group()
@click.version_option("1.0.0")
def cli():
    """💰 finops-cloud-cost-optimizer — Detect waste, cut cloud bills."""

@cli.command()
@click.option("--cloud", default="aws", type=click.Choice(["aws","azure","gcp"]))
@click.option("--days", default=30)
@click.option("--config", default="config/config.yaml")
def scan(cloud, days, config):
    """Scan for idle resources and cost anomalies."""
    cfg = load_config(config)
    click.echo(f"\n🔍 Scanning {cloud.upper()} | Last {days} days\n" + "─"*48)
    collector = AWSCollector(cfg.get("aws", {}))
    end, start = datetime.utcnow(), datetime.utcnow() - timedelta(days=days)
    total   = collector.get_total_spend(start, end)
    idle    = collector.get_idle_resources()
    summary = IdleResourceDetector(cfg).summarise(idle)
    click.echo(f"💰 Total Spend:      ${total:>10,.2f}")
    click.echo(f"🚨 Identified Waste: ${summary['total_monthly_waste_usd']:>10,.2f}  ({summary['total_monthly_waste_usd']/total*100:.1f}%)")
    click.echo(f"📅 Annual Savings:   ${summary['total_annual_waste_usd']:>10,.2f}")
    for item in summary["top_offenders"][:5]:
        click.echo(f"  → {item['id']:30s} {item['action']:12s}  ${item['waste_usd']:>8,.2f}/mo")

@cli.command()
@click.option("--cloud", default="aws")
@click.option("--output", default="reports/cost-report.html")
@click.option("--config", default="config/config.yaml")
def report(cloud, output, config):
    """Generate a full HTML cost savings report."""
    cfg = load_config(config)
    collector = AWSCollector(cfg.get("aws", {}))
    end, start = datetime.utcnow(), datetime.utcnow() - timedelta(days=30)
    total   = collector.get_total_spend(start, end)
    idle    = collector.get_idle_resources()
    summary = IdleResourceDetector(cfg).summarise(idle)
    summary["total_spend_usd"] = total
    summary["waste_percent"]   = summary["total_monthly_waste_usd"] / total * 100
    path = HTMLReporter().generate(summary, output)
    click.echo(f"✅ Report saved to: {path}")

if __name__ == "__main__":
    cli()
