"""Quarter-specific version of the hero metric slide."""

from pptx.presentation import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN

from src.deck.styles import (
    DARK_CHARCOAL, WHITE_RABBIT, PURPLE_RAIN, BLUE_MOON, MID_GRAY,
    CARD_BG_DARK, FONT_HEADING, FONT_BODY,
)
from src.deck.slides.helpers import (
    add_blank_slide, set_slide_bg, add_textbox, add_rounded_rect,
)


def build(prs: Presentation, metrics: dict, config=None, **kwargs):
    from src.config import ReportConfig
    if config is None:
        config = ReportConfig()

    quarter_label = f"{config.quarter.upper()} {config.fiscal_year.upper()}"

    slide = add_blank_slide(prs)
    set_slide_bg(slide, DARK_CHARCOAL)

    # Title
    add_textbox(
        slide, f"{quarter_label} Metrics",
        Inches(0.75), Inches(0.4), Inches(6), Inches(0.5),
        font_name=FONT_HEADING, font_size=Pt(24),
        font_color=WHITE_RABBIT, bold=True,
    )

    # Win rate - big number
    win_rate = metrics["win_rate_fmt"]
    add_textbox(
        slide, win_rate,
        Inches(1.5), Inches(1.5), Inches(5), Inches(1.2),
        font_name=FONT_HEADING, font_size=Pt(72),
        font_color=BLUE_MOON, bold=True,
        alignment=PP_ALIGN.CENTER,
    )
    add_textbox(
        slide, "Team Win Rate",
        Inches(1.5), Inches(2.7), Inches(5), Inches(0.4),
        font_name=FONT_BODY, font_size=Pt(18),
        font_color=WHITE_RABBIT,
        alignment=PP_ALIGN.CENTER,
    )

    won_count = metrics["closed_won_count"]
    lost_count = metrics["closed_lost_count"]
    add_textbox(
        slide, f"{won_count} Won  |  {lost_count} Lost  |  {won_count + lost_count} Closed",
        Inches(1.5), Inches(3.2), Inches(5), Inches(0.3),
        font_name=FONT_BODY, font_size=Pt(11),
        font_color=MID_GRAY,
        alignment=PP_ALIGN.CENTER,
    )

    # Right side - Booked revenue card
    add_rounded_rect(
        slide,
        Inches(7.5), Inches(1.5), Inches(4.5), Inches(2.2),
        fill_color=PURPLE_RAIN,
    )
    add_textbox(
        slide, metrics["closed_won_aud_fmt"],
        Inches(7.7), Inches(1.8), Inches(4), Inches(0.8),
        font_name=FONT_HEADING, font_size=Pt(48),
        font_color=WHITE_RABBIT, bold=True,
        alignment=PP_ALIGN.CENTER,
    )
    add_textbox(
        slide, "Booked Revenue (AUD)",
        Inches(7.7), Inches(2.7), Inches(4), Inches(0.4),
        font_name=FONT_BODY, font_size=Pt(14),
        font_color=WHITE_RABBIT,
        alignment=PP_ALIGN.CENTER,
    )
    add_textbox(
        slide, f"from {won_count} closed-won deals",
        Inches(7.7), Inches(3.15), Inches(4), Inches(0.3),
        font_name=FONT_BODY, font_size=Pt(10),
        font_color=WHITE_RABBIT,
        alignment=PP_ALIGN.CENTER,
    )

    # Bottom metrics row
    bottom_metrics = [
        (metrics["avg_deal_size_fmt"], "Avg Deal Size (AUD)", "closed-won average"),
        (str(metrics["total_opportunities"]), "Total Opportunities", f"{quarter_label} TA-engaged"),
    ]

    card_width = Inches(5.6)
    card_height = Inches(1.6)
    start_x = Inches(0.75)
    y = Inches(4.8)
    gap = Inches(0.45)

    for i, (val, label, sub) in enumerate(bottom_metrics):
        x = start_x + i * (card_width + gap)
        add_rounded_rect(slide, x, y, card_width, card_height, fill_color=CARD_BG_DARK)
        add_textbox(
            slide, val,
            x + Inches(0.2), y + Inches(0.15),
            card_width - Inches(0.4), Inches(0.5),
            font_name=FONT_HEADING, font_size=Pt(22),
            font_color=BLUE_MOON, bold=True,
        )
        add_textbox(
            slide, label,
            x + Inches(0.2), y + Inches(0.7),
            card_width - Inches(0.4), Inches(0.35),
            font_name=FONT_BODY, font_size=Pt(10),
            font_color=WHITE_RABBIT, bold=True,
        )
        add_textbox(
            slide, sub,
            x + Inches(0.2), y + Inches(1.05),
            card_width - Inches(0.4), Inches(0.3),
            font_name=FONT_BODY, font_size=Pt(9),
            font_color=MID_GRAY,
        )
