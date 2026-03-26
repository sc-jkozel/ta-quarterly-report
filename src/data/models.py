"""Pydantic models for report data and insights JSON files."""

from __future__ import annotations

from pydantic import BaseModel


class Opportunity(BaseModel):
    opportunity_name: str
    opportunity_id: str
    account_name: str
    stage: str
    closed_date: str
    created_date: str
    rollup_amount_aud: float
    industry_type: str
    region: str
    technical_architect: str
    fiscal_quarter: str


class MetricRow(BaseModel):
    """A row in a metric table (per TA or Team Total).

    Quarter-level values are stored in `by_quarter` keyed by label
    (e.g. "Q1 FY26", "Q3 FY27").  This keeps the model independent
    of any specific fiscal year or quarter set.
    """
    technical_architect: str
    by_quarter: dict[str, float | None] = {}
    other: float | None = None
    total: float


class PipelineRow(BaseModel):
    """Open pipeline row with count + AUD per quarter.

    `by_quarter` maps quarter label -> {"count": int, "aud": float}.
    """
    technical_architect: str
    by_quarter: dict[str, dict[str, float]] = {}
    other_count: int = 0
    other_aud: float = 0.0
    total_count: int = 0
    total_aud: float = 0.0


class IndustryRow(BaseModel):
    """Industry breakdown row with count + AUD per quarter.

    `by_quarter` maps quarter label -> {"count": int, "aud": float}.
    """
    industry_type: str
    by_quarter: dict[str, dict[str, float]] = {}
    other_count: int = 0
    other_aud: float = 0.0
    total_count: int = 0
    total_aud: float = 0.0


class ReportData(BaseModel):
    """All 9 outputs from the Hex thread."""
    raw_opportunities: list[Opportunity]
    closed_won_count: list[MetricRow]
    closed_won_total_aud: list[MetricRow]
    closed_lost_count: list[MetricRow]
    win_rate: list[MetricRow]
    open_pipeline: list[PipelineRow]
    average_deal_size: list[MetricRow]
    opportunity_velocity: list[MetricRow]
    industry_closed_won: list[IndustryRow]
    industry_open_pipeline: list[IndustryRow]


class ActionItem(BaseModel):
    heading: str
    description: str


class Insights(BaseModel):
    """Claude-generated narrative insights for the deck."""
    strong_signals: list[str]
    watch_evolve: list[str]
    whats_next: list[ActionItem]
    closing_statement: str
