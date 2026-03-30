"""Parse a Salesforce opportunity CSV and render the Hex prompt template."""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path

from src.config import ReportConfig, fiscal_quarter_ranges

_TEMPLATE_PATH = Path(__file__).parent / "templates" / "hex_prompt.txt"

# Salesforce Opportunity IDs start with "006" followed by alphanumeric chars.
_SFDC_OPP_ID_RE = re.compile(r"^006[A-Za-z0-9]{12,15}$")


def _looks_like_opp_id(value: str) -> bool:
    return bool(_SFDC_OPP_ID_RE.match(value.strip()))


def sf_id_15_to_18(id15: str) -> str:
    """Convert a 15-char Salesforce ID to its 18-char equivalent.

    The 18-char ID appends a 3-char checksum that encodes the case of the
    original 15 characters, allowing case-insensitive matching in databases.
    Already-18-char IDs are returned unchanged.
    """
    if len(id15) == 18:
        return id15
    suffix_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ012345"
    suffix = ""
    for chunk_start in range(0, 15, 5):
        chunk = id15[chunk_start : chunk_start + 5]
        bits = sum(1 << i for i, ch in enumerate(chunk) if ch.isupper())
        suffix += suffix_chars[bits]
    return id15 + suffix


def parse_csv(csv_path: str | Path) -> list[dict[str, str]]:
    """Read opportunity CSV, auto-detecting whether a header row is present.

    Returns list of dicts with keys: opp_id, ta_name, region.
    """
    path = Path(csv_path)
    with open(path, newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if not rows:
        raise ValueError(f"CSV file is empty: {path}")

    # Auto-detect header: if the first column of row 0 looks like an opp ID,
    # there's no header; otherwise treat row 0 as column names.
    has_header = not _looks_like_opp_id(rows[0][0])
    data_rows = rows[1:] if has_header else rows

    results = []
    for i, row in enumerate(data_rows, start=2 if has_header else 1):
        if len(row) < 2:
            continue
        opp_id = sf_id_15_to_18(row[0].strip())
        ta_name = row[1].strip()
        region = row[2].strip() if len(row) > 2 else ""
        if not opp_id:
            continue
        results.append({"opp_id": opp_id, "ta_name": ta_name, "region": region})

    return results


def render_hex_prompt(
    opportunities: list[dict[str, str]],
    config: ReportConfig | None = None,
) -> str:
    """Render the Hex prompt template from parsed opportunity data."""
    if config is None:
        config = ReportConfig()

    # All opportunity IDs
    all_ids = [opp["opp_id"] for opp in opportunities]

    # Group by TA
    ta_groups: dict[str, list[str]] = defaultdict(list)
    for opp in opportunities:
        ta_groups[opp["ta_name"]].append(opp["opp_id"])

    # Format TA mappings
    ta_mapping_lines = []
    for ta_name in sorted(ta_groups):
        ids_str = ", ".join(ta_groups[ta_name])
        ta_mapping_lines.append(f"- {ta_name}: {ids_str}")

    # Build fiscal quarter range lines
    ranges = fiscal_quarter_ranges(config.fiscal_year, config.quarter)
    quarter_lines = []
    for label, start, end in ranges:
        quarter_lines.append(
            f"- {label} = Close Date between "
            f"{start.strftime('%b %d, %Y').replace(' 0', ' ')} and "
            f"{end.strftime('%b %d, %Y').replace(' 0', ' ')}"
        )

    # Load and render template
    template = _TEMPLATE_PATH.read_text()
    return template.format(
        num_opportunities=len(all_ids),
        all_opportunity_ids=", ".join(all_ids),
        ta_mappings="\n".join(ta_mapping_lines),
        quarter_ranges="\n".join(quarter_lines),
    )
