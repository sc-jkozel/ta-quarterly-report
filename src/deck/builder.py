"""Deck orchestrator - assembles all slides into a presentation."""

from __future__ import annotations

import datetime
from pathlib import Path

from pptx import Presentation

from src.config import ReportConfig
from src.data.models import ReportData, Insights
from src.insights.metrics import (
    compute_headline_metrics, compute_ta_cards, compute_ta_pipeline_cards,
    compute_headline_metrics_for_quarter, compute_ta_cards_for_quarter,
)
from src.deck.styles import SLIDE_WIDTH, SLIDE_HEIGHT
from src.deck.slides import (
    title_slide,
    hero_metric,
    by_architect,
    quarter_metrics,
    quarter_by_architect,
    current_pipeline,
    pipeline,
    ta_pipeline,
    reading_data,
    whats_next,
    closing,
)


def build_deck(
    data: ReportData,
    insights: Insights,
    config: ReportConfig | None = None,
    output_dir: str = "output",
) -> str:
    """Build the full TA Impact Report deck and return the output path."""
    if config is None:
        config = ReportConfig()

    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT

    # Compute metrics — FY cumulative and quarter-specific
    fy_metrics = compute_headline_metrics(data)
    fy_ta_cards = compute_ta_cards(data)
    pipeline_cards = compute_ta_pipeline_cards(data)
    q_metrics = compute_headline_metrics_for_quarter(
        data, config.quarter, config.fiscal_year
    )
    q_ta_cards = compute_ta_cards_for_quarter(
        data, config.quarter, config.fiscal_year
    )

    # Build slides
    title_slide.build(prs, config=config)                               #  1. Title
    hero_metric.build(prs, metrics=fy_metrics, config=config)           #  2. FY Metrics
    by_architect.build(prs, ta_cards=fy_ta_cards, config=config)        #  3. FY Performance by Architect
    quarter_metrics.build(prs, metrics=q_metrics, config=config)        #  4. Quarter Metrics
    quarter_by_architect.build(prs, ta_cards=q_ta_cards, config=config) #  5. Quarter Performance by Architect
    current_pipeline.build(prs, data=data, metrics=fy_metrics)          #  6. Current TA Pipeline
    ta_pipeline.build(prs, pipeline_cards=pipeline_cards, config=config) #  7. TA Pipeline Overview
    pipeline.build(prs, data=data, metrics=fy_metrics, config=config)   #  8. TA Pipeline by Industry
    reading_data.build(prs, insights=insights)                          #  8. Reading the Data
    whats_next.build(prs, insights=insights)                            #  9. What's Next
    closing.build(prs, config=config, insights=insights)                # 10. Closing

    # Save
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    filename = f"ta_impact_report_{datetime.date.today()}.pptx"
    filepath = output_path / filename
    prs.save(str(filepath))
    return str(filepath)
