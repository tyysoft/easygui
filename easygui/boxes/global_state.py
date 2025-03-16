"""

.. moduleauthor:: easygui developers and Stephen Raymond Ferg
.. default-domain:: py
.. highlight:: python

Version |release|
"""

# Starting and global variables

window_position = "+300+200"

PROPORTIONAL_FONT_FAMILY = ("MS", "Sans", "Serif")
MONOSPACE_FONT_FAMILY = "Courier"

PROPORTIONAL_FONT_SIZE = 10
# a little smaller, because it is more legible at a smaller size
MONOSPACE_FONT_SIZE = 9
TEXT_ENTRY_FONT_SIZE = 12  # a little larger makes it easier to see


STANDARD_SELECTION_EVENTS = ["Return", "space"]
STANDARD_SELECTION_EVENTS_MOUSE = ["Enter", "Leave", "ButtonRelease-1"]

prop_font_line_length = 62
fixw_font_line_length = 80
num_lines_displayed = 50
default_hpad_in_chars = 2

class EgFont:
    text_font_name = "Courier New"
    text_font_size = 10
    text_font_style = "normal"
    text_font_slant = "normal"
    button_font_name = "Courier New"
    button_font_size = 10
    button_font_style = "normal"
    button_font_slant = "normal"