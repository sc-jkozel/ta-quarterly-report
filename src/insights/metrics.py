"""Template-based metric computations from report data."""

from __future__ import annotations

from src.config import TEAM_TOTAL_LABEL, TECHNICAL_ARCHITECTS
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


def _get_quarter_value(row, quarter_label: str) -> float:
    """Get a value from a MetricRow's by_quarter dict."""
    if row is None:
        return 0
    return row.by_quarter.get(quarter_label) or 0


def _get_quarter_pipeline(row, quarter_label: str) -> tuple[int, float]:
    """Get (count, aud) from a PipelineRow's by_quarter dict."""
    if row is None:
        return 0, 0.0
    q = row.by_quarter.get(quarter_label, {})
    return int(q.get("count", 0)), q.get("aud", 0.0)


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
    """Compute per-TA card data.

    Uses TECHNICAL_ARCHITECTS config as the source of truth so every TA
    appears even if they have no closed-won deals yet.  TAs marked as
    ``"new": True`` are excluded — they get a footnote instead.
    """
    ta_names = [
        ta["name"] for ta in TECHNICAL_ARCHITECTS
        if not ta.get("new")
    ]
    cards = []
    for name in ta_names:
        won_row = get_ta_row(data.closed_won_count, name)
        won_aud_row = get_ta_row(data.closed_won_total_aud, name)
        lost_row = get_ta_row(data.closed_lost_count, name)
        pipe_row = get_ta_row(data.open_pipeline, name)
        wr_row = get_ta_row(data.win_rate, name)
        vel_row = get_ta_row(data.opportunity_velocity, name)

        won = int(won_row.total) if won_row else 0
        lost = int(lost_row.total) if lost_row else 0
        pipeline_count = int(pipe_row.total_count) if pipe_row else 0
        booked = won_aud_row.total if won_aud_row else 0
        win_rate = wr_row.total if wr_row else 0
        velocity = vel_row.total if vel_row else None

        cards.append({
            "name": name,
            "opportunities": pipeline_count,
            "won": won,
            "lost": lost,
            "record": f"{won}W / {lost}L",
            "booked_aud": booked,
            "booked_fmt": format_currency(booked),
            "win_rate": win_rate,
            "win_rate_fmt": format_pct(win_rate) if win_rate else "N/A",
            "velocity": velocity,
            "velocity_fmt": f"{velocity:.0f} days" if velocity else "N/A",
        })
    return cards


def compute_ta_pipeline_cards(data: ReportData) -> list[dict]:
    """Compute per-TA pipeline card data from raw_opportunities.

    Each card shows: open pipeline AUD, open opportunity count,
    late-stage deal count (Negotiation + Proposal), and top deal.
    """
    open_stages = {"Qualify", "Discovery", "Pre-Sales", "Proposal", "Negotiation"}
    late_stages = {"Negotiation", "Proposal"}

    ta_names = [
        ta["name"] for ta in TECHNICAL_ARCHITECTS
        if not ta.get("new")
    ]
    cards = []
    for name in ta_names:
        open_deals = [
            o for o in data.raw_opportunities
            if o.technical_architect == name and o.stage in open_stages
        ]
        pipeline_aud = sum(o.rollup_amount_aud for o in open_deals)
        late_stage = [o for o in open_deals if o.stage in late_stages]
        top_deal = max(open_deals, key=lambda x: x.rollup_amount_aud) if open_deals else None

        cards.append({
            "name": name,
            "open_pipeline_aud": pipeline_aud,
            "open_pipeline_fmt": format_currency(pipeline_aud),
            "open_count": len(open_deals),
            "late_stage_count": len(late_stage),
            "top_deal_name": top_deal.account_name if top_deal else "N/A",
            "top_deal_aud": top_deal.rollup_amount_aud if top_deal else 0,
            "top_deal_fmt": format_currency(top_deal.rollup_amount_aud) if top_deal else "N/A",
            "top_deal_stage": top_deal.stage if top_deal else "",
        })
    return cards


