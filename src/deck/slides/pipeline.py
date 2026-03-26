"""Slide 3: Pipeline & Coverage metrics grid."""

from pptx.presentation import Presentation
from pptx.util import Inches, Pt

from src.deck.styles import (
    DARK_CHARCOAL, WHITE_RABBIT, PURPLE_RAIN, BLUE_MOON, MID_GRAY,
    CARD_BG_DARK, FONT_HEADING, FONT_BODY,
)
from src.deck.slides.helpers import (
    add_blank_slide, set_slide_bg, add_textbox, add_rounded_rect,
)
from src.data.models import ReportData
from src.insights.metrics import format_currency


def build(prs: Presentation, data: ReportData, metrics: dict, **kwargs):
    slide = add_blank_slide(prs)
    set_slide_bg(slide, DARK_CHARCOAL)

    # Title
    add_textbox(
        slide, "Pipeline & Coverage",
        Inches(0.75), Inches(0.4), Inches(6), Inches(0.5),
        font_name=FONT_HEADING, font_size=Pt(24),
        font_color=WHITE_RABBIT, bold=True,
    )

    # Top row - 3 big metrics
    top_items = [
        (metrics["open_pipeline_aud_fmt"], "Open TA Pipeline",
         f"AUD across {metrics['open_pipeline_count']} active deals"),
        (metrics["closed_won_aud_fmt"], "Booked Revenue",
         f"AUD from {metrics['closed_won_count']} closed-won deals"),
        (f"{metrics['velocity_days']:.0f} days", "Avg Days to Close",
         "created to closed-won velocity"),
    ]

    card_w = Inches(3.75)
    card_h = Inches(1.8)
    start_x = Inches(0.75)
    gap = Inches(0.29)
    y1 = Inches(1.3)

    for i, (val, label, sub) in enumerate(top_items):
        x = start_x + i * (card_w + gap)
        add_rounded_rect(slide, x, y1, card_w, card_h, fill_color=CARD_BG_DARK)
        add_textbox(
            slide, val,
            x + Inches(0.3), y1 + Inches(0.2),
            card_w - Inches(0.6), Inches(0.7),
            font_name=FONT_HEADING, font_size=Pt(32),
            font_color=BLUE_MOON, bold=True,
        )
        add_textbox(
            slide, label,
            x + Inches(0.3), y1 + Inches(0.95),
            card_w - Inches(0.6), Inches(0.35),
            font_name=FONT_BODY, font_size=Pt(12),
            font_color=WHITE_RABBIT, bold=True,
        )
        add_textbox(
            slide, sub,
            x + Inches(0.3), y1 + Inches(1.3),
            card_w - Inches(0.6), Inches(0.3),
            font_name=FONT_BODY, font_size=Pt(10),
            font_color=MID_GRAY,
        )

    # Bottom row - 3 secondary metrics
    total_opps = len(data.raw_opportunities)
    expansion_count = sum(
        1 for o in data.raw_opportunities
        if "EXP" in o.opportunity_name.upper()
    )
    expansion_pct = (expansion_count / total_opps * 100) if total_opps > 0 else 0

    bottom_items = [
        (f"{expansion_pct:.0f}%", "Expansion Focused",
         f"{expansion_count} of {total_opps} TA deals are expansions"),
        (str(total_opps), "Total TA Opportunities",
         "pipeline-qualified TA-engaged"),
        (metrics["avg_deal_size_fmt"], "Avg Deal Size",
         f"AUD (closed-won average)"),
    ]

    y2 = Inches(3.5)
    for i, (val, label, sub) in enumerate(bottom_items):
        x = start_x + i * (card_w + gap)
        add_rounded_rect(slide, x, y2, card_w, card_h, fill_color=CARD_BG_DARK)
        add_textbox(
            slide, val,
            x + Inches(0.3), y2 + Inches(0.2),
            card_w - Inches(0.6), Inches(0.7),
            font_name=FONT_HEADING, font_size=Pt(32),
            font_color=BLUE_MOON, bold=True,
        )
        add_textbox(
            slide, label,
            x + Inches(0.3), y2 + Inches(0.95),
            card_w - Inches(0.6), Inches(0.35),
            font_name=FONT_BODY, font_size=Pt(12),
            font_color=WHITE_RABBIT, bold=True,
        )
        add_textbox(
            slide, sub,
            x + Inches(0.3), y2 + Inches(1.3),
            card_w - Inches(0.6), Inches(0.3),
            font_name=FONT_BODY, font_size=Pt(10),
            font_color=MID_GRAY,
        )

    # Industry breakdown - top pipeline industries
    add_textbox(
        slide, "Top Pipeline Industries",
        Inches(0.75), Inches(5.6), Inches(4), Inches(0.35),
        font_name=FONT_BODY, font_size=Pt(12),
        font_color=WHITE_RABBIT, bold=True,
    )

    top_industries = sorted(
        data.industry_open_pipeline, key=lambda x: x.total_aud, reverse=True
    )[:5]

    for i, ind in enumerate(top_industries):
        y = Inches(6.05) + i * Inches(0.25)
        text = f"{ind.industry_type}: {format_currency(ind.total_aud)} ({ind.total_count} deals)"
        add_textbox(
            slide, text,
            Inches(0.95), y, Inches(5), Inches(0.25),
            font_name=FONT_BODY, font_size=Pt(9),
            font_color=MID_GRAY,
        )
