"""Report configuration constants."""

from dataclasses import dataclass
from datetime import date


@dataclass
class ReportConfig:
    title: str = "Technical Architect Impact Report"
    prepared_for: str = "Global Head of GTM"
    org_name: str = "SafetyCulture"
    team_name: str = "Technical Architecture"
    author_name: str = "Jason Kozel"
    author_title: str = "Global Manager, Technical Architecture"
    author_email: str = "jason.kozel@safetyculture.io"
    fiscal_year: str = "FY26"
    quarter: str = "Q3"


TECHNICAL_ARCHITECTS = [
    {"name": "Matthew McManus", "region": "APAC", "location": "Sydney"},
    {"name": "Jonathan Soakell", "region": "EMEA", "location": "Manchester"},
    {"name": "Scotty Loewen", "region": "AMER", "location": "Austin"},
    {"name": "Cinco Coates", "region": "AMER", "location": "", "new": True},
]

TEAM_TOTAL_LABEL = "Team Total"

# SafetyCulture fiscal year starts July 1.
# Q1 = Jul–Sep, Q2 = Oct–Dec, Q3 = Jan–Mar, Q4 = Apr–Jun.
_QUARTER_OFFSETS = {
    "Q1": (0, 7, 1, 9, 30),   # Jul 1 – Sep 30
    "Q2": (0, 10, 1, 12, 31), # Oct 1 – Dec 31
    "Q3": (1, 1, 1, 3, 31),   # Jan 1 – Mar 31 (next calendar year)
    "Q4": (1, 4, 1, 6, 30),   # Apr 1 – Jun 30 (next calendar year)
}


def fiscal_quarter_ranges(
    fiscal_year: str, through_quarter: str
) -> list[tuple[str, date, date]]:
    """Return (label, start_date, end_date) for Q1 through *through_quarter*.

    fiscal_year: e.g. "FY26" → calendar year 2025 is the base (FY starts Jul 2025).
    through_quarter: e.g. "Q3" → returns Q1, Q2, Q3.
    """
    fy_num = int(fiscal_year.upper().removeprefix("FY"))
    base_year = 2000 + fy_num - 1  # FY26 base = 2025

    quarter_order = ["Q1", "Q2", "Q3", "Q4"]
    target_idx = quarter_order.index(through_quarter.upper())

    ranges: list[tuple[str, date, date]] = []
    for q in quarter_order[: target_idx + 1]:
        yr_off, sm, sd, em, ed = _QUARTER_OFFSETS[q]
        start = date(base_year + yr_off, sm, sd)
        end = date(base_year + yr_off, em, ed)
        label = f"{q} {fiscal_year.upper()}"
        ranges.append((label, start, end))

    return ranges