def compute_headline_metrics_for_quarter(
    data: ReportData, quarter: str, fiscal_year: str
) -> dict:
    """Compute headline metrics scoped to a single quarter."""
    qlabel = f"{quarter.upper()} {fiscal_year.upper()}"

    team_won_row = get_ta_row(data.closed_won_count, TEAM_TOTAL_LABEL)
    team_won = _get_quarter_value(team_won_row, qlabel)

    team_won_aud_row = get_ta_row(data.closed_won_total_aud, TEAM_TOTAL_LABEL)
    team_won_aud = _get_quarter_value(team_won_aud_row, qlabel)

    team_lost_row = get_ta_row(data.closed_lost_count, TEAM_TOTAL_LABEL)
    team_lost = _get_quarter_value(team_lost_row, qlabel)

    team_wr_row = get_ta_row(data.win_rate, TEAM_TOTAL_LABEL)
    team_win_rate = _get_quarter_value(team_wr_row, qlabel)

    team_avg_row = get_ta_row(data.average_deal_size, TEAM_TOTAL_LABEL)
    team_avg_deal = _get_quarter_value(team_avg_row, qlabel)

    team_vel_row = get_ta_row(data.opportunity_velocity, TEAM_TOTAL_LABEL)
    team_velocity = _get_quarter_value(team_vel_row, qlabel)

    team_pipe_row = get_ta_row(data.open_pipeline, TEAM_TOTAL_LABEL)
    pipe_count, pipe_aud = _get_quarter_pipeline(team_pipe_row, qlabel)

    total_opps = int(team_won + team_lost + pipe_count)

    return {
        "closed_won_count": int(team_won),
        "closed_won_aud": team_won_aud,
        "closed_won_aud_fmt": format_currency(team_won_aud),
        "closed_lost_count": int(team_lost),
        "win_rate": team_win_rate,
        "win_rate_fmt": format_pct(team_win_rate),
        "open_pipeline_count": pipe_count,
        "open_pipeline_aud": pipe_aud,
        "open_pipeline_aud_fmt": format_currency(pipe_aud),
        "avg_deal_size": team_avg_deal,
        "avg_deal_size_fmt": format_currency(team_avg_deal),
        "velocity_days": team_velocity,
        "total_opportunities": total_opps,
    }


def compute_ta_cards_for_quarter(
    data: ReportData, quarter: str, fiscal_year: str
) -> list[dict]:
    """Compute per-TA card data scoped to a single quarter."""
    qlabel = f"{quarter.upper()} {fiscal_year.upper()}"

    ta_names = [
        ta["name"] for ta in TECHNICAL_ARCHITECTS
        if not ta.get("new")
    ]
    cards = []
    for name in ta_names:
        won_row = get_ta_row(data.closed_won_count, name)
        won_aud_row = get_ta_row(data.closed_won_total_aud, name)
        lost_row = get_ta_row(data.closed_lost_count, name)
        wr_row = get_ta_row(data.win_rate, name)
        vel_row = get_ta_row(data.opportunity_velocity, name)

        won = int(_get_quarter_value(won_row, qlabel))
        lost = int(_get_quarter_value(lost_row, qlabel))
        booked = _get_quarter_value(won_aud_row, qlabel)
        win_rate = _get_quarter_value(wr_row, qlabel)
        velocity = _get_quarter_value(vel_row, qlabel)

        cards.append({
            "name": name,
            "won": won,
            "lost": lost,
            "record": f"{won}W / {lost}L",
            "booked_aud": booked,
            "booked_fmt": format_currency(booked),
            "win_rate": win_rate,
            "win_rate_fmt": format_pct(win_rate) if win_rate else "N/A",
            "velocity": velocity if velocity else None,
            "velocity_fmt": f"{velocity:.0f} days" if velocity else "N/A",
        })
    return cards
