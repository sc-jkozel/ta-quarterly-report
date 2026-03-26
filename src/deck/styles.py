"""SafetyCulture brand constants for deck styling."""

from pptx.util import Pt, Inches, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# Brand Colors
PURPLE_RAIN = RGBColor(0x65, 0x59, 0xFF)
BLUE_MOON = RGBColor(0x00, 0xD1, 0xFF)
YELLOW_SUBMARINE = RGBColor(0xFF, 0xD7, 0x00)
DARK_CHARCOAL = RGBColor(0x15, 0x16, 0x1E)
WHITE_RABBIT = RGBColor(0xFF, 0xFF, 0xFF)

# Supplementary
LIGHT_GRAY = RGBColor(0xE0, 0xE0, 0xE0)
MID_GRAY = RGBColor(0x8A, 0x8A, 0x9A)
SUCCESS_GREEN = RGBColor(0x00, 0xC8, 0x53)
WARN_AMBER = RGBColor(0xFF, 0xA0, 0x00)

# Card backgrounds
CARD_BG_DARK = RGBColor(0x1E, 0x1F, 0x2E)
CARD_BG_SIGNAL = RGBColor(0xF0, 0xF8, 0xFF)   # Strong Signals (light blue)
CARD_BG_WATCH = RGBColor(0xFF, 0xFB, 0xF0)     # Watch & Evolve (light amber)

# Fonts
FONT_HEADING = "Poppins"
FONT_BODY = "Open Sans"

# Font Sizes
SIZE_HEADING = Pt(24)
SIZE_SUBHEADING = Pt(14)
SIZE_CATEGORY = Pt(12)
SIZE_BODY = Pt(12)
SIZE_BODY_SMALL = Pt(11)
SIZE_LABEL = Pt(10)
SIZE_LABEL_SMALL = Pt(8)

# Slide dimensions (16:9 widescreen)
SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

# Common margins
MARGIN_LEFT = Inches(0.75)
MARGIN_TOP = Inches(0.5)
MARGIN_RIGHT = Inches(0.75)
CONTENT_WIDTH = Inches(11.833)  # SLIDE_WIDTH - 2 * MARGIN
