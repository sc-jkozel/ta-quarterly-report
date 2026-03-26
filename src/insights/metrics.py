"""Template-based metric computations from report data."""

from __future__ import annotations

from src.config import TEAM_TOTAL_LABEL
from src.data.models import ReportData


def format_currency(value: float) -> str:
    """Format AUD value as $X.XM or $X.XK."""
    if value >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"${value / 1_000:.0f}K"
    return f"${value:,.0f}"


def format_pct(value: float | None) -> str:
    if value is None:
        return "N/A"
    return f"{value:.1f}%"


def get_team_total(rows: list, field: str = "total") -> float:
    for row in rows:
        if row.technical_architect == TEAM_TOTAL_LABEL:
            return getattr(row, field) or 0
    return 0


def get_ta_row(rows: list, name: str):
    for row in rows:
        if row.technical_architect == name:
            return row
    return None


def compute_headline_metrics(data: ReportData) -> dict:
    """Compute the key headline metrics for the deck."""
    team_won = get_team_total(data.closed_won_count)
    team_won_aud = get_team_total(data.closed_won_total_aud)
    team_lost = get_team_total(data.closed_lost_count)
    team_win_rate = get_team_total(data.win_rate)
    team_pipeline_count = get_team_total(data.open_pipeline, "total_count")
    team_pipeline_aud = get_team_total(data.open_pipeline, "total_aud")
    team_avg_deal = get_team_total(data.average_deal_size)
    team_velocity = get_team_total(data.opportunity_velocity)
    total_opps = int(team_won + team_lost + team_pipeline_count)

    return {
        "closed_won_count": int(team_won),
        "closed_won_aud": team_won_aud,
        "closed_won_aud_fmt": format_currency(team_won_aud),
        "closed_lost_count": int(team_lost),
        "win_rate": team_win_rate,
        "win_rate_fmt": format_pct(team_win_rate),
        "open_pipeline_count": int(team_pipeline_count),
        "open_pipeline_aud": team_pipeline_aud,
        "open_pipeline_aud_fmt": format_currency(team_pipeline_aud),
        "avg_deal_size": team_avg_deal,
        "avg_deal_size_fmt": format_currency(team_avg_deal),
        "velocity_days": team_velocity,
        "total_opportunities": total_opps,
    }


def compute_ta_cards(data: ReportData) -> list[dict]:
    """Compute per-TA card data."""
    ta_names = [
        r.technical_architect
        for r in data.closed_won_count
        if r.technical_architect != TEAM_TOTAL_LABEL
    ]
    cards = []
    for name in ta_names:
        won_row = get_ta_row(data.closed_won_count, name)
        won_aud_row = get_ta_row(data.closed_won_total_aud, name)
        lost_row = get_ta_row(data.closed_lost_count, name)
        pipe_row = get_ta_row(data.open_pipeline, name)
        wr_row = get_ta_row(data.win_rate, name)

        won = int(won_row.total) if won_row else 0
        lost = int(lost_row.total) if lost_row else 0
        pipeline_count = int(pipe_row.total_count) if pipe_row else 0
        pipeline_aud = pipe_row.total_aud if pipe_row else 0
        booked = won_aud_row.total if won_aud_row else 0
        win_rate = wr_row.total if wr_row else 0

        cards.append({
            "name": name,
            "opportunities": won + lost + pipeline_count,
            "open_pipeline_aud": pipeline_aud,
            "open_pipeline_fmt": format_currency(pipeline_aud),
            "won": won,
            "lost": lost,
            "record": f"{won}W / {lost}L",
            "booked_aud": booked,
            "booked_fmt": format_currency(booked),
            "win_rate": win_rate,
            "win_rate_fmt": format_pct(win_rate) if win_rate else "N/A",
        })
    return cards
