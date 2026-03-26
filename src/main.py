"""CLI entry point for TA Quarterly Report generator."""

import argparse
import json
import sys
from pathlib import Path

from src.config import ReportConfig


def cmd_prompt(args):
    """Generate a Hex prompt from a Salesforce opportunity CSV."""
    from src.hex_prompt import parse_csv, render_hex_prompt

    config = ReportConfig()
    if args.quarter:
        config.quarter = args.quarter
    if args.fy:
        config.fiscal_year = args.fy

    opportunities = parse_csv(args.csv)
    prompt = render_hex_prompt(opportunities, config)

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(prompt)
        print(f"Hex prompt written to {out}")
    else:
        print(prompt)


def cmd_build(args):
    """Build the PowerPoint deck from report data and insights JSON."""
    from src.data.models import ReportData, Insights
    from src.deck.builder import build_deck

    data_path = Path(args.data)
    if not data_path.exists():
        print(f"Error: Data file not found: {data_path}")
        sys.exit(1)

    insights_path = Path(args.insights)
    if not insights_path.exists():
        print(f"Error: Insights file not found: {insights_path}")
        sys.exit(1)

    with open(data_path) as f:
        data = ReportData.model_validate(json.load(f))

    with open(insights_path) as f:
        insights = Insights.model_validate(json.load(f))

    config = ReportConfig()
    if args.quarter:
        config.quarter = args.quarter

    output_path = build_deck(data, insights, config, args.output_dir)
    print(f"Deck generated: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="TA Quarterly Report Generator"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # -- prompt subcommand --
    p_prompt = subparsers.add_parser(
        "prompt", help="Generate a Hex prompt from a Salesforce opportunity CSV"
    )
    p_prompt.add_argument(
        "--csv", required=True, help="Path to opportunity CSV file"
    )
    p_prompt.add_argument(
        "--output", "-o", default=None, help="Write prompt to file (default: stdout)"
    )
    p_prompt.add_argument(
        "--quarter", default=None, help="Target fiscal quarter (e.g. Q3)"
    )
    p_prompt.add_argument(
        "--fy", default=None, help="Fiscal year (e.g. FY26)"
    )
    p_prompt.set_defaults(func=cmd_prompt)

    # -- build subcommand --
    p_build = subparsers.add_parser(
        "build", help="Build the PowerPoint deck from JSON data"
    )
    p_build.add_argument(
        "--data", default="output/report_data.json",
        help="Path to report_data.json (default: output/report_data.json)",
    )
    p_build.add_argument(
        "--insights", default="output/insights.json",
        help="Path to insights.json (default: output/insights.json)",
    )
    p_build.add_argument(
        "--output-dir", default="output",
        help="Output directory for the deck (default: output)",
    )
    p_build.add_argument(
        "--quarter", default=None, help="Override fiscal quarter (e.g. Q3)"
    )
    p_build.set_defaults(func=cmd_build)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
