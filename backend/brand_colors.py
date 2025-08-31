"""
Brand colors for CuratED platform
These colors define the visual identity and should be used consistently across the application.
"""

# Primary brand colors
MAIN_COLOUR = "#008073"  # Teal - primary brand color
SUB_COLOUR = "#FFB81E"   # Orange/Yellow - secondary accent

# Text and header colors
PART_HEADER_COLOUR = "#B4931F"    # Gold - for section headers
PART_TEXT_COLOUR = "#2D1500"      # Dark brown - main text
HEADER_TEXT_COLOUR = "#0F4C78"    # Dark blue - main headers

# Background and card colors
CARD_TEXT_BG = "#FEF4EA"          # Light cream - card backgrounds
CARD_TEXT_COLOR = "#2D1500"       # Dark brown - text on cards
EVENT_CARD = "rgba(255, 184, 30, 0.775)"  # Semi-transparent orange - event cards

# UI element colors
PART_HEAD_TEXT = "#B4931F"        # Gold - part headings
PLACEHOLDER_COLOR = "#B2B2B2"     # Light gray - placeholder text
GREY_TEXT = "#8A8A8A"             # Gray - secondary text
WHITER = "#ffff"                  # White - pure white

# Color mapping for different contexts
BRAND_COLORS = {
    'primary': MAIN_COLOUR,
    'secondary': SUB_COLOUR,
    'text_primary': PART_TEXT_COLOUR,
    'text_secondary': GREY_TEXT,
    'header': HEADER_TEXT_COLOUR,
    'section_header': PART_HEADER_COLOUR,
    'background_light': CARD_TEXT_BG,
    'background_white': WHITER,
    'accent': EVENT_CARD,
    'placeholder': PLACEHOLDER_COLOR
}