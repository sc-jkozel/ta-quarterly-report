"""Deck orchestrator - assembles all slides into a presentation."""

from __future__ import annotations

import datetime
from pathlib import Path

from pptx import Presentation

from src.config import ReportConfig
from src.data.models import ReportData, Insights
from src.insights.metrics import compute_headline_metrics, compute_ta_cards
from src.deck.styles import SLIDE_WIDTH, SLIDE_HEIGHT
from src.deck.slides import (
    title_slide,
    hero_metric,
    current_pipeline,
    pipeline,
    by_architect,
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

    # Compute metrics
    metrics = compute_headline_metrics(data)
    ta_cards = compute_ta_cards(data)

    # Build slides
    title_slide.build(prs, config=config)                       # 1. Title
    hero_metric.build(prs, metrics=metrics, config=config)      # 2. FY Metrics
    by_architect.build(prs, ta_cards=ta_cards, config=config)   # 3. Performance by Architect
    current_pipeline.build(prs, data=data, metrics=metrics)     # 4. Current TA Pipeline
    pipeline.build(prs, data=data, metrics=metrics, config=config)  # 5. TA Pipeline by Industry
    reading_data.build(prs, insights=insights)                  # 6. Reading the Data
    whats_next.build(prs, insights=insights)                    # 7. What's Next
    closing.build(prs, config=config, insights=insights)        # 8. Closing

    # Save
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    filename = f"ta_impact_report_{datetime.date.today()}.pptx"
    filepath = output_path / filename
    prs.save(str(filepath))
    return str(filepath)
