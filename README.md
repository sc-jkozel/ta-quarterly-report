# TA Quarterly Report Generator

Automated PowerPoint deck generator for the Technical Architecture team's quarterly impact report. Runs inside Claude Code — provide three inputs and it handles the rest.

## Quick Start

Open Claude Code in this project directory and provide:

1. **Fiscal Year** — e.g. `FY26`
2. **Quarter** — e.g. `Q3`
3. **CSV file** — Path to a Salesforce opportunity export showing the opportunity IDs, Technical Architect, and Region. 

```
Generate the Q3 FY26 quarterly report using ~/Downloads/report.csv
```

Claude Code will generate the Hex prompt, query the data, build insights, and produce the deck in `output/`.

### CSV format

Export TA-engaged opportunities from Salesforce with these columns:

| Column | Required | Example |
|--------|----------|---------|
| `opportunity_id` | Yes | `006Dn00000ABC1234` |
| `technical_architect` | Yes | `Matthew McManus` |
| `region` | No | `APAC` |

- Header row is optional (auto-detected)
- Opportunity IDs must be valid Salesforce format (starts with `006`)

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) with Hex MCP configured
- [uv](https://docs.astral.sh/uv/) — Fast Python package and project manager
- Python 3.11+ (uv will install automatically if needed)

**Fonts:** Install [Poppins](https://fonts.google.com/specimen/Poppins) and [Open Sans](https://fonts.google.com/specimen/Open+Sans) on the machine where the deck will be opened. PowerPoint will fall back to Calibri if missing.

## Setup

```bash
uv sync
```

## What it does

Claude Code follows a step-by-step workflow defined in `CLAUDE.md`:

1. **Generate Hex prompt** — Parses the CSV, groups opportunity IDs by TA, and renders a query prompt
2. **Review gate** — Asks you to review the prompt before sending (Y/N)
3. **Query Hex** — Creates a new Hex thread, polls until complete, and parses the 9 metric outputs into `output/report_data.json`
4. **Generate insights** — Analyzes the metrics and writes narratives to `output/insights.json`
5. **Build deck** — Produces a 7-slide branded .pptx in `output/`

## Deck Output

8-slide branded deck:

1. **Title** — "Technical Architect Impact Report" with quarter, date, and hero stat (e.g. 2.2x win rate)
2. **FY Metrics** — Team win rate, booked revenue, avg deal size, and total opportunities
3. **Current Pipeline** — Open pipeline, avg pipeline deal size, opportunity count cards + stage breakdown chart
4. **Industry Pipeline** — Horizontal bar chart showing open pipeline by industry vertical
5. **By Technical Architect** — Per-TA cards (McManus, Soakell, Loewen, Coates)
6. **Reading the Data** — Strong Signals / Watch & Evolve narratives
7. **What's Next** — Numbered action items
8. **Closing** — Summary statement with author attribution

## Data Sources

All data originates from Salesforce via the warehouse tables `mart.dim_salesforce_opportunity` and `mart.dim_salesforce_account`, queried through Hex.

### Metrics (per TA + Team Total)

| Metric | Description |
|--------|-------------|
| Closed Won Count | Number of won deals |
| Closed Won AUD | Total rollup amount for won deals |
| Closed Lost Count | Number of lost deals |
| Win Rate | Won / (Won + Lost) as % |
| Open Pipeline | Count + AUD of deals not yet closed |
| Average Deal Size | Closed Won AUD / Closed Won Count |
| Opportunity Velocity | Avg days from created to closed (won) |
| Industry Breakdown | Closed Won + Open Pipeline by industry |

## Project Structure

```
CLAUDE.md                # Claude Code workflow instructions
src/
├── main.py              # CLI entry point (prompt + build subcommands)
├── config.py            # Report config (TAs, labels, fiscal year, quarter ranges)
├── hex_prompt.py        # CSV parser + Hex prompt template renderer
├── templates/
│   ├── hex_prompt.txt       # Hex prompt template with placeholders
│   └── ta_analysis_prompt.md # Data analysis prompt for insight generation
├── data/
│   └── models.py        # Pydantic models for JSON inputs
├── insights/
│   └── metrics.py       # Derived metric calculations
└── deck/
    ├── builder.py       # Deck orchestrator
    ├── styles.py        # SafetyCulture brand constants
    └── slides/
        ├── helpers.py       # Shared shape/text utilities
        ├── title_slide.py       # Slide 1
        ├── hero_metric.py       # Slide 2
        ├── current_pipeline.py  # Slide 3
        ├── pipeline.py          # Slide 4
        ├── by_architect.py      # Slide 5
        ├── reading_data.py      # Slide 6
        ├── whats_next.py        # Slide 7
        └── closing.py           # Slide 8
```

## Style Guide

| Role | Font | Weight | Size |
|------|------|--------|------|
| Headings | Poppins | Bold | 24pt |
| Subheadings | Open Sans | Semi-Bold | 14pt |
| Category headings | Open Sans | Bold | 12pt |
| Body copy | Open Sans | Normal | 11–12pt |
| Small labels | Open Sans | Normal | 8–10pt |

| Color | Hex | Usage |
|-------|-----|-------|
| PurpleRain | `#6559FF` | Primary brand / accents |
| BlueMoon | `#00D1FF` | Secondary / highlights |
| YellowSubmarine | `#FFD700` | Alerts / emphasis |
| DarkCharcoal | `#15161e` | Dark backgrounds / text |
| WhiteRabbit | `#FFFFFF` | Light backgrounds / text |

## Customisation

- **Brand colors/fonts** — Edit `src/deck/styles.py`
- **Report metadata** — Edit `src/config.py` (author, TAs, fiscal year)
- **New TA flag** — Set `"new": True` on a TA in `TECHNICAL_ARCHITECTS` to show a "recently joined" footnote on slide 4; remove the flag when their data populates
- **Slide layout** — Each slide is an independent module in `src/deck/slides/`
- **Narratives** — Edit `output/insights.json` directly to tweak wording before generating
